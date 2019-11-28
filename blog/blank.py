import os
import random
import sys
import time
import math

if sys.version_info[0] > 2:
    from http.cookiejar import LWPCookieJar
    from urllib.request import Request, urlopen
    from urllib.parse import quote_plus, urlparse, parse_qs
else:
    from cookielib import LWPCookieJar
    from urllib import quote_plus
    from urllib2 import Request, urlopen
    from urlparse import urlparse, parse_qs

try:
    from bs4 import BeautifulSoup
    is_bs4 = True
except ImportError:
    from BeautifulSoup import BeautifulSoup
    is_bs4 = False

# URL templates to make Google searches.
url_home = "https://www.google.%(tld)s/"
url_search = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&"              "btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&tbm=%(tpe)s"
url_next_page = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&"                 "start=%(start)d&tbs=%(tbs)s&safe=%(safe)s&tbm=%(tpe)s"

# Cookie jar. Stored at the user's home folder.
home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'   # Use the current folder on error.
cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass

# Default user agent, unless instructed by the user to change it.
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'

# Request the given URL and return the response page, using the cookie jar.
def get_page(url, user_agent=None):
    """
    Request the given URL and return the response page, using the cookie jar.

    :param str url: URL to retrieve.
    :param str user_agent: User agent for the HTTP requests.
        Use None for the default.

    :rtype: str
    :return: Web page retrieved for the given URL.

    :raises IOError: An exception is raised on error.
    :raises urllib2.URLError: An exception is raised on error.
    :raises urllib2.HTTPError: An exception is raised on error.
    """
    if user_agent is None:
        user_agent = USER_AGENT
    request = Request(url)
    request.add_header('User-Agent', user_agent)
    cookie_jar.add_cookie_header(request)
    response = urlopen(request)
    cookie_jar.extract_cookies(response, request)
    html = response.read()
    response.close()
    try:
        cookie_jar.save()
    except Exception:
        pass
    return html

# Filter links found in the Google result pages HTML code.
# Returns None if the link doesn't yield a valid result.
def filter_result(link):
    try:

        # Valid results are absolute URLs not pointing to a Google domain
        # like images.google.com or googleusercontent.com
        o = urlparse(link, 'http')
        if o.netloc and 'google' not in o.netloc:
            return link

        # Decode hidden URLs.
        if link.startswith('/url?'):
            link = parse_qs(o.query)['q'][0]

            # Valid results are absolute URLs not pointing to a Google domain
            # like images.google.com or googleusercontent.com
            o = urlparse(link, 'http')
            if o.netloc and 'google' not in o.netloc:
                return link

    # Otherwise, or on error, return None.
    except Exception:
        pass
    return None

# Returns a generator that yields URLs.
def search(query, tld='com', lang='en', tbs='0', safe='off', num=10, start=0,
           stop=None, domains=None, pause=2.0, only_standard=False,
           extra_params={}, tpe='', user_agent=None):
    """
    Search the given query string using Google.

    :param str query: Query string. Must NOT be url-encoded.
    :param str tld: Top level domain.
    :param str lang: Language.
    :param str tbs: Time limits (i.e "qdr:h" => last hour,
        "qdr:d" => last 24 hours, "qdr:m" => last month).
    :param str safe: Safe search.
    :param int num: Number of results per page.
    :param int start: First result to retrieve.
    :param int or None stop: Last result to retrieve.
        Use None to keep searching forever.
    :param list of str or None domains: A list of web domains to constrain
        the search.
    :param float pause: Lapse to wait between HTTP requests.
        A lapse too long will make the search slow, but a lapse too short may
        cause Google to block your IP. Your mileage may vary!
    :param bool only_standard: If True, only returns the standard results from
        each page. If False, it returns every possible link from each page,
        except for those that point back to Google itself. Defaults to False
        for backwards compatibility with older versions of this module.
    :param dict of str to str extra_params: A dictionary of extra HTTP GET
        parameters, which must be URL encoded. For example if you don't want
        Google to filter similar results you can set the extra_params to
        {'filter': '0'} which will append '&filter=0' to every query.
    :param str tpe: Search type (images, videos, news, shopping, books, apps)
        Use the following values {videos: 'vid', images: 'isch',
        news: 'nws', shopping: 'shop', books: 'bks', applications: 'app'}
    :param str or None user_agent: User agent for the HTTP requests.
        Use None for the default.

    :rtype: generator of str
    :return: Generator (iterator) that yields found URLs.
        If the stop parameter is None the iterator will loop forever.
    """
    # Set of hashes for the results found.
    # This is used to avoid repeated results.
    hashes = set()

    # Count the number of links yielded
    count = 0

    # Prepare domain list if it exists.
    if domains:
        query = query + ' ' + ' OR '.join(
                                'site:' + domain for domain in domains)

    # Prepare the search string.
    query = quote_plus(query)

    # Check extra_params for overlapping
    for builtin_param in ('hl', 'q', 'btnG', 'tbs', 'safe', 'tbm'):
        if builtin_param in extra_params.keys():
            raise ValueError(
                'GET parameter "%s" is overlapping with \
                the built-in GET parameter',
                builtin_param
            )

    # Grab the cookie from the home page.
    get_page(url_home % vars(), user_agent)

    # Prepare the URL of the first request.
    if start:
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()
    else:
        if num == 10:
            url = url_search % vars()
        else:
            url = url_search_num % vars()

    # Loop until we reach the maximum result, if any (otherwise, loop forever).
    while not stop or count < stop:
        # Remeber last count to detect the end of results
        last_count = count

        try:  # Is it python<3?
            iter_extra_params = extra_params.iteritems()
        except AttributeError:  # Or python>3?
            iter_extra_params = extra_params.items()
        # Append extra GET_parameters to URL
        for k, v in iter_extra_params:
            url += url + ('&%s=%s' % (k, v))

        # Sleep between requests.
        time.sleep(pause)

        # Request the Google Search results page.
        html = get_page(url, user_agent)

        # Parse the response and process every anchored URL.
        if is_bs4:
            soup = BeautifulSoup(html, 'html.parser')
        else:
            soup = BeautifulSoup(html)


        try:
            anchors = soup.find(id='search').findAll('a')
            #anchors = soup.find(id='search').findAll('div')
            # Sometimes (depending on the User-agent) there is
            # no id "search" in html response
        except AttributeError:
            # Remove links of the top bar
            gbar = soup.find(id='gbar')
            if gbar:
                gbar.clear()
            anchors = soup.findAll('a')

        #top_list = soup.select('#rso > div > div > div > div > div.rc > div.r > a > h3')
        top_list = soup.find(id='search').findAll('div')
        #print(soup)

        for a in anchors:
            # Leave only the "standard" results if requested.
            # Otherwise grab all possible links.
            if only_standard and (
                    not a.parent or a.parent.name.lower() != "h3"):
                continue

            # Get the URL from the anchor tag.
            try:
                link = a['href']
            except KeyError:
                continue

            # Filter invalid links and links pointing to Google itself.
            link = filter_result(link)
            if not link:
                continue

            # Discard repeated results.
            h = hash(link)
            if h in hashes:
                continue
            hashes.add(h)

            # Yield the result.
            #yield link
            yield a
            #print(a)

            count += 1
            if stop and count >= stop:
                return


        # End if there are no more results.
        if last_count == count:
            break

        # Prepare the URL for the next request.
        start += num
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()



#my_links = search('자전거', tld='com', lang='ko', tbs='qdr:d', stop=3, pause=2)
#search('자전거', tld='com', lang='ko', tbs='qdr:d', stop=3, pause=2)
items = search('본 고안은 탄성 있게 등받이를 지지하여 주는 틸팅유닛과, 이를 구비한 의자와 관련되며, 실시예로 좌판과 등받이를 이어주며, 등받이의 탄성', tld='com', lang='ko', tbs='qdr_')
#print(top_list[0].text)
#print(items[0].text)


cnt = 0
for l in items:
    cnt += 1
    print(cnt)
    print(l.text)
