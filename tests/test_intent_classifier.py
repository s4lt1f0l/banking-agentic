import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "intent_service"))

from banking77_intents import BANKING77_INTENTS
from classifier import IntentClassifier


class FakeClient:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error

    def predict(self, message):
        if self.error:
            raise self.error
        return self.response


def test_classifier_parses_valid_json():
    classifier = IntentClassifier(
        FakeClient({"intent": "card_arrival", "confidence": 0.82, "reason": "asks about delivery"})
    )

    intent, confidence, reason = classifier.classify("When will my card arrive?")

    assert intent == "card_arrival"
    assert confidence == 0.82
    assert reason == "asks about delivery"


def test_classifier_accepts_all_banking77_intents():
    for expected_intent in BANKING77_INTENTS:
        classifier = IntentClassifier(
            FakeClient({"intent": expected_intent, "confidence": 0.82})
        )

        intent, confidence, reason = classifier.classify("test message")

        assert intent == expected_intent
        assert confidence == 0.82
        assert reason == "Classified by tunneled intent API."


def test_classifier_normalizes_known_legacy_aliases():
    classifier = IntentClassifier(
        FakeClient({"intent": "card_not_received", "confidence": 0.82})
    )

    intent, confidence, reason = classifier.classify("I did not receive my card.")

    assert intent == "card_arrival"
    assert confidence == 0.82
    assert reason == "Classified by tunneled intent API."


def test_classifier_falls_back_on_error():
    classifier = IntentClassifier(FakeClient(error=RuntimeError("offline")))

    intent, confidence, reason = classifier.classify("hello")

    assert intent == "default"
    assert confidence == 0.0
    assert "failed" in reason


def test_classifier_uses_local_fallback_for_known_intent_on_error():
    classifier = IntentClassifier(FakeClient(error=RuntimeError("offline")))

    intent, confidence, reason = classifier.classify(
        "Tôi đã chuyển tiền nhưng người nhận chưa nhận được."
    )

    assert intent == "transfer_not_received_by_recipient"
    assert confidence > 0
    assert "local fallback" in reason


def test_classifier_rejects_unknown_intent():
    classifier = IntentClassifier(
        FakeClient({"intent": "loan_application", "confidence": 0.95, "reason": "loan"})
    )

    intent, confidence, reason = classifier.classify("I need a loan.")

    assert intent == "default"
    assert confidence == 0.0
    assert "Unsupported intent" in reason


def test_classifier_supplies_default_reason():
    classifier = IntentClassifier(
        FakeClient({"intent": "default", "confidence": 0.4})
    )

    intent, confidence, reason = classifier.classify("hello")

    assert intent == "default"
    assert confidence == 0.4
    assert reason == "Classified by tunneled intent API."
