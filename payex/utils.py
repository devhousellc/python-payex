from xml.etree import ElementTree

import datetime
import six
from decimal import Decimal


#####################
# String operations #
#####################


def normalize_value(val):
    """
    Normalize strings with booleans into Python types.
    """
    
    if val is not None:
        if val.lower() == 'false':
            val = False
        elif val.lower() == 'true':
            val = True
    
    return val


def normalize_dictionary_values(dictionary):
    """
    Normalizes the values in a dictionary recursivly.
    """
    
    for key, val in dictionary.items():
        if isinstance(val, dict):
            dictionary[key] = normalize_dictionary_values(val)
        elif isinstance(val, list):
            dictionary[key] = list(val)
        else:
            dictionary[key] = normalize_value(val)
    
    return dictionary


_PROTECTED_TYPES = six.integer_types + (
    type(None), float, Decimal, datetime.datetime, datetime.date, datetime.time
)


def is_protected_type(obj):
    """Determine if the object instance is of a protected type.

    Objects of protected types are preserved as-is when passed to
    force_text(strings_only=True).
    """
    return isinstance(obj, _PROTECTED_TYPES)


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    
    Source:
    django.utils.encoding.smart_str
    """
    if issubclass(type(s), six.text_type):
        return s
    if strings_only and is_protected_type(s):
        return s
    try:
        if not issubclass(type(s), six.string_types):
            if six.PY3:
                if isinstance(s, bytes):
                    s = six.text_type(s, encoding, errors)
                else:
                    s = six.text_type(s)
            elif hasattr(s, '__unicode__'):
                s = six.text_type(s)
            else:
                s = six.text_type(bytes(s), encoding, errors)
        else:
            # Note: We use .decode() here, instead of six.text_type(s, encoding,
            # errors), so that if s is a SafeBytes, it ends up being a
            # SafeText at the end.
            s = s.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(s, Exception):
            s = str(s)
        else:
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            s = ' '.join(smart_str(arg, encoding, strings_only, errors) for arg in s)
    return s


#####################
# XML to dictionary #
#####################


class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    """
    Converts XML to Python dictionaries.
    
    Source: 
    http://code.activestate.com/recipes/410469-xml-as-dictionary/
    
    Example usage:
    
    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)
    
    Or, if you want to use an XML string:
    
    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)
    """
    
    def __init__(self, parent_element):
        
        if parent_element.items():
            self.update(dict(parent_element.items()))
            
        for element in parent_element:
            if len(element) > 0:
                
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: XmlListConfig(element)}
                
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                
                self.update({element.tag: aDict})
            
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
                
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})
