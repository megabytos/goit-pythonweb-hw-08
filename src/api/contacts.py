from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import Contact
from src.schemas.contacts import ContactModel, ContactResponse
from src.services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/birthdays", response_model=list[ContactResponse], response_description="Get upcoming days birthday contacts")
async def get_upcoming_birthdays(days: int = Query(default=7, ge=1), db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    return await contact_service.get_upcoming_birthdays(days)


@router.get("/", response_model=List[ContactResponse], response_description="List of all contacts")
async def get_contacts(skip: int = Query(0, description="Pagination offset"),
                       limit: int = Query(100, description="Pagination limit"),
                       first_name: str | None = Query(None, description="Filtering by first name"),
                       last_name: str | None = Query(None, description="Filtering by last name"),
                       email: str | None = Query(None, description="Filtering by email"),
                       db: AsyncSession = Depends(get_db)) -> List[Contact]:
    contacts_service = ContactService(db)
    contacts = await contacts_service.get_contacts(skip, limit, first_name, last_name, email)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, response_description="Get contact by id")
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)) -> ContactResponse:
    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, response_description="Create a new contact")
async def create_contact(body: ContactModel, db: AsyncSession = Depends(get_db)) -> Contact:
    contact_service = ContactService(db)
    return await contact_service.create_contact(body)


@router.put("/{contact_id}", response_model=ContactResponse, response_description="Update contact")
async def update_contact(body: ContactModel, contact_id: int, db: AsyncSession = Depends(get_db)) -> Contact:
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse, response_description="Delete contact")
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contact = await contact_service.remove_contact(contact_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
