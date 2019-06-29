from page_scrapers.wikipedia.scrapers.film import WikipediaFilmScraper

query_1 = "hellraiser 2"
scraper_1 = WikipediaFilmScraper(query_1)
scraped_1 = scraper_1.scrape()
filtered_1 = scraper_1.filter()
print(filtered_1)

query_2 = "hellraiser judgement"
scraper_2 = WikipediaFilmScraper(query_2)
scraped_2 = scraper_2.scrape()
filtered_2 = scraper_2.filter()
print(filtered_2)
