import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_PEP_links = response.css(
            'section#numerical-index tbody '
            'a.pep.reference.internal::attr(href)'
        ).getall()
        for PEP_link in all_PEP_links:
            yield response.follow(PEP_link, callback=self.parse_pep)

    def parse_pep(self, response):
        for PEP in response.css('section#pep-content'):
            data = {
                'number': PEP.css('h1.page-title').re_first(r'PEP (\d+)'),
                'name': PEP.css(
                    'h1.page-title::text'
                ).re_first(r'PEP \d+ – (.+)'),
                'status': PEP.css('dd.field-even abbr::text').get()
            }
            yield PepParseItem(data)
