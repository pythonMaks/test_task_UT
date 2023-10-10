from django.shortcuts import render

def menu_view(request, path=''):
    return render(request, 'main_template.html', {'path': path})
