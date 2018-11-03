from django.shortcuts import render
from django.http import HttpResponse
from lxml import etree, html

import xmltodict
import requests
from BaseXClient import BaseXClient

# Create your views here.
def home(request):
    if 'url' in request.GET:
        url = request.GET['url']
    else:
        url = 'https://engadget.com/rss.xml'

    r = requests.get(url, allow_redirects=True)
    open('app/data/rss.xml', 'w+').write(r.text)
    file = 'app/data/rss.xml'
    tree = etree.parse(file)
    namespaces = dict([node for _, node in etree.iterparse(file, events=['start-ns'])])

    query = tree.xpath('./channel/item')
    header = tree.xpath('./channel')
    items = []
    
    for q in header:
        feed_title, feed_link = q.find('title').text, q.find('link').text

    for c in query:
        desc = c.find('description').text.replace('<img src="', "")
        ind = desc.find('" />')
        img, desc = desc[:ind], desc[ind+4:]

        date = c.find('pubDate').text
        title = c.find('title').text
        link = c.find('link').text
        
        # if c.find('comments'):
        #     comments = c.find('comments').text
        
        creator = c.find('dc:creator', namespaces).text

        items.append({  'feed_title': feed_title,
                        'feed_link': feed_link,
                        'title': title,
                        'link': link,
                        'description': desc,
                        'image': img,
                        'date': date,
                        # 'comments'      : comments
                        'creator': creator,
                    })

    response = None
    # create basex session
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    # session.create("database.xml", "<xml> database </xml>")

    try:
        input = ''' 
                <root>{
                    for $c in doc("database")/feeds
                    return $c/source
                }</root> 
        '''
        query = session.query(input)
        response = query.execute()
        query.close()
    finally:
        if session:
            session.close()
            sources = list()

            # dres = xmltodict.parse(response)
            # lres = dres['root']['source']
            print (response, '\n')

            res_tree = etree.parse(response)
            
            res_query = res_tree.xpath('/root/source')
            
            for s in res_query:
                sources.append({'name' : s.find('name'), 'logo' : s.find('logo'), 'link' : s.find('link')})
    
    tparams = {
        "items"     : list(items),
        "sources"   : list(sources)
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

def about(request):
    return render(request, 'about.html', {})    




