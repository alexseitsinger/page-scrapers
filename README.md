# Page Scrapers

## Description

Scrapes pages for for urls, descriptions, and images data.

## Installation

```python
pip install page-scrapers
```

or

```python
pipenv install page-scrapers
```

## Methods

1. wikipedia.scrape_page(url) - Scrapes the page for data and returns it as a dictionary.
2. wikipedia.scrape_pages(string, limit) - Finds URL's to pages and then scrapes each page for their data, limiting results to the number specified, or 10 if not provided.

## Usage

```python
from page_scrapers import wikipedia
url = "https://en.wikipedia.org/wiki/Batman_Begins"
scraped_data = wikipedia.scrape_page(url)
```

```python
from page_scrapers import wikipedia
scraped_data = wikipedia.scrape_pages("american gangster film", 3)
```