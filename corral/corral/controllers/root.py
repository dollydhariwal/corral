# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound

from corral.lib.base import BaseController
from corral.controllers.error import ErrorController
from corral.controllers.locateAddresses import AddressController, SelectAddressesForm
from corral.controllers.getComps import CompController, CompAddressForm
from corral.controllers.getViews import ViewController
from corral.controllers.project import ProjectController
from corral.controllers.postAds import PostAdsController, selectProps, postForm
from corral.controllers.trackProps import TrackPropsController, trackPropsForm
from corral.controllers.salesProject import postAdForm,trackPropsForm
from corral.controllers.manageLeads import manageForm
from corral.controllers.manage import ManageController, statusForm, emailForm
from corral.controllers.plot import PlotController
from corral.controllers.post import PostController

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the corral application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """

    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "corral"

    @expose('corral.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('corral.templates.getComps')
    def getComps(self, **kw):
        """Handle the getComps-page."""
        if kw:
            kw['result'] = CompController().findComps(address=kw['address'],zipcode=kw['zipcode'])
         
        return dict(page='getComps', kw=kw, form=CompAddressForm)
        
    @expose('corral.templates.getViews')
    def getViews(self, **kw):
        """Handle the getViews-page."""
        view = ViewController()
        view.readExcelInput()
        kw = view.readAddressesDict()
        
        return dict(page='getViews', kw=kw)
    
    @expose('corral.templates.salesProject')
    def salesProject(self, **kw):
        """Handle the sales project-page."""
        if kw:
            return dict(page='postAds', kw=kw )
        else:
            project = ProjectController()
            projectList = project.listProjects()
        
            return dict(page='salesProject', kw=None, projectList=projectList, postAdform=postAdForm, trackPropsform=trackPropsForm )
        
    @expose('corral.templates.manageLeads')
    def manageLeads(self, **kw):
        """Handle the sales project-page."""
        if kw:
            return dict(page='manage', kw=kw )
        else:
            project = ProjectController()
            projectList = project.listProjects()
        
            return dict(page='manageLeads', kw=None, projectList=projectList, manageform=manageForm )
        
    @expose('corral.templates.postAds')
    def postAds(self, **kw):
        """Handle the posting of Ads."""
        
        for key in kw.keys():
            project = key
            kw = PostAdsController(key).readProject()
            
                    
        return dict(page='postAds', kw=kw, project=project, selectProps=selectProps, postForm=postForm)
    
    
    @expose('corral.templates.manage')
    def manage(self, **kw):
        """Handle the posting of Ads."""
        
        for key in kw.keys():
            project = key
            kw = PostAdsController(key).readProject()
            
        projectName = project.replace(".xlsx","") 
        
        for key,value in kw[projectName].items():
            addressString =  "%s %s %s | price: %s" % (kw[projectName][key]['Property Address'], kw[projectName][key]['State'], kw[projectName][key]['Zip'], kw[projectName][key]['Turnkey/Sales Price'])
            result = ManageController().createKase(addressString)
        
        return dict(page='manage', kw=kw, project=project, statusform=statusForm, emailform=emailForm)
    
    
    @expose('corral.templates.trackProps')
    def trackProps(self, **kw):
        """Handle the tracking of the props."""
        
        for key in kw.keys():
            project = key
            kw = TrackPropsController(key).readProject()
        
        projectName =project.replace(".xlsx", "")   
        return dict(page='trackProps', kw=kw, project=project, projectName=projectName, trackPropsForm=trackPropsForm)
    
    
    @expose('corral.templates.plot')
    def plot(self, **kw):
        """Handle the plotting of the graph."""
        prop_dict = {}
        
        plotObj = PlotController()
        prop_dict = plotObj.plotGraph(kw['project'], list(kw['property']))
        
        projectName =  kw['project'].replace(".xlsx", "")  
        return dict(page='plot/unique', kw=kw, projectName=projectName, prop_dict=prop_dict)
    
    @expose('corral.templates.post')
    def post(self, **kw):
        """Handle the posting of Ads."""
        postObj = PostController()
        postObj.createXML(kw['project'], list(kw['property']))
        
        return None
              
    @expose('corral.templates.locateAddresses')
    def locateAddresses(self):
        """Handle the 'localteAddresses' page."""
        return dict(page='locateAddresses')
    
    @expose()
    def locate(self,**kw):
        return AddressController().locate(**kw)
    
    @expose('corral.public.graphs')
    def graphs(self):
        return None
    
    @expose('corral.public.xmlfiles')
    def xmlfiles(self):
        return None
    
    @expose('corral.public.photos')
    def photos(self):
        return None
    

    
