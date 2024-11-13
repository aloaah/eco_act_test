from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base

class Element(Base):
    __tablename__ = "element"

    element_id = Column(Integer, primary_key=True)
    structure = Column(String, nullable=True)
    statut_element = Column(String, nullable=True)
    nom_base_francais = Column(String, nullable=True)
    code_categorie = Column(String, nullable=True)
    localisation = Column(String, nullable=False)
    sous_localisation = Column(String, nullable=True)

    # Relationship with `emission_data`
    emissions = relationship("EmissionData", back_populates="element")

class EmissionData(Base):
    __tablename__ = 'emission_data'
    
    emission_id = Column(Integer, primary_key=True, autoincrement=True)
    element_id = Column(Integer, ForeignKey('element.element_id'), nullable=False)
    incertitude = Column(String, nullable=True)
    co2f = Column(Float, nullable=True)
    ch4f = Column(Float, nullable=True)
    n2o = Column(Float, nullable=True)
    autres_ges = Column(Float, nullable=True)
    co2b = Column(Float, nullable=True)
    unite_francais = Column(String, nullable=True)
    total_poste_non_decompose = Column(Float, nullable=False)
    divers = Column(Float, nullable=True)
    sf6 = Column(Float, nullable=True)
    
    element = relationship("Element", back_populates="emissions")
    quality_metrics = relationship("QualityMetrics", back_populates="emission_data")
    process_types = relationship("ProcessType", back_populates="emission_data")

class QualityMetrics(Base):
    __tablename__ = 'quality_metrics'
    
    quality_id = Column(Integer, primary_key=True, autoincrement=True)
    emission_id = Column(Integer, ForeignKey('emission_data.emission_id'), nullable=False)
    qualite_ter = Column(String, nullable=True)
    qualite_gr = Column(String, nullable=True)
    qualite_tir = Column(String, nullable=True)
    qualite_c = Column(String, nullable=True)
    qualite_p = Column(String, nullable=True)
    qualite_m = Column(String, nullable=True)
    transparence_score = Column(String, nullable=True)
    qualite_score = Column(String, nullable=True)
    
    # Relationship with `emission_data`
    emission_data = relationship("EmissionData", back_populates="quality_metrics")

class ProcessType(Base):
    __tablename__ = 'process_type'
    
    process_id = Column(Integer, primary_key=True, autoincrement=True)
    emission_id = Column(Integer, ForeignKey('emission_data.emission_id'), nullable=False)
    type_poste = Column(String, nullable=True)
    nom_poste_francais = Column(String, nullable=True)
    type_ligne = Column(String, nullable=False)
    commentaire_français = Column(String, nullable=True)
    
    # Relationship with `emission_data`
    emission_data = relationship("EmissionData", back_populates="process_types")