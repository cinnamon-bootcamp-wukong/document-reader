import os
import shlex


def upload_file(filename: str, rclone_remote_name: str, remote_dir_path: str) -> int:
    """
    Upload a file into cloud services of choice using `rclone`.

    :param filename: Path to the desired file to upload
    :param rclone_remote_name: The remote name set up in `rclone`. Use `rclone listremotes` to see existing configured remotes, and `rclone config` to create one.
    :param remote_dir_path: The desired path for the file to be uploaded

    :return the error code of the `rclone copy` command.
    """
    sanitized_filename = shlex.quote(filename)
    sanitized_remote_name = shlex.quote(rclone_remote_name)
    sanitized_remote_path = shlex.quote(remote_dir_path)
    errcode = os.system(
        f"rclone copy {sanitized_filename} {sanitized_remote_name}:{sanitized_remote_path}"
    )
    return errcode
