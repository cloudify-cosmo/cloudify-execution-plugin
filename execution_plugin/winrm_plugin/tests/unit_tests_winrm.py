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

os.environ['WINRM_USERNAME'] = "Administrator"
os.environ['WINRM_PASSWORD'] = "Aa123456!"
os.environ['WINRM_TRANSPORT'] = "basic"
os.environ['WINRM_ENDPOINT'] = "http://localhost:5985/wsman"


@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_01_get_conn():
    pass

def test_02_get_remote_shell_id():
    pass

def test_03_define_process_var():
    pass

def test_04_check_process_and_ext():
    pass

def test_05_create_encoded_command():
    pass

def test_06_define_script_path():
    pass