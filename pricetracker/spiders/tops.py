import scrapy

from ..utils import write_to_csv


class TopsSpider(scrapy.Spider):
    name = "tops"
    start_urls = [
        "https://www.bmfitgear.com/collections/shirts",
        "https://www.bmfitgear.com/collections/tank-tops",
        "https://www.bmfitgear.com/collections/outerwear",
    ]

    def parse(self, response):
        write_to_csv("tops.csv", response)
