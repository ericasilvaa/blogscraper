
#VERSAO 1 url JOGOS
"""
import os
import time
import json
import logging
import random
import requests
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver #type:ignore 
from selenium.webdriver.common.by import By #type:ignore 
from selenium.webdriver.chrome.options import Options #type:ignore 
from selenium.webdriver.support.ui import WebDriverWait #type:ignore 
from selenium.webdriver.support import expected_conditions as EC #type:ignore 

# Configurar logger
def configurar_logger(nome_logger, log_filename):
    logger = logging.getLogger(nome_logger)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s | %(message)s', datefmt='%Y-%m-%d_%H:%M:%S')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.info(f'Log iniciado em: {date.today()}')
    return logger

# Configurar ChromeDriver
def configurar_chrome_driver():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    logger.info('ChromeDriver configurado com sucesso.')
    return options

# Função para carregar mais notícias
def carregar_mais_noticias(driver, qtd_noticias):
    lista_noticias = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article'))
    )
    while len(lista_noticias) < qtd_noticias:
        print(f'Carregando mais notícias... {len(lista_noticias)} de {qtd_noticias}', end='', flush=True)
        try:
            botao_carregar_mais = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.load-more'))
            )
            driver.execute_script("arguments[0].click();", botao_carregar_mais)
            time.sleep(random.randint(5, 10))
            lista_noticias = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article'))
            )
        except:
            logger.error('Erro ao carregar mais notícias')
            break

# Função para listar notícias
def listar_noticias(qtd_noticias, chrome_options):
    url = "https://tecnoblog.net/tema/games-jogos/"
    logger.info(f'Acessando URL: {url}')
    noticias = {}
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)

    carregar_mais_noticias(driver, qtd_noticias)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    lista_noticias = soup.select('article')
    for noticia in lista_noticias:
        try:
            titulo = noticia.select_one('h2').get_text(strip=True)
            link = noticia.select_one('a').get('href')
            resumo = noticia.select_one('.excerpt').get_text(strip=True) if noticia.select_one('.excerpt') else None
            data_publicacao = noticia.select_one('time').get('datetime') if noticia.select_one('time') else None
            autor = noticia.select_one('.author').get_text(strip=True) if noticia.select_one('.author') else None

            id_unico = hash(link)  # Gerar um identificador único
            noticias[id_unico] = {
                'titulo': titulo,
                'resumo': resumo,
                'link': link,
                'data_publicacao': data_publicacao,
                'autor': autor,
                'conteudo': None  # Inicializa o campo conteúdo como None
            }
            if len(noticias) >= qtd_noticias:
                break
        except Exception as e:
            logger.error(f'Erro ao coletar notícia: {e}')
    driver.quit()
    return noticias

# Função para acessar cada notícia e coletar os dados
def salvar_dados_noticia(url_noticia):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        response = requests.get(url_noticia, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            titulo = soup.select_one('h1[itemprop="headline"], h1.flipboard-title').get_text(strip=True) if soup.select_one('h1[itemprop="headline"], h1.flipboard-title') else None
            data_publicacao = soup.select_one('time[datetime]').get('datetime') if soup.select_one('time[datetime]') else None
            autor = soup.select_one('div.author span.flipboard-author a').get_text(strip=True) if soup.select_one('div.author span.flipboard-author a') else None
            descricao = soup.select_one('p.flipboard-subtitle').get_text(strip=True) if soup.select_one('p.flipboard-subtitle') else None
            
            # Adicionando log para verificar se os elementos são encontrados
            #lista_conteudo = soup.select('article.single-grid.article-content > p, article.single-grid.article-content > h2, article.single-grid.article-content > h3, article.single-grid.article-content > h4, article.single-grid.article-content > h5, article.single-grid.article-content > h6, article.single-grid.article-content > figure')
            #lista_conteudo = soup.select('div[class*="content-text"]')
            lista_conteudo = soup.select('div[class*="content-text"], p, h1, h2, h3, h4, h5, h6, figure') #Coleta tudo ta funcionadndo ok 
           # lista_conteudo = soup.select('div.article-body p, div.article-body h2, div.article-body h3') 

            
            if lista_conteudo:
                conteudo = '\n'.join([elemento.get_text(strip=True) for elemento in lista_conteudo]).strip()
            else:
                logger.warning('Nenhum conteúdo encontrado com o seletor especificado.')
                conteudo = ''

            logger.info(f'Título capturado: {titulo}')
            logger.info(f'Data de publicação capturada: {data_publicacao}')
            logger.info(f'Autor capturado: {autor}')
            logger.info(f'Descrição capturada: {descricao}')
            logger.info(f'Conteúdo capturado: {conteudo[:100]}...')  # Exibe os primeiros 100 caracteres do conteúdo

            return {
                'titulo': titulo,
                'data_publicacao': data_publicacao,
                'autor': autor,
                'descricao': descricao,
                'conteudo': conteudo
            }
        else:
            logger.error(f'Erro ao acessar a URL: {url_noticia}, status code: {response.status_code}')
    except Exception as e:
        logger.error(f'Erro ao capturar dados da notícia: {url_noticia}, erro: {e}')
        return None






# Função para salvar os dados em um arquivo JSON
def salvar_json(dados, nome_arquivo):
    with open(os.path.join(os.getcwd(), nome_arquivo), encoding='utf-8', mode='w') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    logger.info(f'Dados salvos em: {nome_arquivo}')

# Execução principal
if __name__ == '__main__':
    logger = configurar_logger('tecnoblog_logger', 'tecnoblog_scraper.log')
    chrome_options = configurar_chrome_driver()

    try:
        qtd_noticias = int(input('Quantidade de notícias a capturar: '))
        noticias = listar_noticias(qtd_noticias, chrome_options)
        
        for id_noticia, dados_noticia in noticias.items():
            dados_completos = salvar_dados_noticia(dados_noticia['link'])
            if dados_completos:
                noticias[id_noticia].update(dados_completos)
        
        salvar_json(noticias, f'noticias_games_jogos.json')
    except ValueError:
        logger.error('Quantidade de notícias inválida.')
"""

#VERSAO 2 coleta todos os dados sem ecesso 
import os
import time
import json
import logging
import random
import requests
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver  # type:ignore
from selenium.webdriver.common.by import By  # type:ignore
from selenium.webdriver.chrome.options import Options  # type:ignore
from selenium.webdriver.support.ui import WebDriverWait  # type:ignore
from selenium.webdriver.support import expected_conditions as EC  # type:ignore

# Configurar logger
def configurar_logger(nome_logger, log_filename):
    logger = logging.getLogger(nome_logger)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s | %(message)s', datefmt='%Y-%m-%d_%H:%M:%S')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.info(f'Log iniciado em: {date.today()}')
    return logger

# Configurar ChromeDriver
def configurar_chrome_driver():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    logger.info('ChromeDriver configurado com sucesso.')
    return options

# Função para carregar mais notícias
# Função para carregar mais notícias
#def carregar_mais_noticias(driver, qtd_noticias_desejadas, limite_paginas=5):
    pagina_atual = 1
    lista_noticias = []
    textos_noticias = []

    while len(textos_noticias) < qtd_noticias_desejadas and pagina_atual <= limite_paginas:
        logger.info(f"Acessando página {pagina_atual}. Notícias carregadas até agora: {len(textos_noticias)}")
        
        try:
            # Aguardar até que as notícias da página sejam carregadas
            noticias_atualizadas = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article'))
            )
            
            for noticia in noticias_atualizadas:
                # Verificando se o texto não é nulo e garantindo que contém informações suficientes
                if noticia.text:
                    textos_noticias.append(noticia.text)

            # Verificar se já atingiu a quantidade desejada
            if len(textos_noticias) >= qtd_noticias_desejadas:
                break

            # Verificar se existe o link de navegação para a próxima página
            try:
                ul_navegacao = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.page-numbers'))
                )
                logger.info("Encontrado o menu de navegação de páginas!")

                proxima_pagina = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.btn-pagination.btn-prox a'))
                )
                
                if proxima_pagina:
                    driver.execute_script("arguments[0].click();", proxima_pagina)
                    pagina_atual += 1
                    time.sleep(random.randint(5, 10))  # Pausa para garantir que a página seja carregada
                else:
                    logger.warning(f"Não foi possível encontrar o link da próxima página na página {pagina_atual}.")
                    break
            except Exception as e:
                logger.warning(f"Erro ao tentar clicar na próxima página ou não há mais páginas. Detalhes: {e}")
                break

        except Exception as e:
            logger.error(f"Erro ao carregar notícias na página {pagina_atual}: {e}")
            break

    logger.info(f"Número total de notícias carregadas: {len(textos_noticias)}")
   
    return textos_noticias


# Função para listar notícias
#def listar_noticias(qtd_noticias, chrome_options):
    url = "https://tecnoblog.net/tema/games-jogos/"
    logger.info(f'Acessando URL: {url}')
    noticias = {}
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)
    
    #textos_noticias = carregar_mais_noticias(driver, qtd_noticias)
    carregar_mais_noticias(driver, qtd_noticias)
    
    

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    lista_noticias = soup.select('article')
    for noticia in lista_noticias:
        try:
            titulo = noticia.select_one('h2').get_text(strip=True)
            link = noticia.select_one('a').get('href')
            resumo = noticia.select_one('.excerpt').get_text(strip=True) if noticia.select_one('.excerpt') else None
            data_publicacao = noticia.select_one('time').get('datetime') if noticia.select_one('time') else None
            autor = noticia.select_one('.author').get_text(strip=True) if noticia.select_one('.author') else None

            id_unico = hash(link)  # Gerar um identificador único
            noticias[id_unico] = {
                'titulo': titulo,
                'resumo': resumo,
                'link': link,
                'data_publicacao': data_publicacao,
                'autor': autor,
                'conteudo': None  # Inicializa o campo conteúdo como None
            }
            if len(noticias) >= qtd_noticias:
                break
        except Exception as e:
            logger.error(f'Erro ao coletar notícia: {e}')
    driver.quit()
    return noticias

def carregar_mais_noticias(driver, qtd_noticias_desejadas, limite_paginas=8):
    pagina_atual = 1
    textos_noticias = []
    lista_completa_noticias = []

    while len(lista_completa_noticias) < qtd_noticias_desejadas and pagina_atual <= limite_paginas:
        logger.info(f"Acessando página {pagina_atual}. Notícias carregadas até agora: {len(lista_completa_noticias)}")
        
        try:
            # Esperar até que todas as notícias da página sejam carregadas
            noticias_atualizadas = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article'))
            )

            for noticia in noticias_atualizadas:
                if noticia.text:
                    textos_noticias.append(noticia.get_attribute('outerHTML'))  # Coletar o HTML completo da notícia
                    lista_completa_noticias.append(noticia.text)

            # Verificar se já atingiu a quantidade desejada
            if len(lista_completa_noticias) >= qtd_noticias_desejadas:
                break

            # Verificar e clicar no link de navegação para a próxima página
            try:
                proxima_pagina = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.btn-pagination.btn-prox a'))
                )
                if proxima_pagina:
                    driver.execute_script("arguments[0].click();", proxima_pagina)
                    pagina_atual += 1
                    time.sleep(random.randint(5, 10))  # Pausa para o carregamento da página
                else:
                    logger.warning(f"Não foi possível encontrar o link da próxima página na página {pagina_atual}.")
                    break
            except Exception as e:
                logger.warning(f"Erro ao tentar clicar na próxima página ou não há mais páginas. Detalhes: {e}")
                break

        except Exception as e:
            logger.error(f"Erro ao carregar notícias na página {pagina_atual}: {e}")
            break

    logger.info(f"Número total de notícias carregadas: {len(lista_completa_noticias)}")
    return textos_noticias

def listar_noticias(qtd_noticias, chrome_options):
    url = "https://tecnoblog.net/tema/games-jogos/"
    logger.info(f'Acessando URL: {url}')
    noticias = {}
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)

    textos_noticias = carregar_mais_noticias(driver, qtd_noticias)
    
    logger.debug(f'Textos de notícias brutas coletadas: {len(textos_noticias)}')

    for noticia_html in textos_noticias:
        soup = BeautifulSoup(noticia_html, 'html.parser')  # Processar o HTML individualmente
        try:
            titulo = soup.select_one('h2').get_text(strip=True)
            link = soup.select_one('a').get('href')
            resumo = soup.select_one('.excerpt').get_text(strip=True) if soup.select_one('.excerpt') else None
            data_publicacao = soup.select_one('time').get('datetime') if soup.select_one('time') else None
            autor = soup.select_one('.author').get_text(strip=True) if soup.select_one('.author') else None

            id_unico = hash(link)
            noticias[id_unico] = {
                'titulo': titulo,
                'resumo': resumo,
                'link': link,
                'data_publicacao': data_publicacao,
                'autor': autor,
                'conteudo': None
            }

            if len(noticias) >= qtd_noticias:
                break
        except Exception as e:
            logger.error(f'Erro ao coletar notícia: {e}')

    driver.quit()
    return noticias





# Função para acessar cada notícia e coletar os dados
def salvar_dados_noticia(url_noticia):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        response = requests.get(url_noticia, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            titulo = soup.select_one('h1[itemprop="headline"], h1.flipboard-title').get_text(strip=True) if soup.select_one('h1[itemprop="headline"], h1.flipboard-title') else None
            data_publicacao = soup.select_one('time[datetime]').get('datetime') if soup.select_one('time[datetime]') else None
            autor = soup.select_one('div.author span.flipboard-author a').get_text(strip=True) if soup.select_one('div.author span.flipboard-author a') else None
            descricao = soup.select_one('p.flipboard-subtitle').get_text(strip=True) if soup.select_one('p.flipboard-subtitle') else None

            lista_conteudo = soup.select('div[class*="content-text"], p, h1, h2, h3, h4, h5, h6, figure')
            conteudo_completo = []
            for elem in lista_conteudo:
                if elem.find('nav', class_='tags') or elem.get('id') == 'pergunte-ao-tecnochat':
                    break  # Interrompe a coleta ao encontrar as tags especificadas
                conteudo_completo.append(elem.get_text(strip=True))
            conteudo = '\n'.join(conteudo_completo).strip()

            logger.info(f'Título capturado: {titulo}')
            return {
                'titulo': titulo,
                'data_publicacao': data_publicacao,
                'autor': autor,
                'descricao': descricao,
                'conteudo': conteudo
            }
        else:
            logger.error(f'Erro ao acessar a URL: {url_noticia}, status code: {response.status_code}')
    except Exception as e:
        logger.error(f'Erro ao capturar dados da notícia: {url_noticia}, erro: {e}')
        return None

# Função para salvar os dados em um arquivo JSON
def salvar_json(dados, nome_arquivo):
    with open(os.path.join(os.getcwd(), nome_arquivo), encoding='utf-8', mode='w') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    logger.info(f'Dados salvos em: {nome_arquivo}')

# Execução principal
#if __name__ == '__main__':
    logger = configurar_logger('noticias_logger', 'noticias.log')
    chrome_options = configurar_chrome_driver()
    noticias_coletadas = listar_noticias(200, chrome_options) #aumenta o limite de noticias
    logger.info(f'Total de notícias coletadas antes de salvar: {len(noticias_coletadas)}')
    

    try:        
        for id_noticia, dados_noticia in noticias_coletadas.items():
            logger.debug(f'Processando notícia com ID: {id_noticia}')
            dados_completos = salvar_dados_noticia(dados_noticia['link'])
            if dados_completos:
                noticias_coletadas[id_noticia].update(dados_completos)
            logger.debug(f'Notícia atualizada com dados completos: {dados_completos}')
   
        logger.debug(f'Notícias finalmente processadas: {len(noticias_coletadas)}')
        salvar_json(noticias_coletadas, f'JOGOS.json')
    except ValueError:
        logger.error('Quantidade de notícias inválida.')

if __name__ == '__main__':
    logger = configurar_logger('noticias_logger', 'noticias.log')
    chrome_options = configurar_chrome_driver()
    noticias_coletadas = listar_noticias(400, chrome_options)  # Configure um limite alto de notícias

    logger.info(f'Total de notícias coletadas antes de salvar: {len(noticias_coletadas)}')
    
    try:
        for id_noticia, dados_noticia in noticias_coletadas.items():
            logger.debug(f'Processando notícia com ID: {id_noticia}')
            dados_completos = salvar_dados_noticia(dados_noticia['link'])
            if dados_completos:
                noticias_coletadas[id_noticia].update(dados_completos)
            logger.debug(f'Notícias finalizadas: {dados_completos}')

        logger.debug(f'Notícias finalmente processadas: {len(noticias_coletadas)}')
        salvar_json(noticias_coletadas, 'jOGOS.json')
    except ValueError:
        logger.error('Quantidade de notícias inválida.')