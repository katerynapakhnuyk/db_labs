from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime

app = FastAPI()

# ⏱ Ініціалізовані "дані" — аналог INSERT INTO
class Quiz(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    creation_date: datetime
    close_date: Optional[datetime]
    is_active: bool
    owner_id: UUID

class QuizCreate(BaseModel):
    title: str
    description: Optional[str]
    close_date: Optional[datetime]
    is_active: bool
    owner_id: UUID

quizzes: List[Quiz] = [
    Quiz(
        id=uuid4(),
        title="Customer Satisfaction Quiz",
        description="Quiz about customer satisfaction",
        creation_date=datetime(2025, 4, 20, 10, 0, 0),
        close_date=datetime(2025, 4, 30, 23, 59, 59),
        is_active=True,
        owner_id=UUID("e7b3f5b4-8a63-4e2e-baad-5a8c5c5b1234")
    ),
    Quiz(
        id=uuid4(),
        title="Employee Feedback Quiz",
        description="Quiz to collect employee feedback",
        creation_date=datetime(2025, 4, 21, 12, 0, 0),
        close_date=None,
        is_active=True,
        owner_id=UUID("0e00b3e1-2c66-4f56-9332-9e20bfcdb812")
    ),
    Quiz(
        id=uuid4(),
        title="Website Usability Quiz",
        description="Quiz to evaluate website usability",
        creation_date=datetime(2025, 4, 22, 14, 0, 0),
        close_date=datetime(2025, 5, 1, 20, 0, 0),
        is_active=False,
        owner_id=UUID("7f6c9aee-681c-4f61-812d-dcd7edb7b029")
    )
]

# 🔍 GET /quiz/{id}
@app.get("/quiz/{quiz_id}", response_model=Quiz)
def get_quiz(quiz_id: UUID):
    for quiz in quizzes:
        if quiz.id == quiz_id:
            return quiz
    raise HTTPException(status_code=404, detail="Quiz not found")

@app.get("/quiz", response_model=List[Quiz])
def get_all_quizzes():
    return quizzes

# 📥 POST /quiz
@app.post("/quiz", response_model=Quiz)
def create_quiz(quiz_data: QuizCreate):
    quiz = Quiz(
        id=uuid4(),
        title=quiz_data.title,
        description=quiz_data.description,
        creation_date=datetime.utcnow(),
        close_date=quiz_data.close_date,
        is_active=quiz_data.is_active,
        owner_id=quiz_data.owner_id
    )
    quizzes.append(quiz)
    return quiz

# 🔄 PUT /quiz/{id}
@app.put("/quiz/{quiz_id}")
def update_quiz(quiz_id: UUID, quiz_data: QuizCreate):
    for idx, quiz in enumerate(quizzes):
        if quiz.id == quiz_id:
            updated_quiz = quiz.copy(update={
                "title": quiz_data.title,
                "description": quiz_data.description,
                "close_date": quiz_data.close_date,
                "is_active": quiz_data.is_active,
                "owner_id": quiz_data.owner_id
            })
            quizzes[idx] = updated_quiz
            return {"detail": "Quiz updated"}
    raise HTTPException(status_code=404, detail="Quiz not found")

# 🗑 DELETE /quiz/{id}
@app.delete("/quiz/{quiz_id}")
def delete_quiz(quiz_id: UUID):
    for idx, quiz in enumerate(quizzes):
        if quiz.id == quiz_id:
            quizzes.pop(idx)
            return {"detail": "Quiz deleted"}
    raise HTTPException(status_code=404, detail="Quiz not found")
