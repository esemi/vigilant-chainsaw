from pathlib import Path
from typing import List


def screenshots_dir() -> Path:
    folder = Path(__file__).parent.joinpath('./screenshots/')
    assert folder.exists()
    return folder


def cotton_templates() -> List[str]:
    folder = screenshots_dir() / 'cotton'
    return [str(filename) for filename in folder.glob('*.png') if filename.is_file()]