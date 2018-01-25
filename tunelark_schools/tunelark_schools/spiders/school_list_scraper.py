# https://www.niche.com/k12/search/best-private-high-schools/
# SchoolListScraper scrapes each school's Niche.com page from above site 
import scrapy

class SchoolListScraper(scrapy.Spider):
	name = 'listscraper'
	start_urls = ['https://www.niche.com/k12/search/best-private-high-schools/']

	def parse(self,response):
		for school in response.css('div.card'):
			yield {
				'name': school.css('.search-result__title::text').extract_first(),
				'niche_url': school.css('.search-result__link::attr(href)').extract_first()
			}
			# 'Next Page' link URL:
			next = response.css('.pagination__next > a::attr(href)').extract_first()
			if next:
				yield response.follow(next, self.parse)



# response.css('.pagination__next > a::attr(href)').extract_first()