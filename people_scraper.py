import scrapy

class PeopleScraper(scrapy.Spider):
    name = "people_scraper"
    allowed_domains = ["linkedin.com"]
    handle_httpstatus_all = True


    def start_requests(self):
        # define the start URL
        start_url = 'https://www.linkedin.com/company/medtronic/people/?keywords=device%20sales'
        
        # replace [COMPANY] with the company name or ID in the URL
        # you can also add additional parameters to the URL, such as "?keywords=[KEYWORD]"
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        # extract the HTML elements that contain the name and URL for each person
        for person in response.css('.search-result__info'):
            name = person.css('.ember-view.lt-line-clamp.lt-line-clamp--single-line.org-people-profile-card__profile-title.t-black::text').get()

            url = person.css('a::attr(href)').get()

            # clean up the data
            name = name.strip()  # remove extra whitespace
            url = response.urljoin(url)  # convert relative URL to absolute URL

            # return a dictionary with the scraped data
            yield {'name': name, 'url': url}