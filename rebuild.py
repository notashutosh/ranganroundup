import re
import sqlite3
from bs4 import BeautifulSoup
import requests
from Person import Person


def get_people(url):
    # Make a request to the specified URL and get the HTML content
    # Use the requests library for this
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    div_element = soup.find('div', id='mw-content-text')
    li_elements = div_element.find_all('li')

    return li_elements


if __name__ == "__main__":
    url_list = {
        'director': ['https://en.wikipedia.org/wiki/Category:Tamil_film_directors', 'https://en.wikipedia.org/w/index.php?title=Category:Tamil_film_directors&pagefrom=Maharajan%2C+N.%0AN.+Maharajan#mw-pages', 'https://en.wikipedia.org/w/index.php?title=Category:Tamil_film_directors&pagefrom=Sekhar%2C+G.C%0AG.+C.+Sekhar#mw-pages'],
        'actor': ['https://en.wikipedia.org/wiki/Category:Tamil_comedians'],
        'cinematographer': ['https://en.wikipedia.org/wiki/Category:Tamil_film_cinematographers'],
        'editor': ['https://en.wikipedia.org/wiki/Category:Tamil_film_editors']
    }
    for type, links in url_list.items():
        for link in links:
            people = get_people(link)

            for person in people:
                link = person.find('a')
                name = re.sub(r'\([^)]*\)', '', link.text).replace('.', '')
                name = re.sub(r'(?<=\b\w)\s(?=\w\b)', '', name)
                p = Person(
                    name=name,
                    url='https://en.wikipedia.org/'+link.get('href'),
                    type=type
                )
                p.save()
