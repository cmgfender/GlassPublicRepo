# Super VLOOKUP with Fuzzy Matching

This script performs a VLOOKUP-like operation between two tables, with support for fuzzy matching to handle slight variations in key values.

## Features

- Merge data from two files based on a common key.
- Supports multiple join types: `left`, `right`, `outer`, and `inner`.
- Fuzzy matching option for approximate key matching.
- Outputs results to a CSV or Excel file.

## Requirements

- Python 3.7+
- pandas
- rapidfuzz
- tkinter

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/super_vlookup.git
   cd super_vlookup
   ```

2. Install required packages:
   ```bash
   pip install pandas rapidfuzz
   ```

## Usage

1. Run the script:
   ```bash
   python super_vlookup.py
   ```

2. Follow the prompts:
   - Select the main table and lookup table files.
   - Specify merge keys and additional columns to return.
   - Choose join type and enable/disable fuzzy matching.
   - Save the merged results.

## Notes

- Supported file formats: CSV, Excel.
- Fuzzy matching threshold defaults to 90 (0-100 scale).

## License

This project is licensed under the MIT License.
