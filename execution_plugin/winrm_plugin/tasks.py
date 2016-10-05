# standard library imports
import base64
import os.path
# installed libraries imports
import winrm
import winrm.exceptions as exceptions

# our library imports
from cloudify import ctx
from cloudify.decorators import operation
from cloudify.exceptions import NonRecoverableError
from cloudify.exceptions import RecoverableError


@operation
def run_script(address, username, password, process, local_file_path,
               delete_after_running=True, remote_script_path=None,
               winrm_port=5985, winrm_protocol="http", **kwargs):

    '''function to run winrm script over remote machine,
    winrm env vars are required(user, password, protocol, port, etc).
    adress = ??, local file path = the script?
    delete after running and remote script path...
    '''

    file_ext = os.path.splitext(local_file_path)[1]
    remote_script_file_name = "\\script" + os.path.splitext(local_file_path)[1]

    conn = get_conn(winrm_protocol, address, password, username, winrm_port)
    remote_shell_id = get_remote_shell_id(conn)

    powershell_path = define_script_path(remote_script_path, False)
    encoded_script = create_script_creation_command(
            local_file_path, powershell_path, remote_script_file_name)
    cmd_path = define_script_path(remote_script_path)
    check_process_and_ext(file_ext, process)
    path_check = check_remote_path(remote_shell_id, cmd_path, conn)

    if path_check:
        ctx.logger.info('Copying script file on remote machine')
        run_remote_command(remote_shell_id, 'powershell', '-encodedcommand',
                           ' {0}'.format(encoded_script), conn)
        process = define_process_var(process)
        ctx.logger.info('Running the script on remote machine')
        run_remote_command(remote_shell_id, process, cmd_path,
                           remote_script_file_name, conn)
        if delete_after_running:
            ctx.logger.info('Removing script file from remote machine')
            run_remote_command(remote_shell_id, 'del', cmd_path,
                               remote_script_file_name, conn)
    else:
        raise NonRecoverableError('Path {0} or {1} does not exist'
                                  .format(cmd_path, powershell_path))


# this is run multi commands
@operation
def run_commands(commands, address, username, password,
                 process, winrm_port=5985, winrm_protocol='http', **kwargs):
    '''
    function for running direct command via cmd.
    env var are required
    '''
    conn = get_conn(winrm_protocol, address, password, username, winrm_port)
    remote_shell_id = get_remote_shell_id(conn)

    process = define_process_var(process)
    if process == 'powershell':
        for command in commands:
            encode_command = create_encoded_command(command)
            ctx.logger.info('running command: {0}'.format(command))
            # where is remote_shell_id from?
            run_remote_command(remote_shell_id, process, '-encodedcommand',
                               ' {0}'.format(encode_command), conn)
    else:
        for command in commands:
            ctx.logger.info('running command: {0}'.format(command))
            run_remote_command(remote_shell_id, process, '',
                               ' {0}'.format(command), conn)


# call it configure - get inputs and generate environment, including process.
def get_conn(winrm_protocol, address, password, username, winrm_port):
    '''
    generation winrm environment. from username inputs to winrm protocol.
    '''
    endpoint = '{0}://{1}:{2}/wsman'.format(winrm_protocol, address,
                                            winrm_port)
    return winrm.Protocol(endpoint=endpoint, transport='plaintext',
                          username=username, password=password)

# call it from configure
def get_remote_shell_id(conn):
    '''
    return shell id for winrm commands,
    if winrm env was initialized successfully.
    '''
    try:
        return conn.open_shell()
    except (exceptions.WinRMWebServiceError,
            exceptions.TimeoutError,
            exceptions.WinRMAuthorizationError,
            exceptions.UnauthorizedError) as remote_shell_error:
        raise NonRecoverableError('Can\'t create connection. Error: '
                                  '({0})'.format(str(remote_shell_error)))
    except exceptions.WinRMTransportError as remote_shell_error:
        raise RecoverableError('Can\'t create connection. Error: '
                               '({0})'.format(str(remote_shell_error)))

# call it from configure
def create_script_creation_command(local_file_path, powershell_path,
                                   remote_script_file_name):
    '''
    generating a valid script from script file using windows stream writer.
    '''
    try:
        with open(local_file_path, 'r') as script_file:
            script_content = script_file.read()
    except (TypeError, IOError) as read_file_error:
        raise NonRecoverableError('Can\'t read this file. Error: '
                                  '{0}'.format(str(read_file_error)))

    script_creator_cmd_prefix = \
        '''$stream = [System.IO.StreamWriter] "{0}{1}"; $s = @'\n'''.format(
            powershell_path, remote_script_file_name)

    script_creator_cmd_suffix = \
        '''\n'@ | %{ $_.Replace('`n','`r`n') }; $stream.WriteLine($s)
        $stream.close()'''
    command = \
        script_creator_cmd_prefix + script_content + script_creator_cmd_suffix
    return base64.b64encode(command.encode("utf_16_le"))

# call it from configure
def define_process_var(process):
    '''
    if process is cmd return empty string, else returns process for the commands prefix.
    '''
    process = process.lower()
    return process if process != 'cmd' else ' '

# call it from configure
def check_process_and_ext(file_ext, process):
    '''
    verifying that process type and scripts format matches.
    '''
    process = process.lower()
    file_ext = file_ext.lower()
    powershell = True if process == 'powershell' and file_ext == '.ps1' \
        else False
    python = True if process == 'python' and file_ext == '.py' else False
    cmd = True if process == 'cmd' and file_ext == '.bat' else False
    if powershell or python or cmd:
        return True
    else:
        raise NonRecoverableError('process'
                                  ': {0} can\'t run {1} files.'
                                  .format(process, file_ext))



#  this is run command
def run_remote_command(remote_shell_id, process, cmd_path,
                       remote_script_file_name, conn):
    '''
    running the command.
    '''
    try:
        command_id = conn.run_command(
            remote_shell_id, '{0} {1}{2}'.format(process, cmd_path,
                                                 remote_script_file_name))
        stdout, stderr, return_code = conn.get_command_output(remote_shell_id,
                                                              command_id)
        conn.cleanup_command(remote_shell_id, command_id)
        if stdout:
            ctx.logger.info('STDOUT: {0}'.format(stdout))
        if stderr:
            ctx.logger.error('STDERR: {0}'.format(stderr))
    except exceptions.WinRMTransportError as remote_run_error:
        ctx.logger.error('Can\'t run remote command. Error: '
                         '({0})'.format(str(remote_run_error)))
        # TODO: raise NonRecoverable but talk to Nir first to confirm


def create_encoded_command(command):
    '''
    generating encoded command for winrm format.
    '''
    try:
        return base64.b64encode(command.encode("utf_16_le"))
    except AttributeError as encoded_command_error:
        raise NonRecoverableError('command var is None. Error: '
                                  '{0}'.format(str(encoded_command_error)))



# need to refactor this func to default script path which is synchronized with fabric.
def define_script_path(remote_script_path, is_cmd=True):
    '''
    if user input for script destination path is None - return default temp.
    '''
    tmp_env_var = '%TEMP%' if is_cmd else '$env:TEMP'
    return remote_script_path if remote_script_path else tmp_env_var


def check_remote_path(remote_shell_id, cmd_path, conn):
    '''
    Veryfing shell exists
    '''
    cmd_path = base64.b64encode(cmd_path.encode("utf_16_le"))
    try:
        command_id = conn.run_command(remote_shell_id,
                                      'IF EXIST {0} (ECHO 1) ELSE (ECHO 0)'.
                                      format(cmd_path))
        stdout, stderr, return_code = conn.get_command_output(remote_shell_id,
                                                              command_id)
        conn.cleanup_command(remote_shell_id, command_id)
        print (stdout, stderr, return_code)
        return True if int(stdout) == 1 else False
    except exceptions.WinRMTransportError as remote_run_error:
        raise RecoverableError('Can\'t run remote command. Error: '
                               '({0})'.format(str(remote_run_error)))



