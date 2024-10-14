import re
import sqlite3
from bs4 import BeautifulSoup
import requests
from Person import Person


def get_people(url, type='list'):
    # Make a request to the specified URL and get the HTML content
    # Use the requests library for this
    # type can be 'list' or 'table'
    # example of 'list' page: https://en.wikipedia.org/wiki/Category:Tamil_comedians
    # example of 'table' page: https://en.wikipedia.org/wiki/List_of_Tamil_film_actors
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    if type == 'list':
        people = []
        div_element = soup.find('div', id='mw-content-text')
        li_elements = div_element.find_all('li')
        for li_element in li_elements:
            people.append(li_element.find('a'))
        return people
    else:  # type='table'
        people = []
        table_elements = soup.find_all('table', class_='wikitable')
        for table in table_elements:
            tr_elements = table.find_all('tr')
            for tr in tr_elements:
                td_elements = tr.find_all('td')
                # print(len(td_elements), td_elements)
                if len(td_elements) == 4:
                    if (td_elements[1].find('a')):
                        people.append(td_elements[1].find('a'))
                elif len(td_elements) == 3:
                    if (td_elements[0].find('a')):
                        people.append(td_elements[0].find('a'))
                # for td in td_elements:
                #     a_elements = td.find_all('a')
                #     for a in a_elements:
                #         people.append(a)

    return people


def save_people(people, person_type='actor'):
    for person in people:
        # Remove text within parentheses + make R.S. Shivaji -> RS Shivaji so i'ts similar to how it's written in reviews
        name = re.sub(r'\([^)]*\)', '', person.text).replace('.', '')
        name = re.sub(r'(?<=\b\w)\s(?=\w\b)', '', name)
        p = Person(
            name=name,
            url='https://en.wikipedia.org'+person.get('href'),
            type=person_type
        )
        p.save()


if __name__ == "__main__":
    # Links with names as a < ul >'s
    url_list = {
        'director': ['https://en.wikipedia.org/wiki/Category:Tamil_film_directors', 'https://en.wikipedia.org/w/index.php?title=Category:Tamil_film_directors&pagefrom=Maharajan%2C+N.%0AN.+Maharajan#mw-pages', 'https://en.wikipedia.org/w/index.php?title=Category:Tamil_film_directors&pagefrom=Sekhar%2C+G.C%0AG.+C.+Sekhar#mw-pages'],
        'actor': ['https://en.wikipedia.org/wiki/Category:Tamil_comedians'],
        'cinematographer': ['https://en.wikipedia.org/wiki/Category:Tamil_film_cinematographers'],
        'editor': ['https://en.wikipedia.org/wiki/Category:Tamil_film_editors']
    }
    for person_type, links in url_list.items():
        people = []
        for link in links:
            people += get_people(link, type='list')
        save_people(people, person_type)
    # Links in the form of tables
    url_tables = {
        'actor': ['https://en.wikipedia.org/wiki/List_of_Tamil_film_actors', 'https://en.wikipedia.org/wiki/List_of_Tamil_film_actresses']
    }

    people = []
    for type, links in url_tables.items():
        for link in links:
            people += get_people(link, type='table')
    save_people(people)
