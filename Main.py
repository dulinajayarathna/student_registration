from typing import Optional, List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from uuid import uuid4, UUID

app = FastAPI()

class Student(BaseModel):
    id: Optional[UUID] = None
    name: str
    email: EmailStr
    age: Optional[int] = None
    course: str

students: List[Student] = []

# View All Students
@app.get('/students', response_model=List[Student])
def read_all_students():
    return students

# View Student by ID
@app.get('/students/{student_id}', response_model=Student)
def read_student(student_id: UUID):
    for student in students:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

# Create Student
@app.post('/students', response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    student.id = uuid4()
    students.append(student)
    return student

# Delete Student
@app.delete('/students/{student_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: UUID):
    for index, student in enumerate(students):
        if student.id == student_id:
            del students[index]
            return
    raise HTTPException(status_code=404, detail="Student not found")

# Update Student
@app.put('/students/{student_id}', response_model=Student)
def update_student(student_id: UUID, updated_student: Student):
    for index, student in enumerate(students):
        if student.id == student_id:
            updated_student.id = student_id
            students[index] = updated_student
            return updated_student
    raise HTTPException(status_code=404, detail="Student not found")
