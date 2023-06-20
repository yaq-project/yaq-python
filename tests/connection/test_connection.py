import pathlib
import socket
import time
from unittest.mock import Mock
import pytest

import yaqc
import yaqd_core
from yaqd_core import testing


config = pathlib.Path(__file__).parent / "connection.toml"
pyfile = config.with_suffix(".py")


@testing.run_daemon_from_file(pyfile, config)
def test_shutdown():
    shutdown = yaqc.Client(39099)
    assert shutdown.id()["name"] == "shutdown"

    shutdown.shutdown()
    with pytest.raises(ConnectionError):
        shutdown.id()


@testing.run_daemon_from_file(pyfile, config)
def test_restart():
    restart = yaqc.Client(39098)
    assert restart.id()["name"] == "restart"

    restart.shutdown(restart=True)
    x = 0

    def add_one():
        nonlocal x
        x += 1

    restart.register_connection_callback(add_one)
    time.sleep(0.1)
    assert restart.id()["name"] == "restart"
    assert x == 1


@testing.run_daemon_from_file(pyfile, config)
def test_incomplete_connection():
    initial = yaqc.Client(39097)
    assert initial.id()["name"] == "connect"
    socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_.settimeout(None)
    socket_.connect(("127.0.0.1", 39097))
    socket_.sendall(
        b"\x00\x00\x00#                \x00                \x02\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00"
    )
    socket_.sendall(
        b'\x00\x00\x07\x9a-U\xb5\x8c\x97S\xdfp,+!\xe4\x895\xc1\x86\x02\xea\x1d{"config": {"make": {"default": null, "origin": "is-daemon", "type": ["null", "string"]}, "model": {"default": null, "origin": "is-daemon", "type": ["null", "string"]}, "port": {"doc": "TCP port for daemon to occupy.", "origin": "is-daemon", "type": "int"}, "serial": {"default": null, "doc": "Serial number for the particular device represented by the daemon", "origin": "is-daemon", "type": ["null", "string"]}}, "doc": "Core trait common to all yaq daemons.", "messages": {"'
    )
    assert initial.id()["name"] == "connect"


@testing.run_daemon_from_file(pyfile, config)
def test_slow_connection():
    initial = yaqc.Client(39097)
    assert initial.id()["name"] == "connect"
    socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_.settimeout(None)
    socket_.connect(("127.0.0.1", 39097))
    socket_.sendall(
        b"\x00\x00\x00#                \x00                \x02\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00"
    )
    handshake_request = b'\x00\x00\x07\x9a-U\xb5\x8c\x97S\xdfp,+!\xe4\x895\xc1\x86\x02\xea\x1d{"config": {"make": {"default": null, "origin": "is-daemon", "type": ["null", "string"]}, "model": {"default": null, "origin": "is-daemon", "type": ["null", "string"]}, "port": {"doc": "TCP port for daemon to occupy.", "origin": "is-daemon", "type": "int"}, "serial": {"default": null, "doc": "Serial number for the particular device represented by the daemon", "origin": "is-daemon", "type": ["null", "string"]}}, "doc": "Core trait common to all yaq daemons.", "messages": {"busy": {"doc": "Returns true if daemon is currently busy.", "origin": "is-daemon", "request": [], "response": "boolean"}, "get_config": {"doc": "Full configuration for the individual daemon as defined in the TOML file.\\nThis includes defaults and shared settings not directly specified in the daemon-specific TOML table.\\n", "origin": "is-daemon", "request": [], "response": "string"}, "get_config_filepath": {"doc": "String representing the absolute filepath of the configuration file on the host machine.\\n", "origin": "is-daemon", "request": [], "response": "string"}, "get_state": {"doc": "Get version of the running daemon", "origin": "is-daemon", "request": [], "response": "string"}, "id": {"doc": "JSON object with information to identify the daemon, including name, kind, make, model, serial.\\n", "origin": "is-daemon", "request": [], "response": {"type": "map", "values": ["null", "string"]}}, "shutdown": {"doc": "Cleanly shutdown (or restart) daemon.", "origin": "is-daemon", "request": [{"default": false, "name": "restart", "type": "boolean"}], "response": "null"}}, "protocol": "connection-test", "requires": [], "traits": ["is-daemon"], "types": [{"fields": [{"name": "shape", "type": {"items": "int", "type": "array"}}, {"name": "typestr", "type": "string"}, {"name": "data", "type": "bytes"}, {"name": "version", "type": "int"}], "logicalType": "ndarray", "name": "ndarray", "type": "record"}], "version": "0.0.0"}-U\xb5\x8c\x97S\xdfp,+!\xe4\x895\xc1\x86\x02\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00'
    socket_.sendall(handshake_request[:700])
    time.sleep(0.1)
    socket_.sendall(handshake_request[700:])
    assert initial.id()["name"] == "connect"


@testing.run_daemon_from_file(pyfile, config)
def test_invalid_argument():
    initial = yaqc.Client(39097)
    initial._socket._socket = Mock()
    try:
        initial.echo(None)
    except TypeError:
        # Error expected, want to make sure no data was sent in error case
        pass
    initial._socket._socket.sendall.assert_not_called()


def test_timeout():
    # Open a socket which is NOT a yaq daemon
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 36098))
    s.listen(1)
    # socket.timeout is actually deprecated, but is an alias for TimeoutError in py3.10+
    # and its own OSError subclass in py<3.10
    with pytest.raises(socket.timeout):
        yaqc.Client(36098, timeout=0.1)


if __name__ == "__main__":
    test_shutdown()
    test_restart()
    test_incomplete_connection()
    test_slow_connection()
