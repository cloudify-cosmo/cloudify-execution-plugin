


import os
import shutil
from idlelib import PyShell
import unittest
import tempfile
import winrm
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
        password = "uDy=rr@Jm%9c~pe"
        user = "appveyor"
        s = winrm.Session('localhost', auth=(user, password))
        r = s.run_cmd('ipconfig', ['/all'])
        print(r.status_code, r.std_out)

        # path = tempfile.gettempdir()
        # id = PyShell(None)
        # self.assertTrue(tasks.check_remote_path(id, path))
        # path = 'non-exists'
        # self.assertFalse(tasks.check_remote_path(id, path))

