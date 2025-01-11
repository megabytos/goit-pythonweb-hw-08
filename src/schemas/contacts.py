from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(min_length=2, max_length=64)
    last_name: str = Field(min_length=2, max_length=64)
    email: EmailStr = Field(min_length=5, max_length=64)
    phone: str = Field(min_length=7, max_length=16)
    birthday: date | None = Field(None, description='Date of birth (YYYY-MM-DD)')
    info: str | None = None


class ContactResponse(ContactModel):
    id: int
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
