


import os
import shutil
from idlelib import PyShell
import unittest
import tempfile
import winrm
from mock import patch
import pytest
from winrm.tests import conftest
from cloudify.mocks import MockCloudifyContext

from .. import tasks

@pytest.mark.usefixtures("protocol_fake")
class TestWinrmPlugin(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # @pytest.mark.usefixtures("conftest.protocol_fake")
    # @patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
    def test_01_check_remote_path(self):
        path = tempfile.gettempdir()
        id = conftest.protocol_fake.open_shell()
        self.assertTrue(tasks.check_remote_path(id, path))
        path = 'non-exists'
        self.assertFalse(tasks.check_remote_path(id, path))

