import requests
from bs4 import BeautifulSoup


def process_url(url):
    """
    Sends GET request and parses the content of the page received as a response to this request.
    If occurred HTTPError, returns False.

    :param url: URL for the request.
    :return: the result of parsing the page as a dictionary OR False
    """
    try:
        result = requests.get(url)
        result.raise_for_status()
        return parse_content_data(result.text)
    except(requests.RequestException, ValueError):
        return False


def parse_content_data(content):
    """
    Parses the content of the page. The parsing result is stored in the dictionary.
    For tags <h1>, <h2>, <h3>, the dictionary stores the number of times this tag was encountered on the page,
    for tags <a> stores a string of links (attributes 'href') separated by commas.

    Example: {'h1': 1, 'h2': 1, 'h3': 5, 'a': 'http://google.com, http://yandex.ru'}

    :param content: the content of the page.
    :return: the result of parsing the page as a dictionary
    """
    html_doc = BeautifulSoup(content, 'html.parser')
    result_dict = {}
    for i in range(1, 4):
        result_dict[f'h{i}'] = len(html_doc.find_all(f'h{i}'))
    result_dict['a'] = ', '.join([a_tag['href'] for a_tag in html_doc.find_all('a') if 'href' in a_tag.attrs])
    return result_dict
