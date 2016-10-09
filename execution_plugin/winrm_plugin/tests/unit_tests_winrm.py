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
def test_01_get_conn():
    '''
    creating right and wrong protocol and verifying results
    '''
    tasks.get_conn('http', 'localhost', PASSWORD, USER, '5985')
    tasks.get_conn('http', None, PASSWORD, USER, '5985')

def test_02_get_remote_shell_id(protocol_fake):
    '''
    verifying correct shell id for mock fake and error raises with None.
    '''
    shell_id = tasks.get_remote_shell_id(protocol_fake)
    assert shell_id == '11111111-1111-1111-1111-111111111113'
    protocol_fake.close_shell(shell_id)

    with pytest.raises(Exception) as excinfo:
        tasks.get_remote_shell_id(None)
    assert "Can\'t create connection. Error:" in str(excinfo.value)

def test_03_define_process_var():
    assert tasks.define_process_var('cmd') == ' '
    assert tasks.define_process_var('ps') == 'ps'
    assert tasks.define_process_var(None) is None

def test_04_check_process_and_ext():
    assert tasks.check_process_and_ext('test.bat', 'cmd')
    assert tasks.check_process_and_ext('test.ps1', 'powershell')
    assert tasks.check_process_and_ext('test.py', 'python')
    with pytest.raises(Exception) as excinfo:
        tasks.check_process_and_ext('test.txt', 'cmd')
    assert "Can\'t run" in str(excinfo.value)
    with pytest.raises(Exception) as excinfo:
        tasks.check_process_and_ext('test.py', 'python')
    assert "Can\'t run" in str(excinfo.value)
    with pytest.raises(Exception) as excinfo:
        tasks.check_process_and_ext('test.txt', 'powershell')
    assert "Can\'t run" in str(excinfo.value)

# def test_05_create_encoded_command():
#     pass

def test_06_define_script_path():
    assert tasks.define_script_path(None) == '%TEMP%'
    assert tasks.define_script_path(None, is_cmd=False) == '$env:TEMP'
    assert tasks.define_script_path('echo test') == 'echo test'
    assert tasks.define_script_path('echo test', is_cmd=False) == 'echo test'