import sys
import subprocess
import time
import pathlib


__all__ = ["run_daemon_entry_point", "run_daemon_from_file"]


def run_daemon_entry_point(kind, config):
    if type(config) == pathlib.WindowsPath:
        config = str(config)
    def decorator(function):
        def wrapper():
            # https://stackoverflow.com/questions/42572582/winerror-2-the-system-cannot-find-the-file-specified-python
            with subprocess.Popen([f"yaqd-{kind}", "--config", config], shell=True) as proc:
                tries = 100
                while True:
                    # Process exited with nonzero exit status
                    if proc.poll():
                        raise subprocess.SubprocessError(proc.stderr)
                    if tries <= 0:
                        function()
                    try:
                        function()
                    except ConnectionError:
                        time.sleep(0.1)
                    except:
                        proc.terminate()
                        raise
                    else:
                        break
                    tries -= 1
                proc.terminate()

        return wrapper

    return decorator


def run_daemon_from_file(pyfile, config):
    def decorator(function):
        def wrapper():
            with subprocess.Popen([sys.executable, pyfile, "--config", config]) as proc:
                tries = 100
                while True:
                    # Process exited with nonzero exit status
                    if proc.poll():
                        raise subprocess.SubprocessError(proc.stderr)
                    if tries <= 0:
                        function()
                    try:
                        function()
                    except ConnectionError:
                        time.sleep(0.1)
                    except:
                        proc.terminate()
                        raise
                    else:
                        break
                    tries -= 1
                proc.terminate()

        return wrapper

    return decorator
