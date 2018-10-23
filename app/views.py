from django.shortcuts import render
from django.http import HttpResponse
from lxml import etree 
import xmltodict

# Create your views here.
def newslist(request):
    
    file = 'app/data/test2.xml'
    tree = etree.parse(file)
        
    new = tree.xpath('.//title/text()')
    print(new)

    tparams = {
        "TITULO " : new
    }

    return render(request, 'new.html', tparams)      
