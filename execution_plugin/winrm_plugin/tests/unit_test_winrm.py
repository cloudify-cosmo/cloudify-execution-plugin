


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
        s = winrm.Session('windows-host', auth=('john.smith', 'secret'))

        r = s.run_cmd('ipconfig', ['/all'])

        assert r.status_code == 0
        assert b'Windows IP Configuration' in r.std_out
        assert len(r.std_err) == 0

        # path = tempfile.gettempdir()
        # id = PyShell(None)
        # self.assertTrue(tasks.check_remote_path(id, path))
        # path = 'non-exists'
        # self.assertFalse(tasks.check_remote_path(id, path))

