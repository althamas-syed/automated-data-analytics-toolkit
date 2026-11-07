import argparse
import json
from .core import profile_csv, write_report

def main(argv=None):
    parser=argparse.ArgumentParser(description="Non-destructive CSV data profiling")
    parser.add_argument("csv_file")
    parser.add_argument("--output",default="analytics_report.json")
    args=parser.parse_args(argv)
    try:
        report=profile_csv(args.csv_file)
        write_report(report,args.output)
    except (OSError,ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps({"rows":report["row_count"],"duplicates":report["duplicate_rows"],"report":args.output},indent=2))

if __name__=="__main__":
    main()
