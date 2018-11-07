import os
import sys

# Create some variables for us to use
PACKAGE_VENV_DIR = os.path.abspath(os.path.dirname(__file__))
PACKAGE_ROOT = os.path.dirname(os.path.dirname(PACKAGE_VENV_DIR))
PACKAGE_NAME = os.path.basename(PACKAGE_ROOT)
PACKAGE_SRC_DIR = os.path.join(PACKAGE_ROOT, "src/{}".format(PACKAGE_NAME))

# Add the src directory to our import path
sys.path.append(PACKAGE_SRC_DIR)

# Import the module to test and use it.
from wikipedia.scrapers.film import WikipediaFilmScraper


class FilmTest(object):
    def run(self):
        scraper = WikipediaFilmScraper(self.query)
        scraped = list(scraper.scrape())
        filtered = scraper.filter()
        return {
            "scraped": scraped,
            "filtered": filtered,
        }

    def print(self):
        print("{}\n".format(self.run()))


class FilmTestOne(FilmTest):
    query = "hellraiser judgement"


class FilmTestTwo(FilmTest):
    query = "hellraiser 2"


class FilmTestThree(FilmTest):
    query = "ironman 2"


class FilmTestFour(FilmTest):
    query = "ironman 1"


class FilmTestFive(FilmTest):
    query = "house of 1000 corpses"


class FilmTestSix(FilmTest):
    query = "into the wild film"


film_test_one = FilmTestOne()
film_test_one.print()

film_test_two = FilmTestTwo()
film_test_two.print()

film_test_three = FilmTestThree()
film_test_three.print()

film_test_four = FilmTestFour()
film_test_four.print()

film_test_five = FilmTestFive()
film_test_five.print()

film_test_six = FilmTestSix()
film_test_six.print()
