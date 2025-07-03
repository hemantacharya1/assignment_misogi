from __future__ import annotations

import json
from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from .database import engine, get_session, init_db
from .models import Product
from .routers import products as products_router
from .routers import auth as auth_router

app = FastAPI(title="AI Product Recommender", version="0.1.0")

# CORS for dev – allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router.router)
app.include_router(auth_router.router)


@app.on_event("startup")
def on_startup() -> None:
    """Create tables and seed products if necessary."""
    init_db()

    # Seed products
    with Session(engine) as session:
        product_exists = session.exec(select(Product).limit(1)).first() is not None
        if product_exists:
            return

        mock_file = Path(__file__).resolve().parent / "mock_data.json"
        if not mock_file.exists():
            app.logger.warning("mock_data.json not found – skipping seed")
            return

        data: List[dict] = json.loads(mock_file.read_text())
        products = []
        for item in data:
            try:
                product = Product(
                    id=item.get("product_id"),
                    name=item.get("product_name"),
                    category=item.get("category"),
                    price=item.get("price"),
                    description=item.get("description"),
                    rating=item.get("rating"),
                    image_url=item.get("image_url"),
                )
                products.append(product)
            except Exception as exc:
                # Skip problematic records but log in real scenario
                print(f"Failed to parse product: {exc}")
        session.add_all(products)
        session.commit()


@app.get("/", tags=["Root"])
def root():
    return {"status": "ok"} 