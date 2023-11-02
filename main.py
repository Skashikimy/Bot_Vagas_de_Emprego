import discord
import asyncio
from discord.ext import commands
import aiohttp
import bs4
import re
from links.programathor import get_programathor_links

# Definindo Intenções para o Bot
intents = discord.Intents.default()
intents.message_content = True

# Criação do Bot
bot = commands.Bot(command_prefix="!", intents=intents)

# ID do Canal Específico para Envio de Mensagens
canal_id = 1147029744043442287

# Lista para Armazenar Links de Vagas já Enviadas
vagas_enviadas = []

async def get_html(link: str):

    '''
    Obtém o HTML de uma página da web a partir de um link.
    
    Parâmetros:
    link (str): URL da página da web a ser obtida.
    
    Retorna:
    str: Conteúdo HTML da página da web.
    '''

    async with aiohttp.ClientSession() as request:
        async with request.get(link) as resp:
            resp.raise_for_status()
            return await resp.text()

def get_job_info(html: str):
    '''
    Extrai informações da vaga de um conteúdo HTML específico.
    
    Parâmetros:
    html (str): Conteúdo HTML da página da vaga.
    
    Retorna:
    str: Informações da vaga formatadas.
    '''
    soup = bs4.BeautifulSoup(html, "html.parser")

    # Extrai informações da empresa, título, descrição da vaga e link
    company = soup.select_one('.wrapper-content-job-show').get_text().replace('\n', '').strip()
    title = soup.select_one('.wrapper-header-job-show > .container').get_text().replace('\n', '').strip()
    job = re.sub('\n\s*\n', '\n\n', soup.select_one('.line-height-2-4').get_text())
    link = soup.find('meta', {'property': 'og:url'}).get('content')

    result = f"{company}\n{title}\n{job}\n{link}"
    return result

async def search_and_send_vacancies():
    """
    Pesquisa vagas periodicamente e envia para um canal específico.
    """
    await bot.wait_until_ready()  # Espera o bot estar pronto
    
    channel = bot.get_channel(canal_id)  # Obtém o canal pelo ID

    while not bot.is_closed():
        tasks = []
        links = await get_programathor_links()

        # Itera sobre os links das vagas
        for link in links:
            if link not in vagas_enviadas:  # Verifica se a vaga já foi enviada
                vagas_enviadas.append(link)
                tasks.append(asyncio.create_task(get_html(link)))

        # Espera até que todos os HTMLs sejam obtidos
        for task in tasks:
            html = await task
            job_info = get_job_info(html)

            if job_info:
                # Divide as informações em pedaços menores para evitar mensagens muito longas
                chunks = [job_info[i:i+2000] for i in range(0, len(job_info), 2000)]
                for chunk in chunks:
                    await channel.send(chunk)

        # Aguarda por 2 minutos antes da próxima busca
        await asyncio.sleep(120)

# Adiciona a Função de Pesquisa e Envio de Vagas como um Evento
@bot.event
async def on_ready():
    bot.loop.create_task(search_and_send_vacancies())

# Inicializa o Bot com o Token Fornecido
bot.run(keyring.get_password('discord', 'token'))
