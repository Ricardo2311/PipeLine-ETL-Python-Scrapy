import scrapy


class MercadolivreSpider(scrapy.Spider):
    #propriedades
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    page_count = 1
    max_pages = 10

    
    #request
    def start_requests(self):
        start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    #response

    def parse(self, response):
        products = response.xpath("//div[@class='ui-search-result__content']")
        for product in products :
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            cents = product.css('span.andes-money-amount__cents::text').getall()
            yield {
                'brand_name' : product.xpath(".//span[@class='ui-search-item__brand-discoverability ui-search-item__group__element']/text()").get(),
                'name' : product.xpath(".//h2[@class='ui-search-item__title']/text()").get(),
                'old_price_reais': prices[0] if len(prices) > 0 else None,
                'old_price_centavos': cents[0] if len(cents) > 0 else None,
                'new_price_reais': prices[1] if len(prices) > 1 else None,
                'new_price_centavos' : cents[1] if len(cents) > 1 else None,
                'reviews_rating_number': product.xpath(".//span[@class='ui-search-reviews__rating-number']/text()").get(),
                'reviews_amount': product.xpath(".//span[@class='ui-search-reviews__amount']/text()").get()
            }
        if self.page_count < self.max_pages:
            next_page = response.xpath("//li[@class='andes-pagination__button andes-pagination__button--next']/a/@href").get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page,callback=self.parse)
