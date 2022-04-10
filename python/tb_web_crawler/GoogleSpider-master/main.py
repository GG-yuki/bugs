# Import dependencies
from pprint import pprint
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup


class GoogleSpider(object):
    def __init__(self):
        """Crawl Google search results

        This class is used to crawl Google's search results using requests and BeautifulSoup.
        """
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Host': 'www.google.com',
            'Referer': 'https://www.google.com/'
        }

    def __get_source(self, url: str) -> requests.Response:
        """Get the web page's source code

        Args:
            url (str): The URL to crawl

        Returns:
            requests.Response: The response from URL
        """
        return requests.get(url, headers=self.headers)

    def __get_total_page(self, response: requests.Response) -> int:
        """Get the current total pages

        Args:
            response (requests.Response): the response requested to Google using requests

        Returns:
            int: the total page number (might be changing when increasing / decreasing the current page number)
        """
        soup = BeautifulSoup(response.text, 'html.parser')
        pages_ = soup.find('div', id='foot', role='navigation').findAll('td')
        maxn = 0
        for p in pages_:
            try:
                if int(p.text) > maxn:
                    maxn = int(p.text)
            except:
                pass
        return maxn

    def __search_video(self, response: requests.Response) -> list:
        """Search for video results based on the given response

        Args:
            response (requests.Response): the response requested to Google search

        Returns:
            list: A list of found video results, usually three if found
        """
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            cards = soup.find('g-scrolling-carousel').findAll('g-inner-card')
        except AttributeError:
            return []
        # Pre-process the video covers
        covers_ = soup.find('span', id='fld').findNextSiblings('script')[1:]
        # Get the cover images
        covers = []
        for c in covers_:
            # Fetch cover image
            try:
                covers.append(str(c).split('s=\'')[-1].split(
                    '\';var ii')[0].rsplit('\\', 1)[0])
            except IndexError:
                pass
        results = []
        # Generate video information
        for card in cards:
            try:
                # Title
                # If the container is not about videos, there won't be a div with
                # attrs `role="heading"`. So to catch that, I've added a try-except
                # to catch the error and return.
                try:
                    title = card.find('div', role='heading').text
                except AttributeError:
                    return []
                # Video length
                length = card.findAll('div', style='height:118px;width:212px')[
                    1].findAll('div')[1].text
                # Video upload author
                author = card.find(
                    'div', style='max-height:1.5800000429153442em;min-height:1.5800000429153442em;font-size:14px;padding:2px 0 0;line-height:1.5800000429153442em').text
                # Video source (Youtube, for example)
                source = card.find(
                    'span', style='font-size:14px;padding:1px 0 0 0;line-height:1.5800000429153442em').text
                # Video publish date
                date = card.find(
                    'div', style='font-size:14px;padding:1px 0 0 0;line-height:1.5800000429153442em').text.lstrip(source).lstrip('- ')  # Strip the source out because they're in the same container
                # Video link
                url = card.find('a')['href']
                # Video cover image
                try:  # Just in case that the cover wasn't found in page's JavaScript
                    cover = covers[cards.index(card)]
                except IndexError:
                    cover = None
            except IndexError:
                continue
            else:
                # Append result
                results.append({
                    'title': title,
                    'length': length,
                    'author': author,
                    'source': source,
                    'date': date,
                    'cover': cover,
                    'url': url,
                    'type': 'video'
                })
        return results

    def __search_result(self, response: requests.Response) -> list:
        """Search for normal search results based on the given response

        Args:
            response (requests.Response): The response requested to Google

        Returns:
            list: A list of results
        """
        # Initialize BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Get the result containers
        result_containers = soup.findAll('div', class_='rc')
        # Final results list
        results = []
        # Loop through every container
        for container in result_containers:
            # Result title
            title = container.find('h3').text
            # Result URL
            url = container.find('a')['href']
            # Result description
            des = container.find('span', class_='st').text
            results.append({
                'title': title,
                'url': url,
                'des': des,
                'type': 'result'
            })
        return results

    def __search_wiki(self, response: requests.Response) -> list:
        """Search for wiki results based on the given response

        Args:
            response (requests.Response): The response requested to Google

        Returns:
            list: A list of wiki results, usually only one if found.
        """
        soup = BeautifulSoup(response.text, 'html.parser')
        # Get the info container card
        container = soup.find('div', class_='kp-wholepage')
        # If the container is empty (None), then there isn't a wiki tab for the
        # given response.
        if container is None:
            return []
        # Title
        title = container.find('h2', attrs={'data-attrid': 'title'}).text
        # Subtitle
        try:
            subtitle = container.find(
                'div', attrs={'data-attrid': 'subtitle'}).text
        except AttributeError:
            subtitle = None
        # Description
        des = container.find('div', class_='kno-rdesc').find('span').text
        # The link to Wikipedia
        url = container.find('div', class_='kno-rdesc').find('a')['href']
        # Details table
        try:
            table = container.findAll(
                'div', class_='wp-ms')[1].findAll('div', class_='mod')[1:]
        except IndexError:
            table = []
        details = []
        # Loop through all details
        for row in table:
            name = row.find('span').text.strip(': ')
            # Find all spans and get their text one-by-one
            detail_ = row.findAll('span')[1:]
            detail = ''
            # Get their text
            for _ in detail_:
                detail += _.text + ' '  # Add a whitespace to prevent descriptions connected to each other
            details.append({
                'name': name,
                'detail': detail.strip()
            })
        result = {
            'title': title,
            'subtitle': subtitle,
            'des': des,
            'url': url,
            'details': details,
            'type': 'wiki'
        }
        return [result]

    def search(self, query: str, page: int = 1) -> dict:
        """Search Google

        Args:
            query (str): The query to search for
            page (int): The page number of search result

        Returns:
            dict: The search results and the total page number
        """
        # Get response
        response = self.__get_source(
            'https://www.google.com/search?q=%s&start=%d' % (quote(query), (page - 1) * 10))
        results = []
        video = self.__search_video(response)
        result = self.__search_result(response)
        wiki = self.__search_wiki(response)
        pages = self.__get_total_page(response)
        results.extend(result)
        results.extend(video)
        results.extend(wiki)
        return {
            'results': results,
            'pages': pages
        }


if __name__ == '__main__':
    pprint(GoogleSpider().search(input('Search for what? ')))
