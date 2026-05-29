import os
import uuid

import requests
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(page_title="Banking AI-Agent", layout="wide")
st.title("Banking AI-Agent")

with st.form("agent-form"):
    customer_id = st.text_input("Customer ID", value="customer-demo")
    message = st.text_area("Customer message", height=140)
    submitted = st.form_submit_button("Run agent")

if submitted:
    if not message.strip():
        st.warning("Enter a customer message.")
    else:
        payload = {
            "message_id": str(uuid.uuid4()),
            "customer_id": customer_id.strip() or "customer-demo",
            "message": message.strip(),
        }
        try:
            response = requests.post(
                f"{API_BASE_URL}/run-agent",
                json=payload,
                timeout=180,
            )
            response.raise_for_status()
            result = response.json()
        except Exception as exc:
            st.error(f"API request failed: {exc}")
        else:
            st.subheader("Result")
            st.write(f"Decision: `{result.get('decision')}`")
            final_reply = result.get("final_reply")
            if final_reply:
                st.write(final_reply)

            trace = result.get("trace", {})
            cols = st.columns(3)
            with cols[0]:
                st.metric("Intent", trace.get("intent_detection", {}).get("intent", "unknown"))
            with cols[1]:
                st.metric("Priority", trace.get("priority_assessment", {}).get("priority_level", "unknown"))
            with cols[2]:
                st.metric("Suggested action", trace.get("response_drafting", {}).get("suggested_action", "unknown"))

            st.subheader("Workflow trace")
            st.json(trace)
