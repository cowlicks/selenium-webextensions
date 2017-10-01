# -*- coding: UTF-8 -*-
import os
import unittest

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .shim import Shim
from .config import Config
from .util import get_git_root

DEFAULT_TIMEOUT = 30

class ExtensionTestCase(unittest.TestCase):
    shim = None

    @classmethod
    def set_shim(cls):
        if cls.shim is None:
            cls.shim = Shim()

    @classmethod
    def setUpClass(cls):
        cls.set_shim()
        cls.manager = cls.shim.manager
        cls.base_url = cls.shim.urls.background
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

    def run(self, result=None):
        with self.manager() as driver:
            self.init(driver)
            super(ExtensionTestCase, self).run(result)

    def query_selector(self, css_selector, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))

    def wait(self, func, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(func)
