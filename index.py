from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database_handler import DatabaseHandler  # Make sure the path is correct for your project structure

app = FastAPI()
db_handler = DatabaseHandler()

class QuestionEntry(BaseModel):
    question: str
    answer: str = None

class EditEntry(BaseModel):
    question: str
    new_answer: str

@app.post("/add_question")
def add_question(entry: QuestionEntry):
    try:
        db_handler.add_question(entry.question, entry.answer)
        return {"message": "Question added successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/remove_question/{question}")
def remove_question(question: str):
    db_handler.remove_question(question)
    return {"message": "Question removed successfully if it existed."}

@app.put("/edit_question")
def edit_question(entry: EditEntry):
    db_handler.edit_question(entry.question, entry.new_answer)
    return {"message": "Question updated successfully."}

@app.get("/get_answer/{question}")
def get_answer(question: str):
    answer = db_handler.get_answer(question)
    return {"answer": answer}

@app.get("/list_questions")
def list_questions():
    questions = db_handler.list_all_questions()
    return {"questions": questions}
