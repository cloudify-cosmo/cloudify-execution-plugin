


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

@pytest.mark.usefixtures("conftest.protocol_fake")
@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_01_check_remote_path():
    path = tempfile.gettempdir()
    id = conftest.protocol_fake.open_shell()
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
#     @pytest.mark.usefixtures("conftest.protocol_fake")
#     def test_01_check_remote_path(self):
#         path = tempfile.gettempdir()
#         id = conftest.protocol_fake.open_shell()
#         assert tasks.check_remote_path(id, path) == True
#         path = 'non-exists'
#         assert tasks.check_remote_path(id, path) == False
#
