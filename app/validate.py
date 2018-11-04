import os
import logging
import requests
from lxml import etree

class Validate:
    def validate_schema(self, filename_xsd, filename_xml):
        schema_to_check = open(filename_xsd, 'r')
        xml_to_check = open(filename_xml, 'r')
        
        xmlschema_doc = etree.parse(schema_to_check)
        xmlschema = etree.XMLSchema(xmlschema_doc)

        try:
            doc = etree.parse(xml_to_check)
            logging.info('XML well formed, syntax ok.')
            return True
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
            return True
        except etree.DocumentInvalid as err:
            logging.exception('Schema validation error, see error_schema.log')
            with open('error_schema.log', 'w') as error_log_file:
                error_log_file.write(str(err.error_log))
            quit()
        except:
            logging.exception('Unknown error, exiting.')
            quit()
        return False