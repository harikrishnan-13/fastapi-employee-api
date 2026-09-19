from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.employees import router as employee_router


app = FastAPI()


app.include_router(employee_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Employee Management API",
        "status": "running"
    }