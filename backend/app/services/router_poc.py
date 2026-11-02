import fitz
from typing import Tuple, Dict, Any
from .pdf_parser import FinancialTextExtractor
from .ocr_engine import LowPowerOCREngine

class HybridDocumentRouter:
    """Gelen belgeyi analiz ederek dijital PDF ayrıştırıcıya veya yerel OCR hattına yönlendirir."""

    MIN_DIGITAL_TEXT_LENGTH = 40

    def __init__(self, use_gpu: bool = False):
        self.ocr_engine = LowPowerOCREngine(use_gpu=use_gpu)

    def route_and_extract(self, file_bytes: bytes, filename: str) -> Tuple[str, str, Dict[str, Any], float]:
        lower_name = filename.lower()

        if lower_name.endswith(".pdf"):
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            extracted_text = ""
            for page in doc:
                extracted_text += page.get_text("text")

            if len(extracted_text.strip()) >= self.MIN_DIGITAL_TEXT_LENGTH:
                fields, confidence = FinancialTextExtractor.extract_fields(extracted_text, base_confidence=0.99)
                return "DIGITAL_PDF", extracted_text, fields, confidence

            first_page_pix = doc[0].get_pixmap(dpi=200)
            img_bytes = first_page_pix.tobytes("png")
            raw_text, fields, confidence = self.ocr_engine.process_image_bytes(img_bytes)
            return "OCR_PIPELINE", raw_text, fields, confidence

        raw_text, fields, confidence = self.ocr_engine.process_image_bytes(file_bytes)
        return "OCR_PIPELINE", raw_text, fields, confidence
