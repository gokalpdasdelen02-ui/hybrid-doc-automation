from typing import Tuple, Dict, Any
from .pdf_parser import FinancialTextExtractor

class LowPowerOCREngine:
    """Taranmış fatura ve dekont görselleri için yerel OCR motoru (PoC)."""

    def __init__(self, use_gpu: bool = False):
        self.use_gpu = use_gpu
        self._reader = None

    def _get_reader(self):
        if self._reader is None:
            import easyocr
            self._reader = easyocr.Reader(["tr", "en"], gpu=self.use_gpu)
        return self._reader

    def process_image_bytes(self, image_bytes: bytes) -> Tuple[str, Dict[str, Any], float]:
        reader = self._get_reader()
        results = reader.readtext(image_bytes)

        if not results:
            return "", {}, 0.0

        lines = [item[1] for item in results]
        confidences = [float(item[2]) for item in results]
        avg_ocr_conf = sum(confidences) / len(confidences)

        raw_text = "\n".join(lines)
        fields, final_conf = FinancialTextExtractor.extract_fields(raw_text, base_confidence=avg_ocr_conf)
        return raw_text, fields, final_conf
