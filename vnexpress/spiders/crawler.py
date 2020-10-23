import scrapy
import textwrap


class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    allowed_domains = ['example.com']
    start_urls = ['']

    def __init__(self, *args, **kwargs):
        super(CrawlerSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]

    def parse(self, response):
        detail = response.xpath('//*[@class="fck_detail "]')
        paragraphs = detail.xpath('//*[@class="Normal"]')

        with open('output.txt', 'w', encoding='utf-8') as f:
            for paragraph in paragraphs:
                extracted_text = ''.join(paragraph.xpath('text()').extract())
                processed_text = textwrap.wrap(extracted_text, 80, break_long_words=False)
                for text in processed_text:
                    f.write(text + '\n')
                f.write('\n')

