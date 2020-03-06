import scrapy
import random
from scrapy_proxycrawl import ProxyCrawlRequest
import requests
from .shops_categories import shops, categories_urls


class AmazonSpider(scrapy.Spider):
    name = 'yandexspider'
    shop = random.choice(list(shops.keys()))
    shop_id = shops[shop]['id']
    category = random.choice(shops[shop]['categories'])
    url = categories_urls[category]

    def clean_price_to_int(self, str_to_number):
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        price = str_to_number
        for i in price:
            if i not in numbers:
                price = price.replace(i, '')
        return price

    def start_requests(self):
        yield ProxyCrawlRequest(url=self.url.format(self.shop_id),
                                device='desktop',
                                country='DE',
                                callback=self.parse)

    def parse(self, response):
        deal_links = response.xpath('.//h3[@class="n-snippet-cell2__title"]/a/@href').getall()
        random_link = random.choice(deal_links)
        absolute_url = response.urljoin(random_link)
        yield ProxyCrawlRequest(url=absolute_url,
                                device='desktop',
                                country='DE',
                                callback=self.parse_detail,
                                )

    def parse_detail(self, response):
        data = {}
        data['name'] = response.css('div.n-title__text h1::text').get()
        data['price'] = self.clean_price_to_int(response.css('div.n-product-price-cpa2__price span::text').get())
        data['oldprice'] = self.clean_price_to_int(response.css('div.n-product-default-offer__old-price-cpa2 span::text').get())
        data['description'] = response.css('ul.n-product-spec-list').get()
        data['image'] = 'https:' + response.css('div.n-gallery__item img::attr(src)').get()
        data['brand'] = response.css('span.n-product-summary__brand-text-all-products-brandname::text').get()
        data['shop'] = self.shop
        data['category'] = self.category
        url_to_shop = response.css('div.n-offer-action__main a::attr(href)').get()
        request_to_shop = requests.get('https:' + url_to_shop).url
        data['link_to_shop'] = request_to_shop[0:request_to_shop.find('?')]
        yield data


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info/']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a/text()').getall()

        yield {
            'title': title,
            'countries': countries,
        }