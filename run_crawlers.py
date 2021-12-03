from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

setting = get_project_settings()
process = CrawlerProcess(setting)

for spider in process.spiders.list():
    print(f"Running spider: {spider}")
    process.crawl(spider)

process.start()
