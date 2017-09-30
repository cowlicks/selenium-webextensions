'''
path to pages, keyed with user's preferred name. For example:

pages = {
    'popup': 'popup.html',
    }

becomes:

shim.pages.popup # chrome-extension://youridishere/popup.html
'''
pages = {} # page name: path

'''
info needed for firefox and chrome
'''
firefox_info = {'extension_id': 'https-everywhere-eff@eff.org', 'uuid': 'd56a5b99-51b6-4e83-ab23-796216679614'}
chrome_info = {'extension_id': 'nmleinhehnmmepmdbjddclicgpfhbdjo'}

