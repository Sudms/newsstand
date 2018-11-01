from django.shortcuts import render
from django.http import HttpResponse
from lxml import etree, html
import requests

# Create your views here.
def home(request):
    file = 'app/data/rss2.xml'
    tree = etree.parse(file)
    query = tree.xpath('./channel/item')
    items = []
    
    for c in query:
        desc = c.find('description').text.replace('<img src="', "")
        ind = desc.find('" />')
        
        date = c.find('pubDate').text
        img, desc = desc[:ind], desc[ind+4:]
       
        items.append({'title' : c.find('title').text, 'link' : c.find('link').text, 'description': desc, 'image' : img, 'date': date })
        print('SUSANA LINDA O QUE PROCURAS ESTÁ AQUI ->', img)
        tparams = {
            "items": list(items)
        }
    return render(request, 'index.html', tparams)      

def arquivo(request):
    return render(request,'archive.html',{})

def categoria(request):
    return render(request, 'category.html', {})

def post_gallery(request):
    return render(request, 'gallery-post.html', {})

def images(request):
    return render(request, 'image-post.html', {})

def std_post(request):
    return render(request, 'standar-post.html', {})





