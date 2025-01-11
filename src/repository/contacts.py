from datetime import date, timedelta
from typing import List

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas.contacts import ContactModel


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, skip: int, limit: int, first_name: str | None, last_name: str | None, email: str | None) -> List[Contact]:
        stmt = select(Contact).offset(skip).limit(limit)
        if first_name:
            stmt = stmt.filter(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            stmt = stmt.filter(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            stmt = stmt.filter(Contact.email.ilike(f"%{email}%"))
        contacts = await self.db.execute(stmt)
        return list(contacts.scalars().all())

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).filter_by(id=contact_id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactModel) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update_contact(self, contact_id: int, body: ContactModel) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            for key, value in body.model_dump(exclude_unset=True).items():
                setattr(contact, key, value)
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def is_contact_exists(self, email: str, phone: str) -> bool:
        stmt = select(Contact).where(or_(Contact.email == email, Contact.phone == phone))
        result = await self.db.execute(stmt)
        return result.scalars().first() is not None

    async def get_upcoming_birthdays(self, days: int = 7) -> List[Contact]:
        today = date.today()
        upcoming_date = today + timedelta(days=days)
        stmt = select(Contact).where(
            Contact.birthday.is_not(None),
            Contact.birthday >= today,
            Contact.birthday <= upcoming_date
        ).order_by(Contact.birthday.asc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
