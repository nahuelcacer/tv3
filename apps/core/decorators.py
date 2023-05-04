import requests

def login_ott_decorator(funcion):
    def wrapper(*args, **kwargs):
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
        headers['cookie'] = response_1.headers.get('Set-Cookie')
       
        return funcion(session=session,headers=headers,response_2=response_2, *args, **kwargs)
    return wrapper
