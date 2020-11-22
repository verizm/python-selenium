#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import urllib.parse


class Server(BaseHTTPRequestHandler):  # наследуемся от базового класса handler
    def _set_response(self):  # формирование заголовков
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))  # создаем тело wfile

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)
        fragment = urllib.parse.urlparse(self.path).fragment
        value_dict = dict(urllib.parse.parse_qsl(fragment))
        # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()

        result = self.send_to_codeforces(value_dict[0], value_dict[1], value_dict[2])

        self.wfile.write("POST request for {}".format(result).encode('utf-8'))

    def send_to_codeforces(self, number_conftest, letter_task, programm):
        # отправка задачи
        driver.get(f"https://codeforces.com/contest/{number_conftest}/submit")

        select_task_field = Select(driver.find_element(By.CSS_SELECTOR, "[name='submittedProblemIndex']"))
        select_task_field.select_by_value(letter_task)

        time.sleep(2)

        select_program_language = Select(driver.find_element(By.CSS_SELECTOR, "[name='programTypeId']"))
        select_program_language.select_by_visible_text("GNU G++17 7.3.0")

        input_solution_field = driver.find_element(By.CSS_SELECTOR, "[id='editor']  .ace_text-input")
        driver.execute_script("arguments[0].click();", input_solution_field)

        input_solution_field.send_keys(programm)
        driver.find_element(By.CSS_SELECTOR, "[value='Отослать']").click()

        # получение результата
        table = driver.find_elements(By.CSS_SELECTOR, ".status-frame-datatable tbody tr [waiting='false'] a")
        time.sleep(3)
        return table[0].text


def run(server_class=HTTPServer, handler_class=Server, port=9090):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    driver = webdriver.Chrome()
    driver.get("https://codeforces.com/enter")
    # логин
    email_field = driver.find_element(By.CSS_SELECTOR, "[id='handleOrEmail']").send_keys(
        "v.lazunina@yandex.ru")
    pass_field = driver.find_element(By.CSS_SELECTOR, "[id='password']").send_keys("+_h3wr#6VGMf4Rt")
    go_button = driver.find_element(By.CSS_SELECTOR, "[value='Войти']").click()
    time.sleep(5)

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
