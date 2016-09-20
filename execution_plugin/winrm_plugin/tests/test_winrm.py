


import os
import shutil
from idlelib import PyShell
import unittest
import tempfile
from winrm.tests.conftest import protocol_fake, protocol_real

from mock import patch
import pytest
from cloudify.mocks import MockCloudifyContext

from .. import tasks

pytestmark = pytest.mark.usefixtures("protocol_fake", "protocol_real")


@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_01_check_remote_path(pytestmark):
    path = tempfile.gettempdir()
    shell_id = pytestmark.open_shell()
    assert tasks.check_remote_path(shell_id, path, pytestmark)
    path = 'non-exists'
    assert not tasks.check_remote_path(shell_id, path, pytestmark)


@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_02_run_remote_command(pytestmark):
    path = tempfile.gettempdir()
    shell_id = pytestmark.open_shell()
    tasks.run_remote_command(shell_id, 'powershell', path, 'echo 1', pytestmark)
