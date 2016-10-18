


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

USER = os.environ['WINRM_USERNAME'] = "Administrator"
PASSWORD = os.environ['WINRM_PASSWORD'] = "Aa123456!"
TRANSPORT = os.environ['WINRM_TRANSPORT'] = "basic"
ENDPOINT = os.environ['WINRM_ENDPOINT'] = "http://localhost:5985/wsman"


@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_01_run_remote_command(protocol_real):
    path = tempfile.gettempdir()
    shell_id = protocol_real.open_shell()
    assert tasks.check_remote_path(shell_id, path, protocol_real)
    path = 'not-exists'
    assert not tasks.check_remote_path(shell_id, path, protocol_real)
    protocol_real.close_shell(shell_id)

@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_02_run_script(protocol_real, mocker):
    mocker.patch('execution_plugin.winrm_plugin.tasks.get_winrm_protocol', return_value=protocol_real)
    tasks.run_script('http://localhost:5985/wsman', 'Administrator', 'Aa123456', 'powershell', os.path.join('execution_plugin', 'winrm_plugin', 'tests', 'scripts', 'test.ps1'))
    tasks.run_script('http://localhost:5985/wsman', 'Administrator', 'Aa123456', 'cmd', os.path.join('execution_plugin', 'winrm_plugin', 'tests', 'scripts', 'test.bat'))
#
# def test_03_run_commands():
#     pass
#
# def test_04_get_remote_shell_id():
#     pass
#
#
# def test_05_create_script_creation_command():
#     pass
#
# def test_06_run_remote_command():
#     pass
