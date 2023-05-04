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
from selenium.webdriver.common.keys import Keys
import threading

load_dotenv()

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

print("Iniciando o script monitorar_preco.py")



def obter_info_kabum(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)
    driver.get(url)

    try:
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h4.finalPrice"))
        )
        price = price_element.text.strip()

        stock_element = driver.find_element_by_css_selector(".cNxeVG b")
        stock = int(stock_element.text.split()[0].replace('%', ''))

        promo_time_element = driver.find_element_by_css_selector(".eWpxwv span.countdownOffer")
        promo_time = promo_time_element.text.strip()

    except NoSuchElementException:
        price, stock, promo_time = None, None, None

    driver.quit()
    return price, stock, promo_time

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
            EC.presence_of_element_located((By.CLASS_NAME, "samsungbr-app-pdp-1-x-summaryInstalmentsContent"))
        )
        price_element = driver.find_elements_by_css_selector(".samsungbr-app-pdp-1-x-summaryInstalmentsContent span")[0]
        price = price_element.text.strip()
    except NoSuchElementException:
        price = None

    driver.quit()
    return price

ultimo_preco_por_url = {}

def monitorar_kabum(url, product_name):
    global ultimo_preco_por_url

    while True:
        preco, estoque, tempo_promocao = obter_info_kabum(url)

        if preco and estoque and tempo_promocao:
            print(f"O preço atual do {product_name} é: {preco}")
            print(f"O estoque atual do {product_name} é: {estoque}")
            print(f"O tempo restante da promoção do {product_name} é: {tempo_promocao}")
            
            preco_num = float(preco.replace("R$", "").replace(".", "").replace(",", "."))
            dias_promocao = int(tempo_promocao.split("D")[0])

            if url not in ultimo_preco_por_url or preco_num < ultimo_preco_por_url[url] or estoque <= 5 or dias_promocao <= 4:
                if url in ultimo_preco_por_url:
                    print(f"Enviando e-mail para o {product_name}...")
                    send_email(preco, product_name, url)

                ultimo_preco_por_url[url] = preco_num

        else:
            print(f"Não foi possível obter informações do {product_name}.")

        time.sleep(60 * 60)

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
    product_name1 = 'Samsung: Monitor Curvo Samsung Odyssey 49'

    url2 = 'https://shop.samsung.com/br/monitor-gamer-curvo-samsung-odyssey-49--mini-led-dqhd-240hz-2002/p'
    product_name2 = 'Samsung: Monitor Curvo Samsung Odyssey Neo G9 49'

    url3 = 'https://www.kabum.com.br/produto/129919/monitor-gamer-samsung-odyssey-g9-49-curvo-dqhd-240hz-1ms-hdmi-e-displayport-hdr-1000-freesync-premium-ajuste-de-altura-lc49g95tsslxzd'
    product_name3 = 'KABUM: Monitor Curvo Samsung Odyssey 49'

    thread1 = threading.Thread(target=monitorar_preco, args=(url1, product_name1))
    thread2 = threading.Thread(target=monitorar_preco, args=(url2, product_name2))
    thread3 = threading.Thread(target=monitorar_kabum, args=(url3, product_name3))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

if __name__ == '__main__':
    main()
