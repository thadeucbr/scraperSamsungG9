import os
import smtplib
import ssl
import time
from email.message import EmailMessage
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import threading

load_dotenv()

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

print("Iniciando o script monitorar_preco.py")

def send_email(price, product_name, url):
    msg = EmailMessage()
    msg.set_content(f"O preço do {product_name} caiu para R${price}!\n\nConfira a oferta aqui: {url}")

    msg["Subject"] = f"Alerta de Preço: {product_name}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Ocorreu um erro ao enviar o e-mail: {e}")

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

ultimo_preco_por_url = {}

def monitorar_preco(url, product_name):
    global ultimo_preco_por_url

    while True:
        preco = obter_preco(url)

        if preco:
            print(f"O preço atual do {product_name} é: {preco}")
            
            preco_num = float(preco.replace("R$", "").replace(".", "").replace(",", "."))

            if url not in ultimo_preco_por_url or preco_num < ultimo_preco_por_url[url]:
                if url in ultimo_preco_por_url:
                    print(f"O preço do {product_name} caiu! Enviando e-mail...")
                    send_email(preco, product_name, url)

                ultimo_preco_por_url[url] = preco_num

        else:
            print(f"Não foi possível obter o preço do {product_name}.")

        time.sleep(60 * 60)

def main():
    url1 = 'https://shop.samsung.com.br/monitor-gamer-curvo-samsung-odyssey-49/p?cid=br_site_e-store_neoqledgamer_full__link_monitocurvorodysseygamer49_none'
    product_name1 = 'Monitor Gamer Curvo Samsung Odyssey 49'

    url2 = 'https://shop.samsung.com/br/monitor-gamer-curvo-samsung-odyssey-49--mini-led-dqhd-240hz-2002/p'
    product_name2 = 'Monitor Curvo Samsung Odyssey Neo G9 49'

    thread1 = threading.Thread(target=monitorar_preco, args=(url1, product_name1))
    thread2 = threading.Thread(target=monitorar_preco, args=(url2, product_name2))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == '__main__':
    main()
