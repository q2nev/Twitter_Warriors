from xml.dom.minidom import parseString
from xml.etree.ElementTree import ElementTree,dump

# tree = ElementTree()
# tree.parse('file.xml')
# for item in items:
#


XML = 'current_user.xml'

def replace_value(node,newText):
    if node.firstChild.nodeType != node.TEXT_NODE:
        raise Exception("node does not contain text")
    node.firstChild.replaceWholeText(newText)

def main(item,newItem):
    doc = parseString(XML)

    node = doc.getElementsByTagName(str(item))[0]
    replace_value(node, str(newItem))

    print doc.toxml()

main(SavedAts)