from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from form_workes.formConnetion import FormConnection
from settings import form_url


def get_blocks_info(driver):
    wait = WebDriverWait(driver, 20)
    questions = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listitem"]'))
    )
    return questions


if __name__ == '__main__':
    form_connection = FormConnection(form_url)

    res = get_blocks_info(form_connection.get_driver())

    for i, question_block in enumerate(res):
        try:
            label_element = question_block.find_element(By.XPATH, './/span[@class="M7eMe"]')
            label_text = label_element.text.strip()

            is_required = False
            if question_block.find_elements(By.XPATH, './/span[@aria-label="Обязательно"]'):
                is_required = True

            field_type = "unknown"

            if question_block.find_elements(By.TAG_NAME, "input"):
                input_elem = question_block.find_element(By.TAG_NAME, "input")
                input_type = input_elem.get_attribute("type")
                if input_type == "text":
                    field_type = "text"
                elif input_type == "url":
                    field_type = "url"
                elif input_type == "number":
                    field_type = "number"
                else:
                    field_type = f"input[{input_type}]"

            elif question_block.find_elements(By.TAG_NAME, "textarea"):
                field_type = "textarea"

            elif question_block.find_elements(By.XPATH, './/div[@role="radio"]'):
                field_type = "radio"

            elif question_block.find_elements(By.XPATH, './/div[@role="checkbox"]'):
                field_type = "checkbox"

            elif question_block.find_elements(By.TAG_NAME, "select"):
                field_type = "select"

            print(f"{i + 1}. [{field_type}] {label_text} {'*' if is_required else ''}")
        except:
            pass
