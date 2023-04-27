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


def Extender(user):

    url = f"http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?M4t14sCh4c0&usr={user}&ext=1"
    payload = f"transfer=1&receptor=1&cuenta={user}&orden=Vencimiento&cantidad=1&extend=&modusr=&modcom=&newusr=&newcom="
    response = requests.post(url, data=payload)

    print(response.content)





#     fetch("http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?M4t14sCh4c0&usr=m4rt1nv4ll3j0s&ext=1", {
#   "headers": {
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "accept-language": "es-ES,es;q=0.9",
#     "cache-control": "max-age=0",
#     "content-type": "application/x-www-form-urlencoded",
#     "upgrade-insecure-requests": "1",
#     "cookie": "PHPSESSID=42r6qbqmarpgtrqiqn8e2tlf5i",
#     "Referer": "http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?M4t14sCh4c0&usr=m4rt1nv4ll3j0s&ext=1",
#     "Referrer-Policy": "strict-origin-when-cross-origin"
#   },
#   "body": "transfer=1&receptor=1&cuenta=V3roV4ll3jo5&orden=Vencimiento&cantidad=1&extend=&modusr=&modcom=&newusr=&newcom=",
#   "method": "POST"
# });


# $session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
# $session.UserAgent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
# $session.Cookies.Add((New-Object System.Net.Cookie("PHPSESSID", "42r6qbqmarpgtrqiqn8e2tlf5i", "/", "198.23.223.196")))
# Invoke-WebRequest -UseBasicParsing -Uri "http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?M4t14sCh4c0&usr=m4rt1nv4ll3j0s&ext=1" `
# -Method "POST" `
# -WebSession $session `
# -Headers @{
# "Accept"="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
#   "Accept-Encoding"="gzip, deflate"
#   "Accept-Language"="es-ES,es;q=0.9"
#   "Cache-Control"="max-age=0"
#   "Origin"="http://198.23.223.196"
#   "Referer"="http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?M4t14sCh4c0&usr=m4rt1nv4ll3j0s&ext=1"
#   "Upgrade-Insecure-Requests"="1"
# } `
# -ContentType "application/x-www-form-urlencoded" `
# -Body "transfer=1&receptor=1&cuenta=V3roV4ll3jo5&orden=Vencimiento&cantidad=1&extend=&modusr=&modcom=&newusr=&newcom="


# url
# http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?M4t14sCh4c0&usr=m4rt1nv4ll3j0s&ext=1