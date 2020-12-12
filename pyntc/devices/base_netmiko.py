"""The module contains the base class that all devices that use Netmiko libraries should inherit from."""

import abc
import importlib
import warnings


from pyntc.errors import NTCError, FeatureNotFoundError
from .base_device import BaseDevice, fix_docs


class BaseNetmiko(BaseDevice):
    """Base Device ABC."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, host, username, password, secret="", port=22, confirm_active=True, device_type=None, **kwargs):
        super().__init__(host, username, password, device_type)
        self.native = None
        self.port = port
        self.secret = secret
        self.global_delay_factor = kwargs.get("global_delay_factor", 1)

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
    def _file_copy_instance(self, src, dest=None, file_system="flash:")::
        """Perform file tranfer and return file copy instance using Netmiko FileTransfer."""
        raise NotImplementedError

    @abc.abstractmethod
    def enable(self)::
        """Ensure device is in enable mode."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def connected(self):
        """Connected boolean property.

        Raises:
            NotImplementedError: returns not implemented if not included in facts.
        """
        raise NotImplementedError 
