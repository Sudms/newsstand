import os
import socket
import logging
import requests
from lxml import etree, html

feeds = []

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='aux.log',
                    level=logging.DEBUG)

def check_internet_connectivity(host='8.8.8.8', port=53, timeout=3):
    logging.info('Checking internet connectivity...')
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        logging.info('Connected.')
        return True
    except Exception:
        logging.info('You don\'t have internet connection.')

def load_RSS(url):
    r = requests.get(url, allow_redirects=True)
    open('rss2.xml', 'w+').write(r.text)

def get_RSS(url):
    tree = html.fromstring(requests.get(url).content)
    rss = tree.xpath('//link[@type="application/rss+xml"]/@href')
    if not rss:
        logging.info('We cannot found rss feed from ' + url)
        return
    else:
        logging.info('We find a rss feed at... ' + str(rss))
        return rss

def validate_schema(filename_xsd, filename_xml):
    schema_to_check = open(filename_xsd, 'r')
    xml_to_check = open(filename_xml, 'r')
    xmlschema_doc = etree.parse(schema_to_check)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    try:
        doc = etree.parse(xml_to_check)
        logging.info('XML well formed, syntax ok.')
    except IOError:
        logging.exception('Invalid File')
    except etree.XMLSyntaxError as err:
        logging.exception('XML Syntax Error, see error_syntax.log')
        with open('error_syntax.log', 'w') as error_log_file:
            error_log_file.write(str(err.error_log))
        quit()
    except:
        logging.exception('Unknown error, exiting.')
        quit()

    try:
        xmlschema.assertValid(doc)
        logging.info('XML valid, schema validation ok.')
    except etree.DocumentInvalid as err:
        logging.exception('Schema validation error, see error_schema.log')
        with open('error_schema.log', 'w') as error_log_file:
            error_log_file.write(str(err.error_log))
        quit()
    except:
        logging.exception('Unknown error, exiting.')
        quit()

def main():
    # check_internet_connectivity()
    load_RSS('http://www.engadget.com/rss.xml')
    # validate_schema('test.xsd', 'test.xml')
    # print(get_RSS('https://www.engadget.com/'))


if __name__ == '__main__':
    main()
