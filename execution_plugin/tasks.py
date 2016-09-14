from local import tasks as local_tasks
from fabric_plugin import tasks as ssh_tasks


def run_locally(script_path, process=None, **kwargs):
    return local_tasks.run(script_path, process, **kwargs)


def run_ssh(script_path,
            fabric_env=None,
            process=None,
            use_sudo=False,
            hide_output=None,
            **kwargs):
    return ssh_tasks.run_script(script_path,
                                fabric_env,
                                process,
                                use_sudo,
                                hide_output,
                                **kwargs)


def execute_workflow(script_path, **kwargs):
    return local_tasks.execute_workflow(script_path, **kwargs)
