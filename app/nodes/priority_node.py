from app.core.schemas import PriorityOutput

class PriorityDetectionNode:
    def execute(self, message: str, intent: str = "default") -> PriorityOutput:
        # 1. Ưu tiên phân tích dựa trên Intent (chính xác hơn)
        high_risk_intents = [
            "compromised_card", "lost_or_stolen_card", "lost_or_stolen_phone", 
            "cash_withdrawal_not_recognised", "card_payment_not_recognised", 
            "direct_debit_payment_not_recognised"
        ]
        medium_risk_intents = [
            "transfer_not_received_by_recipient", "failed_transfer", 
            "declined_card_payment", "declined_cash_withdrawal", 
            "declined_transfer", "card_swallowed"
        ]

        if intent in high_risk_intents:
            return PriorityOutput(priority_level="high", reason=f"Intent rủi ro cao: {intent}")
        elif intent in medium_risk_intents:
            return PriorityOutput(priority_level="medium", reason=f"Intent cần xử lý sớm: {intent}")

        # 2. Fallback: Dùng keyword nếu intent là default hoặc thuộc nhóm low
        msg_lower = message.lower()
        high_risk_keywords = ["hack", "mất tiền", "lừa đảo", "khóa tài khoản", "lost money", "blocked"]
        medium_risk_keywords = ["thất bại", "chưa nhận", "lỗi", "failure", "not received"]

        if any(kw in msg_lower for kw in high_risk_keywords):
            return PriorityOutput(priority_level="high", reason="Chứa từ khóa rủi ro/khẩn cấp cao.")
        elif any(kw in msg_lower for kw in medium_risk_keywords):
            return PriorityOutput(priority_level="medium", reason="Vấn đề giao dịch/vận chuyển cần theo dõi.")
        
        return PriorityOutput(priority_level="low", reason="Câu hỏi tra cứu thông tin cơ bản.")