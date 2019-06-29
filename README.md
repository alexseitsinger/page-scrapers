# Page Scrapers

## Description

Scrapers for specific websites.

## Installation

```
pip install page-scrapers
```

## Usage

```python
from page_scrapers.wikipedia.scrapers.film import WikipediaFilmScraper

scraper = WikipediaFilmScraper("hellraiser 2")
scraped = scraper.scrape()
filtered = scraper.filter()
```
