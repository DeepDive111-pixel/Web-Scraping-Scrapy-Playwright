import scrapy
from scrapy_playwright.page import PageMethod

class Code456(scrapy.Spider):
    name = "spider"
    start_urls = ["http://quotes.toscrape.com/js/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", ".quote", state="visible")  
                    ],
                },
            )
        
    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        try:
            
          items = response.css("div.quote")

          for item in items:
              
              qoute = item.css("span.text::text").get()
              authour = item.css("small.author::text").get()
              tags = items.css("div.tags a.tag::text").getall()

              yield {
                  "qoute": qoute,
                  "authour": authour,
                  "tags": tags
              }
          next_page = response.css("li.next a::attr(href)").get()
          if next_page:
                next_page_url = response.urljoin(next_page)

                yield response.follow(
                    url=next_page_url,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_selector", ".quote", state="visible")
                        ],
                    },
                    callback=self.parse,
                )
        finally:
            await page.close()

     
        

        
   
  

