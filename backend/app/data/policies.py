
POLICIES = {
    "card_arrival": "Thẻ vật lý sẽ được giao đến địa chỉ đăng ký trong vòng 3-5 ngày làm việc. Nếu quá 7 ngày chưa nhận được, vui lòng yêu cầu phát hành lại qua ứng dụng.",
    "transfer_not_received_by_recipient": "Giao dịch liên ngân hàng thông thường có thể mất đến 24 giờ. Nếu người nhận vẫn chưa nhận được sau 24 giờ, vui lòng cung cấp mã tra soát (Trace ID).",
    "compromised_card": "Trường hợp nghi ngờ lộ thông tin hoặc có giao dịch bất thường, thẻ sẽ bị khóa khẩn cấp để bảo vệ tài sản.",
    "cash_withdrawal_not_recognised": "Nếu bạn phát hiện giao dịch rút tiền không rõ nguồn gốc, vui lòng khóa thẻ ngay trên ứng dụng và liên hệ tổng đài khẩn cấp để được hỗ trợ tra soát.",
    "default": "Cảm ơn bạn đã liên hệ. Chúng tôi sẽ kiểm tra thông tin và hỗ trợ bạn sớm nhất."
}

def get_policy_for_intent(intent: str) -> str:
    if intent in POLICIES:
        return POLICIES[intent]
    if "card" in intent or intent in {"apple_pay_or_google_pay", "cash_withdrawal_charge", "cash_withdrawal_not_recognised", "contactless_not_working", "pin_blocked", "visa_or_mastercard"}:
        return "Chúng tôi sẽ kiểm tra trạng thái thẻ, giao dịch hoặc phương thức thanh toán liên quan và hướng dẫn bước xử lý phù hợp."
    if "transfer" in intent or intent in {"beneficiary_not_allowed", "receiving_money"}:
        return "Chúng tôi sẽ kiểm tra trạng thái giao dịch chuyển tiền, phí, thời gian xử lý và thông tin người nhận nếu cần."
    if "top_up" in intent or intent == "topping_up_by_card":
        return "Chúng tôi sẽ kiểm tra trạng thái nạp tiền, hạn mức, phí và nguồn tiền liên quan đến giao dịch top-up."
    if "verify" in intent or intent in {"unable_to_verify_identity", "why_verify_identity"}:
        return "Chúng tôi sẽ hướng dẫn quy trình xác minh danh tính hoặc nguồn tiền theo yêu cầu tuân thủ."
    if "refund" in intent or intent in {"Refund_not_showing_up", "reverted_card_payment?", "transaction_charged_twice"}:
        return "Chúng tôi sẽ kiểm tra trạng thái hoàn tiền, giao dịch bị đảo chiều hoặc khoản thu trùng và hướng dẫn tra soát nếu cần."
    if intent in {"terminate_account", "edit_personal_details", "passcode_forgotten", "age_limit", "country_support"}:
        return "Chúng tôi sẽ hướng dẫn cập nhật thông tin, truy cập tài khoản hoặc điều kiện sử dụng dịch vụ theo chính sách ngân hàng."
    return POLICIES["default"]
