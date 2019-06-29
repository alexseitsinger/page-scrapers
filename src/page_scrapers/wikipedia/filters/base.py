import re
from ..utils import int_to_roman, get_best_match


class WikipediaBaseFilter(object):
    def description_has_keywords(self, description):
        if any(x in description for x in self.keywords):
            return True
        # if any(x in description.split(" ") for x in self.keywords):
        #     return True
        return False

    def description_has_name(self, description, name):
        if name in description:
            return True
        if get_best_match(name, description)[1] >= 0.95:
            return True
        return False

    def url_has_name(self, url, name):
        name_lower = name.lower()
        name_lower_underscore = name_lower.replace(" ", "_")
        name_lower_slug = name_lower.replace(" ", "-")
        return any(x in url.lower() for x in [
            name_lower,
            name_lower_underscore,
            name_lower_slug,
        ])

    def clean_description(self, description):
        description = re.sub(r"[^\x00-\x7F]", " ", description)
        description = re.sub(r"\n", " ", description)
        description = re.sub("\'", "", description)
        description = re.sub("'", "", description)
        description = re.sub(r"\s\s+", " ", description)
        return description

    def filter(self, film_name, scraped_data):
        result = None
        while len(scraped_data) != 0:
            item = scraped_data.pop(0)
            if result is None:
                url = item["url"]
                raw_description = item["description"]
                if raw_description is None:
                    continue
                cleaned_description = self.clean_description(raw_description)
                if self.description_has_name(cleaned_description, film_name):
                    if self.description_has_keywords(cleaned_description):
                        result = item
                else:
                    try:
                        m = re.search(r"\d+", film_name)
                        number = m.group(0)
                        roman = int_to_roman(int(number))
                        roman_name = film_name.replace(number, roman)
                        roman_name_lower = film_name.replace(number, roman.lower())
                        if self.decription_has_name(cleaned_description, roman_name):
                            if self.description_has_keywords(cleaned_description):
                                result = item
                        if self.decription_has_name(cleaned_description, roman_name_lower):
                            if self.description_has_keywords(cleaned_description):
                                result = item
                        if self.url_has_name(url, roman_name):
                            result = item
                        if self.url_has_name(url, roman_name_lower):
                            result = item
                    except AttributeError:
                        pass
                if self.url_has_name(url, film_name):
                    result = item
        return result

