import json
import logging
from tqdm import tqdm
from bs4 import BeautifulSoup
import asyncio

from src.mongo.data import MongoData
from src.mongo.default import MongoDefault
from src.embedding_formatter import  ToolkitArticle_Chunk
from src.embedding_model import get_embedding
from src.text_processing.get_token_length import count_tokens
from src.text_processing.chunking import splitter
from src.config import DESCRIPTION_SIZE,OPENSEARCH_PASSWORD,OPENSEARCH_USERNAME

from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk

logger = logging.getLogger(__name__)


class Pipeline():
    def __init__(self):
        self._mongo_data = MongoData()
        self._mongo_default = MongoDefault()
        self.open_search_client = OpenSearch(
            hosts=["https://search-ai-test-domain-343yonb3wnzzilhdnlbn3cdesm.us-west-1.es.amazonaws.com"],
            http_auth=(OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD),
            use_ssl=True,
            verify_certs=False,
            timeout=60,
            max_retries=5,
            retry_on_timeout=True )
        logger.info("Pipeline initialized: OpenSearch client and Mongo clients ready")

    async def run(self, toolkit_article_id):
        logger.info("Pipeline run started for toolkit_article_id=%s", toolkit_article_id)
        try:
            users_data = await self._mongo_data.get_all_active_users(toolkit_article_id)
            total_users = len(users_data)
            logger.info("Fetched %d active users from Mongo for collection %s", total_users, toolkit_article_id)

            # Slice for processing (e.g. users_data[100:])
            slice_start = 100
            to_process = users_data[slice_start:]
            process_count = len(to_process)
            logger.info("Processing %d users (slice [%d:])", process_count, slice_start)

            result = []

            for idx, user_data in enumerate(to_process):
                if idx % 10 == 0 or idx == 0:
                    logger.info("Processing user %d/%d", idx + 1, process_count)
                _id = user_data.get("_id")
                created_at = user_data.get("createdAt")
                updated_at = user_data.get("updatedAt")
                creator_id = user_data.get("creatorId")
                val = await self._mongo_default.get_user_details(creator_id)
                creator_id_role = val["name"]["first"] +" "+ val["name"]["middle"] +" "+ val["name"]["last"]
                creator_id_email = val["email"]

                updated_by_id = user_data.get("updatedById")
                val = await self._mongo_default.get_user_details(updated_by_id)
                updated_by_role = val["name"]["first"] +" "+ val["name"]["middle"] +" "+ val["name"]["last"]
                updated_by_email = val["email"]
                # is_deleted = user_data.get("isDeleted")

                title = user_data.get("title")
                resource_type = user_data.get("resourceType")
                sub_resource = user_data.get("subResource")
    
                topics = user_data.get("topics", []) # topics filter
                sub_resource_type = user_data.get("subResourceType", []) # sub refource type fileter

                description = user_data.get("description")
                if description:
                    soup = BeautifulSoup(description, "html.parser")
                    text = soup.get_text(separator="\n", strip=True)
                    description = splitter(text,3000)

                    # print("rifhif",embddings)
                abstract = user_data.get("abstract")
                description_text = user_data.get("descriptionText")
                abstract_text = user_data.get("abstractText")

                keywords = user_data.get("keywords", []) # keyword filter
                thumbnail_id = user_data.get("thumbnailId")

                # practices = user_data.get("practices", []) # filter need to verify it has yes no practice 
                disciplines = user_data.get("disciplines", []) # filter
                practice_ids = user_data.get("practiceIds", []) # has object ids need to find the collection

                is_general = user_data.get("isGeneral") 
                is_pinned = user_data.get("isPinned")

                contributors = user_data.get("contributors", []) # object id 

                contributors_str = ""

                for index, contri in enumerate(contributors):
                    val = await self._mongo_default.get_user_details(updated_by_id)
                    contributors_role = val["name"]["first"] +" "+  val["name"]["middle"] +" "+ val["name"]["last"]
                    contributors_email = val["email"]
                    contributors_str += f"{index+1}.) email {contributors_email} role : {contributors_role}\n"
                contributors_str = contributors_str.strip()

                # article_video_id = user_data.get("articleVideoId")
                # article_video_link = user_data.get("articleVideoLink")
                # article_video_type = user_data.get("articleVideoType")

                # likes_count = user_data.get("likesCount") 
                # update_flag = user_data.get("updateFlag")

                # flag_note = user_data.get("flagNote")
                # flagged_by_id = user_data.get("flaggedById")

                # article_status = user_data.get("articleStatus") # filter
                # miro_link = user_data.get("miroLink")  # private 
                # issuu_link = user_data.get("issuuLink") # private
                if not description:
                    description = [{"exact_content":None,
                                    "search_content":None}]
                for desc in description:

                    toolkit_article_json =  {
                        "created_at": created_at,
                        "updated_at": updated_at,
                        "creator_id_email": creator_id_email,
                        "creator_id_role": creator_id_role,
                        "updated_by_email": updated_by_email,
                        "updated_by_role": updated_by_role,
                        "title": title,
                        "resource_type": resource_type,
                        "sub_resource": sub_resource,
                        "description": desc["exact_content"],
                        "abstract": abstract,
                        "description_text": description_text,
                        "abstract_text": abstract_text,
                        "contributors_str": contributors_str
                    }

                    toolkit_formated_value = ToolkitArticle_Chunk.format(_id=str(_id),
                                                created_at = created_at,
                                                updated_at = updated_at,
                                                creator_id_email = creator_id_email,
                                                creator_id_role = creator_id_role,
                                                updated_by_email = updated_by_email,
                                                updated_by_role = updated_by_role,
                                                title = title,
                                                resource_type = resource_type,
                                                sub_resource = sub_resource,
                                                description = desc["exact_content"],
                                                abstract=abstract,
                                                description_text = description_text,
                                                abstract_text = abstract_text,
                                                contributors_str = contributors_str,
                                                toolkit_article_json  = ("```json\n" + json.dumps(toolkit_article_json,indent=4,default=str)+ "\n```")
                                                )
                    toolkit_article_json["id"] = str(_id)
                    embeddings = await get_embedding(toolkit_formated_value)
                    logger.debug("Embedding obtained for _id=%s (description chunks=%s)", _id, len(description) if description else 0)
                    final_json = { "id": str(_id), 
                            "text":toolkit_formated_value, 
                            "search_content" : desc["search_content"],
                            "exact_content" : desc["exact_content"],
                            "metadata":toolkit_article_json, 
                            "vector_field": embeddings}
                    result.append(final_json)
                    # with open("result.json",'w') as f:
                    #     json.dump(final_json,f,indent=4 ,default=str)
            logger.info("Prepared %d documents for bulk index", len(result))

            actions = [
                {
                    "_index": "marketing_toolkit_dag",

                    "_source": {
                        "id": str(doc["id"]),
                        "text": doc["text"],
                        "metadata": doc["metadata"],
                        "vector_field": doc["vector_field"]
                    }
                }
                for doc in result
            ]
            # with open("ok.json",'w') as f:
            #     json.dump({
            #         "_index": "marketing_toolkit",
                    
            #         "_source": {
            #             "id": str(result[0]["id"]),
            #             "text": result[0]["text"],
            #             "metadata": result[0]["metadata"],
            #             "vector_field": result[0]["vector_field"]
            #         }
            #     },f,indent=4,default=str)
            loop = asyncio.get_running_loop()
            logger.info("Starting bulk index to OpenSearch (chunk_size=200, request_timeout=60)")
            await loop.run_in_executor(
                None,
                lambda: bulk(
                    self.open_search_client,
                    actions,
                    chunk_size=200,
                    request_timeout=60
                )
            )
            logger.info("Bulk index to OpenSearch completed successfully")
            bulk(self.open_search_client, actions)
            logger.info("Pipeline run completed for toolkit_article_id=%s", toolkit_article_id)
        except Exception as e:
            logger.exception("Pipeline run failed for toolkit_article_id=%s: %s", toolkit_article_id, e)
            raise RuntimeError(f"General error occurred: {e}")


                

