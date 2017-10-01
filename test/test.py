import os

from selenium_webextensions import ExtensionTestCase, Config
from selenium_webextensions.util import get_git_root, run_shell_command


def build_crx():
    '''Builds the .crx file for Chrome and returns the path to it'''
    cmd = ['make', '-sC', get_git_root(), 'crx']
    return os.path.join(get_git_root(), run_shell_command(cmd).split()[-1])


def build_xpi():
    cmd = ['make', '-sC', get_git_root(), 'xpi']
    return os.path.join(get_git_root(), run_shell_command(cmd).split()[-1])


conf = {
    'url_info': {},
    'firefox_info': {
        'extension_id': 'thisisfake@stuff.org',
        'uuid': 'd56a5b99-51b6-4e83-ab23-796216679615',
        },
    'chrome_info': {
        'extension_id': 'domkkphemjplbkmgjalpfpakbfdkfepe',
        },
    'make_crx': build_crx,
    'make_xpi': build_xpi,
}


Config(conf)


class TestCase(ExtensionTestCase):
    def test(self):
        import ipdb
        ipdb.set_trace()
        self.assertTrue(True)
