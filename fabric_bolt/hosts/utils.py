from Crypto.PublicKey import RSA
from django.core.files.base import ContentFile

from fabric_bolt.hosts import models


def create_ssh_config(remote_user='root', name='Auto Generated SSH Key',
                      file_name='fabricbolt_private.key', email='deployments@fabricbolt.io', public_key_text=None,
                      private_key_text=None):
    """Create SSH Key"""

    if not private_key_text and not public_key_text:
        key = RSA.generate(2048)
        pubkey = key.publickey()

        private_key_text = key.exportKey('PEM')
        public_key_text = pubkey.exportKey('OpenSSH')

    ssh_config = models.SSHConfig()
    ssh_config.name = name
    ssh_config.private_key_file.save(file_name, ContentFile(private_key_text))
    ssh_config.public_key = '{} {}'.format(public_key_text, email)
    ssh_config.remote_user = remote_user
    ssh_config.save()

    return ssh_config
