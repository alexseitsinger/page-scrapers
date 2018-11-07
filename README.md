# Page Scrapers

## Description

Scrapes wikipedia pages for for url, description, plot, images, genre, and year data.

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
from page_scrapers.wikipedia.scrapers.film import WikipediaFilmScraper

scraper = WikipediaFilmScraper("hellraiser 2")
scraped = scraper.scrape()
filtered = scraper.filter()
```
