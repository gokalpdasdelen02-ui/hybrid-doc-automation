from typing import Optional
from pydantic import BaseModel, Field

class ExtractedFieldsSchema(BaseModel):
    vendor_tax_id: Optional[str] = Field(None, description="Vergi Kimlik veya TC Kimlik Numarası")
    invoice_number: Optional[str] = Field(None, description="Fatura veya Belge Numarası")
    invoice_date: Optional[str] = Field(None, description="Belge Tarihi")
    tax_amount: Optional[float] = Field(None, description="Toplam KDV Tutarı")
    total_amount: Optional[float] = Field(None, description="Genel Toplam Tutarı")

class DocumentAnalysisResponse(BaseModel):
    document_id: int
    filename: str
    routing_path: str
    processing_time_ms: float
    confidence_score: float
    requires_manual_review: bool
    status: str
    extracted_data: ExtractedFieldsSchema

    class Config:
        from_attributes = True
