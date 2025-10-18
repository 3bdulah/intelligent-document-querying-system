provider "aws" {
  region = "us-east-1"
}

module "bedrock_kb" {
  source = "../modules/bedrock_kb"

  knowledge_base_name        = "my-bedrock-kb"
  knowledge_base_description = "Knowledge base connected to Aurora Serverless database"

  aurora_arn        = "<YOUR_AURORA_ARN>"
  aurora_db_name    = "bedrockdb"
  aurora_endpoint   = "<YOUR_AURORA_ENDPOINT>"
  aurora_table_name = "bedrock_integration.bedrock_kb"
  aurora_primary_key_field = "id"
  aurora_metadata_field = "metadata"
  aurora_text_field = "content"
  aurora_verctor_field = "embedding"
  aurora_username   = "dbadmin"
  aurora_secret_arn = "<YOUR_AURORA_SECRET_ARN>"
  s3_bucket_arn     = "<YOUR_S3_BUCKET_ARN>"
}