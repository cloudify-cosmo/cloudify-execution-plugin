import json
import os


def is_windows():
    return os.name == 'nt'


def create_process_config(process, operation_kwargs):
    """
    update a process with it's environment variables, and return it.

    Get a dict representing a process and a dict representing the environment
    variables. Convert each environment variable to a format of
    <string representing the name of the variable> :
    <json formatted string representing the value of the variable>.
    Finally, update the process with the newly formatted environment variables,
    and return the process.

    :param process: a dict representing a process
    :type process: dict
    :param operation_kwargs: a dict representing environment variables that
    should exist in the process' running environment.
    :type operation_kwargs: dict
    :return: the process updated with its environment variables.
    :rtype: dict
    """

    env_vars = operation_kwargs.copy()
    if 'ctx' in env_vars:
        del env_vars['ctx']
    env_vars.update(process.get('env', {}))
    for k, v in env_vars.items():
        if isinstance(v, (dict, list, tuple, bool)):
            env_var_value = json.dumps(v)
            if is_windows():
                # These <k,v> environment variables will subsequently
                # be used in a subprocess.Popen() call, as the `env` parameter.
                # In some windows python versions, if an environment variable
                # name is not of type str (e.g. unicode), the Popen call will
                # fail.
                k = str(k)
                # The windows shell removes all double quotes - escape them
                # to still be able to pass JSON in env vars to the shell.
                env_var_value = env_var_value.replace('"', '\\"')
            env_vars[k] = env_var_value
    process['env'] = env_vars
    return process


