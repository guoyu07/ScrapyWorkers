# -*- coding: utf-8 -*-
# from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
import datetime
import re
import sys
try:
    reload(sys)
    sys.setdefaultencoding("utf-8")
except:
    pass


from ScrapyWorkers.items import UserComment


class MUserComments(CrawlSpider):

    name = 'MUserComments'
    allowed_domains = ["china-mmm.net"]
    start_url_format = "https://china-mmm.net/cn/testimonials/?email=&date=%(date)s"
    # day = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
    start_date = (datetime.datetime.now() - datetime.timedelta(days=3)).date()
    end_date = (datetime.datetime.now() - datetime.timedelta(days=0)).date()
    # start_date = datetime.datetime.strptime('2017-02-02', '%Y-%m-%d').date()
    # end_date =  datetime.datetime.strptime('2017-04-12', '%Y-%m-%d').date()
    start_urls = []
    while start_date <= end_date:
        start_urls.append(start_url_format % {'date': start_date.strftime('%Y-%m-%d')})
        start_date += datetime.timedelta(days=1)
    # https://china-mmm.net/cn/testimonials/?email=&date=2017-01-18

    # https://china-mmm.net/cn/testimonials/?email=&date=2017-01-18

    # url format: https://china-mmm.net/cn/testimonials/page-2/
    # url format: https://china-mmm.net/cn/testimonials/page-2/?date=2017-01-18

    def parse(self, response):
        url = response.url

        date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        matchs = date_pattern.findall(url)
        partitions = [partition for partition in matchs]

        max_page_xpath = '/html/body/div[1]/div[2]/section/div[3]/ul/li[last()-1]/a/text()'
        next_url_format = 'https://china-mmm.net/cn/testimonials/page-%(page)d/?date=%(date)s'

        max_page = int(response.xpath(max_page_xpath).extract()[0])

        for item in self.parse_details(response):
            yield item
        # return
        for page in range(2, max_page+1):
            yield Request(next_url_format % {'page': page, 'date': partitions[0]}, self.parse_details)

    def parse_details(self, response):
        url = response.url

        date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        matchs = date_pattern.findall(url)
        partitions = [partition for partition in matchs]

        page_pattern = re.compile(r'page-(\d+)')
        matchs = page_pattern.findall(url)
        pages = [page for page in matchs]

        if len(pages) == 0:
            pages = [1]

        # /html/body/div[1]/div[2]/section/div[4]/div[1]/p[1]
        # _date_xpath = '//div[@class="wineletters_best_list"]/div[@class="wineletters_list best_item"]/p[@class="date"]/b[1]/text() | ' \
        #               '//div[@class="wineletters_list"]/p[@class="date"]/b[1]/text()'

        _chunk_xpath = '//div[@class="wineletters_best_list"]/div[@class="wineletters_list best_item"] | ' \
                      '//div[@class="wineletters_list"]'

        # TEST
        # print("-"*100000)
        # print(response.xpath(_chunk_xpath).xpath('//p[@class="date"]').extract())
        # print(response.xpath(_date_xpath).extract())

        for index, html in enumerate(response.xpath(_chunk_xpath).extract()):
            try:
                yield self._selector_chunk(html, index = index, partition = partitions[0], page = int(pages[0]))
            except:
                import traceback
                print(traceback.print_exc())

    def _selector_chunk(self, html, **kwargs):
        xpath_obj = Selector(text=html)
        item = UserComment()

        item["partition"] = kwargs["partition"]
        item["page"] = kwargs["page"]
        item["page_pos"] = kwargs['index']

        item["tm"] = xpath_obj.xpath('//p[@class="date"]/b[1]/text()')[0].extract().strip()
        _no = xpath_obj.xpath('//p[@class="date"]/b[2]/text()').extract()[0].replace(' ', '')
        if _no:
            item["no"] = int(_no)
        else:
            item["no"] = -1
        amount = xpath_obj.xpath('//p[@class="amount"]/span[@class="summ"]/text()').extract()
        item["amount"] = float(amount[0].replace(' ', ''))
        cash_type = xpath_obj.xpath('//p[@class="amount"]/span[@class="currency"]/text()').extract()
        item["cash_type"] = cash_type[0].strip()
        comment = xpath_obj.xpath('//p[@class="testimonial_item_content"]/text() | '
                                  '//div[@class="wineletters_list"]/p[position()>3]/text()').extract()
        item["comment"] = comment[0]
        item["_id"] = self.get_id(
            "".join(map(lambda item: str(item), [item["partition"], item["tm"], item["comment"].encode('utf-8'), item["amount"], item["cash_type"]])))
        return item

    def get_id(self, content):
        import hashlib
        md5er = hashlib.md5()
        md5er.update(content.encode('utf-8'))
        return md5er.hexdigest()











