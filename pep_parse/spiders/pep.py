import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = [f'https://{domain}/' for domain in allowed_domains]

    def parse(self, response):
        for PEP_link in response.css(
            'section#numerical-index tbody '
            'a.pep.reference.internal::attr(href)'
        ).getall():
            yield response.follow(PEP_link, callback=self.parse_pep)

    def parse_pep(self, response):
        find_title = 'h1.page-title'
        yield PepParseItem(
            dict(
                number=response.css(find_title).re_first(r'PEP (\d+)'),
                name=response.css(
                    f'{find_title}::text'
                ).re_first(r'PEP \d+ – (.+)'),
                status=response.css('dd.field-even abbr::text').get()
            )
        )
