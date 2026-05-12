import requests
from app.core.settings import settings
from app.core.schemas import IntentOutput

class IntentDetectionNode:
    def __init__(self):
        print(f"🔗 Kết nối Intent Node tới Kaggle API: {settings.INTENT_API_URL}")

    def execute(self, message: str) -> IntentOutput:
        try:
            response = requests.post(
                settings.INTENT_API_URL, 
                json={"message": message},
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return IntentOutput(
                intent=result.get("intent", "default"), 
                confidence=result.get("confidence", 0.95)
            )
            
        except Exception as e:
            print(f"❌ Lỗi gọi Kaggle Intent API: {e}")
            return IntentOutput(intent="default", confidence=0.0)