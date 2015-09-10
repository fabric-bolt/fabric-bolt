from django.core.files.storage import FileSystemStorage


class FileStorageCHMOD600(FileSystemStorage):

    def __init__(self, location=None, base_url=None, file_permissions_mode=None, directory_permissions_mode=None):

        return super(FileStorageCHMOD600, self).__init__(location=location, base_url=base_url,
             file_permissions_mode=0o600, directory_permissions_mode=directory_permissions_mode)
