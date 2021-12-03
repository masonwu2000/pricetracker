import scrapy

from ..utils import write_to_csv


class TopsSpider(scrapy.Spider):
    name = "bottoms"
    start_urls = [
        "https://www.bmfitgear.com/collections/shorts",
        "https://www.bmfitgear.com/collections/bottoms",
    ]

    def parse(self, response):
        write_to_csv("bottoms.csv", response)
