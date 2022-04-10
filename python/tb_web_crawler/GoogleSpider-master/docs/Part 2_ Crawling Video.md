# Crawling Google Search Results - Part 2: Crawling Video

In the previous part of this tutorial, we've created a very simple spider that allows us to crawl Google's *normal* search results. In this part of the tutorial, we're going further than before.

WARNING: Don't ***ever*** use this spider to scrape lots of data. As of Google provides a public API that allows you to call 100 times for free, your IP will be banned if Google noticed the unusual traffic from your computer. This spider is built only for learning purposes, and it shouldn't be used in real projects. So keep that in mind, and we'll get started.

## What We Are Crawling

You might not fully understand what I'm talking about this crazy video thing. All right, let me explain it. If you search Google for `Python`, for example, there will be a card containing videos related to the search as the picture shown below.

![Video results](https://dev-to-uploads.s3.amazonaws.com/i/vkuicm7solqv7ackqk6w.png)

The part with a `Videos` heading is what we're going to crawl. Seems easy, right? Will, it's not gonna be as easy as Part 1's work.

## Analyze Time

Okay, so now we know where we're building, let's take a look at the webpage.

If you look for the results, you can see that they're surrounded by a `g-scrolling-carousel` element.

![g-scrolling-carousel](https://dev-to-uploads.s3.amazonaws.com/i/aorh1xw50rh37ky6w191.png)

Inside it, there's another `g-inner-card` element containing video details for every videos.

![g-inner-card](https://dev-to-uploads.s3.amazonaws.com/i/i5gyduqi2oop792guebp.png)

All right, so now we've got all the containers, let's take a look at the details. First, we need to have the video title. It's inside a `div` element with attribute `role="heading"`.

![video title](https://dev-to-uploads.s3.amazonaws.com/i/2rvj77bs1iu2j5kr5gt4.png)

...And the link inside an `a` element:

![video link](https://dev-to-uploads.s3.amazonaws.com/i/o4k4uzutjqyl6j2sgizb.png)

Then, we'll look for the video author, which has a style with `max-height:1.5800000429153442em;min-height:1.5800000429153442em;font-size:14px;padding:2px 0 0;line-height:1.5800000429153442em`:

![video author](https://dev-to-uploads.s3.amazonaws.com/i/2490ea9p9fds35kddd62.png)

We've also need to fetch for the video's source, or platform. For example, Youtube. It's inside a `span` whose parent is a `div` with style `font-size:14px;padding:1px 0 0 0;line-height:1.5800000429153442em`.

![video source](https://dev-to-uploads.s3.amazonaws.com/i/cu1uvz46mieku2xsvqx4.png)

And we'll also get the video's upload date. It's right below video author's `span`, inside the same parent element. We'll just strip the video author's text to get its text when we reach the code.

![video date](https://dev-to-uploads.s3.amazonaws.com/i/hxqr0jh9imp8h8odgjx4.png)

Finally, we are going to look for the video length. It's in the second child element of a `div` styled with `height:118px;width:212px`.

![video length](https://dev-to-uploads.s3.amazonaws.com/i/nwl0wb8cv9sgu33djuel.png)

## Where's the Cover?

You might wonder about the video cover image. Where's that? Well, it's inside the JavaScript. If you take a closer look under the video details, you will find three `<script>` tags containing Base64 images. Copy one of them and you will probably get the video cover. So now we've got the information, let's see how can we locate them. The easiest way is to locate their parent `<div>` and find all the script tags. But, there's lots of them! The way I'm using is to locate their sibling element `<span id="fld"></span>`. With that, we can locate **its** sibling elements - script tags. The tags we're looking for are the last three script element, excluding the first one. We can just use `[1:]` in Python to get rid of it.

## Alright, Hands On!

Create a function called `__search_video` and we'll put all of our code inside it.

```python
class GoogleSpider(object):
    # ...
    def __search_video(self, response: requests.Response) -> list:
        """Search for video results based on the given response

        Args:
            response (requests.Response): the response requested to Google search

        Returns:
            list: A list of found video results, usually three if found
        """
        pass
```

And we will create our BeautifulSoup object from the response:

```python
class GoogleSpider(object):
    # ...
    def __search_video(self, response: requests.Response) -> list:
        """Search for video results based on the given response

        Args:
            response (requests.Response): the response requested to Google search

        Returns:
            list: A list of found video results, usually three if found
        """
        soup = BeautifulSoup(response.text, 'html.parser')
```

Then, let's locate our `g-inner-card`:

```python
class GoogleSpider(object):
    # ...
    def __search_video(self, response: requests.Response) -> list:
        # ...
        cards = soup.find('g-scrolling-carousel').findAll('g-inner-card')
```

And loop through them to generate our search result:

```python
class GoogleSpider(object):
    # ...
    def __search_video(self, response: requests.Response) -> list:
        # ...
        results = []
        # Generate video information
        for card in cards:
            try:  # Just in case
                # Title
                title = card.find('div', role='heading').text
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
                    'url': url,
                    'type': 'video'
                })
        return results
```

And finally, we'll do the cover part together. First, let's create a variable called `covers_` to store the scripts we've found. Note that I used `[1:]` to create a slice of the list to remove the first tag.

```python
class GoogleSpider(object):
    # ...
    def __search_video(self, response: requests.Response) -> list:
        # ...
        # Pre-process the video covers
        covers_ = soup.find('span', id='fld').findNextSiblings('script')[1:]
        # ...
```

Then, we will loop through them:

```python
class GoogleSpider(object):
    # ...
    def __search_video(self, response: requests.Response) -> list:
        # ...
        # Pre-process the video covers
        covers_ = soup.find('span', id='fld').findNextSiblings('script')[1:]
        # Get the cover images
        covers = []
        for c in covers_:
            # TODO
        # ...
```

And we will append each base64-coded images to the list `covers`. Here we need to remove the unnecessary JavaScript code and only keep the image. If you don't know about `rsplit` which I've used in my code, well, it's a special version of `split`. It will start from the end to scan for the result and split them. For example, if I have a variable called `text`:

```python
>>> text = 'Hi everyone! Would you like to say Hi to me?'
```

If you split it the normal way:

```python
>>> text.split('Hi', 1)
['', ' everyone! Would you like to say Hi to me?']
```

But with `rsplit`:

```python
>>> text.rsplit('Hi', 1)
['Hi everyone! Would you like to say ', ' to me?']
```

The reason I used it here is because there might be another `;var ii` inside the base64 image, and if I used `split`, it would create a broken image.

```python
class GoogleSpider(object):
    # ...
    def __search_video(self, response: requests.Response) -> list:
        # ...
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
        # ...
```

...and add them to our list:

```python
class GoogleSpider(object):
    # ...
    def __search_video(self, response: requests.Response) -> list:
        # ...
        for card in cards:
            # ...
            try:  # Just in case
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
                    # ...
                    'cover': cover,
                    # ...
                })
        # ...
```

OK, so we are almost there. There's one more thing that we need to work on, is that when we search something that doesn't contain a video result, our program will throw an `AttributeError`. To prevent that, we need to add a `try-except`:

```python
class GoogleSpider(object):
    # ...

    def __search_video(self, response: requests.Response) -> list:
        # ...
        try:
            cards = soup.find('g-scrolling-carousel').findAll('g-inner-card')
        except AttributeError:
            return []
        # ...
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
                # ...
            except IndexError:
                continue
            else:
                # ...
        return results
```

I re-structured the structure of the `GoogleSpider` class, so you might want to do the same thing as I did. I put all of the Part 1's code inside the `__search_result` method, and re-created the `search` function. All its doing is to call the private functions and put the results together:

```python
class GoogleSpider(object):
    # ...

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
        pages = self.__get_total_page(response)
        results.extend(result)
        results.extend(video)
        return {
            'results': results,
            'pages': pages
        }
    
    # ...
```

## Full Code

The full code of this tutorial until Part 2 is below.

```python
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
        pages = self.__get_total_page(response)
        results.extend(result)
        results.extend(video)
        return {
            'results': results,
            'pages': pages
        }


if __name__ == '__main__':
    pprint(GoogleSpider().search(input('Search for what? ')))

```

## Summing Up

So now we can crawl Google's related video results, but you might be asking: Why can it only crawl 3 video results? Well, that's because in Google's source code, there's only three. If you found a way of scraping more, please leave a comment and I'll add it to the post as soon as I can. Of course, if you have any questions or having an error when coding, leave a comment below and I'll be happy to help.
