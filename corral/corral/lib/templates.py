# -*- coding: utf-8 -*-

"""The dropbox  Controller API."""
from corral.lib.base import BaseController
from tg import TGController, tmpl_context
from tg.render import render
from tg.i18n import ugettext as _, ungettext
import os, glob

__all__ = ['NoteController', 'PeopleController', 'TaskController', 'KasesController']


class NoteController(BaseController):
    """Represents a Task template"""
    def __init__(self):
        """Stores xml template for Task
        """   
        self._noteXml = """
    <note>
	<body>%(body)s</body>
	<subject-id type="integer">%(subject)s</subject-id>
	<subject-type>%(type)s</subject-type>
    </note>"""

       
    def _getNoteTemplate(self):

        return self._noteXml



class KasesController(BaseController):
    """Represents a Kases template"""
    def __init__(self):
        """Stores xml template for Kase
        """   
        self._kaseXml = '''
    <kase>
	    <name>%(name)s</name>
    </kase>'''

       
    def _getKaseTemplate(self):

        return self._kaseXml


class PeopleController(BaseController):
    """Represents a People template"""
    def __init__(self):
        """Stores xml template for people
        """   
        self._peopleXml = """
    <person>
        <first-name>%(first-name)s</first-name>
        <last-name>%(last-name)s</last-name>
        <title>%(title)s</title>
     </person>"""

       
    def _getPeopleTemplate(self):

        return self._peopleXml


class TaskController(BaseController):
    """Represents a Task template"""
    def __init__(self):
        """Stores xml template for Task
        """   
        self._taskXml = """
    <task>
	<body>%(body)s</body>
	<public type="boolean">%(type)s</public>
	<due-at>%(due-at)s</due-at>
	<subject-id>%(subject-id)s</subject-id>
    </task>"""

       
    def _getTaskTemplate(self):

        return self._taskXml
