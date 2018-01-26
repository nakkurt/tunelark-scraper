# https://www.niche.com/k12/search/best-private-high-schools/
# SchoolListScraper scrapes 8,000+ schools' Niche.com page from above site
import logging
from scrapy.utils.log import configure_logging  
import scrapy

class SchoolListScraper(scrapy.Spider):
	name = 'listscraper'
	# input school list page here
	start_urls = ['https://www.niche.com/k12/search/best-private-high-schools/']
	configure_logging(install_root_handler=False)
	logging.basicConfig(filename='log.txt', format='%(levelname)s: %(message)s',level=logging.INFO)

	# scraper starts scraping from school list page
	def parse(self,response):
		for school_object in response.css('div.card'):
			school = {'name' : school_object.css('.search-result__title::text').extract_first()}
			school['niche_url'] = school_object.css('.search-result__link::attr(href)').extract_first()
			if school.get('niche_url'):
				request = scrapy.Request(school['niche_url'], callback=self.parse_school_page)
				# passing school link/name to school page scraper below
				request.meta['school'] = school
				yield request
				# moves to 'Next Page' using link:
				next = response.css('.pagination__next > a::attr(href)').extract_first()
				if next:
					yield response.follow(next, self.parse)		

	# each page has 25 links to schools which are followed and school data is scraped:
	def parse_school_page(self, response):
		school = response.meta.get("school", "")
		print(school)
		if school:
			school['url'] = response.css('.profile__website__link::attr(href)').extract_first() or 'N/A'
			school['phone'] = response.css('.scalar--three .scalar__value span::text').extract_first() or 'N/A'
			school['address_street'] = response.css('.profile__address div div:nth-child(1)::text').extract_first() or 'N/A'
			school['address_city'] = response.css('.profile__address div+ div::text').extract_first() or 'N/A'
			school['address_state'] = response.css('.profile__address div+ div').re(r', [A-Z]{2}')[0][2:] or 'N/A'
			school['nr_of_students'] = response.css('#students .scalar__value span::text').extract_first() or 'N/A'
			school['annual_tuition'] = response.css('#tuition .scalar__value span::text').extract_first() or 'N/A'
			school['tuition_with_boarding'] = response.css('#tuition .scalar--three:nth-child(1) .scalar__value span::text').extract_first() or 'N/A'
			# In case tuition_with_boarding is missing from the page then received_financial_aid and average_financial_aid selectors are adjusted
			if response.css('#tuition').re(r'\bBoarding\b\s\(\bTuition\b\s\+\s\bBoarding\b'):
				school['received_financial_aid'] = response.css('#tuition .scalar--three:nth-child(2) .scalar__value span::text').extract_first() or 'N/A'
				school['average_financial_aid'] = response.css('#tuition .scalar--three:nth-child(3) .scalar__value span::text').extract_first() or 'N/A'
			else:
				school['received_financial_aid'] = response.css('#tuition .scalar--three:nth-child(1) .scalar__value span::text').extract_first() or 'N/A'
				school['average_financial_aid'] = response.css('#tuition .scalar--three:nth-child(2) .scalar__value span::text').extract_first() or 'N/A'
			school['niche_grade'] = response.css('.niche__grade::text').extract_first() or 'N/A'
			# output:			
			yield {
				'name': school.get('name'),
				'school_url': school.get('url'),
				'phone': school.get('phone'),
				'street': school.get('address_street'),
				'city': school.get('address_city'),
				'state': school.get('address_state'),
				'nr_of_students': school.get('nr_of_students'),
				'annual_tuition': school.get('annual_tuition'),
				'tuition_with_boarding': school.get('tuition_with_boarding'),
				'received_financial_aid': school.get('received_financial_aid'),
				'average_financial_aid': school.get('average_financial_aid'),
				'niche_url': school.get('niche_url'),
				'niche_grade': school.get('niche_grade')
			}

		else:
			yield {'no_school'}
