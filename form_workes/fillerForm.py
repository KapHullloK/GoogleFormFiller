import asyncio
from concurrent.futures import ThreadPoolExecutor

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FillerForm:
    timeout = 10

    def __init__(self, driver):
        self.driver = driver
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, 'input'))
        )

    def input_field(self, question, text) -> None:
        xpath = f'//span[contains(normalize-space(), "{question}")]/following::input[1] | ' \
                f'//span[contains(normalize-space(), "{question}")]/following::textarea[1]'
        # input_fio = WebDriverWait(self.driver, self.timeout).until(
        #     EC.element_to_be_clickable((By.XPATH, f'//span[contains(text(), "{question}")]/following::input[1]'))
        # )
        input_fio = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        input_fio.send_keys(text)

    def one_of_the_list(self, answer):
        radio_button_xpath = f'//span[contains(text(), "{answer}")]'
        wait = WebDriverWait(self.driver, self.timeout)
        radio_button = wait.until(EC.element_to_be_clickable((By.XPATH, radio_button_xpath)))
        radio_button.click()

    def few_from_the_list(self, answer):
        checkbox_xpath = f'//span[contains(text(), "{answer}")]'
        wait = WebDriverWait(self.driver, self.timeout)
        checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
        checkbox.click()


class AsyncFillerForm:
    def __init__(self, driver):
        self.driver = driver
        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor()
        self.filler = None

    async def create(self):
        self.filler = await self.loop.run_in_executor(self.executor, FillerForm, self.driver)

    async def input_field(self, question, text):
        await self.loop.run_in_executor(self.executor, self.filler.input_field, question, text)

    async def one_of_the_list(self, answer):
        await self.loop.run_in_executor(self.executor, self.filler.one_of_the_list, answer)

    async def few_from_the_list(self, answer):
        await self.loop.run_in_executor(self.executor, self.filler.few_from_the_list, answer)
