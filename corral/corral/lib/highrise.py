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
        self._defaultContact = {'name':"Support 4WindsRE", "email":"supportre@4windsre.com"}
        self._connection()
        
       

       
    def _connection(self):
        password = 'X'
        passmanager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passmanager.add_password(None, self._url, self._privateToken, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passmanager)
        self.opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(self.opener)

    def _getKasesList(self):
        return self._kases
    
    def _getDefaultContact(self):
        return self._defaultContact

    def createKasesList(self):
        kasesList = []
        contactList = []
        page = urllib2.urlopen("%s/kases.xml" % self._url).read()
        root = ET.fromstring(page)

        for kase in root.findall('kase'):
            
		    if kase.find('name').text is not None :
                        contactList = []
                        for parties in kase.findall('parties'):
                            for party in parties.findall('party'):
                                emailaddress = ""
                                name = "%s %s" % (party.find('first-name').text, party.find('last-name').text)
                                emailaddresses = "supportre@4windsre.com"
                                for emailaddress in party.find('contact-data').find('email-addresses').findall('email-address'):
                                    emailaddress = "%s, %s" % (emailaddresses,emailaddress.find('address').text )
                            
                                contactList.append({'name':name, 'email': emailaddress})
                            
                        kasesList.append({kase.find('name').text : {'status': kase.find('background').text, 'contact': contactList}})

	return kasesList
    
    def createContactDict(self):
        urllib2.install_opener(self.opener)
        page = urllib2.urlopen("%s/people.xml" % self._url).read()
        root = ET.fromstring(page)

        contactDict = {}
        for person in root.findall('person'):
                name = "%s %s" % ( person.find('first-name').text, person.find('last-name').text)
                contactDict[person.find('id').text] = name

        return contactDict    
    


    def createKase(self, kaseName):
        xmlTemplate = KasesController()._getKaseTemplate()
        #kaseName = kaseName.split("|")[0]
        print kaseName
        data = {'name': str(kaseName)}
        xml_string = xmlTemplate%data
        print xml_string
        url = "%s/kases.xml" % self._url
        self._kases = self.createKasesList()
        new_entry = 0
        
        
        for x in self._kases:
            if (x != "None" and x.keys()[0] == str(kaseName)):
                new_entry =1
                break
       
        
       	if new_entry == 0:
    	        try:
            	    req = urllib2.Request(url=url,
                    	      data=xml_string,
                                  headers={'Content-Type': 'application/xml'})
    	            urllib2.urlopen(req)
                    return {kaseName:{'status':"for sale","contact": [{'name':"Support 4WindsRE", "email":"supportre@4windsre.com"}]}}
    
            	except:
            	    return {str(kaseName):{'status':"unknown","contact": [{'name':"Support 4WindsRE", "email":"supportre@4windsre.com"}]}}
        else:
            #try:
            print x
            return {str(kaseName):{'status':x[str(kaseName)]["status"], "contact": x[kaseName]["contact"]}}
            #except:
            #    return {str(kaseName):{'status':"unknown","contact": [{'name':"Support 4WindsRE", "email":"supportre@4windsre.com"}]}}
    
      
    
    
    
    



   
