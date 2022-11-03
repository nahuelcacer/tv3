from django.shortcuts import redirect
def Index(request):
    if request.user.is_authenticated:
        return redirect('apps.core:index')
    else:
        return redirect('apps.usuario:login')