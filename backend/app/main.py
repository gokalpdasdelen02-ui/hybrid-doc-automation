import time
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
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

router_service = HybridDocumentRouter(use_gpu=False)
CONFIDENCE_THRESHOLD = 0.95

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "hybrid-doc-automation-api"}

@app.post("/api/v1/documents/analyze", response_model=DocumentAnalysisResponse)
async def analyze_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Geçerli bir dosya yüklenmelidir.")

    start_time = time.perf_counter()
    file_bytes = await file.read()

    routing_path, raw_text, fields, confidence = router_service.route_and_extract(
        file_bytes=file_bytes,
        filename=file.filename
    )

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
    requires_review = confidence < CONFIDENCE_THRESHOLD
    status_label = "MANUEL_ONAY_BEKLIYOR" if requires_review else "OTOMATIK_ONAY"

    record = DocumentRecord(
        filename=file.filename,
        routing_path=routing_path,
        processing_time_ms=elapsed_ms,
        confidence_score=confidence,
        status=status_label,
        vendor_tax_id=fields.get("vendor_tax_id"),
        invoice_number=fields.get("invoice_number"),
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
