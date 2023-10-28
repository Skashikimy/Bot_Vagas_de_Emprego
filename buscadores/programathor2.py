import aiohttp
from bs4 import BeautifulSoup
import re

async def get_job_cards():
    base_url = 'https://programathor.com.br'

    print('\nBuscando vagas em Programathor...')

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url+'/jobs') as response:
            response.raise_for_status()
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            print(soup)

def get_job_info(html: str):
    '''
    Extrai informações da vaga de um conteúdo HTML específico.
    
    Parâmetros:
    html (str): Conteúdo HTML da página da vaga.
    
    Retorna:
    str: Informações da vaga formatadas.
    '''
    soup = BeautifulSoup(html, "html.parser")

    print(soup)

    # Extrai informações da empresa, título, descrição da vaga e link
    link = soup.select_one('a[href^="/jobs/"]').get('href')                     # ^ operador usado para selecionar atributo começa com um valor específico
    title = soup.select_one('h3.text-24').get_text().replace('\n', '').strip()  
    company = soup.select_one('.cell-list-content-icon > span:nth-child(1)').get_text().replace('\n', '').strip()
    location = soup.select_one('.cell-list-content-icon > span:nth-child(2)').get_text().replace('\n', '').strip()
    level = soup.select_one('.cell-list-content-icon > span:nth-child(5)').get_text().replace('\n', '').strip()
    regime = soup.select_one('.cell-list-content-icon > span:nth-child(6)').get_text().replace('\n', '').strip()
    skills = soup.select_one()

    result = f"{link}\n{title}\n{company}\n{location}\n{level}\n{regime}\n{skills}"
    return result

get_job_cards()