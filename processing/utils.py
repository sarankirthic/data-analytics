from pathlib import Path


def get_latest_subdirectory(base_path: Path) -> Path:
    subdirectories = [d for d in base_path.iterdir() if d.is_dir()]
    if not subdirectories:
        raise FileNotFoundError(f"No subdirectories found in {base_path}")
    latest = sorted(subdirectories, key=lambda d: d.name, reverse=True)[0]
    return latest


def find_file_by_extension(directory: Path, extension: str) -> Path:
    files = list(directory.glob(f"*.{extension}"))
    if not files:
        raise FileNotFoundError(f"No *.{extension} files found in {directory}")
    return files[0]
