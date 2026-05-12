
POLICIES = {
    "card_arrival": "Thẻ vật lý sẽ được giao đến địa chỉ đăng ký trong vòng 3-5 ngày làm việc. Nếu quá 7 ngày chưa nhận được, vui lòng yêu cầu phát hành lại qua ứng dụng.",
    "transfer_not_received_by_recipient": "Giao dịch liên ngân hàng thông thường có thể mất đến 24 giờ. Nếu người nhận vẫn chưa nhận được sau 24 giờ, vui lòng cung cấp mã tra soát (Trace ID).",
    "card_not_received": "Hệ thống sẽ hỗ trợ kiểm tra trạng thái vận chuyển hoặc hủy thẻ cũ để phát hành thẻ mới miễn phí.",
    "compromised_card": "Trường hợp nghi ngờ lộ thông tin hoặc có giao dịch bất thường, thẻ sẽ bị khóa khẩn cấp để bảo vệ tài sản.",
    "cash_withdrawal_not_recognised": "Nếu bạn phát hiện giao dịch rút tiền không rõ nguồn gốc, vui lòng khóa thẻ ngay trên ứng dụng và liên hệ tổng đài khẩn cấp để được hỗ trợ tra soát.",
    "default": "Cảm ơn bạn đã liên hệ. Chúng tôi sẽ kiểm tra thông tin và hỗ trợ bạn sớm nhất."
}

def get_policy_for_intent(intent: str) -> str:
    return POLICIES.get(intent, POLICIES["default"])