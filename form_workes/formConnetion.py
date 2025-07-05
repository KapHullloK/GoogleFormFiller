import asyncio
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FormConnection:

    def __init__(self, url):
        self.url = url
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless=new")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument("start-maximized")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.execute_script("delete navigator.__proto__.webdriver")
        self.driver.get(self.url)

    def get_driver(self):
        return self.driver

    def switch_driver(self):
        try:
            iframe = self.driver.find_element_by_tag_name('iframe')
            self.driver.switch_to.frame(iframe)
        except:
            pass

    def quite(self):
        self.driver.switch_to.default_content()

        send_button = 'Отправить'
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{send_button}']"))
        )
        self.driver.execute_script("arguments[0].click();", submit_button)
        # submit_button.click()
        self.driver.quit()


class AsyncFormConnection:
    def __init__(self, url):
        self.url = url
        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor()

    async def __aenter__(self):
        self.form_connection = await self.loop.run_in_executor(self.executor, FormConnection, self.url)
        return self.form_connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.loop.run_in_executor(self.executor, self.form_connection.quite)
        self.executor.shutdown()
