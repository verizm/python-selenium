import argparse
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time

parser = argparse.ArgumentParser()  # создаем обьект класса ArgumentParser
parser.add_argument("number_conftest", type=str, help="get number of conftest")
parser.add_argument("letter_task", type=str, help="get letter of task")
parser.add_argument("programm", type=str, help="input task code")
args = parser.parse_args()


driver = webdriver.Chrome()
driver.get("https://codeforces.com/enter")
# логин
email_field = driver.find_element(By.CSS_SELECTOR, "[id='handleOrEmail']").send_keys("v.lazunina@yandex.ru")
pass_field = driver.find_element(By.CSS_SELECTOR, "[id='password']").send_keys("")
go_button = driver.find_element(By.CSS_SELECTOR, "[value='Войти']").click()
time.sleep(5)

# отправка задачи
driver.get(f"https://codeforces.com/contest/{args.number_conftest}/submit")

select_task_field = Select(driver.find_element(By.CSS_SELECTOR, "[name='submittedProblemIndex']"))
select_task_field.select_by_value(args.letter_task)

time.sleep(2)

select_program_language = Select(driver.find_element(By.CSS_SELECTOR, "[name='programTypeId']"))
select_program_language.select_by_visible_text("GNU G++17 7.3.0")

input_solution_field = driver.find_element(By.CSS_SELECTOR, "[id='editor']  .ace_text-input")
driver.execute_script("arguments[0].click();", input_solution_field)

input_solution_field.send_keys(args.programm)
submit_button = driver.find_element(By.CSS_SELECTOR, "[value='Отослать']").click()

# получение результата

table = driver.find_elements(By.CSS_SELECTOR, ".status-frame-datatable tbody tr [waiting='false'] a")
time.sleep(3)
print("Итоговый результат: " + table[0].text)

driver.close()
