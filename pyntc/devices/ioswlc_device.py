"""Module for using a Cisco IOSXE WLC device over SSH.
"""

import signal
import os
import re
import time
import warnings

from netmiko import ConnectHandler
from netmiko import FileTransfer

from pyntc.utils import get_structured_data
from .base_device import RollbackError, fix_docs
from .ios_device import IOSDevice
from pyntc.errors import (
    NTCError,
    CommandError,
    OSInstallError,
    CommandListError,
    FileTransferError,
    RebootTimeoutError,
    DeviceNotActiveError,
    NTCFileNotFoundError,
    FileSystemNotFoundError,
    SocketClosedError,
)

class IOSXEWLCDevice(IOSDevice):
    """Cisco IOSXE WLC Device Implementation."""

    vendor = "cisco"
    active_redundancy_states = {None, "active"}

    def __init__(self, host, username, password, secret="", port=22, confirm_active=True, fast_cli=True, **kwargs):
        """
        PyNTC Device implementation for Cisco IOSXE WLC.

        Args:
            host (str): The address of the network device.
            username (str): The username to authenticate with the device.
            password (str): The password to authenticate with the device.
            secret (str): The password to escalate privilege on the device.
            port (int): The port to use to establish the connection.
            confirm_active (bool): Determines if device's high availability state should be validated before leaving connection open.
            fast_cli (bool): Fast CLI mode for Netmiko, it is recommended to use False when opening the client on code upgrades
        """
        super().__init__(host, username, password, device_type="cisco_ios_ssh")

        self.native = None
        self.secret = secret
        self.port = int(port)
        self.global_delay_factor = kwargs.get("global_delay_factor", 1)
        self.delay_factor = kwargs.get("delay_factor", 1)
        self._fast_cli = fast_cli
        self._connected = False
        self.open(confirm_active=confirm_active)