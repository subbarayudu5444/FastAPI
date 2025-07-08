from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

employees = []
employee_id_count = 1

class Employee(BaseModel):
    first_name: str
    last_name: str
    email: str
    mobile_number: str

class EmployeeWithID(Employee):
    id: int

@app.get("/")
def welcome():
    return {"Greeting": "Welcome To CoastalSeven"}

@app.post("/employee", response_model=EmployeeWithID)
def create_employee(employee: Employee):
    global employee_id_count
    employee_data = employee.dict()
    employee_data["id"] = employee_id_count
    employees.append(employee_data)
    employee_id_count += 1
    return employee_data

@app.get("/employees", response_model=List[EmployeeWithID])
def get_all_employees():
    return employees

@app.get("/employee/{employee_id}", response_model=EmployeeWithID)
def get_employee(employee_id: int):
    for emp in employees:
        if emp["id"] == employee_id:
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")

@app.put("/employee/{employee_id}", response_model=EmployeeWithID)
def update_employee(employee_id: int, updated_data: Employee):
    for index, emp in enumerate(employees):
        if emp["id"] == employee_id:
            updated_employee = updated_data.dict()
            updated_employee["id"] = employee_id
            employees[index] = updated_employee
            return updated_employee
    raise HTTPException(status_code=404, detail="Employee not found")

@app.delete("/employee/{employee_id}")
def delete_employee(employee_id: int):
    for index, emp in enumerate(employees):
        if emp["id"] == employee_id:
            deleted_employee = employees.pop(index)
            return {"message": "Employee deleted successfully", "employee": deleted_employee}
    raise HTTPException(status_code=404, detail="Employee not found")
