# related to local
PYTHON_SCRIPT_FILE_EXTENSION = '.py'
POWERSHELL_SCRIPT_FILE_EXTENSION = '.ps1'
DEFAULT_POWERSHELL_EXECUTABLE = 'powershell'

# related to both local and fabric
ILLEGAL_CTX_OPERATION_MESSAGE = 'ctx may only abort or return once'
UNSUPPORTED_SCRIPT_FEATURE_MESSAGE = ('ctx abort & retry commands are only '
                                      'supported in Cloudify 3.4 or later')
# related to fabric
DEFAULT_BASE_DIR = '/tmp/cloudify-ctx'
FABRIC_ENV_DEFAULTS = {
    'connection_attempts': 5,
    'timeout': 10,
    'forward_agent': False,
    'abort_on_prompts': True,
    'keepalive': 0,
    'linewise': False,
    'pool_size': 0,
    'skip_bad_hosts': False,
    'status': False,
    'disable_known_hosts': True,
    'combine_stderr': True,
}
# Very low level workaround used to support manager recovery
# that is executed on a client different than the one used
# to bootstrap
CLOUDIFY_MANAGER_PRIVATE_KEY_PATH = 'CLOUDIFY_MANAGER_PRIVATE_KEY_PATH'