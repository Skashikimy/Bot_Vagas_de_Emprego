import discord
import asyncio
from discord.ext import commands
import aiohttp
import bs4
import re

# Importa a função para obter links das vagas do módulo "programathor"
from links.programathor import get_programathor_links

# Define as intenções necessárias para o bot
intents = discord.Intents.default()
intents.message_content = True

# Criação do bot com o prefixo de comando e as intenções definidas
bot = commands.Bot(command_prefix="!", intents=intents)

# ID do canal específico onde as mensagens serão enviadas
canal_id = 1146495292292743188

# Lista para armazenar os links das vagas já enviadas
vagas_enviadas = []

# Função para obter o HTML de um link
async def get_html(link: str):
    async with aiohttp.ClientSession() as request:
        async with request.get(link) as resp:
            resp.raise_for_status()
            return await resp.text()

# Função para extrair informações da vaga a partir do HTML
def get_job_info(html: str):
    soup = bs4.BeautifulSoup(html, "html.parser")

    # Extrai informações da empresa, título, descrição da vaga e link
    company = soup.select_one('.wrapper-content-job-show').get_text().replace('\n', '').strip()
    title = soup.select_one('.wrapper-header-job-show > .container').get_text().replace('\n', '').strip()
    job = re.sub('\n\s*\n', '\n\n', soup.select_one('.line-height-2-4').get_text())
    link = soup.find('meta', {'property': 'og:url'}).get('content')

    result = f"{company}\n{title}\n{job}\n{link}"
    return result

# Função assíncrona para pesquisar vagas e enviar para o canal
async def search_and_send_vacancies():
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

# Adiciona a função de pesquisa e envio de vagas como um evento
@bot.event
async def on_ready():
    bot.loop.create_task(search_and_send_vacancies())

# Inicializa o bot com o token fornecido
bot.run('MTE0NTAxODA0ODEyNjkyMjc1NA.GWQMke.jzqOF7W8jvV8zcdCO8MLbEf2rs-KmOyfwY6mxg')

