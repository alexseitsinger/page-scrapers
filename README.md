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
from page_scrapers import wikipedia

scraper = wikipedia.Scraper(string="batman begins", limit=1)
scraped = scraper.scrape()
```