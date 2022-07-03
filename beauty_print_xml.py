from bs4 import BeautifulSoup
from lxml import etree
import re

def get_value_from_param(text, param ):
    regex = '{0}="(.*?)"'.format(param)

    res = re.findall(regex, text)[0]
    # res = res.replace(param+"=","")
    # res = res.replace('"',"")

    return res


def escape_cdata(text):
    if "&lt;" in text:
        text = text.replace( "&lt;","<")
    if "&gt;" in text:
        text = text.replace( "&gt;",">")
    if "&amp;" in text:
        text = text.replace( "&amp;", "&")
    if "&quot;" in text:
        text = text.replace( "&quot;", '"')
    return text

def beauty_print_xml(content):
    # bs = BeautifulSoup(content, 'xml')
    # pretty_xml = bs.prettify()
    # result = escape_cdata(pretty_xml)
    x = etree.fromstring(content)
    pretty_xml = etree.tostring(x, pretty_print=True, encoding=str)
    result = escape_cdata(pretty_xml)
    return result