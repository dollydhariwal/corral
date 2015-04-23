# -*- coding: utf-8 -*-
"""locate address controller."""

from corral.lib.base import BaseController
import tw2.forms as forms
from tg import redirect, require, flash, url
import requests
import urllib2
import xlrd
import os
import datetime 
import xml.etree.ElementTree as ET
import cPickle as pickle
import plotly.plotly as py
from plotly.graph_objs import *

#from DNS.Type import NULL





__all__ = ['ViewController']


class ViewController(BaseController):
    """
    The View Address hits Controller for the corral Application
    """
    def __init__(self,privateToken=None):
        """Stores information about the server
        url : the URL of the zillow server
        private_token: the user private token
        email: the user email/login
        password: the user password (associated with email)
        location: location of excel sheet
        """
        self._url = 'http://www.zillow.com/webservice'
        self._privateToken = 'X1-ZWz1azdtprntor_8xo7s'
        self.input_location = "/home/vipul/corral/corral/exceldata"
        self.output_location = "/home/vipul/corral/corral/excelresults"
        self.image_location = "/home/vipul/corral/corral/corral/public/resultimages"
        py.sign_in('ddhariwal','9nnxcdskrt')
        self.final_dict = {}
        self.flag_for_change = {}
        
        for filename in os.listdir(self.input_location):
            self.flag_for_change[filename] = 0
        
        self._connection()
        
        
    def _connection(self):
        password = 'X'
        passmanager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passmanager.add_password(None, self._url, self._privateToken, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passmanager)
        self.opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(self.opener)

    def getPropertyId(self, address=None, zipcode=None):
        #deep_search_response = self.zillow_data.get_deep_search_results(address, zipcode) 
        #result = GetDeepSearchResults(deep_search_response)
        page = urllib2.urlopen("%s/GetDeepSearchResults.htm?zws-id=%s&address=%s&citystatezip=%s" % (self._url,self._privateToken,address.replace(" ", "+"), zipcode)).read()
        root = ET.fromstring(page)
        property_id = 'None'
        
        for view in root.iter('result'):
            property_id = view.find('zpid').text 
            
        return property_id
       
    def findHits(self, address=None, zipcode=None):
        zpid = self.getPropertyId(address=address, zipcode=zipcode)
        page = urllib2.urlopen("%s/GetUpdatedPropertyDetails.htm?zws-id=%s&zpid=%s" % (self._url,self._privateToken,zpid)).read()
        root = ET.fromstring(page)
        num_hits = 'None'
        
        for view in root.iter('pageViewCount'):
            num_hits = view.find('total').text 
        return num_hits 
    
 
    def readExcelInput(self):
        address_dict = {}
        today_date = datetime.date.today()
        date_array = str(today_date).split("-")
        
        for filename in os.listdir(self.input_location):
            workbook = xlrd.open_workbook("%s/%s" % (self.input_location, filename))
            sheet = workbook.sheet_by_index(0)
            
            try:
                os.mkdir("%s/%s" %(self.output_location,filename.replace(".xlsx","")))
            
            except:
                pass
            
             
            for row in range(sheet.nrows):
                address_file = '%s/%s/address%s.pkl' % (self.output_location, filename.replace(".xlsx",""), row)
                self.flag_for_change[filename] = 0
                
                if not os.path.exists(address_file):
                    address_dict['id']=os.path.basename(address_file).replace("address", "").replace(".pkl", "")
                    for col in range(sheet.ncols):
                        if (row != 0):
                            address_dict[sheet.cell_value(0,col)] = sheet.cell_value(row,col)
                               
                    if (row != 0):
                        try: 
                            address_dict[date_array[0]] = {date_array[1]:{date_array[2]:self.findHits(address="%s %s %s" % (address_dict['Property Address'], address_dict['City'], address_dict['State'] ), zipcode=address_dict['Zip'])}}
                        except:
                            address_dict[date_array[0]] = {date_array[1]:{date_array[2]: 'unknown'}}
                            
                        output = open(address_file, 'wb')
                        pickle.dump(address_dict, output)
                        output.close()
                        address_dict = {}
                    self.flag_for_change[filename] += 1
                    
                else:
                    output = open(address_file, 'rb')
                    address_dict = pickle.load(output)
                    output.close()
                    
                            
                    if (date_array[0] not in address_dict):
                            address_dict[date_array[0]] = {date_array[1] : {date_array[2] : self.findHits(address="%s %s %s" % (address_dict['Property Address'], address_dict['City'], address_dict['State'] ), zipcode=address_dict['Zip'])}}
                            self.flag_for_change[filename] += 1
                    
                    elif (date_array[1] not in address_dict[date_array[0]]):
                            address_dict[date_array[0]][date_array[1]] = { date_array[2]: self.findHits(address="%s %s %s" % (address_dict['Property Address'], address_dict['City'], address_dict['State'] ), zipcode=address_dict['Zip'])}
                            self.flag_for_change[filename] += 1
                            
                    elif (date_array[2] not in address_dict[date_array[0]][date_array[1]]):
                            address_dict[date_array[0]][date_array[1]][date_array[2]] = self.findHits(address="%s %s %s" % (address_dict['Property Address'], address_dict['City'], address_dict['State'] ), zipcode=address_dict['Zip'])
                            self.flag_for_change[filename] += 1
    
                    
                    if self.flag_for_change[filename] != 0:            
                        output = open(address_file, 'wb')
                        pickle.dump(address_dict, output)
                        output.close()
                    
                        x = []
                        y = []
                    
                        
                        for month in address_dict[date_array[0]].keys():
                            for date in sorted(address_dict[date_array[0]][month].keys()):
                                x.append(datetime.datetime(year=int(date_array[0]), month=int(month), day=int(date)))
                                y.append(address_dict[date_array[0]][month][date])
                        
                        data = Data([
                                     Scatter(
                                             x=x,
                                             y=y
                                             )
                                     ])           
                #py.plot(data, filename='%s/%s.png' % (self.image_location, address_file))
                
                        try:
                            py.image.save_as({'data': data}, '%s/%s.png' % (self.image_location, os.path.basename(address_file)))
                        #py.plot(data, filename="test")
                        except:
                            pass
                
                        x = []
                        y = []
                    
                address_dict = {}
                
                    
        return None
    
    
        
    def readAddressesDict(self):
        self.return_dict = {}
        
        for xlfilename in os.listdir(self.input_location):
            pklFilename = open("%s/%s" %(self.output_location,xlfilename.replace(".xlsx", ".data")), 'a')
            filename = "%s/%s" % (self.output_location, xlfilename.replace(".xlsx", ""))
            
            # If some data has changed in the address files the self.flag_for_change[xlfilename] is set to 1
            # and the.data file nees to repopulated else not
            
            if self.flag_for_change[xlfilename] != 0:
                self.final_dict[os.path.basename(filename)] = {}
                for address_file in os.listdir(filename):
                    pkl_file = open('%s/%s' % (filename,address_file), 'rb')
                    #final_dict[filename][address_file] = {'a':1,'b':2}
                    self.final_dict[os.path.basename(filename)][address_file] = pickle.load(pkl_file)
                    pkl_file.close()
                
                pickle.dump(self.final_dict, pklFilename )
                
            pklFilename.close()
            
            
            pklFilename = open("%s/%s" %(self.output_location,xlfilename.replace(".xlsx", ".data")), 'rb')
            self.return_dict = pickle.load(pklFilename)
            
            pklFilename.close()
                
        return self.return_dict
                
        
            
                
            
        
    
    
        
    
    
    