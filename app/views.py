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

    rss_file = 'app/data/rss.xml'
    r = requests.get(url, allow_redirects=True)
    open(rss_file, 'w+').write(r.text)
    tree = etree.parse(rss_file)
    # namespaces = dict([node for _, node in etree.iterparse(rss_file, events=['start-ns'])])

    # schema_to_check = open('app/data/rss.xsd', 'r')
    # xml_to_check = open(rss_file, 'r')
    # xmlschema_doc = etree.parse(schema_to_check)
    # xmlschema = etree.XMLSchema(xmlschema_doc)
    
    # # # # # # # # # # # #  XSLT # # # # # # # # # # # # # # 
    # xslt_file = open('app/data/new.xsl', 'r')             #
    # xslt = etree.parse(xslt_file)                         # 
    # xslt = etree.XSLT(xslt)                               #
    # xhtml_file = open('new.html', 'wr+').write(str(xslt)) #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    # XML Schema (XSD)
    # try:
    #     tree = etree.parse(xml_to_check)
    #     print('XML well formed, syntax ok.')
    # except IOError:
    #     print('Invalid File')
    # except etree.XMLSyntaxError as err:
    #     print('XML Syntax Error, see error_syntax.log')
    #     with open('error_syntax.log', 'w') as error_log_file:
    #         error_log_file.write(str(err.error_log))
    #     quit()
    # except:
    #     print('Unknown error, exiting.')
    #     quit()

    # try:
    #     xmlschema.assertValid(tree)
    #     print('XML valid, schema validation ok.')
    # except etree.DocumentInvalid as err:
    #     print('Schema validation error, see error_schema.log')
    #     with open('error_schema.log', 'w') as error_log_file:
    #         error_log_file.write(str(err.error_log))
    #     quit()
    # except:
    #     print('Unknown error, exiting.')
    #     quit()

    namespaces = dict(
        [node for _, node in etree.iterparse(rss_file, events=['start-ns'])])

    if not tree.xpath('./channel/item'):
        query = tree.xpath('./channel/entry')
    else:
        query = tree.xpath('./channel/item')
    header = tree.xpath('./channel')
    items = []
    
    for q in header:
        feed_title, feed_link = q.find('title').text, q.find('link').text

    for c in query:
        if not 'media' in namespaces:
            desc = c.find('description').text.replace('<img src="', "")
            ind = desc.find('" />')
            img, desc = desc[:ind], desc[ind+4:]
        else:
            desc = c.find('description').text
            # img = c.find('media:thumbnail[@url]', namespaces).text

        date = c.find('pubDate').text
        title = c.find('title').text
        link = c.find('link').text
        
        if 'dc' in namespaces:
            creator = c.find('dc:creator', namespaces).text
        else:
            creator = c.find('author').text

        # if c.find('comments'):
        #     comments = c.find('comments').text

        items.append({  'feed_title': feed_title,
                        'feed_link': feed_link,
                        'title': title,
                        'link': link,
                        'description': desc,
                        'image': img,
                        'date': date,
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
            dres = xmltodict.parse(response)                    
            sources = list()
            for source in dres['root']['source']:
                sources.append(
                    {'name': source['name'], 'logo': source['logo'], 'link': source['link']})
    
    response = None

    try:
        input = ''' 
                <root>{
                    for $c in distinct-values(doc("database")/feeds/source/category)
                    order by $c
                    return $c 
                }</root> 
        '''

        query = session.query(input)
        response = query.execute()
        query.close()
    finally:
        if session:
            session.close()
            dres = xmltodict.parse(response)
            categories = response.replace("<root>", "").replace("</root>", "").split(" ")

    tparams = {
        "items"     : list(items),
        "sources"   : list(sources),
        "categories": list(categories)
    }

    return render(request, 'index.html', tparams)     

def insert(request):
    # create basex session
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    response = id = None
    name = logo = link = category = None

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
            dres = xmltodict.parse(response)
            sources = list()
            for source in dres['root']['source']:
                sources.append(
                    {'name': source['name'], 'logo': source['logo'], 'link': source['link']})

    response = None

    try:
        input = ''' 
                <root>{
                    for $c in distinct-values(doc("database")/feeds/source/category)
                    order by $c
                    return $c 
                }</root> 
        '''

        query = session.query(input)
        response = query.execute()
        query.close()
    finally:
        if session:
            dres = xmltodict.parse(response)
            categories = response.replace("<root>", "").replace("</root>", "").split(" ")

    response = None

    try:
        input = ''' for $c in doc('database')/feeds/source/id return $c '''
        query = session.query(input)
        response = query.execute()
        query.close()
    finally:
        if session:
            res = response.replace("<id>", "").replace("</id>", "").replace("\n", "")
            id = int(max(list(res)))

    response = None
       
    try:
        if 'name' in request.POST:
            name = request.POST.get("name")
            logo = request.POST.get("logo")
            link = request.POST.get("link")
            category = request.POST.get("category")

            input = ''' insert nodes <source><id>{}</id> <name>{}</name> <logo>{}</logo> <link>{}</link> <category>{}</category></source> into doc('database')/feeds '''.format(id+1, name, logo, link, category)
            query = session.query(input)
            response = query.execute()
            query.close()
    finally:
        if session:
            session.close()
            print(response)

    tpararms = {
        "sources": list(sources),
        "categories": list(categories)
    }
    
    return render(request, 'insert.html', tpararms)

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




