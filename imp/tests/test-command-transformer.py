import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from communication.imp-command-transformer import CommandTransformer


def test_build_and_parse():
    transformer = CommandTransformer()
    msg = transformer.build("ls", {"path": "/tmp"})
    cmd, params = transformer.parse(msg)
    assert cmd == "ls"
    assert params["path"] == "/tmp"


def test_handshake_ack():
    transformer = CommandTransformer()
    path = transformer.handshake("ack")
    assert path[-1] == "bottom->imp"
