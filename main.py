import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from models.db_models import Produtos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.db_models import base


class ProdutosSite:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--lang=pt-BR')
        chrome_options.add_argument('--disable-notifications')
        self.driver = webdriver.Chrome(
            executable_path=os.getcwd() + os.sep + 'chromedriver' + os.sep + 'chromedriver.exe',
            options=chrome_options)
        self.driver.implicitly_wait(10)


    def Iniciar(self):
        self.session = self.configurar_banco_de_dados()
        self.captura_informacoes()


    def captura_informacoes(self):
        for numero_pagina in range(2):
            self.driver.get(f'https://cursoautomacao.netlify.app/produtos{numero_pagina + 1}.html')

            self.nome_produto = self.driver.find_elements(By.XPATH, "//*[@class='name']")
            self.preco_produto = self.driver.find_elements(By.XPATH, "//*[@class='price-container']")
            self.descricao = self.driver.find_elements(By.XPATH, "//*[@class='description']")

            self.armazenar_dados_banco()
            time.sleep(2)
        self.driver.close()

    def configurar_banco_de_dados(self):
        engine = create_engine('sqlite:///db_produtos.db', echo=True)
        base.metadata.drop_all(bind=engine)
        base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        return session

    def armazenar_dados_banco(self):
        for item in range(0, len(self.nome_produto)):
            novo_produto = Produtos()
            novo_produto.nome = self.nome_produto[item].text
            preco_produto = float(self.preco_produto[item].text[1:])
            novo_produto.preco = preco_produto
            novo_produto.descricao = self.descricao[item].text

            self.session.add(novo_produto)
            self.session.commit()


produtos = ProdutosSite()
produtos.Iniciar()
