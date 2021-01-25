import socket
import sys
import re
import json
import threading

global_lock = threading.Lock()

class ACL2Command:
    """Constants for ACL2 Bridge Command Types"""
    HELLO = "ACL2_BRIDGE_HELLO"
    READY = "READY"
    ERROR = "ERROR"
    STDOUT = "STDOUT"
    RETURN = "RETURN"
    JSON = "JSON"
    LISP_MV = "LISP_MV"
    LISP = "LISP"

class ACL2BridgeError(Exception):
    """Exceptions Thrown from ACL2 Bridge"""
    def __init__(self, message):
        self.message = message

class ACL2Bridge:
    """Connector to an ACL2 Bridge Process

    This class implements the ACL2 Bridge protocol to allow an
    ACL2 server to be called from Python. 

    Methods
    -------
    acl2_command(self, msgtype=ACL2Command.LISP, cmd="T")
        Sends a command to ACL2 and returns the value from ACL2
    """

    DEFAULT_PORT = 55433

    def __init__(self, host="localhost", port=DEFAULT_PORT, socket_file=None, log=None):
        """Constructor for ACL2Bridge

        Parameters
        ----------
        host : str, optional
            The hostname of the ACL2 Bridge server (default is localhost)
        post : int, optional
            The TCP port the server is listening to (default is ACL2 Bridge default port of 55433)
        socket_file : str, optional
            The name of a named pipe the server is listening on (default is None)
        log : logging, optional
            A log on which to write status updates (default is None)
        """

        self.port = port
        self.host = host
        self.socket_file = socket_file
        self.log = log

        self._sock = None
        self._worker = None
        self._lock = global_lock

        if self.socket_file is not None:
            self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self._sock.connect(self.socket_file)
        else:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self.host, self.port))

        msgtype, content = self._read_message()
        if msgtype == ACL2Command.HELLO:
            self._worker = content
        else:
            raise ACL2BridgeError(f"Expected hello message, but got: [{msgtype}] {content}")

        msgtype, content = self._read_message()

        if msgtype != ACL2Command.READY:
            raise ACL2BridgeError(f"Expected ready message, but got: {msgtype} {content}")

    def close(self):
        """Close Connection to ACL2 Bridge Server"""

        self._sock(close)
        self._sock = None

    def _send_string(self, s):
        self._sock.sendall(bytes(str(s), 'utf-8'))

    def _send_command(self, msgtype, cmd):
        if self.log is not None:
            self.log.debug(f">>> {msgtype} {cmd}")
        self._send_string(msgtype.upper())
        self._send_string(" ")
        self._send_string(len(cmd))
        self._send_string("\n")
        self._send_string(cmd)
        self._send_string("\n")

    def _read_message(self):
        line = ""
        while True:
            ch = self._sock.recv(1).decode("utf-8")
            if ch is None:
                raise ACL2BridgeError("Expecting a header response from ACL2 but received EOF")
            if ch == '\n':
                break
            line += str(ch)

        m = re.fullmatch(r"(\w+) (\d+)", line, re.ASCII)
        if m:
            msgtype = m[1]
            msglen = int(m[2])
        else:
            raise ACL2BridgeError(f"Invalid header: {line}")

        content = ""
        while len(content) < msglen:
            chunk = self._sock.recv(msglen-len(content)).decode("utf-8")
            if chunk is None:
                raise ACL2BridgeError("Expecting a content response from ACL2 but received EOF")
            content += chunk

        ch = self._sock.recv(1).decode("utf-8")
        if ch is None:
            raise ACL2BridgeError("Expecting a newline after content response from ACL2 but received EOF")
        if ch != "\n":
            raise ACL2BridgeError(f"Expecting a newline after content response from ACL2 but received {ch}")

        if self.log is not None:
            self.log.debug(f"<<< {msgtype} {content}")
        return msgtype.upper(), content

    def acl2_command(self, msgtype=ACL2Command.LISP, cmd="T"):
        """Send a single ACL2 Command to ACL2 Bridge Server

        Parameters
        ----------
        msgtype : ACL2Command, optional
            Type of message to send (defaults to ACL2Command.LISP)
        cmd : str, optional
            The ACL2 command to send (defaults to T)
        """

        with self._lock:
            if self.log is not None:
                self.log.debug("Executing " + msgtype + ": " + cmd)
            self._send_command(msgtype, "(bridge::in-main-thread " + cmd + ")")
            response = { "CMD": cmd }
            while True:
                resptype, content = self._read_message()
                if resptype == ACL2Command.READY:
                    break
                if resptype not in response:
                    response[resptype] = ""
                response[resptype] += content
            if self.log is not None:
                self.log.debug(response)
            # if ACL2Command.ERROR in response:
            #     raise ACL2BridgeError(f"ACL2 encountered an error: \n{response[ACL2Command.ERROR]}")
            if ACL2Command.RETURN not in response and ACL2Command.ERROR not in response:
                raise ACL2BridgeError(f"ACL2 response does not contain a return value")
            if msgtype == ACL2Command.JSON:
                #print("json")
                #print(response[ACL2Command.RETURN])
                response[ACL2Command.RETURN] = json.loads(response[ACL2Command.RETURN])
            if self.log is not None:
                self.log.debug("Finished " + msgtype + ": " + cmd)
            return response

if __name__ == "__main__":
    import logging
    bridge = ACL2Bridge(logging)

    response = bridge.acl2_command(ACL2Command.JSON, "(cdr (assoc 'acl2-version *initial-global-table*))")
    print ("Connected to: " + response["RETURN"])
    response = bridge.acl2_command(ACL2Command.LISP, "(set-slow-alist-action nil)")
    print(json.dumps(response, indent=2))

    import random

    for _ in range(1000):
        idx = random.randint(1, 1000000)
        command = f"(ld '( (set-slow-alist-action nil) (acl2s::definec acl2s::foo{idx} (acl2s::x acl2s::nat) acl2s::nat (acl2s::/ acl2s::x 2)) ) :ld-pre-eval-print t :ld-verbose nil :current-package \"ACL2S\")"
        response = bridge.acl2_command(ACL2Command.LISP, command)
        print(json.dumps(response, indent=2))
