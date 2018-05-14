from xml.dom import minidom


def get_xml_doc(filepath):
    return minidom.parse(filepath)


def get_elements_by_name(xmldoc, attribute):
    return xmldoc.getElementsByTagName(attribute)
