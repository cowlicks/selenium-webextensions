import os
from contextlib import contextmanager
from collections import namedtuple
import subprocess
import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from .config import Config, make_urls
from .util import get_git_root, run_shell_command

BROWSER_TYPES = ['chrome', 'firefox']
BROWSER_NAMES = ['google-chrome', 'google-chrome-stable', 'google-chrome-beta', 'firefox']

Specifics = namedtuple('Specifics', ['manager', 'background_url', 'info'])


def unix_which(command, silent=False):
    try:
        return run_shell_command(['which', command])
    except subprocess.CalledProcessError as e:
        if silent:
            return None
        raise e


def get_browser_type(string):
    for t in BROWSER_TYPES:
        if t in string:
            return t
    raise ValueError("couldn't get browser type from %s" % string)


def get_browser_name(string):
    if ('/' in string) or ('\\' in string):  # its a path
        return os.path.basename(string)
    else:  # its a browser type
        for bn in BROWSER_NAMES:
            if string in bn and unix_which(bn, silent=True):
                return os.path.basename(unix_which(bn))
        raise ValueError('Could not get browser name from %s' % string)


def install_ext_on_ff(driver, extension_path):
    '''
    Use Selenium's internal API's to manually send a message to geckodriver
    to install the extension. We should remove this once the functionality is
    included in Selenium. See https://github.com/SeleniumHQ/selenium/issues/4215
    '''
    command = 'addonInstall'
    driver.command_executor._commands[command] = ('POST', '/session/$sessionId/moz/addon/install')
    driver.execute(command, params={'path': extension_path, 'temporary': True})
    time.sleep(2)


class Shim:
    instance = None
    _browser_msg = '''BROWSER should be one of:
* /path/to/a/browser
* a browser executable name so we can find the browser with "which $BROWSER"
* something from BROWSER_TYPES
'''
    __doc__ = 'Chooses the correct driver and extension_url based on the BROWSER environment\nvariable. ' + _browser_msg

    def __init__(self):
        if Config.instance is None:
            raise ValueError("No configuration set. Make a Config instance")

        print('Configuring the test run')
        self.config = Config.instance
        self.chrome_info = self.config.chrome_info
        self.firefox_info = self.config.firefox_info
        self._specifics = None
        browser = os.environ.get('BROWSER')
        # get browser_path and broser_type first
        if browser is None:
            raise ValueError("The BROWSER environment variable is not set. " + self._browser_msg)
        elif ("/" in browser) or ("\\" in browser):  # path to a browser binary
            self.browser_path = browser
            self.browser_type = get_browser_type(self.browser_path)

        elif unix_which(browser, silent=True):  # executable browser name like 'google-chrome-stable'
            self.browser_path = unix_which(browser)
            self.browser_type = get_browser_type(browser)

        elif get_browser_type(browser):  # browser type like 'firefox' or 'chrome'
            bname = get_browser_name(browser)
            self.browser_path = unix_which(bname)
            self.browser_type = browser
        else:
            raise ValueError("could not infer BROWSER from %s" % browser)

        self.extension_path = self.get_ext_path()
        self._set_specifics()
        print('\nUsing browser path: %s \nwith browser type: %s \nand extension path: %s' %
              (self.browser_path, self.browser_type, self.extension_path))
        self._set_urls(self.base_url)

    def _set_specifics(self):
        self._specifics = self._specifics or {
            'chrome': Specifics(self.chrome_manager,
                                'chrome-extension://%s/' % self.chrome_info['extension_id'],
                                self.chrome_info),
            'firefox': Specifics(self.firefox_manager,
                                 'moz-extension://%s/' % self.firefox_info['uuid'],
                                 self.firefox_info)}
        self.manager, self.base_url, self.info = self._specifics[self.browser_type]

    def _set_urls(self, base_url):
        self.urls = make_urls(base_url, self.config.url_info)

    def get_ext_path(self):
        if self.browser_type == 'chrome':
            return self.config.make_crx()
        elif self.browser_type == 'firefox':
            return self.config.make_xpi()
        else:
            raise ValueError("bad browser getting extension path")

    @property
    def wants_xvfb(self):
        if self.on_travis or bool(int(os.environ.get('ENABLE_XVFB', 0))):
            return True
        return False

    @property
    def on_travis(self):
        if "TRAVIS" in os.environ:
            return True
        return False

    @contextmanager
    def chrome_manager(self):
        opts = Options()
        if self.on_travis:  # github.com/travis-ci/travis-ci/issues/938
            opts.add_argument("--no-sandbox")
        opts.add_extension(self.extension_path)
        opts.binary_location = self.browser_path
        opts.add_experimental_option("prefs", {"profile.block_third_party_cookies": False})

        caps = DesiredCapabilities.CHROME.copy()

        driver = webdriver.Chrome(chrome_options=opts, desired_capabilities=caps)
        try:
            yield driver
        finally:
            driver.quit()

    @contextmanager
    def firefox_manager(self):
        ffp = webdriver.FirefoxProfile()
        # make extension id constant across runs
        ffp.set_preference('extensions.webextensions.uuids', '{"%s": "%s"}' %
                           (self.info['extension_id'], self.info['uuid']))

        driver = webdriver.Firefox(firefox_profile=ffp, firefox_binary=self.browser_path)
        install_ext_on_ff(driver, self.extension_path)
        try:
            yield driver
        finally:
            time.sleep(2)
            driver.quit()
            time.sleep(2)
