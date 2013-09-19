#!/usr/bin/env python
"""Script to autogen a class for input parsing from an XML file"""
import sys
from xml.sax import make_parser

from xml_setup.gen_from_base_xml import NodeHandler

# """This tool now uses the base_xml as the base class to get the flatten capability
#     as long as new nodes added are also added to the 'children' data structure.
#
# """

def generate_class(target_name):
    """Make a "handler" class from an XML file for the wedge framework"""
    saxparser = make_parser()
    saxparser.setContentHandler(NodeHandler(target_name[:-4]+'.py'))
    saxparser.parse(target_name)

generate_class('current_user.xml')