import os


def upload_file(filename: str, rclone_remote_name: str, remote_dir_path: str) -> int:
    """
    Upload a file into cloud services of choice using `rclone`.

    :param filename: Path to the desired file to upload
    :param rclone_remote_name: The remote name set up in `rclone`. Use `rclone listremotes` to see existing configured remotes, and `rclone config` to create one.
    :param remote_dir_path: The desired path for the file to be uploaded

    :return the error code of the `rclone copy` command.
    """
    errcode = os.system(f"rclone copy {filename} {rclone_remote_name}:{remote_dir_path}")
    return errcode
