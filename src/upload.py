import os
import shlex


def upload_folder(folder_path: str, rclone_remote_name: str, remote_dir_path: str) -> int:
    """
    Upload a folder into cloud services of choice using `rclone`.

    :param folder_path: Path to the desired folder to upload
    :param rclone_remote_name: The remote name set up in `rclone`. Use `rclone listremotes` to see existing configured remotes, and `rclone config` to create one.
    :param remote_dir_path: The desired path for the folder to be uploaded

    :return the error code of the `rclone copy` command.
    """
    folder_name = os.path.basename(os.path.normpath(folder_path))
    complete_remote_path = os.path.join(remote_dir_path, folder_name)

    sanitized_folder_path = shlex.quote(folder_path)
    sanitized_remote_name = shlex.quote(rclone_remote_name)
    sanitized_complete_remote_path = shlex.quote(complete_remote_path)

    errcode = os.system(
        f"rclone copy {sanitized_folder_path} {sanitized_remote_name}:{sanitized_complete_remote_path}"
    )
    return errcode
