import requests

def si_tiene_url(arr):
    if len(arr) <=1:
        arr.append('Link para el cliente: NO TIENE URL')
        return arr
   
    return arr

