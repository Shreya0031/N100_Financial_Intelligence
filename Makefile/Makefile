.PHONY: install db peer radar report test clean

install:
	pip install -r requirements.txt

db:
	python src/etl/create_database.py

peer:
	python src/analytics/peer.py

radar:
	python src/visualization/radar.py

report:
	python src/reporting/peer_report.py

test:
	python -m pytest

clean:
	@if exist reports\radar_charts del /Q reports\radar_charts\*.png
	@if exist reports\peer_comparison.xlsx del reports\peer_comparison.xlsx