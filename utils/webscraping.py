#!/usr/bin/env python3
# -*- coding: utf-8 -*

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd
from tqdm import tqdm
from datetime import datetime



class Scraping():
    
    def __init__(self):
        self.webdriver = webdriver.Chrome(ChromeDriverManager().install()) # Inicializa o driver do Chrome
        pass

    def extract_apartment_data(self, bairro, url, pages):
        driver = self.webdriver
        errors = []  # Lista para armazenar URLs que causaram erros durante a extração
        results = []  # Lista para armazenar os resultados extraídos dos apartamentos

        current_url = url
        driver.get(url) # Abre a URL no navegador
        sleep(2)
        actions = ActionChains(driver) # Cria uma instância de ActionChains para ações de mouse

        try:
            driver.find_element_by_class_name("cookie-notifier__cta").click() # Fecha a mensagem de notificação de cookies, se existir
        except:
            print("No cookies!") # Exibe uma mensagem se não houver mensagem de notificação de cookies

        for i in tqdm(range(pages), desc=bairro):
            sleep(5)
            main_div = driver.find_element_by_class_name("results-main__panel") # Encontra a seção principal de resultados
            properties = main_div.find_elements_by_class_name("js-property-card") # Encontra os elementos que representam os apartamentos na página
            paginator = driver.find_element_by_class_name("js-results-pagination") # Encontra o elemento que contém o paginador
            next_page = paginator.find_element_by_xpath('//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[9]/button') # Encontra o botão "próxima página"

            for i, apartment in enumerate(properties): # Loop para extrair informações de cada apartamento na página
                url = apartment.find_element_by_class_name("js-card-title").get_attribute("href") # Extrai a URL do apartamento
                apto_id = url.split("id-")[-1][:-1]  # Extrai o ID do apartamento a partir da URL
                header = apartment.find_element_by_class_name("property-card__title").text # Extrai o título do apartamento
                address = apartment.find_element_by_class_name("property-card__address").text  # Extrai o endereço do apartamento
                area = apartment.find_element_by_class_name("js-property-card-detail-area").text # Extrai a área do apartamento
                rooms = apartment.find_element_by_class_name("js-property-detail-rooms").text # Extrai o número de quartos do apartamento
                bathrooms = apartment.find_element_by_class_name("js-property-detail-bathroom").text  #Extrai o número de banheiros do apartamento
                garages = apartment.find_element_by_class_name("js-property-detail-garages").text # Extrai o número de vagas de garagem do apartamento
                try:
                    amenities = apartment.find_element_by_class_name("property-card__amenities").text # Extrai as comodidades do apartamento, se estiverem disponíveis
                except:
                    amenities = None
                    errors.append(url)  # Adiciona a URL à lista de erros se ocorrer um erro ao extrair as comodidades
                price = apartment.find_element_by_class_name("js-property-card-prices").text # Extrai o preço do apartamento
                try:
                    condo = apartment.find_element_by_class_name("js-condo-price").text # Extrai a taxa do condomínio, se estiver disponível
                except:
                    condo = None
                    errors.append(url) # Adiciona a URL à lista de erros se ocorrer um erro ao extrair a taxa do condomínio

                crawler = bairro # Define o bairro como o nome do crawler
                crawled_at = datetime.now().strftime("%Y-%m-%d %H:%M")  # Obtém a data e hora atual formatada

                results.append({"id": apto_id,
                                "url": url,
                                "header": header,
                                "address": address,
                                "area": area,
                                "rooms": rooms,
                                "bathrooms": bathrooms,
                                "garages": garages,
                                "amenities": amenities,
                                "price": price,
                                "condo": condo,
                                "crawler": crawler,
                                "crawled_at": crawled_at}) # Adiciona um dicionário com as informações do apartamento à lista de resultados
            try:
                next_page.click() # Clica no botão "próxima página" para avançar para a próxima página de resultados
            except:
                print("Next page not clickable") #Quando atingir o Next page not clickable vai para proximo bairro
                break
        return results
    
    def close(self):
        self.webdriver.close() # Fecha o navegador