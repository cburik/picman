from pathlib import Path

_COMMON_IMAGE_EXTENSIONS = """
3fr ari arw avif bay bmp cap cr2 cr3 crw dcr dcs dds dng drf eip erf fff gif gpr heic heif iiq
j2c j2k jp2 jpeg jpg jxl k25 kdc mef mos mrw nef nrw orf pef png ptx pxn raf raw rwl rw2 sr2 srf
srw tif tiff webp x3f
"""


class Scanner:
    img_extensions: frozenset[str] = frozenset(f".{extension}" for extension in _COMMON_IMAGE_EXTENSIONS.split())

    def __init__(self) -> None:
        self.all_image_paths: list[Path] = []

    def scan(self, path: Path) -> list[Path]:
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")

        matches = [
            candidate
            for candidate in path.rglob("*")
            if candidate.is_file() and candidate.suffix.lower() in self.img_extensions
        ]
        self.all_image_paths.extend(matches)
        return matches
