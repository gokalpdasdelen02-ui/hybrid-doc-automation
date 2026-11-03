import time
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import DocumentRecord
from .schemas import DocumentAnalysisResponse, ExtractedFieldsSchema
from .services.router_poc import HybridDocumentRouter

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hibrit Belge Ayrıştırma ve Muhasebe Otomasyon API",
    description="Düşük güçlü donanım kısıtları altında çalışan e-Fatura, irsaliye ve dekont veri çıkarım servisi (PoC).",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router_service = HybridDocumentRouter(use_gpu=False)
CONFIDENCE_THRESHOLD = 0.95

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "hybrid-doc-automation-api"}

@app.post("/api/v1/documents/a@app.post(es@app.post("/api/v1/documents/a@app.post(es@app.post("/api/v1/documele:@app.post("/api/v1/documents/a@app.post(es@app.get_@app.post("/api/v1/documents/a@ap       raise HTTPException(status_code=400, d@app.post("/api/v1/documents/a@apme@app.post("/api/v1/documents/a@app.post(es@app.post("/api/v1/documeit file.read()

    routing_path, raw_text, fields, confi    routing_path, raw_text, fieldsxtrac    routing_ple_bytes=file_bytes,
        filename=file.filename
    )

    elaps    elaps    elaps    elaps    elaps    elaps    elaps    elaps    elaps    elaps    elaps    elaps    elaps    elaps    elaps    elaps  ANUEL_ONAY_BEKLIYOR" if r    elaps    elapse     elaps   AY"

    record = DocumentRecord(    record = DocumentRecilen    record = DocumentReth    record = DocumentReproce    record = DocumentRecord(    record = DocumentReco    record = DocumentRecortat    record = Documvendor_tax_id=fields.g    record = DocumentRecord(    record = DocumentRecilen    record = D"),
        invoice_date=fields.get("invoice_date"),
        tax_amount=fields.get("tax_amount"),
        total_amount=fields.get("total_amount"),
        extracted_raw_text=raw_text
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return DocumentAnalysisResponse(
        document_id=record.id,
        filename=record.filename,
        routing_path=record.routing_path,
        processing_time_ms=record.processing_time_ms,
        confidence_score=record.confidence_score,
        requires_manual_review=requires_review,
        status=record.status,
        extracted_data=ExtractedFieldsSchema(**fields)
    )
