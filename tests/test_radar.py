from pathlib import Path


def test_radar_images():

    folder = Path("reports/radar_charts")

    assert folder.exists()

    images = list(folder.glob("*.png"))

    assert len(images) > 0