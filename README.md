# New York QSO Party Cabrillo Fixer

A Python tool to convert PDF contest logs to valid Cabrillo format files for the New York QSO Party contest.

## Overview

This project extracts QSO data from PDF log files and generates properly formatted Cabrillo submission files compliant with the New York QSO Party rules.

## Features

- Extracts QSO data from PDF log files using PyPDF2
- Parses contest log format: frequency, mode, date/time, callsigns, and exchanges
- Removes duplicate QSOs (same station on same band) **Note: Not a desirable feature--will be removed on next release**
- Generates valid Cabrillo 3.0 format files
- Provides contest summary with band breakdown and counties worked
- Compliant with 2025 NY QSO Party rules

## Requirements

- Python 3.x
- PyPDF2 library

## Installation

1. Clone this repository:
```bash
git clone [<repository-url>](https://github.com/rusk2ua/nyqp-cabrillo-fixer)
cd nyqp-cabrillo-fixer
```

2. Create virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install PyPDF2
```

## Usage

1. Place your contest log PDF file in the project directory
2. Update the PDF file path in the script
3. Run the generator:
```bash
python3 create_ny_qso_party_cabrillo_corrected.py
```

## Output Files

- **Cabrillo Log**: `CALLSIGN_NY_QSO_PARTY_YYYY_CORRECTED.log`
- **Contest Summary**: `NY_QSO_Party_YYYY_Summary.txt`
- **Extracted Log Text**: `ny_qso_party_log.txt`
- **Extracted Rules Text**: `ny_qso_party_rules.txt`

## Example Results

For K4GSX 2025 entry:
- **Total QSOs**: 61 (after duplicate removal)
- **Counties Worked**: 23 NY counties
- **Bands**: 15m (22), 20m (33), 40m (6)
- **Mode**: CW only

## Cabrillo Format

The generated file includes:
- Proper contest identifier: `NY-QSO-PARTY`
- Standard Cabrillo 3.0 headers
- Correct QSO line formatting
- Appropriate category classifications

## Contest Rules Compliance

Generated files comply with New York QSO Party requirements:
- Correct band designators (kHz for HF, MHz for VHF+)
- Proper mode codes (CW, PH, FM, RY, DG)
- Valid exchange formats (RST + State/County)
- Chronological QSO ordering

## File Structure

```
nyqp-cabrillo-project/
├── README.md
├── create_ny_qso_party_cabrillo_corrected.py
├── ny_qso_party_log.txt
├── ny_qso_party_rules.txt
├── K4GSX_NY_QSO_PARTY_2025_CORRECTED.log
└── NY_QSO_Party_2025_Summary.txt
```

## License

This project is open source. Feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues or questions, please open a GitHub issue.
