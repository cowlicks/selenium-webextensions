from collections import namedtuple
'''
path to pages, keyed with user's preferred name. For example:
'''
url_info = {} # url name: path

def make_urls(base, url_info):
    '''
    >>> make_urls('ext://foo/', {
    ... 'foo': 'yep.html',
    ... 'bar': 'bar.html'
    ... })
    Urls(background='ext://foo/_generated_background_page.html', bar='ext://foo/bar.html', foo='ext://foo/yep.html')
    '''
    if 'background' not in url_info:
        url_info['background'] = '_generated_background_page.html'
    keys = sorted(url_info.keys())
    Urls = namedtuple('Urls', keys)
    return Urls(*(base + url_info[k] for k in keys))

'''
info needed for firefox and chrome
'''
firefox_info = {'extension_id': 'https-everywhere-eff@eff.org', 'uuid': 'd56a5b99-51b6-4e83-ab23-796216679614'}
chrome_info = {'extension_id': 'nmleinhehnmmepmdbjddclicgpfhbdjo'}
