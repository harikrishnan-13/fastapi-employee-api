from fastapi import FastAPI

from app.routes.employees import router as employee_router


app = FastAPI()


app.include_router(employee_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Employee Management API",
        "status": "running"
    }