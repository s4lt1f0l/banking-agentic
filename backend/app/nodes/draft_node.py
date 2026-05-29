from app.clients.ollama_client import OllamaClient
from app.core.schemas import DraftOutput, CustomerRequest, IntentOutput, PriorityOutput, PolicyOutput

class ResponseDraftingNode:
    def __init__(self):
        self.client = OllamaClient()

    def execute(self, request: CustomerRequest, intent_out: IntentOutput,
                priority_out: PriorityOutput, policy_out: PolicyOutput) -> DraftOutput:

        prompt = f"""You are a professional banking support agent. Draft a polite reply strictly following the policy below.

Customer Message: "{request.message}"
Detected Intent: {intent_out.intent}
Priority Level: {priority_out.priority_level}
Policy Guideline: "{policy_out.policy_text}"

Draft a clear response in the language of the customer. Ask for necessary trace IDs or account details politely if the policy mentions it.
"""
        draft_text = self.client.generate(prompt)
        if not draft_text:
            draft_text = self._fallback_reply(request, intent_out, priority_out, policy_out)

        missing = []
        suggested = "send_reply"

        # Đưa ra đề xuất hành động tiếp theo nếu thấy thiếu thông tin quan trọng
        policy_lower = policy_out.policy_text.lower()
        msg_lower = request.message.lower()

        if "trace id" in policy_lower and "trace id" not in msg_lower:
            missing.append("Trace ID")
        if "số tài khoản" in policy_lower and not any(char.isdigit() for char in msg_lower):
            missing.append("Số tài khoản")

        if missing:
            suggested = "ask_info"

        return DraftOutput(draft_reply=draft_text, missing_info=missing, suggested_action=suggested)

    def _fallback_reply(
        self,
        request: CustomerRequest,
        intent_out: IntentOutput,
        priority_out: PriorityOutput,
        policy_out: PolicyOutput,
    ) -> str:
        if priority_out.priority_level == "high":
            return (
                "Cảm ơn bạn đã báo ngay cho chúng tôi. Trường hợp này có dấu hiệu rủi ro cao, "
                "vui lòng khóa thẻ hoặc tài khoản trên ứng dụng nếu có thể và liên hệ tổng đài khẩn cấp. "
                f"Chúng tôi sẽ chuyển yêu cầu để nhân viên hỗ trợ kiểm tra ngay. Chính sách áp dụng: {policy_out.policy_text}"
            )

        if intent_out.intent == "transfer_not_received_by_recipient":
            return (
                "Cảm ơn bạn đã liên hệ. Giao dịch liên ngân hàng thông thường có thể mất đến 24 giờ. "
                "Nếu đã quá 24 giờ mà người nhận vẫn chưa nhận được tiền, vui lòng cung cấp mã tra soát "
                "(Trace ID) để chúng tôi kiểm tra chi tiết."
            )

        if intent_out.intent in {"card_arrival", "card_delivery_estimate"}:
            return (
                "Cảm ơn bạn đã thông tin. Thẻ vật lý thường được giao đến địa chỉ đăng ký trong vài ngày làm việc. "
                "Nếu đã quá thời gian dự kiến, chúng tôi sẽ hỗ trợ kiểm tra trạng thái vận chuyển hoặc hướng dẫn "
                "phát hành lại thẻ theo chính sách hiện hành."
            )

        return (
            "Cảm ơn bạn đã liên hệ. Chúng tôi đã ghi nhận yêu cầu và sẽ kiểm tra thêm thông tin để hỗ trợ bạn. "
            f"Thông tin chính sách liên quan: {policy_out.policy_text}"
        )
