import scrapy

from scrapy_example.items import QuoteItem


class QuoteSpider(scrapy.Spider):
    
    name = "quotes"
    start_urls = [
        "http://quotes.toscrape.com"
    ]

    """
        parse ex:
        title = response.css("title::text").extract()
        # title = response.xpath("//title/text()").extract()
        # title = response.xpath("//span[@class='text']/text()").extract()
        # title = response.css("a").xpath("@href").extract()
        yield { "title_text": title }

    """

    def parse(self, response, **kwargs):
        quote_items = QuoteItem()

        all_div_quotes = response.css("div.quote")
        for div_quote in all_div_quotes:
            title = div_quote.css("span.text::text").extract()
            author = div_quote.css("small.author::text").extract()
            tags = div_quote.css("a.tag::text").extract()

            quote_items["title"] = title
            quote_items["author"] = author
            quote_items["tags"] = tags

            yield quote_items

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self._parse)
