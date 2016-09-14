


import os
import shutil
import unittest
import tempfile

import distro
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
        self.assertTrue(tasks.check_remote_path(self.pyshell, path))
        path = 'non-exists'
        self.assertFalse(tasks.check_remote_path(self.pyshell, path))

