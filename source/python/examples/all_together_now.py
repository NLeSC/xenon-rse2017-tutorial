import xenon
from xenon import FileSystem, PasswordCredential, CopyRequest, Path, CopyStatus, Scheduler, JobDescription, JobStatus


def upload():

    # define which file to upload
    local_file = Path('/home/daisycutter/tmp/home/tutorial/xenon/sleep.sh')
    remote_file = Path('/home/xenon/sleep.sh')

    # create the destination file only if the destination path doesn't exist yet
    mode = CopyRequest.CREATE

    # no need to recurse, we're just uploading a file
    recursive = False

    # perform the copy/upload and wait 1000 ms for the successful or
    # otherwise completion of the operation
    copy_id = local_fs.copy(local_file, remote_fs, remote_file,
                            mode=mode, recursive=recursive)

    copy_status = local_fs.wait_until_done(copy_id, timeout=5000)

    assert copy_status.done

    # rethrow the Exception if we got one
    assert copy_status.error_type == CopyStatus.NONE, copy_status.error_message

    print('Done uploading.')


def submit():

    description = JobDescription(executable='bash',
                                 arguments=['sleep.sh', '60'],
                                 stdout='sleep.stdout.txt')

    scheduler = Scheduler.create(adaptor='slurm',
                                 location='localhost:10022',
                                 password_credential=credential)

    job_id = scheduler.submit_batch_job(description)

    print('Done submitting.')

    # wait for the job to finish before attempting to copy its output file(s)
    job_status = scheduler.wait_until_done(job_id, 10*60*1000)

    assert job_status.done

    # rethrow the Exception if we got one
    assert job_status.error_type == JobStatus.NONE, job_status.error_message

    print('Done executing on the remote.')

    # make sure to synchronize the remote filesystem
    job_id = scheduler.submit_batch_job(JobDescription(executable='sync'))
    scheduler.wait_until_done(job_id)

    scheduler.close()


def download():

    # define which file to download
    remote_file = Path('/home/xenon/sleep.stdout.txt')
    local_file = Path('/home/daisycutter/tmp/home/tutorial/xenon/sleep.stdout.txt')

    # create the destination file only if the destination path doesn't exist yet
    mode = CopyRequest.CREATE

    # no need to recurse, we're just uploading a file
    recursive = False

    # perform the copy/download and wait 1000 ms for the successful or
    # otherwise completion of the operation
    copy_id = remote_fs.copy(remote_file, local_fs, local_file,
                             mode=mode, recursive=recursive)

    copy_status = remote_fs.wait_until_done(copy_id, timeout=5000)

    assert copy_status.done

    # rethrow the Exception if we got one
    assert copy_status.error_type == CopyStatus.NONE, copy_status.error_message

    print('Done downloading.')


xenon.init()

# use the local file system adaptor to create a file system representation
local_fs = FileSystem.create(adaptor='file')

# use the sftp file system adaptor to create another file system representation;
# the remote filesystem requires credentials to log in, so we'll have to
# create those too.
credential = PasswordCredential(username='xenon',
                                password='javagat')

remote_fs = FileSystem.create(adaptor='sftp',
                              location='localhost:10022',
                              password_credential=credential)

upload()
submit()
download()

# remember to close the FileSystem instances
remote_fs.close()
local_fs.close()

print('Done')
