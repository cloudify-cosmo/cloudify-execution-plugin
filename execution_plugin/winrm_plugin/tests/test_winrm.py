


import os
import shutil
import base64
from idlelib import PyShell
import unittest
import tempfile
from winrm.tests.conftest import protocol_fake, protocol_real

from mock import patch
import pytest
from cloudify.mocks import MockCloudifyContext

from .. import tasks

# pytestmark = pytest.mark.usefixtures("protocol_fake", "protocol_real")
list = ['WINRM_USERNAME', 'WINRM_PASSWORD']
for elem in list:
    with open(os.path.join("c:\\", elem+".txt"), 'r') as f:
        x = f.read()
        b = base64.b64encode(x)
    os.environ[elem] = b
os.environ['WINRM_TRANSPORT'] = base64.b64encode('basic')
os.environ['WINRM_ENDPOINT'] = base64.b64encode('http://localhost:5985/wsman')

@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_01_check_remote_path(protocol_fake):
    path = tempfile.gettempdir()
    shell_id = protocol_fake.open_shell()
    assert tasks.check_remote_path(shell_id, path, protocol_fake)
    path = 'non-exists'
    assert not tasks.check_remote_path(shell_id, path, protocol_fake)


@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_02_run_remote_command(protocol_real):
    path = tempfile.gettempdir()
    shell_id = protocol_real.open_shell()
    tasks.run_remote_command(shell_id, 'powershell', path, 'echo 1', protocol_real)
