from typing import List

from requests import Session, Response
from scrapy import Spider
from scrapy.http import HtmlResponse

from models.point_of_interest import PointOfInterest


def parse_betamax_response(session: Session, spider: Spider, url: str) -> List[PointOfInterest]:
    """
    Loads response for a given URL through Betamax  and parses it with a given spider
    """
    scrapy_response = get_betamax_response(session, url)
    results = [PointOfInterest(**result) for result in spider.parse(scrapy_response)]

    return results


def get_betamax_response(session: Session, url: str) -> HtmlResponse:
    response: Response = session.get(url)
    return HtmlResponse(body=response.content, url=url)
