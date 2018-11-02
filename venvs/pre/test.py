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
from wikipedia.scraper import WikipediaScraper


class Test(object):
    def run(self):
        scraper = WikipediaScraper(self.query)
        scraped = list(scraper.scrape(self.limit))
        filtered = scraper.filter()
        return {
            "scraped": scraped,
            "filtered": filtered,
        }

    def print(self):
        print("{}\n".format(self.run()))


class TestOne(Test):
    query = "hellraiser judgement"

class TestTwo(Test):
    query = "hellraiser 2"

class TestThree(Test):
    query = "ironman 2"

class TestFour(Test):
    query = "ironman 1"

class TestFive(Test):
    query = "house of 1000 corpses"


test_one = TestOne()
test_one.print()

test_two = TestTwo()
test_two.print()

test_three = TestThree()
test_three.print()

test_four = TestFour()
test_four.print()

test_five = TestFive()
test_five.print()
