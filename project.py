# Install Libraries: pip install fastapi uvicorn pydantic

# Execution Command: uvicorn project_get:app --reload

from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open('student_data.json', 'r') as f:
        data = json.load(f)

    return data


@app.get("/")
def hello_world():
    return {"Message": "Student Management System API"}


@app.get("/about")
def about():
    return {"Message": "A fully functional API to manage your student records."}


@app.get("/view")
def view():
    data = load_data()

    return data


@app.get("/student/{student_id}")
def view_student(student_id:str = Path(..., description='Please enter ID of student in records', example='S001')):
    #  = Path(..., description='Please enter ID of student in records', example='S001')

    # load all students
    data = load_data()
    student_id = student_id.strip().upper()
    if student_id in data:
        return data[student_id]
    else:
        # return {'Error Message': 'Student not found, Please enter correct student id'}
        raise HTTPException(status_code=404, detail=f"Student not found with ID {student_id}, Please enter correct student id")


@app.get("/students/search")
def search_students(
    name: str | None = Query(default=None, min_length=1),
    age: int | None = Query(default=None, ge=0),
    city: str | None = Query(default=None, min_length=1),
    student_class: str | None = Query(default=None, min_length=1),
    division: str | None = Query(default=None, min_length=1),
    result: str | None = Query(default=None, min_length=1),
):
    text_filters = {
        "name": name,
        "city": city,
        "student_class": student_class,
        "division": division,
        "result": result,
    }
    filters = {}
    for field, value in text_filters.items():
        if value is not None:
            query = value.strip().casefold()
            if not query:
                raise HTTPException(status_code=400, detail=f"{field} cannot be empty")
            filters[field] = query

    if age is None and not filters:
        raise HTTPException(status_code=400, detail="Provide at least one search filter")

    data = load_data()
    return [
        student
        for student in data.values()
        if (age is None or student.get("age") == age)
        and all(
            query in str(student.get(field, "")).casefold()
            for field, query in filters.items()
        )
    ]


@app.get("/sort")
def sort_students(
    sort_by: str = Query(..., description="Sort on the basis of age etc."), 
    order_by: str = Query('asc', description="Sort in asc or desc order")):

    # all valid fields (integer or float)
    valid_fields = ['age','name']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_fields}")
    
    if order_by not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order select between asc and desc")

    data = load_data()

    sort_order = True if order_by == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data





