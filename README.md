# Automated Data Analytics Toolkit

Dependency-light Python toolkit for profiling CSV datasets and generating structured JSON reports.

## Features
- Row/column counts
- Missing values
- Duplicate rows
- Numeric/categorical detection
- Min/max/mean/median
- IQR outlier flags
- Top categorical values
- JSON export

The tool is non-destructive and does not automatically delete or impute data.

## Quick start
```bash
python -m pip install -e .
analyze-csv examples/retail_sample.csv --output report.json
python -m unittest discover -s tests -v
```

## License
MIT
