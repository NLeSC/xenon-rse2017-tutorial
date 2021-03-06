import xenon
from xenon import Path, FileSystem, PasswordCredential

xenon.init()

credential = PasswordCredential(username='xenon', password='javagat')

remote_fs = FileSystem.create(adaptor='sftp', location='localhost:10022', password_credential=credential)
path = Path("/home/xenon")

listing = remote_fs.list(path, recursive=False)

for entry in listing:
    if not entry.path.is_hidden():
        print(entry.path)

remote_fs.close()
