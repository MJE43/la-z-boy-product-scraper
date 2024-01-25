import scrapy
from recliners.items import LzbItem

class ProductSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['la-z-boy.com']
    start_urls = [
        'https://www.la-z-boy.com/b/living-room-recliners/_/N-musa9i?intpromo=header.Recliners#/b/living-room-recliners-rocking-recliners/_/N-1e7xutk?intpromo=header.Recliners&living=room-recliners'
    ]

    def parse(self, response):
        # Extract product links
        product_links = response.css('.item-detail-content .product-name.js-to-pdp::attr(href)').getall()
        for link in product_links:
            # Join the relative URL with the base URL
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse_product)

    def parse_product(self, response):
        # Create an instance of LzbItem
        item = LzbItem()

        # Extract product details using the provided CSS selectors
        item['name'] = response.css('.prod-name-favorite-icon .product-name::text').get()
        item['price'] = response.css('.original-price::text').get()
        item['saleprice'] = response.css('.msrp-price::text').get()
        item['description'] = response.css('.at-a-glance-section::text').get()
        
        # Extract pitch; join paragraphs if there are multiple
        item['pitch'] = ' '.join(response.css('.whytobuy-subtext p::text').getall())
        
        # Extract features; join list items into a single string
        features_selectors = [
            '#product-details-body li:nth-child(2)',
            '#product-details-body li:nth-child(3)',
            '#product-details-body li:nth-child(4)',
            '#product-details-body li:nth-child(5)',
            '#product-details-body li:nth-child(8)',
            '#product-details-body li:nth-child(1)'
        ]
        item['features'] = ' '.join(response.css(', '.join(features_selectors) + '::text').getall())

        item['stylenumber'] = response.css('.product-details-info-container:nth-child(1) .flow-section:nth-child(1) .title+ p::text').get()
        
        # Extract image URL; ensure it's absolute by joining with the base URL
        relative_image_url = response.css('.slick-active:nth-child(11) img::attr(src)').get()
        item['image'] = response.urljoin(relative_image_url)

        yield item
