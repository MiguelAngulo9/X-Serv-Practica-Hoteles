#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import urllib2
import sys
import os.path

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.diccionario = {}
        self.lista = []
        self.diccionario['url'] =[]
        self.cont = 1
        self.myattr =""


    def startElement (self, name, attrs):
        if name == 'name':
            self.inItem = True
            self.inContent = True
        elif name == 'address':
            self.inItem = True
            self.inContent = True
        elif name == 'phone':
            self.inItem = True
            self.inContent = True
        elif name == "web":
            self.inItem = True
            self.inContent = True
        elif name == "body":
            self.inItem = True
            self.inContent = True
        elif name == "url" :
            self.inItem = True
            self.inContent = True
        elif name == "item" and attrs["name"]== "Categoria":
            self.myattr ="Categoria"
            self.inItem = True
            self.inContent = True
        elif name == "item" and attrs["name"]== "SubCategoria":
            self.myattr ="SubCategoria"
            self.inItem = True
            self.inContent = True

    def endElement (self, name):
        if name == "name":
            self.diccionario[name] = self.theContent
            self.inItem = False
            self.inContent = False
        if name == 'address':
            self.diccionario[name] = self.theContent
            self.inItem = False
            self.inContent = False
        elif name == 'phone':
            self.diccionario[name] = self.theContent
            self.inItem = False
            self.inContent = False
        elif name == "web":
            self.diccionario[name] = self.theContent
            self.inItem = False
            self.inContent = False
        elif name == "body":
            self.diccionario[name] = self.theContent
            self.inItem = False
            self.inContent = False
        elif name == "item" and self.theContent:
            if self.myattr == "Categoria":
                self.diccionario["cat"] = self.theContent
                self.myattr =""
            elif self.myattr == "SubCategoria":
                self.diccionario["subcat"] = self.theContent
                self.myattr =""
            self.inItem = False
            self.inContent = False
        elif name == "url":
            if len(self.diccionario['url'])<6:
                self.diccionario['url'].append(self.theContent)
        elif name == 'service':
            self.lista.append(self.diccionario)
            self.diccionario = {}
            self.diccionario['url'] =[]

        self.inContent = False
        self.theContent = ""

    def characters (self, content):
        if self.inContent:
            self.theContent = content

    def lista_hoteles(self):
        return self.lista
