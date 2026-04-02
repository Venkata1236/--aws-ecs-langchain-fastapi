from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.chain import get_chain
from app.config import APP_TITLE

app = FastAPI(
    title=APP_TITLE,
    description="LangChain AI API deployed on AWS ECS Fargate",
    version="1.0.0"
)

chain = get_chain()

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str

@app.get("/")
def root():
    return {
        "message": "LangChain FastAPI is live on AWS ECS! 🚀",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        answer = chain.invoke({"question": request.question})
        return AnswerResponse(question=request.question, answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ask")
def ask_get(question: str):
    """Quick test via browser URL"""
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        answer = chain.invoke({"question": question})
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))