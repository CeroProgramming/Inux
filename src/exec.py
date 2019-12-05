from subprocess import run, PIPE, STDOUT


class FailedToExecute(Exception):
    def __init__(self, command, exit_code, error_output):
        super(FailedToExecute, self).__init__('The execution of the command \'%s\' returned error code %d. Stderr: \n%s' \
                        % (command, exit_code, error_output))

def execute(command, text=True, shell=True):

    process = run(command, capture_output=True, text=text, shell=shell, executable='/bin/bash')

    return process.stdout, process.returncode
