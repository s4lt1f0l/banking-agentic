from intent_api_client import IntentApiClient
from banking77_intents import BANKING77_INTENTS

INTENT_ALIASES = {
    "card_not_received": "card_arrival",
}

ALLOWED_INTENTS = set(BANKING77_INTENTS) | {"default"}


class IntentClassifier:
    def __init__(self, client: IntentApiClient | None = None):
        self.client = client or IntentApiClient()

    def classify(self, message: str) -> tuple[str, float, str]:
        try:
            payload = self.client.predict(message)
            intent = self._normalize_intent(str(payload.get("intent", "default")))
            confidence = float(payload.get("confidence", 0.0))
            reason = str(payload.get("reason", "")).strip()
        except Exception as exc:
            intent = self._classify_locally(message)
            confidence = 0.45 if intent != "default" else 0.0
            return intent, confidence, f"Intent API call failed; used local fallback: {exc}"

        if intent not in ALLOWED_INTENTS:
            return "default", 0.0, f"Unsupported intent returned by intent API: {intent}"

        confidence = max(0.0, min(1.0, confidence))
        return intent, confidence, reason or "Classified by tunneled intent API."

    def _normalize_intent(self, intent: str) -> str:
        return INTENT_ALIASES.get(intent, intent)

    def _classify_locally(self, message: str) -> str:
        msg = message.lower()
        rules = [
            (
                "compromised_card",
                ["hack", "lộ thông tin", "khóa ngay", "khóa thẻ", "bị trừ tiền", "giao dịch bất thường"],
            ),
            (
                "cash_withdrawal_not_recognised",
                ["rút tiền", "atm", "không rõ nguồn gốc"],
            ),
            (
                "transfer_not_received_by_recipient",
                ["chuyển tiền", "người nhận", "chưa nhận", "trace id", "mã tra soát"],
            ),
            (
                "card_arrival",
                ["thẻ vật lý", "phát hành thẻ", "chưa thấy gửi", "chưa nhận được thẻ"],
            ),
            (
                "card_arrival",
                ["thẻ khi nào tới", "khi nào nhận thẻ", "giao thẻ"],
            ),
        ]
        for intent, keywords in rules:
            if any(keyword in msg for keyword in keywords):
                return intent
        return "default"
