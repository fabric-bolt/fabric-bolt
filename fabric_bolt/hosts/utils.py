from Crypto.PublicKey import RSA
from django.core.files.base import ContentFile

from fabric_bolt.hosts import models


def create_default_ssh_config(remote_user='root'):
    key = RSA.generate(2048)
    pubkey = key.publickey()

    ssh_config = models.SSHConfig()
    ssh_config.name = 'Auto Generated SSH Key'
    ssh_config.private_key_file.save('fabricbolt_private.key', ContentFile(key.exportKey('PEM')))
    ssh_config.public_key = pubkey.exportKey('OpenSSH') + ' deployments@fabricbolt.io'
    ssh_config.remote_user = remote_user
    ssh_config.save()

    return ssh_config
