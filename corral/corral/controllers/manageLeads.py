# -*- coding: utf-8 -*-
"""locate address controller."""

from corral.lib.base import BaseController
import tw2.forms as forms
from tg import redirect, require, flash, url
import requests
import urllib2
import xml.etree.ElementTree as ET





__all__ = ['ManageLeadsController']


class ManageLeadsController(BaseController):
    """
    The Manage Leads Controller for the corral Application
    """
    def __init__(self,privateToken=None):
        pass
    
    
    
class manageForm(forms.SubmitButton):
    type = "submit"
    value = "Manage"
    
        
    