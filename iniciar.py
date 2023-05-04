import requests
from bs4 import BeautifulSoup
from apps.core.decorators import login_ott_decorator

@login_ott_decorator
def getDataWeb(session,headers,response_2):
    
    soup = BeautifulSoup(response_2.text, 'html.parser')

    data = {}

    # Extraer el vendedor y los créditos
    data['vendedor'] = soup.find('h3').text.split(': ')[1]
    data['creditos'] = soup.find_all('h3')[1].text.split(': ')[1]

    data['tabla'] = [] 
    # Extraer los datos de la tabla
    table = soup.find('table')
    headers = [header.text for header in table.find_all('th')]
    for row in table.find_all('tr')[1:]:
        row_data = {}
        for i, dates in enumerate(row.find_all('td')):
            row_data[headers[i]] = dates.text
        data['tabla'].append(row_data)

    # Imprimir el objeto
    return data 


