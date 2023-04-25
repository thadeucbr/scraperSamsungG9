import os
import smtplib
import ssl
import time
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException



def obter_preco(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "samsungbr-app-pdp-1-x-currencyContainer"))
        )
        price_element = driver.find_elements_by_css_selector(".samsungbr-app-pdp-1-x-currencyContainer")[0]
        price = "".join([e.text for e in price_element.find_elements_by_css_selector("*") if e.text.strip()])
    except NoSuchElementException:
        price = None

    driver.quit()
    return price


def monitorar_preco():
    url = 'https://shop.samsung.com.br/monitor-gamer-curvo-samsung-odyssey-49/p?cid=br_site_e-store_neoqledgamer_full__link_monitocurvorodysseygamer49_none'

    while True:
        preco = obter_preco(url)
        if preco:
            print(f'O preço atual do monitor é: {preco}')
        else:
            print('Não foi possível obter o preço do monitor.')

        time.sleep(60 * 60)  # Aguarde uma hora (3600 segundos) antes de verificar novamente

if __name__ == '__main__':
    monitorar_preco()
