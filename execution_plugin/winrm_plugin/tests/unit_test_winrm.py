


import os
import shutil
from idlelib import PyShell
import unittest
import tempfile

from mock import patch


from cloudify.mocks import MockCloudifyContext

from .. import tasks

class TestWinrmPlugin(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
    def test_01_check_remote_path(self):
        path = tempfile.gettempdir()
        id = PyShell(self)
        self.assertTrue(tasks.check_remote_path(id, path))
        path = 'non-exists'
        self.assertFalse(tasks.check_remote_path(id, path))

