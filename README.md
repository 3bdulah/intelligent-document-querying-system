# AWS Bedrock Knowledge Base with Aurora Serverless

This project sets up an AWS Bedrock Knowledge Base integrated with an Aurora Serverless PostgreSQL database. It also includes scripts for database setup and file upload to S3.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Deployment Steps](#deployment-steps)
5. [Using the Scripts](#using-the-scripts)
6. [Customization](#customization)
7. [Troubleshooting](#troubleshooting)
8. [Student Addendum](#Student-Addendum)

## Project Overview

This project consists of several components:

1. Stack 1 - Terraform configuration for creating:
   - A VPC
   - An Aurora Serverless PostgreSQL cluster
   - s3 Bucket to hold documents
   - Necessary IAM roles and policies

2. Stack 2 - Terraform configuration for creating:
   - A Bedrock Knowledge Base
   - Necessary IAM roles and policies

3. A set of SQL queries to prepare the Postgres database for vector storage
4. A Python script for uploading files to an s3 bucket

The goal is to create a Bedrock Knowledge Base that can leverage data stored in an Aurora Serverless database, with the ability to easily upload supporting documents to S3. This will allow us to ask the LLM for information from the documentation.

> **Cost and security warning:** provisioning can create billable AWS resources, including networking, Aurora, S3, and Bedrock-related storage or processing. Review `terraform plan`, AWS pricing, IAM permissions, and network exposure before applying changes. Use least-privilege credentials and never commit real keys. After testing, review each stack's resources and remove them deliberately when no longer needed; confirm the target workspace and back up any data before running destructive cleanup.

## Prerequisites

Before you begin, ensure you have the following:

- AWS CLI installed and configured with appropriate credentials
- Terraform installed (version 0.12 or later)
- Python 3.10 or later
- pip (Python package manager)

## Project Structure

```
project-root/
│
├── stack1
|   ├── main.tf
|   ├── outputs.tf
|   └── variables.tf
|
├── stack2
|   ├── main.tf
|   ├── outputs.tf
|   └── variables.tf
|
├── modules/
│   ├── aurora_serverless/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── bedrock_kb/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
├── scripts/
│   ├── aurora_sql.sql
│   └── upload_to_s3.py
│
├── spec-sheets/
│   └── machine_files.pdf
│
└── README.md
```

## Deployment Steps

1. Clone this repository to your local machine.

2. Navigate to the project Stack 1. This stack includes VPC, Aurora servlerless and S3

3. Initialize Terraform:
   ```
   terraform init
   ```

4. Review and modify the Terraform variables in `main.tf` as needed, particularly:
   - AWS region
   - VPC CIDR block
   - Aurora Serverless configuration
   - s3 bucket

5. Deploy the infrastructure:
   ```
   terraform apply
   ```
   Review the planned changes and type "yes" to confirm.

6. After the Terraform deployment is complete, note the outputs, particularly the Aurora cluster endpoint.

7. Prepare the Aurora Postgres database. This is done by running the sql queries in the script/ folder. This can be done through Amazon RDS console and the Query Editor.

8. Navigate to the project Stack 2. This stack includes Bedrock Knowledgebase

9. Initialize Terraform:
   ```
   terraform init
   ```

10. Use the values outputs of the stack 1 to modify the values in `main.tf` as needed:
     - Bedrock Knowledgebase configuration

11. Deploy the infrastructure:
      ```
      terraform apply
      ```
      - Review the planned changes and type "yes" to confirm.


12. Upload pdf files to S3, place your files in the `spec-sheets` folder and run:
      ```
      python scripts/upload_to_s3.py
      ```
      - Make sure to update the S3 bucket name in the script before running.

13. Sync the data source in the knowledgebase to make it available to the LLM.

## Using the Scripts

### S3 Upload Script

The `upload_to_s3.py` script does the following:
- Uploads all files from the `spec-sheets` folder to a specified S3 bucket
- Maintains the folder structure in S3

To use it:
1. Update the `bucket_name` variable in the script with your S3 bucket name.
2. Optionally, update the `prefix` variable if you want to upload to a specific path in the bucket.
3. Run `python scripts/upload_to_s3.py`.

## Complete chat app

### Complete invoke model and knoweldge base code
- Open the bedrock_utils.py file and the following functions:
  - query_knowledge_base
  - generate_response

### Complete the prompt validation function
- Open the bedrock_utils.py file and the following function:
  - valid_prompt

  Hint: categorize the user prompt

## Troubleshooting

- If you encounter permissions issues, ensure your AWS credentials have the necessary permissions for creating all the resources.
- For database connection issues, check that the security group allows incoming connections on port 5432 from your IP address.
- If S3 uploads fail, verify that your AWS credentials have permission to write to the specified bucket.
- For any Terraform errors, ensure you're using a compatible version and that all module sources are correctly specified.

For more detailed troubleshooting, refer to the error messages and logs provided by Terraform and the Python scripts.

---

## Student Addendum

### Overview
This section documents the additional components, enhancements, and verification steps implemented by **Abdullah Hani Abdellatif Al-Shobaki** to extend the AWS Bedrock Knowledge Base project beyond the base requirements. The focus was on practical integration, interactive usability, and full security compliance.

---

### Enhancements Implemented

#### 1. Streamlit Web Application (`app.py`)
Developed a clean, interactive web interface that allows real-time querying of the Bedrock Knowledge Base through a chat-style UI.  
Key features include:
- **User Input Validation** via `valid_prompt()` to filter unrelated or unsafe queries.  
- **Dynamic Context Injection** from retrieved knowledge base results for more accurate responses.  
- **Configurable Parameters** for model selection, temperature, and top-p through Streamlit sidebar controls.  
- **Persistent Chat History** providing a smooth conversational flow.  

#### 2. Python–Bedrock Integration Testing
Verified complete functionality of the core modules:
- `valid_prompt()` → Correctly classifies prompts into Category E (heavy machinery).  
- `query_knowledge_base()` → Retrieves relevant documents from the Aurora-connected Knowledge Base.  
- `generate_response()` → Produces coherent, contextual answers using the Bedrock runtime models.  

All tests executed successfully in both terminal and Streamlit environments. Screenshots of each test are included in the `/Screenshots` folder.

#### 3. Security and Sanitization
Performed a comprehensive workspace audit to ensure **no sensitive AWS data** remains:
- Replaced all ARNs, endpoints, account IDs, and secret identifiers with placeholders such as `<YOUR_AURORA_ARN>` or `<YOUR_SECRET_ARN>`.  
- Removed `.terraform` and state files.  
- Added `.gitignore` to prevent accidental inclusion of credentials or environment files.  

Final verification confirmed the workspace is **100 % sanitized and safe for public GitHub release**.

#### 4. Documentation and Clarity
- Added `temperature_top_p_explanation.pdf` describing how the parameters influence Bedrock LLM outputs.  
- Organized all screenshots under a dedicated `/Screenshots` directory following Udacity’s rubric order.  
- Cross-checked every rubric requirement from Terraform setup to Python integration.  

---

### Outcome
The final system integrates AWS Bedrock, Aurora Serverless, and Streamlit into a cohesive, secure, and fully functional **Intelligent Document Querying System**.  
All features have been verified, documented, and prepared for public submission while maintaining complete data security.

---