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
from corral.controllers.project import ProjectController
from corral.lib.highrise import HighriseController
#from DNS.Type import NULL





__all__ = ['ManageController']


class ManageController(BaseController):
    """
    The Manage Controller for the corral Application
    """
    def __init__(self,project=None):
        self._url = "https://organization223.highrisehq.com"
        self._token = "77427d6a0fae05a6bd5a34df27221ab1"
        
    
    def createKase(self, kaseName):    
        highriseObj = HighriseController(self._url, self._token)
        result = highriseObj.createKase(kaseName)
        return result  
  
class statusForm(forms.SubmitButton):
        #class child(forms.TableForm):
        type = "submit"
        value = "Highrise Status"
        
        
class emailForm(forms.SubmitButton):
        #class child(forms.TableForm):
        type = "submit"
        value = "email"                    
                
        
            
                
            
        
    
    
        
    
    
    
