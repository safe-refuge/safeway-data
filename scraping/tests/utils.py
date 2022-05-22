from typing import Generator, List

from requests import Session, Response
from scrapy import Spider
from scrapy.http import HtmlResponse

from models.point_of_interest import PointOfInterest


def parse_betamax_response(session: Session, spider: Spider, url: str) -> List[PointOfInterest]:
    """
    Loads response for a given URL through Betamax  and parses it with a given spider
    """
    response: Response = session.get(url)
    scrapy_response = HtmlResponse(body=response.content, url=url)
    results = [PointOfInterest(**result) for result in spider.parse(scrapy_response)]

    return results
