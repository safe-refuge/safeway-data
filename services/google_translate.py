from dataclasses import dataclass
from typing import Callable, List

from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from returns.io import impure_safe

from config.settings import Settings


def make_request(request: HttpRequest) -> dict:
    result = request.execute()
    return result


@dataclass
class GoogleTranslateReader:
    # Injected dependencies
    settings: Settings
    make_request: Callable = make_request

    @impure_safe
    def translate(self, source_text: List[str]) -> List[str]:
        service = build('translate', 'v2', developerKey=self.settings.developer_key)
        request: HttpRequest = service.translations().list(target='en', q=source_text)
        response = self.make_request(request)
        result = self.process_response(response)
        return result

    def process_response(self, response: dict) -> List[str]:
        translations = response['translations']
        return [translation['translatedText'] for translation in translations]
