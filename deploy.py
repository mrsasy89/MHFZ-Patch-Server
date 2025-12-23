from pathlib import Path
from shutil import copy2, copytree, rmtree
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).parent

RELEASE_DIR = ROOT / "releases"
WIN_DIR     = RELEASE_DIR / "Windows" / "patchserver"
LINUX_DIR   = RELEASE_DIR / "Linux" / "patchserver"

def clean_dir(path: Path):
    if path.exists():
        rmtree(path)
    path.mkdir(parents=True, exist_ok=True)

def prepare_common(target: Path):
    # copia cartelle game/ e images/
    copytree(ROOT / "game",   target / "game")
    copytree(ROOT / "images", target / "images")

    # copia json di config/launcher
    copy2(ROOT / "launcher.json",    target / "launcher.json")
    copy2(ROOT / "patch_config.json", target / "patch_config.json")

def make_zip(src: Path, zip_path: Path):
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as z:
        for path in src.rglob("*"):
            if path.is_file():
                z.write(path, path.relative_to(src.parent))

def main():
    RELEASE_DIR.mkdir(exist_ok=True)

    # Linux
    if (ROOT / "patchserver").exists():
        clean_dir(LINUX_DIR)
        prepare_common(LINUX_DIR)
        copy2(ROOT / "patchserver", LINUX_DIR / "patchserver")
        make_zip(LINUX_DIR, RELEASE_DIR / "Linux-amd64.zip")

    # Windows
    if (ROOT / "patchserver.exe").exists():
        clean_dir(WIN_DIR)
        prepare_common(WIN_DIR)
        copy2(ROOT / "patchserver.exe", WIN_DIR / "patchserver.exe")
        make_zip(WIN_DIR, RELEASE_DIR / "Windows-amd64.zip")

if __name__ == "__main__":
    main()
