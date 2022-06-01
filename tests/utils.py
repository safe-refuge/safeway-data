from typing import List, Callable

from requests import Session, Response
from scrapy.http import HtmlResponse

from models.point_of_interest import PointOfInterest


def parse_betamax_response(session: Session, parse_function: Callable, url: str) -> List[PointOfInterest]:
    """
    Loads response for a given URL through Betamax
    and parses it with a given parse function
    """
    scrapy_response = get_betamax_response(session, url)
    results = [
        PointOfInterest(**result) for result in parse_function(scrapy_response)
    ]

    return results


def get_betamax_response(session: Session, url: str) -> HtmlResponse:
    response: Response = session.get(url)
    return HtmlResponse(body=response.content, url=url)
