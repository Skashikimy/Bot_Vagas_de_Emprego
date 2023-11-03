import httpx
from bs4 import BeautifulSoup
import asyncio

def check_none(value) -> str:
    '''
    DOCSTRING
    '''
    
    if value == None:
        return 'Não informado'
    else:
        return value.get_text(strip=True)

async def get_programathor_jobs() -> list:
    '''
    DOCSTRING
    '''

    base_url = 'https://programathor.com.br'
    jobs = []

    for page in range(1,21):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{base_url}/jobs/page/{page}')
            soup = BeautifulSoup(response.content, 'html.parser')
            
            cells = soup.find_all('div', class_='cell-list')
            for cell in cells:
                title = cell.find('h3')
                if title == None or title.text.startswith('Vencida'):
                    continue
                code = int(''.join(cell.find('a')['href'].split('/jobs/')[1].split('-')[0]))    # Utilizado para verificar repetição de envio do bot no Discord
                title = title.get_text(strip=True)
                company = check_none(cell.find('span'))
                location = check_none(cell.find('span').find_next_sibling())
                link = base_url + cell.find('a')['href']

                job = [code, title, company, location, link]

                jobs.append(job)
        
    return jobs

# O código abaixo possui função apenas para teste, não sendo necessário no release
# O asyncio.run deve ser invocado pelo bot do Discord

resultados = asyncio.run(get_programathor_jobs())

for resultado in resultados:
    print('-'*50)
    print(f'Título da Vaga: {resultado[1]}')
    print(f'Empresa: {resultado[2]}')
    print(f'Local: {resultado[3]}')
    print(f'Link: {resultado[4]}')
    print('-'*50+'\n')