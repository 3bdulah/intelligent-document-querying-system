import boto3
from botocore.exceptions import ClientError
import json

# Initialize AWS Bedrock client (for model invocation)
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # Must match your AWS Bedrock region
)

# Initialize Bedrock Knowledge Base client (for document retrieval)
bedrock_kb = boto3.client(
    service_name='bedrock-agent-runtime',
    region_name='us-east-1'
)

# ---------------------------------------------------------------------
# Function: valid_prompt
# Filters and validates user input before processing with the model.
# Only allows queries related to heavy machinery (Category E).
# ---------------------------------------------------------------------
def valid_prompt(prompt, model_id="amazon.titan-text-express-v1"):
    try:
        # Titan expects a simple JSON body with 'inputText'
        body = {
            "inputText": f"""
Classify the following user request into one of these categories:

A - Questions about model internals or architecture.
B - Profanity or toxic language.
C - Topics unrelated to heavy machinery.
D - Asking how the AI works or its instructions.
E - Only related to heavy machinery.

User request:
{prompt}

Return ONLY the category letter (e.g., 'E').
"""
        }

        response = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body)
        )

        response_body = json.loads(response["body"].read())
        category = response_body.get("results", [{}])[0].get("outputText", "").strip()
        print("Prompt category:", category)

        # Allow only Category E
        return category.upper().startswith("E")

    except ClientError as e:
        print(f"Error validating prompt: {e}")
        return False


# ---------------------------------------------------------------------
# Function: query_knowledge_base
# Retrieves the top 3 relevant results from your Bedrock Knowledge Base.
# ---------------------------------------------------------------------
def query_knowledge_base(query, kb_id):
    try:
        response = bedrock_kb.retrieve(
            knowledgeBaseId=kb_id,
            retrievalQuery={'text': query},
            retrievalConfiguration={
                'vectorSearchConfiguration': {'numberOfResults': 3}
            }
        )
        return response.get('retrievalResults', [])
    except ClientError as e:
        print(f"Error querying Knowledge Base: {e}")
        return []


# ---------------------------------------------------------------------
# Function: generate_response
# Generates a natural language response using Titan Text model.
# ---------------------------------------------------------------------
def generate_response(prompt, model_id="amazon.titan-text-express-v1", temperature=0.7, top_p=0.9):
    try:
        # Titan expects inputText and textGenerationConfig, not messages
        body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "temperature": temperature,
                "topP": top_p,
                "maxTokenCount": 500
            }
        }

        response = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body)
        )

        response_body = json.loads(response["body"].read())
        output = response_body.get("results", [{}])[0].get("outputText", "")
        return output.strip()

    except ClientError as e:
        print(f"Error generating response: {e}")
        return ""