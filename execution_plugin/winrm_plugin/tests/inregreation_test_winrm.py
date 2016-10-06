


import os
import shutil
import base64
import unittest
import tempfile
from winrm.tests.conftest import protocol_fake, protocol_real

from mock import patch
from cloudify.mocks import MockCloudifyContext

from .. import tasks

os.environ['WINRM_USERNAME'] = "Administrator"
os.environ['WINRM_PASSWORD'] = "Aa123456!"
os.environ['WINRM_TRANSPORT'] = "basic"
os.environ['WINRM_ENDPOINT'] = "http://localhost:5985/wsman"


@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_01_run_remote_command(protocol_real):
    path = tempfile.gettempdir()
    shell_id = protocol_real.open_shell()
    assert tasks.check_remote_path(shell_id, path, protocol_real)
    path = 'not-exists'
    assert not tasks.check_remote_path(shell_id, path, protocol_real)



def test_02_run_script():
    pass

def test_03_run_commands():
    pass

def test_04_get_remote_shell_id():
    pass


def test_05_create_script_creation_command():
    pass

def test_06_run_remote_command():
    pass