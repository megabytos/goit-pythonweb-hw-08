from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.repository.contacts import ContactRepository
from src.schemas.contacts import ContactModel


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def get_contacts(self, skip: int, limit: int, first_name: str | None, last_name: str | None, email: str | None) -> List[Contact]:
        return await self.repository.get_contacts(skip, limit, first_name, last_name, email)

    async def create_contact(self, body: ContactModel) -> Contact:
        if await self.repository.is_contact_exists(body.email, body.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Contact with such email or such phone number already exists."
            )
        return await self.repository.create_contact(body)

    async def get_contact(self, contact_id: int):
        return await self.repository.get_contact_by_id(contact_id)

    async def update_contact(self, contact_id: int, body: ContactModel) -> Contact:
        return await self.repository.update_contact(contact_id, body)

    async def remove_contact(self, contact_id: int):
        return await self.repository.remove_contact(contact_id)

    async def get_upcoming_birthdays(self, days: int) -> List[Contact]:
        return await self.repository.get_upcoming_birthdays(days)
