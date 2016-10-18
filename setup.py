#########
# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.

from setuptools import setup

setup(
    name='cloudify-execution-plugin',
    version='1.0',
    author='Gigaspaces',
    author_email='cosmo-admin@gigaspaces.com',
    packages=['execution_plugin'],
    license='LICENSE',
    description='Plugin for running scripts locally and remotely, '
                'using fabric and winrm',
    install_requires=[
        # TODO decide on plugins-common dependency (if any)
        'fabric==1.8.3',
        'six>=1.8.0',
        'pywinrm',
        'pytest',
        'pytest-mock'
    ]
)
