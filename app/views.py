from django.shortcuts import render
from django.http import HttpResponse
from lxml import etree, html
import requests

# Create your views here.
def newslist(request):
    file = 'app/data/rss.xml'
    tree = etree.parse(file)
    query = tree.xpath('./channel/item')
    items = []
    
    for c in query:
        desc = c.find('description').text.replace('<img ', "<img class='fit' ")
        ind = desc.find(" />")
        print('ind: ',ind)
        img, desc = desc[:ind+3], '<p>' + desc[ind+3:] + '</p>'
        print('img: ', img)
        print('desc:', desc)
        items.append({'title' : c.find('title').text, 'link' : c.find('link').text, 'description': desc, 'image' : img })
        
        tparams = {
            "items": list(items)
        }
    return render(request, 'new.html', tparams)      
