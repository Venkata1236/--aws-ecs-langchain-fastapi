# ☁️ AWS ECS Fargate — LangChain FastAPI Deployment

> Deploy a LangChain FastAPI app to AWS ECS Fargate — publicly accessible, running 24/7 on the cloud with secured API keys

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green)
![LangChain](https://img.shields.io/badge/LangChain-0.2.6-green)
![Docker](https://img.shields.io/badge/Docker-containerized-blue)
![AWS ECS](https://img.shields.io/badge/AWS-ECS_Fargate-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-orange)

---

## 📌 What Is This?

A LangChain-powered FastAPI app containerized with Docker and deployed to AWS ECS Fargate. Anyone in the world can call the AI API via a public URL. API keys are stored securely in AWS Secrets Manager — never exposed in code or Docker images.

---

## 🗺️ Simple Flow
```
User (browser / Postman / any client)
        ↓
HTTP request to Public IP:8000
        ↓
AWS ECS Fargate (running Docker container)
        ↓
FastAPI endpoint
        ↓
LangChain chain (GPT-3.5 Turbo)
        ↓
OpenAI API
        ↓
JSON response back to user
```

---

## 🏗️ Architecture
```
day19-aws-ecs-langchain/
├── app/
│   ├── main.py          ← FastAPI endpoints
│   ├── chain.py         ← LangChain GPT chain
│   └── config.py        ← Environment variable loader
├── aws/
│   ├── task-definition.json  ← ECS container blueprint
│   └── deploy-notes.md       ← Step-by-step AWS guide
├── Dockerfile           ← Container build instructions
├── requirements.txt
└── .env.example
```

---

## 🧠 Key Concepts

| Concept | What It Does |
|---|---|
| **AWS ECR** | Private Docker image registry — stores your built image |
| **AWS ECS** | Elastic Container Service — runs your Docker container |
| **AWS Fargate** | Serverless ECS — AWS manages servers, you just deploy |
| **Task Definition** | Blueprint: which image, CPU/RAM, secrets to inject |
| **Secrets Manager** | Encrypted vault for OPENAI_API_KEY — injected at runtime |
| **Security Group** | Firewall rules — opens port 8000 to public internet |
| **CloudWatch** | Centralized logs from your running ECS container |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root — confirms API is live |
| GET | `/health` | Health check |
| POST | `/ask` | Ask AI a question (JSON body) |
| GET | `/ask?question=...` | Quick browser test |

---

## ⚙️ Setup

**Step 1 — Install dependencies:**
```bash
pip install -r requirements.txt
```

**Step 2 — Add to `.env`:**
```
OPENAI_API_KEY=sk-your-key
APP_TITLE=LangChain AI API
```

**Step 3 — Run locally:**
```bash
uvicorn app.main:app --reload --port 8000
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API docs.

---

## 🚀 AWS Deployment
```bash
# 1. Create ECR repo and push Docker image
aws ecr create-repository --repository-name langchain-fastapi --region ap-south-1
docker build -t langchain-fastapi .
docker tag langchain-fastapi:latest <account_id>.dkr.ecr.ap-south-1.amazonaws.com/langchain-fastapi:latest
docker push <account_id>.dkr.ecr.ap-south-1.amazonaws.com/langchain-fastapi:latest

# 2. Store secret
aws secretsmanager create-secret --name langchain-secrets \
  --secret-string '{"OPENAI_API_KEY":"your-key"}' --region ap-south-1

# 3. Create ECS cluster + register task
aws ecs create-cluster --cluster-name langchain-cluster --region ap-south-1
aws ecs register-task-definition --cli-input-json file://aws/task-definition.json --region ap-south-1

# 4. Create ECS service
aws ecs create-service --cluster langchain-cluster --service-name langchain-service \
  --task-definition langchain-fastapi-task --desired-count 1 --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --region ap-south-1
```

---

## 📦 Tech Stack

- **FastAPI** — REST API framework
- **LangChain** — GPT-3.5 Turbo chain
- **Docker** — Containerization
- **AWS ECR** — Docker image storage
- **AWS ECS Fargate** — Serverless container hosting
- **AWS Secrets Manager** — Encrypted API key storage
- **AWS CloudWatch** — Production logs

---

## 👤 Author

**Venkata Reddy Bommavaram**
- 📧 bommavaramvenkat2003@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/venkatareddy1203)
- 🐙 [GitHub](https://github.com/venkata1236)