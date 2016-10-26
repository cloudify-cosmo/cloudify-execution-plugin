


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
def test_01_run_script(protocol_real, mocker):
    mocker.patch('execution_plugin.winrm_plugin.tasks.get_winrm_protocol',
                 return_value=protocol_real)
    tasks.run_script('http://localhost:5985/wsman', 'Administrator', 'Aa123456',
                     'powershell', os.path.join('execution_plugin',
                                                'winrm_plugin', 'tests',
                                                'scripts', 'test.ps1'))
    tasks.run_script('http://localhost:5985/wsman', 'Administrator', 'Aa123456',
                     'cmd', os.path.join('execution_plugin', 'winrm_plugin',
                                         'tests', 'scripts', 'test.bat'))

@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_02_run_script_fails():
    with pytest.raises(Exception) as excinfo:
        tasks.run_script(None, None, None, None, 'cmd')
    assert "wrong parameters" in str(excinfo.value)
    with pytest.raises(Exception) as excinfo:
        tasks.run_script('', '', '', '', 'cmd')
    assert "wrong parameters" in str(excinfo.value)
    with pytest.raises(Exception) as excinfo:
        tasks.run_script('a', 'b', 'c', 'd', 'test')
    assert "Can\'t run script" in str(excinfo.value)

@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_03_run_commands(protocol_real, mocker):
    mocker.patch('execution_plugin.winrm_plugin.tasks.get_winrm_protocol',
                 return_value=protocol_real)
    tasks.run_commands(['echo test', 'dir'], 'http://localhost:5985/wsman',
                       'Administrator', 'Aa123456', 'powershell')
    tasks.run_commands(['echo test', 'dir'], 'http://localhost:5985/wsman',
                       'Administrator', 'Aa123456', 'cmd')

@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_04_run_commands_fails():
    with pytest.raises(Exception) as excinfo:
        tasks.run_commands(None, None, None, None, 'cmd')
    assert "wrong parameters" in str(excinfo.value)
    with pytest.raises(Exception) as excinfo:
        tasks.run_commands('', '', '', '', 'cmd')
    assert "wrong parameters" in str(excinfo.value)
    with pytest.raises(Exception) as excinfo:
        tasks.run_commands('a', 'b', 'c', 'd', 'test')
    assert "Can\'t run command" in str(excinfo.value)

def test_05_get_remote_shell_id(protocol_real):
    shell_id = tasks.get_remote_shell_id(protocol_real)
    protocol_real.close_shell(shell_id)

@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_06_check_remote_path(protocol_real):
    path = tempfile.gettempdir()
    shell_id = protocol_real.open_shell()
    assert tasks.check_remote_path(shell_id, path, protocol_real)
    path = 'not-exists'
    assert not tasks.check_remote_path(shell_id, path, protocol_real)
    protocol_real.close_shell(shell_id)

@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_07_check_remote_path_fails(protocol_real):
    with pytest.raises(Exception) as excinfo:
        tasks.check_remote_path(None, '', protocol_real)
    assert "wrong parameters" in str(excinfo.value)
    with pytest.raises(Exception) as excinfo:
        shell_id = protocol_real.open_shell()
        tasks.check_remote_path(shell_id, '', None)
    assert "wrong parameters" in str(excinfo.value)

@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_08_run_remote_command(protocol_real):
    shell_id = tasks.get_remote_shell_id(protocol_real)
    stdout, stderr, return_code = tasks.run_remote_command(shell_id,
                                                           'powershell', '',
                                                           'echo test',
                                                           protocol_real)
    assert stdout == 'test\r\n'
    assert stderr == ''
    assert return_code == 0
    stdout, stderr, return_code = tasks.run_remote_command(shell_id, '', '',
                                                           'echo test',
                                                           protocol_real)
    assert stdout == 'test\r\n'
    assert stderr == ''
    assert return_code == 0
    protocol_real.close_shell(shell_id)
