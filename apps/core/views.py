from multiprocessing import context
import turtle
from django.shortcuts import render, redirect
from urllib.request import urlopen
import re
from apps.usuario.models import Usuario
from django.views.generic.base import RedirectView
# Create your views here.
from datetime import datetime

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
        ind = data.index(i)
        if (len(i)>1):
            date = datetime.strptime(i[1], '%d-%m-%Y')
            dias_a_vencer = date-now
            print(type(dias_a_vencer))
            name = i[2].split('**')
            dataFormateada['data'].append({
                'index': f'{ind}', 
                'usuario':f'{i[0]}',
                # 'vencimiento':f'{"{}/{}/{}".format(date.day, date.month, date.year)}',
                'vencimiento':date,
                'vencimiento_set':f'{"{}/{}/{}".format(date.day, date.month, date.year)}',
                'dias_a_vencer':f'{"{}".format(int(dias_a_vencer.days))}',
                'nombre':f'{name[0]}',
                'link':f'{name}'
            })
        else:
            dataFormateada['creditos'] = i[0]
        
    return dataFormateada

def filter(arr,param):
    res = []
    for i in arr:
        if(i['nombre'] == param):
            res.append(i)

    return res
def Index(request):
    if request.user.is_authenticated:
        #get data
        search = request.GET.get('buscar')
        data = getDataofPage(request.user.first_name)
        #format data
        formattedData = formatterData(data)
        clientes = formattedData['data']
        # if search:
        if search:
            res = []
            for i in clientes:
                if re.findall(search,i['nombre']):
                    res.append(i)
                
            clientes = res
        import operator
        clientes_ult = sorted(clientes, key=operator.itemgetter('vencimiento'))
        context = {
            "data":clientes_ult,
            "creditos": formattedData['creditos']
        }
    return render(request,'index.html', context)

def Profile(request,id):
    data = getDataofPage(request.user.first_name)
    #####
    formattedData = formatterData(data)
    clientes = formattedData['data']
    cliente = []
    for i in clientes:
        if int(i['index']) == id:
            cliente.append(i)
    context = {
        'cliente':cliente[0]
    }
    
    return render(request,'cliente/perfil.html', context)
    

###############BOTONES##############################
def Extender(request,usuario):
    # print(f"http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?{request.user.first_name}&usr={usuario}&ext=1")
    return redirect(f"http://198.23.223.196/hSsfQeSmxkdW_mtv/credit.php?{request.user.first_name}&usr={usuario}&ext=1")