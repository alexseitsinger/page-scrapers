import json
import re
import requests
import bs4
# from .strings import capitalize
# from lib.minifiers.utils import compress_string

# Formats allowed for image urls scraped.
# NOTE: Uppercase formats added because wikipedia stores images
#       files with uppercased format names sometimes.
IMAGE_FILETYPES = (
    'jpg', 'jpeg', 'gif', 'png',
    "JPG", "JPEG", "GIF", "PNG",
)

SKIPPED_FILETYPES = tuple([
    "svg.%s" % filetype for filetype in IMAGE_FILETYPES
])

# Remove [0] from string of text output from wikipedia page.
RE_WIKIPEDIA_ANNOTATIONS = r'(\[[0-9]+\])'

IGNORED_WIKIPEDIA_DESCRIPTIONS = (
    'this article contains a list of works that does not follow the manual of style for lists of works',
)


def make_api_query_url(string, limit=10):
    """A function that builds the url to use for wikipedias api."""
    # Remove leading and trailing whitespace
    string = string.strip()
    # Replace excess whitespace with single whitespace
    string = string.replace(r"\s\s+", " ")
    # URL-encode the inner whitespace
    query = string.replace(" ", "%20")
    url = "https://en.wikipedia.org/w/api.php?action=opensearch&search={}&limit={}&namespace=0&format=json".format(query, limit)
    return url


def get_page_urls(string, limit=10):
    """ A function that returns a list of wikipedia page urls to be used by scraper."""
    query_url = make_api_query_url(string, limit)
    req = requests.get(query_url)
    text = req.text
    data = json.loads(text)
    wikipedia_page_urls = data[-1]
    return wikipedia_page_urls

# def _get_wikipedia_url(keyword):
#     return '/'.join([
#         "http://en.wikipedia.org/wiki",
#         '_'.join([capitalize(bit) for bit in keyword.split(' ')]),
#     ])


def get_soup(url):
    req = requests.get(url)
    if req.status_code != 200:
        raise Exception("Failed to download page.")
    return bs4.BeautifulSoup(req.content, 'html.parser')


def get_images(soup):
    images = []
    for tag in soup.findAll("img"):
        src = tag["src"]
        if src.endswith(IMAGE_FILETYPES):
            if not src.endswith(SKIPPED_FILETYPES):
                if src.startswith("//upload.wikimedia.org"):
                    images.append(src)
    return images


def get_description(soup):
    try:
        infobox = soup.findAll('table')[0]
        desc = infobox.findNextSibling()
        if desc is not None:
            desc = desc.getText().strip().lower()
            desc = re.sub(RE_WIKIPEDIA_ANNOTATIONS, '', desc)
            if not any(s in desc for s in IGNORED_WIKIPEDIA_DESCRIPTIONS):
                return desc
    except IndexError:
        return ""


def scrape_page(url):
    soup = get_soup(url)
    return {
        "url": url,
        "description": get_description(soup),
        "images": get_images(soup),
    }


def scrape_pages(string, limit=10):
    page_urls = get_page_urls(string, limit)
    scraped_pages = []
    for url in page_urls:
        scraped_page = scrape_page(url)
        scraped_pages.append(scraped_page)
    return scraped_pages

