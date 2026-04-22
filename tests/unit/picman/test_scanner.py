import pytest
from picman.scanner import Scanner


def test_scan_finds_supported_images(tmp_path):
    image_jpg = tmp_path / "photo.jpg"
    image_heic_upper = tmp_path / "mobile.HEIC"
    nested_dir = tmp_path / "nested"
    nested_dir.mkdir()
    image_png_nested = nested_dir / "image.png"
    non_image = tmp_path / "notes.txt"

    image_jpg.write_bytes(b"jpg")
    image_heic_upper.write_bytes(b"heic")
    image_png_nested.write_bytes(b"png")
    non_image.write_text("not an image")

    scanner = Scanner()

    result = scanner.scan(tmp_path)

    expected = {image_jpg, image_heic_upper, image_png_nested}
    assert set(result) == expected
    assert set(scanner.all_image_paths) == expected


def test_scan_accumulates_all_image_paths(tmp_path):
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    first_dir.mkdir()
    second_dir.mkdir()
    first_file = first_dir / "first.jpg"
    second_file = second_dir / "second.png"

    first_file.write_bytes(b"jpg")
    second_file.write_bytes(b"png")

    scanner = Scanner()

    first_result = scanner.scan(first_dir)
    second_result = scanner.scan(second_dir)

    assert set(first_result) == {first_file}
    assert set(second_result) == {second_file}
    assert set(scanner.all_image_paths) == {first_file, second_file}


def test_scan_raises_for_missing_path(tmp_path):
    missing = tmp_path / "does-not-exist/"
    scanner = Scanner()

    with pytest.raises(FileNotFoundError):
        scanner.scan(missing)


def test_scan_raises_for_non_directory(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("not a directory")
    scanner = Scanner()

    with pytest.raises(NotADirectoryError):
        scanner.scan(file_path)
