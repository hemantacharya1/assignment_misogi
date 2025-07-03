from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Interaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    product_id: int = Field(foreign_key="product.id", nullable=False, index=True)
    type: str = Field(index=True, description="view | like | purchase")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="interactions")
    product: Optional["Product"] = Relationship(back_populates="interactions")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    interactions: list[Interaction] = Relationship(back_populates="user")


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    category: str = Field(index=True)
    price: float
    description: str
    rating: Optional[float] = Field(default=None)
    image_url: Optional[str] = Field(default=None)

    interactions: list[Interaction] = Relationship(back_populates="product")


# Back-populate relationships
Interaction.user = Relationship(back_populates="interactions")  # type: ignore
Interaction.product = Relationship(back_populates="interactions")  # type: ignore 