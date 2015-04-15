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
from corral.controllers.salesProject import postAdForm,trackPropsForm

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
            return dict(page='salesProject', kw=kw, projectList=None, postAdform=postAdForm, trackPropsform=trackPropsForm )
        else:
            project = ProjectController()
            projectList = project.listProjects()
        
            return dict(page='salesProject', kw=None, projectList=projectList, postAdform=postAdForm, trackPropsform=trackPropsForm )
        
    @expose('corral.templates.postAds')
    def postAds(self, **kw):
        """Handle the posting of Ads."""
        if kw:
            return dict(page='postAds', kw=kw, projectList=None, postAdform=postAdForm, trackPropsform=trackPropsForm )
        else:
            project = ProjectController()
            projectList = project.listProjects()
        
            return dict(page='postAds', kw=None, projectList=projectList, postAdform=postAdForm, trackPropsform=trackPropsForm )
       
    @expose('corral.templates.locateAddresses')
    def locateAddresses(self):
        """Handle the 'localteAddresses' page."""
        return dict(page='locateAddresses')
    
    @expose()
    def locate(self,**kw):
        return AddressController().locate(**kw)

    