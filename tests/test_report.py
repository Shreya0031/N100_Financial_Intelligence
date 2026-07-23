from pathlib import Path


def test_peer_report():

    report = Path("reports/peer_comparison.xlsx")

    assert report.exists()