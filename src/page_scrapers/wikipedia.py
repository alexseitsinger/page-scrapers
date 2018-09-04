import json
import re
import requests
import bs4


class Scraper(object):
    def __init__(self, string,
                       limit=10,
                       disambiguation_id="Film_and_television",
                       disambiguation_keyword="film"):
        # the string to scrape for.
        self.string = string
        # number of items to return from scraping.
        self.limit = limit
        # Id of the disambiguation element to get anchors from.
        self.disambiguation_id = disambiguation_id
        # The keyword to search for in the disambiguated links list.
        self.disambiguation_keyword = disambiguation_keyword
        self.IMAGE_FILETYPES = (
            'jpg', 'jpeg', 'gif', 'png',
            "JPG", "JPEG", "GIF", "PNG",
        )
        self.SKIPPED_FILETYPES = tuple([
            "svg.%s" % filetype
            for filetype in self.IMAGE_FILETYPES
        ])
        self.RE_WIKIPEDIA_ANNOTATIONS = r'(\[[0-9]+\])'
        self.IGNORED_WIKIPEDIA_DESCRIPTIONS = (
            'this article contains a list of works that does not follow the manual of style for lists of works',
        )
        self.WIKIMEDIA_UPLOAD_URL = "//upload.wikimedia.org"
        self.WIKIPEDIA_URL = "https://en.wikipedia.org"
        self.WIKIPEDIA_API_URL = "w/api.php?action=opensearch&search={}&limit={}&namespace=0&format=json"

    def get_soup(self, url):
        req = requests.get(url)
        if req.status_code != 200:
            raise Exception("Failed to download page.")
        return bs4.BeautifulSoup(req.content, 'html.parser')

    def filter_images(self, soup):
        images = []
        for tag in soup.findAll("img"):
            src = tag["src"]
            if src.endswith(self.IMAGE_FILETYPES):
                if not src.endswith(self.SKIPPED_FILETYPES):
                    if src.startswith(self.WIKIMEDIA_UPLOAD_URL):
                        images.append(src)
        return images

    def filter_description(self, soup):
        try:
            infobox = soup.findAll('table')[0]
            desc = infobox.findNextSibling()
            if desc is not None:
                desc = desc.getText().strip().lower()
                desc = re.sub(self.RE_WIKIPEDIA_ANNOTATIONS, '', desc)
                if not any(x in desc for x in self.IGNORED_WIKIPEDIA_DESCRIPTIONS):
                    return desc
        except IndexError:
            return ""

    def is_disambiguated(self, soup):
        title = soup.find("title")
        results = re.search(r"\(disambiguation\)", title.text)
        try:
            result = results.group()
            return True
        except AttributeError:
            # Didn't match anything.
            return False
        return False

    def filter_disambiguated(self, soup):
        anchors = soup.find(id=self.disambiguation_id).find_next("ul").find_all("a")
        urls = []
        for anchor in anchors:
            for k,v in anchor.attrs.items():
                if k == "href":
                    if self.disambiguation_keyword in v:
                        if not v.startswith(self.WIKIPEDIA_URL):
                            v = "{}{}".format(self.WIKIPEDIA_URL, v)
                        urls.append(v)
        return urls

    def make_data(self, url, soup):
        return {
            "url": url,
            "description": self.filter_description(soup),
            "images": self.filter_images(soup),
        }

    def scrape(self, limit=None):
        if limit is None:
            limit = self.limit
        scraped_pages = []
        for url in self.make_urls(limit):
            for scraped_page in self.scrape_page(url):
                scraped_pages.append(scraped_page)
        return scraped_pages

    def scrape_page(self, url):
        scraped = []
        original_soup = self.get_soup(url)
        if self.is_disambiguated(original_soup):
            # add if condition for different disambiguation paths
            # ie for: films -> if string ends with 'film'
            #         music -> if string ends with 'music'
            for ft_page_url in self.filter_disambiguated(original_soup):
                ft_page_soup = self.get_soup(ft_page_url)
                ft_page_data = self.make_data(ft_page_url, ft_page_soup)
                scraped.append(ft_page_data)
        else:
            scraped.append(self.make_data(url, original_soup))
        return scraped

    def make_urls(self, limit):
        # Make a url for for a page to scrape.
        query_string = self.string.strip()
        query_string = query_string.replace(r"\s\s+", " ")
        query_string = query_string.replace(" ", "%20")
        query_url = "{}/{}".format(
            self.WIKIPEDIA_URL,
            self.WIKIPEDIA_API_URL.format(
                query_string,
                limit,
            )
        )
        req = requests.get(query_url)
        text = req.text
        # Convert the data into a list of urls
        data = json.loads(text)
        all_urls = data[-1]
        # split the search term into parts
        bits = query_string.lower().split()
        suffix = bits.pop()
        prefix = ' '.join(bits)
        prefix_underscore = prefix.replace(" ", "_")
        prefix_slug = prefix.replace(" ", "-")
        # Create a list of urls that have the film name in it.
        prefixes = [prefix, prefix_underscore, prefix_slug]
        confirmed_urls = []
        for url in all_urls:
            if any(x in url.lower() for x in prefixes):
                confirmed_urls.append(url)
        return confirmed_urls
