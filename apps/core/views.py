from multiprocessing import context
from django.shortcuts import render, redirect
from urllib.request import urlopen
import re
from apps.usuario.models import Usuario
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
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
            # print(type(dias_a_vencer))
            # name = i[2].split('**')
            dataFormateada['data'].append({
                'index':data.index(i),
                'usuario':i['Cuenta'],
                # 'vencimiento':f'{"{}/{}/{}".format(date.day, date.month, date.year)}',
                'vencimiento':date,
                'vencimiento_set':f'{"{}/{}/{}".format(date.day, date.month, date.year)}',
                'dias_a_vencer':f'{"{}".format(int(dias_a_vencer.days))}',
                # 'nombre':f'{name[0]}',
                # 'link':f'{name}'
            })
            print(dataFormateada)
        
            # dataFormateada['creditos'] = i[0]
        
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
        print(data) 
        #format data
        formattedData = formatterData(data)
        clientes = formattedData['data']
        ####rretiro
        # if search:
        #     res = []
        #     for i in clientes:
        #         if re.findall(search,i['nombre']):
        #             res.append(i)
                
        #     clientes = res
        # import operator
        # clientes_ult = sorted(clientes, key=operator.itemgetter('vencimiento'))
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
    print(id)
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
    context = {
        'cliente':cliente[0]
    }
    usuario_cliente = cliente[0]['usuario']
    long_url = f"http://198.23.223.196/hSsfQeSmxkdW_mtv?{usuario_cliente}&v=10"
    # print(ShortUrl(long_url))
    
    return render(request,'cliente/perfil.html', context)
    

###############BOTONES##############################
@login_required(login_url='/usuario/login/')
def Extender(request,usuario):
    # print(f"http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?{request.user.first_name}&usr={usuario}&ext=1")
    return redirect(f"http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?{request.user.first_name}&usr={usuario}&ext=1")



@login_required(login_url='/usuario/login/')
def Crear(request):
    
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        usuario = request.POST.get('usuario')
        
        # print(nombre, usuario)
        return redirect(f'http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?{request.user.first_name}&usr={usuario}&com={nombre}')
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