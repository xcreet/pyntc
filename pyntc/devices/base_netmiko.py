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

    # TODO(drx): ask Jacob if we should have this. 
    # Aireos does not have this method but also does not use Netmiko FileTransfer
    @abc.abstractmethod
    def def _file_copy_instance(self, src, dest=None, file_system="flash:")::
        """Enter into config mode using Netmiko FileTransfer."""
        raise NotImplementedError