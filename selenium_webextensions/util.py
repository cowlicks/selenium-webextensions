# -*- coding: UTF-8 -*-
from contextlib import contextmanager
import os
import unittest
import subprocess
import time
from functools import wraps

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchWindowException

import shim

DEFAULT_TIMEOUT = 30

parse_stdout = lambda res: res.strip().decode('utf-8')

run_shell_command = lambda command: parse_stdout(subprocess.check_output(command))

get_git_root = lambda: run_shell_command(['git', 'rev-parse', '--show-toplevel'])


class ExtensionTestCase(unittest.TestCase):

    shim = shim.Shim(shim.chrome_info, shim.firefox_info)

    @classmethod
    def setUpClass(cls):
        cls.manager = cls.shim.manager
        cls.base_url = cls.shim.bg_url
        cls.wants_xvfb = cls.shim.wants_xvfb
        if cls.wants_xvfb:
            from xvfbwrapper import Xvfb
            cls.vdisplay = Xvfb(width=1280, height=720)
            cls.vdisplay.start()

        # setting DBUS_SESSION_BUS_ADDRESS to nonsense prevents frequent
        # hangs of chromedriver (possibly due to crbug.com/309093).
        os.environ["DBUS_SESSION_BUS_ADDRESS"] = "/dev/null"
        cls.proj_root = get_git_root()

    @classmethod
    def tearDownClass(cls):
        if cls.wants_xvfb:
            cls.vdisplay.stop()

    def init(self, driver):
        driver.set_script_timeout(DEFAULT_TIMEOUT)
        self.driver = driver
        self.bg_url = self.base_url + "_generated_background_page.html"

    def run(self, result=None):
        with self.manager() as driver:
            self.init(driver)
            super(ExtensionTestCase, self).run(result)

    def query_selector(self, css_selector, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))

    def wait(self, func, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(func)
