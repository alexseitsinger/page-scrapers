# Page Scrapers

## Description

Scrapes pages for for urls, descriptions, and images data.

## Installation

```
pip install page-scrapers
```

or

```
pipenv install page-scrapers
```

## Usage

```python
from page_scrapers.wikipedia.scraper import WikipediaScraper

scraper = WikipediaScraper("hellraiser 2")
scraped = scraper.scrape(3)
filtered = scraper.filter()
```