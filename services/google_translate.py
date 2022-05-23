from dataclasses import dataclass
from typing import Callable, List

from googleapiclient.discovery import build, Resource
from googleapiclient.http import HttpRequest

from config.settings import Settings


def make_translate_request(request: HttpRequest) -> dict:
    result = request.execute()
    return result


def build_translate_request(service: Resource, multiple_texts: List[str]) -> HttpRequest:
    request: HttpRequest = service.translations().list(target='en', q=multiple_texts)
    return request


TRANSLATE_QUERY_DATA_BATCH_SIZE = 60


@dataclass
class BatchRequestsBuilder:
    data: List[str]
    service: Resource
    batch_size: int = TRANSLATE_QUERY_DATA_BATCH_SIZE
    build_request: Callable = build_translate_request

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.data[self.current_index:]:
            start_index = self.current_index
            self.current_index += self.batch_size
            end_index = self.current_index
            return self.build_request(self.service, self.data[start_index:end_index])
        else:
            raise StopIteration


@dataclass
class GoogleTranslateReader:
    # Injected dependencies
    settings: Settings
    make_request: Callable = make_translate_request
    build_request: Callable = build_translate_request

    def translate(self, source_text: List[str]) -> List[str]:
        service = build('translate', 'v2', developerKey=self.settings.developer_key)
        requests = BatchRequestsBuilder(source_text, service)
        response = [self.make_request(request) for request in requests]
        result = self.process_response(response)
        return result

    @staticmethod
    def process_response(response: List[dict]) -> List[str]:
        translations = [row['translations'] for row in response]
        flatted = [item for sublist in translations for item in sublist]
        return [translation['translatedText'] for translation in flatted]
