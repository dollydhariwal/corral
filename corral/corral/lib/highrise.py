# -*- coding: utf-8 -*-

"""The dropbox  Controller API."""
from corral.lib.base import BaseController
from corral.lib.templates import NoteController, TaskController, PeopleController, KasesController
from tg import TGController, tmpl_context
from tg.render import render
from tg.i18n import ugettext as _, ungettext
import os, glob, time, commands
import requests
import urllib2
import xml.etree.ElementTree as ET

__all__ = ['HighriseController']


class HighriseController(BaseController):
    """Represents a Highrise server connection"""
    def __init__(self,url,privateToken=None):
        """Stores information about the server   
        url : the URL of the highrise server
        private_token: the user private token
        email: the user email/login
        password: the user password (associated with email)
        """   
        self._url = '%s' % url
        self._privateToken = privateToken
        self._printFlag = True
        self._connection()
       

       
    def _connection(self):
        password = 'X'
        passmanager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passmanager.add_password(None, self._url, self._privateToken, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passmanager)
        self.opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(self.opener)



    def createKase(self, kaseName):
        xmlTemplate = KasesController()._getKaseTemplate()
        #kaseName = kaseName.split("|")[0]
        print kaseName
        data = {'name': str(kaseName)}
        xml_string = xmlTemplate%data
        print xml_string
        url = "%s/kases.xml" % self._url
        try:
                req = urllib2.Request(url=url,
                              data=xml_string,
                              headers={'Content-Type': 'application/xml'})
                urllib2.urlopen(req)

                result = True
        except:
            result = False

        return result



   