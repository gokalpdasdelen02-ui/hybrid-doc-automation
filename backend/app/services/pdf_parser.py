import re
from typing import Dict, Any, Tuple

class FinancialTextExtractor:
    """Ham metin içerisinden kurumsal fatura/dekont alanlarını ayrıştırır."""

    VKN_PATTERN = r"(?:VKN|Vergi\s*No|TCKN)[:\s]*([0-9]{10,11})"
    INVOICE_NO_PATTERN = r"(?:Fatura\s*No|Belge\s*No)[:\s]*([A-Z0-9]{3}20[0-9]{11})"
    DATE_PATTERN = r"([0-9]{2}[./-][0-9]{2}[./-]20[0-9]{2})"
    TOTAL_PATTERN = r"(?:Genel\s*Toplam|Ödenecek\s*Tutar|Toplam\s*Tutar)[:\s]*([0-9.,]+)"
    TAX_PATTERN = r"(?:Hesaplanan\s*KDV|Toplam\s*KDV|KDV)[:\s]*([0-9.,]+)"

    @staticmethod
    def _parse_amount(val: str) -> float:
        cleaned = val.replace(".", "").replace(",", ".")
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    @classmethod
    def extract_fields(cls, raw_text: str, base_confidence: float = 0.98) -> Tuple[Dict[str, Any], float]:
        vkn_match = re.search(cls.VKN_PATTERN, raw_text, re.IGNORECASE)
        inv_match = re.search(cls.INVOICE_NO_PATTERN, raw_text, re.IGNORECASE)
        date_match = re.search(cls.DATE_PATTERN, raw_text)
        total_match = re.search(cls.TOTAL_PATTERN, raw_text, re.IGNORECASE)
        tax_match = re.search(cls.TAX_PATTERN, raw_text, re.IGNORECASE)

        extracted = {
            "vendor_tax_id": vkn_match.group(1) if vkn_match else None,
            "invoice_number": inv_match.group(1) if inv_match else None,
            "invoice_date": date_match.group(1) if date_match else None,
            "total_amount": cls._parse_amount(total_match.group(1)) if total_match else None,
            "tax_amount": cls._parse_amount(tax_match.group(1)) if tax_match else None,
        }

        found_count = sum(1 for v in extracted.values() if v is not None)
        completeness_ratio = found_count / len(extracted)
        final_confidence = round(base_confidence * (0.5 + 0.5 * completeness_ratio), 4)

        return extracted, final_confidence
