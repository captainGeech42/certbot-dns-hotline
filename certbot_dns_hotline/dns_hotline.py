"""DNS Authenticator for Hotline"""

import hashlib
import logging

from certbot import errors
from certbot import interfaces
from certbot.compat import filesystem
from certbot.compat import os
from certbot.plugins import dns_common
import zope.interface

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Hotline

    This authenticator writes a challenge to disk for Hotline to fulfill a dns-01 challenge. 
    """

    description = "Obtain certificates using a DNS TXT record (if you are using Hotline)."

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.path = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=5
        )
        add("path", help="Path to directory shared with the Hotline DNS callback service")

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using "
            + "the Hotline DNS callback service."
        )

    def _setup_credentials(self):
        # no authentication for this
        pass

    def _perform(self, domain, validation_name, validation):
        self._get_hotline_client().add_txt_record(
            domain, validation_name, validation
        )

    def _cleanup(self, domain, validation_name, validation):
        self._get_hotline_client().del_txt_record(
            domain, validation_name, validation
        )

    def _get_hotline_client(self):
        if self.path is None:
            self._configure("path", "Path to directory shared with the Hotline DNS callback service")
            self.path = self.conf("path")

        logger.debug("getting client")
        return _HotlineDNSClient(
            self.path
        )

class _HotlineDNSClient(object):
    """
    Encapsulates all communication with the Hotline DNS callback service.
    """

    def __init__(self, path):
        logger.debug("creating hotline client")
        self.path = path

    def _get_record_path(self, domain, record_hash):
        """Build the path to the file where the verification data will be stored."""

        dir_path = os.path.join(self.path, domain)
        if not os.path.exists(dir_path):
            filesystem.mkdir(dir_path)

        return os.path.join(self.path, domain, record_hash)

    def _hash_value(self, val):
        return hashlib.sha256(val.encode()).hexdigest()
    
    def add_txt_record(self, domain, record_name, record_content):
        """
        Add a TXT record using the supplied information.
        :param str domain: The domain to use to look up the managed zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :raises certbot.errors.PluginError: if an error occurs communicating with Hotline
        """
        try:
            # get the hash of the record contents
            # this is used in the filepath to ensure its idempotent, unique, and a valid name
            record_hash = self._hash_value(record_content)

            fp = self._get_record_path(record_name, record_hash)

            with open(fp, "w") as f:
                logger.debug(f"Writing record contents to disk at {fp}")
                f.write(record_content)

        except (FileNotFoundError, PermissionError) as e:
            raise errors.PluginError(f"Failed to write TXT record contents to {fp}")

    def del_txt_record(self, domain, record_name, record_content):
        """
        Delete a TXT record using the supplied information.
        :param str domain: The domain to use to look up the managed zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :raises certbot.errors.PluginError: if an error occurs communicating with Hotline
        """
        
        record_hash = self._hash_value(record_content)

        fp = self._get_record_path(record_name, record_hash)

        try:
            logger.debug(f"Removing record contents at {fp}")
            os.unlink(fp)
        except FileNotFoundError:
            pass