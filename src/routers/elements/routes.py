from fastapi import APIRouter
from src.database.db import SessionLocal
from src.database.models import Element
from src.routers.elements.models import ElementCreate, ElementRead
from sqlalchemy.orm import joinedload
from typing import List

elements_router = APIRouter(tags=["Elements Rest Api"], prefix="/elements")


@elements_router.get("/", response_model=List[ElementRead])
def get_all_elements():
    with SessionLocal() as session:
        elements = session.query(Element).options(joinedload(Element.emissions)).all()
        return [
            {
                "element_id": e.element_id,
                "structure": e.structure,
                "statut_element": e.statut_element,
                "nom_base_francais": e.nom_base_francais,
                "code_categorie": e.code_categorie,
                "localisation": e.localisation,
                "sous_localisation": e.sous_localisation,
                "emission_ids": [emission.emission_id for emission in e.emissions],
            }
            for e in elements
        ]


@elements_router.post("/", response_model=ElementRead, status_code=201)
def create_element(element: ElementCreate):
    with SessionLocal() as session:
        db_element = Element(**element.model_dump())
        session.add(db_element)
        session.commit()
        session.refresh(db_element)
        return db_element
