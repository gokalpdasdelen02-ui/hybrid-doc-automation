from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from .database import Base

class DocumentRecord(Base):
    __tablename__ = "document_records"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    document_type = Column(String(50), default="FATURA")
    routing_path = Column(String(50), nullable=False)
    processing_time_ms = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)
    vendor_tax_id = Column(String(20), nullable=True)
    invoice_number = Column(String(100), nullable=True)
    invoice_date = Column(String(50), nullable=True)
    tax_amount = Column(Float, nullable=True)
    total_amount = Column(Float, nullable=True)
    extracted_raw_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
