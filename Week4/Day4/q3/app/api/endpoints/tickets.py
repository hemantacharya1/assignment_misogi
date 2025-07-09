from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.ticket import TicketCreate, TicketOut
from app.services.ticket_processor import process_ticket
from app.db.models import Ticket
from app.api.deps import get_db

router = APIRouter()

@router.post("/tickets", response_model=TicketOut)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    enriched = process_ticket(ticket.title, ticket.description)

    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        generated_response=enriched["response"],
        auto_category=enriched["category"],
        priority=enriched["priority"],
        tags=enriched["tags"],
        confidence_score=enriched["confidence_score"],
        status="completed"
    )

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
