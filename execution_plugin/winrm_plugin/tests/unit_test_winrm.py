


import os
import shutil
from idlelib import PyShell
import unittest
import tempfile
import winrm
from mock import patch
import pytest
from cloudify.mocks import MockCloudifyContext

from .. import tasks

@pytest.mark.usefixtures("protocol_fake")
@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_01_check_remote_path():
    path = tempfile.gettempdir()
    id = protocol_fake.open_shell()
    assert tasks.check_remote_path(id, path) == True
    path = 'non-exists'
    assert tasks.check_remote_path(id, path) == False


# class TestWinrmPlugin(unittest.TestCase):
#
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     @patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
#     def test_01_check_remote_path(self, protocol_fake):
#         path = tempfile.gettempdir()
#         id = protocol_fake.open_shell()
#         self.assertTrue(tasks.check_remote_path(id, path))
#         path = 'non-exists'
#         self.assertFalse(tasks.check_remote_path(id, path))

