# Page Scrapers

## Description

Scrapes pages, like wikipedia, for for urls, descriptions, and images.

## Installation

```python
pip install page_scrapers
```

## Methods

1. scrape_page(url)
2. scrape_pages(string, limit)

## Usage

```python
from page_scrapers.wikipedia import scrape_page
url = "https://en.wikipedia.org/wiki/Batman_Begins"
scraped_data = scrape_page(url)
```

```python
from page_scrapers.wikipedia import scrape_pages
scraped_data = scrape_pages("american gangster film", 3)
```