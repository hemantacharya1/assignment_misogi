from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import Product

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[Product])
def list_products(
    *,
    session: Session = Depends(get_session),
    search: Optional[str] = Query(None, description="Search keyword"),
    category: Optional[str] = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    offset = (page - 1) * page_size

    statement = select(Product)

    if search:
        ilike = f"%{search.lower()}%"
        statement = statement.where(
            (Product.name.ilike(ilike)) | (Product.description.ilike(ilike))
        )
    if category:
        statement = statement.where(Product.category == category)

    statement = statement.offset(offset).limit(page_size)

    products = session.exec(statement).all()
    return products


@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, *, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product 