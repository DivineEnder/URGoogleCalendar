from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
process.crawl('cdcs_search', ddlTerm = 'D-20182', txtCourse = "CSC 172")
process.start() # the script will block here until the crawling is finished
