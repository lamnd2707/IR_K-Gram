import scrapy
import textwrap


class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    allowed_domains = ['example.com']
    start_urls = ['https://vnexpress.net/them-18-tuyen-duong-o-tp-hcm-bi-ngap-4180851.html']

    def parse(self, response):
        detail = response.xpath('//*[@class="fck_detail "]')
        paragraphs = detail.xpath('//*[@class="Normal"]')

        with open('output.txt', 'w') as f:
            for paragraph in paragraphs:
                extracted_text = ''.join(paragraph.xpath('text()').extract())
                processed_text = textwrap.wrap(extracted_text, 80, break_long_words=False)
                for text in processed_text:
                    f.write(text + '\n')
                f.write('\n')

