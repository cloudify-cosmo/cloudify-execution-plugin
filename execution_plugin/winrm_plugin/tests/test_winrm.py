


import os
import shutil
from idlelib import PyShell
import unittest
import tempfile
from winrm.tests import conftest
from mock import patch
import pytest
from cloudify.mocks import MockCloudifyContext

from .. import tasks

@pytest.mark.usefixtures(conftest.protocol_real)
class WinrmPluginTest(unittest.TestCase):

    @patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
    def test_01_check_remote_path(self, protocol_real):
        path = tempfile.gettempdir()
        shell_id = protocol_real.open_shell()
        assert tasks.check_remote_path(shell_id, path, protocol_real)
        path = 'non-exists'
        assert not tasks.check_remote_path(shell_id, path, protocol_real)

    @patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
    def test_02_run_remote_command(self, protocol_real):
        path = tempfile.gettempdir()
        shell_id = protocol_real.open_shell()
        tasks.run_remote_command(shell_id, 'powershell', path, 'echo 1', protocol_real)
