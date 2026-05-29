class IntentApiClient:
    def __init__(self, url: str | None = None):
        if url is None:
            from settings import settings

            url = settings.INTENT_API_URL
        self.url = url

    def predict(self, message: str) -> dict:
        if not self.url:
            raise ValueError("INTENT_API_URL is not configured")

        import requests

        response = requests.post(
            self.url,
            json={"message": message},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()
