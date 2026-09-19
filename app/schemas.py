
from pydantic import BaseModel, ConfigDict, EmailStr


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str

    model_config = ConfigDict(
        from_attributes=True
    )


class EmployeeListResponse(BaseModel):
    page: int
    page_size: int
    total_count: int
    total_pages: int
    data: list[EmployeeResponse]


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str