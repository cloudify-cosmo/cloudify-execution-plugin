


import os
import shutil
from idlelib import PyShell
import unittest
import tempfile
from winrm.tests.conftest import protocol_fake
from winrm.tests.conftest import protocol_real
from mock import patch
import pytest
from cloudify.mocks import MockCloudifyContext

from .. import tasks

@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_01_check_remote_path(protocol_fake):
    path = tempfile.gettempdir()
    id = protocol_fake.open_shell()
    assert tasks.check_remote_path(id, path, protocol_fake) == True
    path = 'non-exists'
    assert tasks.check_remote_path(id, path, protocol_fake) == False

@patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
def test_02_check_remote_path(protocol_real):
    path = tempfile.gettempdir()
    id = protocol_real.open_shell()
    assert tasks.check_remote_path(id, path, protocol_real) == True
    path = 'non-exists'
    assert tasks.check_remote_path(id, path, protocol_real) == False
