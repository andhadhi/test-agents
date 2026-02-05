ToolkitArticle_Chunk_str = '''
the marketing toolkit id is {_id}. it was created at {created_at}. it was updated at {updated_at}. it was created by {creator_id_email} and his name or role is {creator_id_role}. the marketing toolkit was last updated by {updated_by_email} and  his name or role is {updated_by_role}.
marketing toolkid's fields are
title : {title}
resource_type : {resource_type}
sub_resource : {sub_resource}
description : {description}
abstract : {abstract}
description_text : {description_text}
abstract_text : {abstract_text}

contributors for the marketing toolkits are : \n{contributors_str}
'''

ToolkitArticle_Chunk = '''

{toolkit_article_json}

##  Marketing Toolkit Article

- **Toolkit ID:** `{_id}`
- **Created At:** `{created_at}`
- **Updated At:** `{updated_at}`

### Created By
- **Email:** `{creator_id_email}`
- **Name / Role:** `{creator_id_role}`

### Last Updated By
- **Email:** `{updated_by_email}`
- **Name / Role:** `{updated_by_role}`

## Toolkit Details

- **Title:** `{title}`
- **Resource Type:** `{resource_type}`
- **Sub Resource:** `{sub_resource}`

### Description
{description}

### Abstract
{abstract}

### Description (Plain Text)
{description_text}

### Abstract (Plain Text)
{abstract_text}

## Contributors
{contributors_str}
'''