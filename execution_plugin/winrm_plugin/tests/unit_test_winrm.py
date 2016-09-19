


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

#
# @pytest.fixture(scope='module')
# def protocol_fake(request):
#     uuid4_patcher = patch('uuid.uuid4')
#     uuid4_mock = uuid4_patcher.start()
#     uuid4_mock.return_value = uuid.UUID(
#         '11111111-1111-1111-1111-111111111111')
#
#     from winrm.protocol import Protocol
#
#     protocol_fake = Protocol(
#         endpoint='http://windows-host:5985/wsman',
#         transport='plaintext',
#         username='john.smith',
#         password='secret')
#
#     protocol_fake.transport = TransportStub()
#
#     def uuid4_patch_stop():
#         uuid4_patcher.stop()
#
#     request.addfinalizer(uuid4_patch_stop)
#     return protocol_fake
#
# x = protocol_fake(conftest.)
#
# @patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
# def test_01_check_remote_path(protocol_fake):
#     path = tempfile.gettempdir()
#     id = protocol_fake.open_shell()
#     assert tasks.check_remote_path(id, path) == True
#     path = 'non-exists'
#     assert tasks.check_remote_path(id, path) == False


class TestWinrmPlugin(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @pytest.mark.usefixtures('protocol_fake')
    @patch('execution_plugin.winrm_plugin.tasks.ctx', MockCloudifyContext())
    def test_01_check_remote_path(self):
        x = conftest.protocol_fake
        path = tempfile.gettempdir()
        id = x.open_shell()
        self.assertTrue(tasks.check_remote_path(id, path))
        path = 'non-exists'
        self.assertFalse(tasks.check_remote_path(id, path))

