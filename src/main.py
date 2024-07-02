import argparse
from processing import wordLevelPaddleOCR
from upload import upload_folder


def create_parser():
    """
    Create and return the argument parser for the OCR script.

    The parser is configured to handle the following arguments:
    --input_file: Path to the directory containing input file (required).
    --upload: Flag to determine if the results should be uploaded to cloud storage (optional).
    --rclone_remote_name: Name of the rclone remote to upload to (required if --upload is specified).
    --remote_dir_path: Path in the remote where the folder should be uploaded (required if --upload is specified).

    Returns:
        argparse.ArgumentParser: Configured argument parser.
    """
    parser = argparse.ArgumentParser(description="Perform word-level OCR on files.")
    parser.add_argument(
        '--input_file',
        type=str,
        required=True,
        help="Path to the directory containing input file.",
    )
    parser.add_argument(
        '--upload',
        action='store_true',
        help="If specified, upload to cloud; otherwise, save to local.",
    )
    parser.add_argument(
        '--rclone_remote_name',
        type=str,
        help="Name of the rclone remote to upload to.",
    )
    parser.add_argument(
        '--remote_dir_path',
        type=str,
        help="Path in the remote where the folder should be uploaded.",
    )

    return parser


def main():
    """
    Main function to perform word-level OCR on file.
    """

    parser = create_parser()
    args = parser.parse_args()

    if args.upload:
        if not (args.rclone_remote_name and args.remote_dir_path):
            parser.error("--rclone_remote_name and --remote_dir_path are required for upload.")

    ocr = wordLevelPaddleOCR()
    folder_path = ocr.export(path=args.input_file)

    if args.upload:
        upload_folder(folder_path, args.rclone_remote_name, args.remote_dir_path)
        print("Upload success!")
    else:
        print("Saved to local!")


if __name__ == "__main__":
    main()
