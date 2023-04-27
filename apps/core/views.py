from multiprocessing import context
from django.shortcuts import render, redirect
from urllib.request import urlopen
import re
from apps.usuario.models import Usuario
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .utilities import si_tiene_url
# Create your views here.
from datetime import datetime
from iniciar import getDataWeb
def getDataofPage(user=str):
    '''Obtiene datos de la pagina y retorna array con estos'''
    full_url = "http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?" + user
    response = urlopen(full_url)
    data_cr = response.read().decode('utf-8')
    data_arr = data_cr.rsplit('\n\n')
    data = []
    for i in data_arr:
        data.append(i.rsplit("\n"))
    data.pop()
    return data
def formatterData(data):
    dataFormateada = {
        "data":[],
        "creditos":""
    }
    for i in data:
        now = datetime.now()
        if (len(i)>1):
            date = datetime.strptime(i['Vencimiento'], '%d-%m-%Y')
            dias_a_vencer = date-now
            name = i['Comentario'].split('**')
            dataFormateada['data'].append({
                'index':data.index(i),
                'usuario':i['Cuenta'],
                'vencimiento':date,
                'vencimiento_set':f'{"{}/{}/{}".format(date.day, date.month, date.year)}',
                'dias_a_vencer':int(dias_a_vencer.days),
                'nombre':name[0],
                'url':si_tiene_url(name)[1]
            })
     
    return dataFormateada

def filter(arr,param):
    res = []
    for i in arr:
        if(i['nombre'] == param):
            res.append(i)

    return res



@login_required(login_url='/usuario/login/')
def Index(request):
    
    if request.user.is_authenticated:
        #get data
        search = request.GET.get('buscar')
        data = getDataWeb()['tabla']
    
        #format data
        formattedData = formatterData(data)
        clientes = formattedData['data']
        ####rretiro
        
        if search:
            res = []
            for i in clientes:
                if re.findall(search,i['nombre'], re.IGNORECASE) or re.findall(search,i['usuario'], re.IGNORECASE):
                    res.append(i)
                
            clientes = res
        import operator
        clientes_ult = sorted(clientes, key=operator.itemgetter('vencimiento'))
        total_clientes = len(clientes)
        # print(clientes_ult)
        context = {
            "data":clientes,
            # "creditos": formattedData['creditos'],
            "total_clientes":total_clientes
        }
    return render(request,'index.html', context)

@login_required(login_url='/usuario/login/')
def Profile(request,id):
    
    data = getDataWeb()['tabla']
    ####      ####   ############ 
    #######   ####   ####     
    #### #### ####   ####
    ####   #######   ####
    ####      ####   ############ 
    formattedData = formatterData(data)
    clientes = formattedData['data']
    cliente = []
    for i in clientes:
        if int(i['index']) == id:
            cliente.append(i)
    url = cliente[0]['url'].split(":")
    context = {
        'cliente':cliente[0],
        'url': url[1]
    }
    usuario_cliente = cliente[0]['usuario']
   
    
    return render(request,'cliente/perfil.html', context)
    

###############BOTONES##############################
@login_required(login_url='/usuario/login/')


def Extender(request,usuario):
    import requests
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
    url = f"http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?M4t14sCh4c0&usr={usuario}&ext=1"
    payload = f"transfer=1&receptor=1&cuenta=ff{usuario}&orden=Vencimiento&cantidad=1&extend=&modusr=&modcom=&newusr=&newcom="
    response_3 = session.post(url, headers=headers, data=payload)
  
    print(usuario)
   
    
    return HttpResponse(f'<h1>Se agrego un mes a {usuario}</h1>')



@login_required(login_url='/usuario/login/')
def Crear(request):
    
    # fetch("http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php", {
    #         "headers": {
    #             "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #             "accept-language": "es-ES,es;q=0.9",
    #             "cache-control": "max-age=0",
    #             "content-type": "application/x-www-form-urlencoded",
    #             "upgrade-insecure-requests": "1"
    #         },
    #         "referrer": "http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php",
    #         "referrerPolicy": "strict-origin-when-cross-origin",
    #         "body": "transfer=1&receptor=1&cuenta=NUEVA&orden=Vencimiento&cantidad=1&modusr=&modcom=&newusr=n4hu3l&newcom=Nahuel+Caceres&newacc=",
    #         "method": "POST",
    #         "mode": "cors",
    #         "credentials": "include"
    #         });

    if request.method == "POST":
        nombre = request.POST.get('nombre')
        usuario = request.POST.get('usuario')
        
        # print(nombre, usuario)
        return HttpResponse(f'Nombre:{nombre}, usuario:{usuario}')
        # return render(request, 'cliente/crear.html')
    
    else:
        return render(request, 'cliente/crear.html')
    
@login_required(login_url='/usuario/login/')
def Modificar(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        usuario = request.POST.get('usuario')
        last_user = request.POST.get('last_user')
        
        # print(nombre, usuario, last_user)
        return redirect(f'http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?{request.user.first_name}&usr={last_user}&new={usuario}&com={nombre}')



###########################ACORTAR URL#################################################

def ShortUrl(url):
    import bitly_api
    Access_token = "499301b1ee741c2e69c40b020507bb3c43a7cb38"
    connection = bitly_api.Connection(access_token=Access_token)
    shorten_url = connection.shorten(url)
    return shorten_url

def Acortar(request,id):
    data = getDataofPage(request.user.first_name)
    ####      ####   ############ 
    #######   ####   ####     
    #### #### ####   ####
    ####   #######   ####
    ####      ####   ############ 
    formattedData = formatterData(data)
    clientes = formattedData['data']
    cliente = []
    for i in clientes:
        if int(i['index']) == id:
            cliente.append(i)
    usuario_cliente = cliente[0]['usuario']
    long_url = f"http://198.23.223.196/hSsfQeSmxkdW_mtv?{usuario_cliente}&v=10"
    # print(ShortUrl(long_url))
    url_short = ShortUrl(long_url)
    # print(url_short)
    context = {
        'cliente':cliente[0],
        'url_short': url_short

    }
    return render(request,'cliente/perfil.html', context)