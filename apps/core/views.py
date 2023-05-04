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
from .decorators import login_ott_decorator

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
        data = getDataWeb()
        
        #format data
        formattedData = formatterData(data['tabla'])
        clientes = formattedData['data']
        ####rretiro
        
        total_clientes = len(clientes)
        if search:
            res = []
            for i in clientes:
                if re.findall(search,i['nombre'], re.IGNORECASE) or re.findall(search,i['usuario'], re.IGNORECASE):
                    res.append(i)
                
            clientes = res
        import operator
        clientes_ult = sorted(clientes, key=operator.itemgetter('vencimiento'))
        # print(clientes_ult)
        context = { 
            "creditos":data['creditos'],
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
   
    
    return render(request,'cliente/perfil.html', context)
    

###############BOTONES##############################
@login_required(login_url='/usuario/login/')
@login_ott_decorator
def Extender(request,usuario,session,headers,response_2):
   
    url = f"http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?M4t14sCh4c0&usr={usuario}&ext=1"
    payload = f"transfer=1&receptor=1&cuenta={usuario}&orden=Vencimiento&cantidad=1&extend=&modusr=&modcom=&newusr=&newcom="
    response_3 = session.post(url, headers=headers, data=payload)
  
    
    response_html = f'<h1>Se agregó un mes a {usuario}</h1>'
    response_html += '<button onclick="window.location.href=\'/\'">Volver</button>'

    
    return HttpResponse(response_html)



@login_required(login_url='/usuario/login/')

@login_ott_decorator
def Crear(request,session,headers,response_2):

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
        setNombre = nombre.split(' ')
        fNombre = "+".join(setNombre)

        payload = f"transfer=1&receptor=1&cuenta=NUEVA&orden=Vencimiento&cantidad=1&modusr=&modcom=&newusr={usuario}&newcom={fNombre}&newacc="
        url = "http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?M4t14sCh4c0"
        response_3 = session.post(url, headers=headers, data=payload)

        response_html = f'<h1>Cliente creado, usuario:{usuario}, nombre:{nombre}</h1>'
        response_html += '<button onclick="window.location.href=\'/\'">Volver</button>'

        return HttpResponse(response_html)
    
    else:
        return render(request, 'cliente/crear.html')
    
@login_required(login_url='/usuario/login/')
@login_ott_decorator
def Modificar(request,session,headers,response_2):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        usuario = request.POST.get('usuario')
        last_user = request.POST.get('last_user')
        last_name = request.POST.get('last_name')



        payload = f"transfer=&receptor=&cuenta={last_user}&orden=Vencimiento&cantidad=1&modusr={usuario}&modcom={nombre}&modif=&newusr=&newcom="
        url = "http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?M4t14sCh4c0"
        response_3 = session.post(url, headers=headers, data=payload)
        response_html = f'<h1>Usuario Modificado</h1>'
        response_html += f'<div>nombre: {last_name}, usuario: {last_user} </div>'
        response_html += f'<h1>Usuario Nuevo</h1>'
        response_html += f'<div>nombre: {nombre}, usuario: {usuario} </div>'
        response_html += '<button class="btn btn-primary" onclick="window.location.href=\'/\'">Volver</button>'

        return HttpResponse(response_html)
    


@login_required(login_url='/usuario/login/')
@login_ott_decorator
def Delete(request,usuario,session,headers,response_2):
    # import requests
    # session = requests.Session()

    # # Enviar el nombre de usuario
    # login_url = 'http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php'
    # headers = {
    #     'Content-Type': 'application/x-www-form-urlencoded',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    # }
    # username = {'usr': 'M4t14sCh4c0', 'next': ''}
    # response_1 = session.post(login_url, headers=headers, data=username)

    # # Enviar la contraseña
    # password = {'pass': 'mati', 'envPass': ''}
    # response_2 = session.post(login_url, headers=headers, data=password)
    
    
    # headers['cookie'] = response_1.headers.get('Set-Cookie')
    url = f"http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?M4t14sCh4c0&usr"
    payload = f"transfer=&receptor=&cuenta={usuario}&orden=Vencimiento&delete={usuario}&cantidad=1&modusr=&modcom=&newusr=&newcom="
    session.post(url, headers=headers, data=payload)
    print(usuario)
    response_html = f'<h1>Se elimino el usuario {usuario}</h1>'
    response_html += '<button onclick="window.location.href=\'/\'">Volver</button>'
    return HttpResponse(response_html)
