import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.core.schemas import CustomerRequest, DraftOutput, IntentOutput, PolicyOutput, PriorityOutput, ValidationOutput
from app.nodes.draft_node import ResponseDraftingNode
from app.nodes.policy_node import PolicyRetrievalNode
from app.nodes.router_node import RouterNode


def test_policy_retrieval_falls_back_to_default():
    output = PolicyRetrievalNode().execute("unknown_intent")

    assert "Cảm ơn" in output.policy_text


def test_router_escalates_high_priority():
    output = RouterNode().execute(
        PriorityOutput(priority_level="high", reason="risk"),
        ValidationOutput(is_valid=True, feedback="ok"),
        DraftOutput(draft_reply="A complete draft reply."),
    )

    assert output.decision == "escalate"


def test_router_asks_for_missing_info():
    output = RouterNode().execute(
        PriorityOutput(priority_level="low", reason="basic"),
        ValidationOutput(is_valid=True, feedback="ok"),
        DraftOutput(draft_reply="A complete draft reply.", missing_info=["Trace ID"]),
    )

    assert output.decision == "ask_info"


def test_draft_node_fallback_reply_when_llm_returns_empty():
    node = ResponseDraftingNode()
    node.client.generate = lambda prompt: ""

    output = node.execute(
        CustomerRequest(
            message_id="msg_01",
            customer_id="c_100",
            message="Tôi đã chuyển tiền nhưng người nhận chưa nhận được.",
        ),
        IntentOutput(intent="transfer_not_received_by_recipient", confidence=0.45),
        PriorityOutput(priority_level="medium", reason="fallback"),
        PolicyOutput(policy_text="Nếu quá 24 giờ, vui lòng cung cấp mã tra soát (Trace ID)."),
    )

    assert len(output.draft_reply) > 15
    assert "Trace ID" in output.draft_reply
    assert output.missing_info == ["Trace ID"]
