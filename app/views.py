from django.shortcuts import render
from django.http import HttpResponse
from lxml import etree, html

import xmltodict
import requests
from BaseXClient import BaseXClient

NAMESPACES = {  'dc'        : 'https://purl.org/dc/elements/1.1/', 
                'itunes'    : 'https://www.itunes.com/dtds/podcast-1.0.dtd'}

# create basex session
session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

def getrss(url):
    tree = html.fromstring(requests.get(url).content)
    rss = tree.xpath('//link[@type="application/rss+xml"]/@href')
    return rss

# Create your views here.
def home(request):
    file = 'app/data/rss2.xml'
    tree = etree.parse(file)
    query = tree.xpath('./channel/item')
    query2 = tree.xpath('./channel')
    items = []
    
    for q in query2:
        feed_title, feed_link = q.find('title').text, q.find('link').text
    
    print(feed_title)
    print(feed_link)

    for c in query:
        desc = c.find('description').text.replace('<img src="', "")
        ind = desc.find('" />')
        
        date = c.find('pubDate').text
        img, desc = desc[:ind], desc[ind+4:]
        comments = c.find('comments').text
        creator = c.find('dc:creator', NAMESPACES).text
       
        items.append({  'feed_title'    : feed_title,
                        'feed_link'     : feed_link,                   
                        'title'         : c.find('title').text, 
                        'link'          : c.find('link').text, 
                        'description'   : desc, 
                        'image'         : img, 
                        'date'          : date,
                        'creator'       : creator,
                        'comments'      : comments
                    })

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





