import sys
import subprocess
import time


__all__ = ["run_daemon_entry_point", "run_daemon_from_file"]


def run_daemon_entry_point(kind, config):
    def decorator(function):
        def wrapper():
            with subprocess.Popen([f"yaqd-{kind}", "--config", config]) as proc:
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
