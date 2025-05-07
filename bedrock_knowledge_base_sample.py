"""
Amazon Bedrock Knowledge Bases Sample Code

This script demonstrates how to use Amazon Bedrock Knowledge Bases to:
1. Create a knowledge base
2. Ingest data into the knowledge base
3. Query the knowledge base using RAG (Retrieval Augmented Generation)

Requirements:
- AWS account with Amazon Bedrock access
- Appropriate IAM permissions
- boto3 library installed (pip install boto3)
"""

import boto3
import json
import time
import uuid
from botocore.exceptions import ClientError

def create_s3_bucket(bucket_name, region="XXXXXXXXX"):
    """Create an S3 bucket to store the knowledge base data"""
    s3_client = boto3.client('s3', region_name=region)
    
    try:
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
        print(f"Created S3 bucket: {bucket_name}")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"Bucket {bucket_name} already exists and is owned by you.")
            return True
        else:
            print(f"Error creating bucket: {e}")
            return False

def upload_file_to_s3(file_path, bucket_name, s3_key):
    """Upload a file to the S3 bucket"""
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
        return True
    except ClientError as e:
        print(f"Error uploading file: {e}")
        return False

def create_sample_data_file(file_path):
    """Create a sample text file with data for the knowledge base"""
    with open(file_path, 'w') as f:
        f.write("""# Amazon Bedrock Knowledge Bases

Amazon Bedrock Knowledge Bases is a capability that allows you to connect your data with 
foundation models (FMs) available through Amazon Bedrock. Knowledge bases enable you to use 
foundation models to retrieve information from your data and generate responses to queries.

## Key Features

1. **Data Ingestion**: Easily ingest and process various data formats.
2. **Vector Embeddings**: Automatically converts your data into vector embeddings.
3. **Semantic Search**: Uses advanced semantic search to find relevant information.
4. **Retrieval Augmented Generation (RAG)**: Enhances model responses with retrieved information.
5. **Fine-tuning Free**: No need to fine-tune models to work with your data.

## Common Use Cases

- Customer support chatbots
- Internal knowledge management
- Research and analysis tools
- Document search and summarization
        """)
    print(f"Sample data file created at {file_path}")
    return file_path

def create_knowledge_base(kb_name, role_arn, bucket_name, s3_prefix, region="us-east-1"):
    """Create a Knowledge Base in Amazon Bedrock"""
    bedrock_agent = boto3.client('bedrock-agent', region_name=region)
    
    try:
        # Create the knowledge base
        response = bedrock_agent.create_knowledge_base(
            name=kb_name,
            roleArn=role_arn,
            knowledgeBaseConfiguration={
                'type': 'VECTOR',
                'vectorKnowledgeBaseConfiguration': {
                    'embeddingModelArn': f'arn:aws:bedrock:{region}::foundation-model/amazon.titan-embed-text-v1'
                }
            },
            description="Sample knowledge base created via Python SDK",
            storageConfiguration={
                'type': 'S3',
                's3Configuration': {
                    'bucketName': bucket_name,
                    'prefix': s3_prefix
                }
            }
        )
        
        kb_id = response['knowledgeBase']['knowledgeBaseId']
        print(f"Created Knowledge Base with ID: {kb_id}")
        
        # Wait for the knowledge base to be active
        print("Waiting for knowledge base to become active...")
        waiter = bedrock_agent.get_waiter('knowledge_base_active')
        waiter.wait(knowledgeBaseId=kb_id, WaiterConfig={'Delay': 5, 'MaxAttempts': 60})
        
        return kb_id
    except ClientError as e:
        print(f"Error creating knowledge base: {e}")
        return None

def create_data_source(kb_id, data_source_name, bucket_name, s3_prefix, role_arn, region="us-east-1"):
    """Create a data source for the knowledge base"""
    bedrock_agent = boto3.client('bedrock-agent', region_name=region)
    
    try:
        response = bedrock_agent.create_data_source(
            knowledgeBaseId=kb_id,
            name=data_source_name,
            dataSourceConfiguration={
                'type': 'S3',
                's3Configuration': {
                    'bucketName': bucket_name,
                    'inclusionPrefixes': [s3_prefix]
                }
            },
            vectorIngestionConfiguration={
                'chunkingConfiguration': {
                    'chunkingStrategy': 'FIXED_SIZE',
                    'fixedSizeChunkingConfiguration': {
                        'maxTokens': 300,
                        'overlapPercentage': 20
                    }
                }
            },
            roleArn=role_arn
        )
        
        data_source_id = response['dataSource']['dataSourceId']
        print(f"Created Data Source with ID: {data_source_id}")
        
        # Wait for the data source to be active
        print("Waiting for data source to become active...")
        waiter = bedrock_agent.get_waiter('data_source_active')
        waiter.wait(knowledgeBaseId=kb_id, dataSourceId=data_source_id, WaiterConfig={'Delay': 5, 'MaxAttempts': 60})
        
        return data_source_id
    except ClientError as e:
        print(f"Error creating data source: {e}")
        return None

def start_data_ingestion_job(kb_id, data_source_id, region="us-east-1"):
    """Start a data ingestion job for the data source"""
    bedrock_agent = boto3.client('bedrock-agent', region_name=region)
    
    try:
        response = bedrock_agent.start_ingestion_job(
            knowledgeBaseId=kb_id,
            dataSourceId=data_source_id
        )
        
        ingestion_job_id = response['ingestionJob']['ingestionJobId']
        print(f"Started Ingestion Job with ID: {ingestion_job_id}")
        
        # Wait for the ingestion job to complete
        print("Waiting for ingestion job to complete...")
        while True:
            job_status = bedrock_agent.get_ingestion_job(
                knowledgeBaseId=kb_id,
                dataSourceId=data_source_id,
                ingestionJobId=ingestion_job_id
            )['ingestionJob']['status']
            
            if job_status in ['COMPLETE', 'FAILED']:
                print(f"Ingestion job status: {job_status}")
                break
                
            print(f"Current status: {job_status}. Waiting...")
            time.sleep(30)
            
        return job_status == 'COMPLETE'
    except ClientError as e:
        print(f"Error starting ingestion job: {e}")
        return False

def query_knowledge_base(kb_id, query_text, model_id="anthropic.claude-v2", region="us-east-1"):
    """Query the knowledge base with RAG"""
    bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name=region)
    
    try:
        response = bedrock_agent_runtime.retrieve_and_generate(
            input={
                'text': query_text
            },
            retrieveAndGenerateConfiguration={
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': kb_id,
                    'modelArn': f'arn:aws:bedrock:{region}::foundation-model/{model_id}'
                }
            }
        )
        
        # Extract the generated response
        answer = response['output']['text']
        
        # Print retrieved citations
        print("\n=== Retrieved Citations ===")
        for citation in response.get('citations', []):
            print(f"- {citation['retrievedReferences'][0]['location']['s3Location']['uri']}")
            
        return answer
    except ClientError as e:
        print(f"Error querying knowledge base: {e}")
        return None

def main():
    # Configuration parameters
    region = "us-east-1"  # Change to your preferred region
    unique_id = str(uuid.uuid4())[:8]  # Create a unique identifier for resources
    
    bucket_name = f"bedrock-kb-demo-{unique_id}"
    s3_prefix = "knowledge-base-data/"
    sample_file_path = "sample_knowledge.txt"
    s3_key = f"{s3_prefix}sample_knowledge.txt"
    
    # Replace with your IAM role ARN that has permissions for Bedrock and S3
    role_arn = "arn:aws:iam::123456789012:role/BedrockKnowledgeBaseRole"
    
    kb_name = f"Sample-KB-{unique_id}"
    data_source_name = f"Sample-Data-Source-{unique_id}"
    
    # Create a bucket and upload sample data
    if not create_s3_bucket(bucket_name, region):
        print("Failed to create S3 bucket. Exiting.")
        return
    
    # Create sample data file
    create_sample_data_file(sample_file_path)
    
    # Upload file to S3
    if not upload_file_to_s3(sample_file_path, bucket_name, s3_key):
        print("Failed to upload sample file. Exiting.")
        return
    
    # Create knowledge base
    kb_id = create_knowledge_base(kb_name, role_arn, bucket_name, s3_prefix, region)
    if not kb_id:
        print("Failed to create knowledge base. Exiting.")
        return
    
    # Create data source
    data_source_id = create_data_source(kb_id, data_source_name, bucket_name, s3_prefix, role_arn, region)
    if not data_source_id:
        print("Failed to create data source. Exiting.")
        return
    
    # Start data ingestion
    if not start_data_ingestion_job(kb_id, data_source_id, region):
        print("Data ingestion failed. Exiting.")
        return
    
    # Query the knowledge base using RAG
    print("\n=== Querying Knowledge Base ===")
    query = "What is Amazon Bedrock Knowledge Bases and what are its key features?"
    response = query_knowledge_base(kb_id, query, region=region)
    
    print("\n=== Response ===")
    print(response)
    
    print("\nDemo completed successfully!")

if __name__ == "__main__":
    main()