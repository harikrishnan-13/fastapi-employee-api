from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeResponse


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=EmployeeResponse)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department
    )

    try:
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return new_employee

@router.get("/", response_model=list[EmployeeResponse])
def get_employees(
    db: Session = Depends(get_db)
):
    employees = db.query(Employee).all()

    return employees

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee_by_id(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    employee.name = employee_data.name
    employee.email = employee_data.email
    employee.department = employee_data.department

    try:
        db.commit()
        db.refresh(employee)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return employee

@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }