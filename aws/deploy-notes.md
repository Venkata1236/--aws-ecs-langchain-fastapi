# AWS Deployment Guide (Beginner-Friendly)

## What is ECS Fargate?
ECS = Elastic Container Service (runs Docker containers)
Fargate = Serverless mode (AWS manages servers, you just deploy your container)

## Step-by-Step Deployment

### STEP 1: Create AWS Free Tier Account
- Go to https://aws.amazon.com → Create Account
- Region to use: ap-south-1 (Mumbai, closest to Hyderabad)

### STEP 2: Install AWS CLI
```bash
# On Windows (PowerShell as Admin)
winget install Amazon.AWSCLI
aws --version
aws configure
# Enter: Access Key, Secret Key, Region: ap-south-1, Format: json
```

### STEP 3: Create ECR Repository (store your Docker image)
```bash
aws ecr create-repository --repository-name langchain-fastapi --region ap-south-1
```
Copy the repositoryUri from the output.

### STEP 4: Build & Push Docker Image
```bash
# Login to ECR
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com

# Build image
docker build -t langchain-fastapi .

# Tag image
docker tag langchain-fastapi:latest YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/langchain-fastapi:latest

# Push image
docker push YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/langchain-fastapi:latest
```

### STEP 5: Store Secret in AWS Secrets Manager
- AWS Console → Secrets Manager → Store a new secret
- Key: OPENAI_API_KEY, Value: your actual key
- Name it: langchain-secrets

### STEP 6: Create ECS Cluster
```bash
aws ecs create-cluster --cluster-name langchain-cluster --region ap-south-1
```

### STEP 7: Register Task Definition
- Update task-definition.json with YOUR_ACCOUNT_ID
```bash
aws ecs register-task-definition --cli-input-json file://aws/task-definition.json
```

### STEP 8: Create ECS Service
- AWS Console → ECS → Clusters → langchain-cluster → Create Service
- Launch type: FARGATE
- Task definition: langchain-fastapi-task
- Enable public IP: YES
- Security group: Allow inbound port 8000

### STEP 9: Access Your API
- Go to ECS → Your running task → Click on the task → Copy Public IP
- Open browser: http://PUBLIC_IP:8000/docs ✅