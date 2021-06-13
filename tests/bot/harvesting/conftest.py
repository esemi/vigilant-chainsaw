from pathlib import Path
from typing import List


def screenshots_dir() -> Path:
    folder = Path(__file__).parent.joinpath('./screenshots/')
    assert folder.exists()
    return folder


def cotton_templates() -> List[str]:
    return [str(screenshots_dir() / i) for i in ['cotton-example.png', 'cotton-example2.png', 'cotton-example3.png', 'cotton-example4.png']]
