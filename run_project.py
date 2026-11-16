"""Run the complete data-cleaning and reporting pipeline."""
from pathlib import Path
import argparse
from src.cleaning import save_outputs

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Path to an authorized Excel or CSV file")
    parser.add_argument("--output", type=Path, default=Path("reports"), help="Directory for visual reports")
    parser.add_argument("--processed", type=Path, default=Path("data/processed"), help="Directory for cleaned data and audit outputs")
    args = parser.parse_args()
    if not args.input.is_file():
        raise SystemExit(f"Input file not found: {args.input}")
    save_outputs(args.input, args.processed)
    from src.analyze import build_visuals
    build_visuals(args.input, args.output)
    print("Cleaning and visual report generation completed.")


if __name__ == "__main__":
    main()
