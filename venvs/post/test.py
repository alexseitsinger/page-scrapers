from page_scrapers.wikipedia.scraper import WikipediaScraper

query_1 = "hellraiser 2"
scraper_1 = WikipediaScraper(query_1)
scraped_1 = scraper_1.scrape(3)
filtered_1 = scraper_1.filter()
print(filtered_1)

query_2 = "hellraiser judgement"
scraper_2 = WikipediaScraper(query_2)
scraped_2 = scraper_2.scrape(3)
filtered_2 = scraper_2.filter()
print(filtered_2)
