# -*- coding: utf-8 -*-
import scrapy
import pymongo


class MsSupportSpiderSpider(scrapy.Spider):
    name = 'ms_support_spider'
    allowed_domains = ['https://developer.mozilla.org/']
    start_urls = ['https://developer.mozilla.org/en-US/docs/Web/HTTP/Status']

    def parse(self, response):
        print("processing: ", response.url)

        # extract the data using xpath
        http_status_code_and_header = response.xpath('//dl/dt/a/code/text()').extract()
        error_description = response.xpath('//dl/dd/text()').extract()

        row_data=zip(http_status_code_and_header, error_description)

        # making extracted data row-wise
        for item in row_data:
            # create a dictonary for scraped data
            scraped_info = {
                'http_status_header': item[0],
                'description': item[1]
            }

            yield scraped_info