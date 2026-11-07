import csv
import json
from collections import Counter
from pathlib import Path
from statistics import mean, median, quantiles

MISSING = {"", "null", "none", "na", "n/a"}

def is_missing(value):
    return value is None or value.strip().lower() in MISSING

def profile_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        columns = reader.fieldnames
        if not columns or any(not col for col in columns) or len(set(columns)) != len(columns):
            raise ValueError("CSV must have non-empty, unique column headers")
        rows = []
        for line, row in enumerate(reader, start=2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"Malformed CSV row at line {line}: wrong number of columns")
            rows.append(row)
    duplicates = len(rows) - len({tuple(row[c] for c in columns) for row in rows})
    results = {}
    for column in columns:
        values = [row[column] for row in rows]
        present = [value.strip() for value in values if not is_missing(value)]
        numeric = []
        for value in present:
            try:
                number = float(value)
                if number != number or number in (float("inf"), float("-inf")):
                    raise ValueError()
                numeric.append(number)
            except ValueError:
                pass
        is_numeric = bool(present) and len(numeric) == len(present)
        info = {"missing": len(values)-len(present),"unique_nonmissing":len(set(present)),"type":"numeric" if is_numeric else "categorical"}
        if is_numeric:
            info["summary"]={"min":min(numeric),"max":max(numeric),"mean":round(mean(numeric),4),"median":median(numeric)}
            if len(numeric)>=4:
                q1,_,q3=quantiles(numeric,n=4,method="inclusive")
                iqr=q3-q1; lower=q1-1.5*iqr; upper=q3+1.5*iqr
                info["iqr_outliers"]=sum(value<lower or value>upper for value in numeric)
            else:
                info["iqr_outliers"]=None
        else:
            info["top_values"]=[{"value":value,"count":count} for value,count in Counter(present).most_common(5)]
        results[column]=info
    return {"source":Path(path).name,"row_count":len(rows),"column_count":len(columns),"duplicate_rows":duplicates,"columns":results}

def write_report(report, output):
    Path(output).write_text(json.dumps(report,indent=2,allow_nan=False)+"\n",encoding="utf-8")
