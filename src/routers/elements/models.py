from pydantic import BaseModel
from typing import List, Optional


class ElementBase(BaseModel):
    structure: Optional[str]
    statut_element: Optional[str]
    nom_base_francais: Optional[str]
    code_categorie: Optional[str]
    localisation: str
    sous_localisation: Optional[str]
    element_id: int

    class Config:
        from_attributes = True


class ElementCreate(ElementBase):
    pass


class ElementRead(ElementBase):
    emission_ids: List[int] = []
