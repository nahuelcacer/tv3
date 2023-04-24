import requests
from bs4 import BeautifulSoup

def getDataWeb():
    session = requests.Session()

    # Enviar el nombre de usuario
    login_url = 'http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }
    username = {'usr': 'M4t14sCh4c0', 'next': ''}
    response_1 = session.post(login_url, headers=headers, data=username)

    # Enviar la contraseña
    password = {'pass': 'mati', 'envPass': ''}
    response_2 = session.post(login_url, headers=headers, data=password)


    # print(response_2.text)

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