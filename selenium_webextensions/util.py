import subprocess

parse_stdout = lambda res: res.strip().decode('utf-8')

run_shell_command = lambda command: parse_stdout(subprocess.check_output(command))

get_git_root = lambda: run_shell_command(['git', 'rev-parse', '--show-toplevel'])
