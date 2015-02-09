# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound

from corral.lib.base import BaseController
from corral.controllers.error import ErrorController
from corral.controllers.locateAddresses import AddressController, SelectAddressesForm
from corral.controllers.getComps import CompController, CompAddressForm

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
    def getComps(self):
        """Handle the getComps-page."""
        return dict(page='getComps', form=CompAddressForm)

    @expose('corral.templates.locateAddresses')
    def locateAddresses(self):
        """Handle the 'localteAddresses' page."""
        return dict(page='locateAddresses')
    
    @expose()
    def locate(self,**kw):
        return AddressController().locate(**kw)

    