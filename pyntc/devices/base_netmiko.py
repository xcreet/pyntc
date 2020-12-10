"""The module contains the base class that all devices that use Netmiko libraries should inherit from."""

import abc
import importlib
import warnings


from pyntc.errors import NTCError, FeatureNotFoundError
from .base_device import BaseDevice, fix_docs


class BaseNetmiko(BaseDevice):
    """Base Device ABC."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, host, username, password, device_type=None, **kwargs):
        super().__init__(host, username, password, device_type)
        self.native = None
        self.connected = False

    ####################
    # ABSTRACT METHODS #
    ####################
    @abc.abstractmethod
    def _send_command(self, command, expect_string=None):
        """Send command to remote device using Netmiko ConnectHandler."""
        raise NotImplementedError

    @abc.abstractmethod
    def _enter_config(self):
        """Enter into config mode using Netmiko ConnectHandler."""
        raise NotImplementedError


class RebootTimerError(NTCError):
    def __init__(self, device_type):
        super().__init__("Reboot timer not supported on %s." % device_type)


class RollbackError(NTCError):
    pass


class SetBootImageError(NTCError):
    pass
