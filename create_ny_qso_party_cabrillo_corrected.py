#!/usr/bin/env python3

import PyPDF2
import re
from datetime import datetime

def extract_pdf_text(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return None

def parse_qso_log(log_text):
    """Parse QSO data from the extracted log text"""
    qsos = []
    
    # Pattern from the log: QSO:21027CW202510181451K4GSX599GAWB2SIH599WAR
    # Let's break this down more carefully:
    # QSO:21027CW202510181451K4GSX599GA + WB2SIH599WAR
    
    # More precise pattern to capture the structure
    qso_pattern = r'QSO:(\d+)(CW|PH|FM|RY|DG)(\d{4})(\d{2})(\d{2})(\d{4})K4GSX599GA([A-Z0-9/]+?)599([A-Z]{3})'
    
    matches = re.findall(qso_pattern, log_text)
    
    for match in matches:
        freq, mode, year, month, day, time, their_call, rcvd_exch = match
        
        # Format date as YYYY-MM-DD
        date = f"{year}-{month}-{day}"
        
        qso = {
            'freq': freq,
            'mode': mode,
            'date': date,
            'time': time,
            'my_call': 'K4GSX',
            'rst_sent': '599',
            'sent_exchange': 'GA',
            'their_call': their_call,
            'rst_rcvd': '599',
            'rcvd_exchange': rcvd_exch
        }
        qsos.append(qso)
    
    return qsos

def remove_duplicates(qsos):
    """Remove duplicate QSOs based on callsign, band, and mode"""
    seen = set()
    unique_qsos = []
    
    for qso in qsos:
        # Create a key for duplicate detection - same call on same band
        freq = int(qso['freq'])
        if freq >= 21000:
            band = "15m"
        elif freq >= 14000:
            band = "20m"
        elif freq >= 7000:
            band = "40m"
        else:
            band = "other"
            
        key = (qso['their_call'], band, qso['mode'])
        
        if key not in seen:
            seen.add(key)
            unique_qsos.append(qso)
    
    return unique_qsos

def calculate_score(qsos):
    """Calculate basic score - 1 point per QSO"""
    return len(qsos)

def create_cabrillo_file(qsos, callsign="K4GSX"):
    """Create properly formatted Cabrillo file for NY QSO Party"""
    
    # Remove duplicates
    unique_qsos = remove_duplicates(qsos)
    
    # Sort by date and time
    unique_qsos.sort(key=lambda x: (x['date'], x['time']))
    
    # Calculate score
    score = calculate_score(unique_qsos)
    
    # Header lines
    cabrillo_lines = [
        "START-OF-LOG: 3.0",
        f"CALLSIGN: {callsign}",
        "CONTEST: NY-QSO-PARTY",
        "CATEGORY-OPERATOR: SINGLE-OP",
        "CATEGORY-ASSISTED: NON-ASSISTED",
        "CATEGORY-BAND: ALL",
        "CATEGORY-MODE: CW",
        "CATEGORY-POWER: HIGH",
        "CATEGORY-STATION: FIXED",
        "CATEGORY-TRANSMITTER: ONE",
        f"CLAIMED-SCORE: {score}",
        f"CLUB: ",
        f"OPERATORS: {callsign}",
        f"NAME: ",
        f"ADDRESS: ",
        f"ADDRESS-CITY: ",
        f"ADDRESS-STATE-PROVINCE: GA",
        f"ADDRESS-POSTALCODE: ",
        f"ADDRESS-COUNTRY: UNITED STATES",
        f"EMAIL: ",
        f"CREATED-BY: Python NY QSO Party Cabrillo Generator",
        ""
    ]
    
    # Add QSO lines in proper Cabrillo format
    for qso in unique_qsos:
        # Format: QSO: freq mode date time mycall rst_sent sent_exch theircall rst_rcvd rcvd_exch
        qso_line = f"QSO: {qso['freq']:>5} {qso['mode']:>2} {qso['date']} {qso['time']} {qso['my_call']:<13} {qso['rst_sent']:>3} {qso['sent_exchange']:<6} {qso['their_call']:<13} {qso['rst_rcvd']:>3} {qso['rcvd_exchange']:<6}"
        cabrillo_lines.append(qso_line)
    
    cabrillo_lines.append("END-OF-LOG:")
    
    return "\n".join(cabrillo_lines), unique_qsos

def main():
    print("NY QSO Party Cabrillo File Generator - CORRECTED VERSION")
    print("=" * 60)
    
    # Extract QSO log
    log_pdf = "/Users/rushealy/Downloads/NY QSO PARTY.2025.K4GSX.pdf"
    print("Extracting QSO log from PDF...")
    log_text = extract_pdf_text(log_pdf)
    
    if not log_text:
        print("ERROR: Could not extract log data from PDF")
        return
    
    print("Parsing QSO data...")
    qsos = parse_qso_log(log_text)
    
    print(f"Found {len(qsos)} total QSOs")
    
    if len(qsos) == 0:
        print("ERROR: No QSOs found in log")
        # Show sample of text for debugging
        print("\nSample text from log:")
        sample_lines = log_text.split('\n')[:5]
        for line in sample_lines:
            if 'QSO:' in line:
                print(f"Sample QSO line: {line[:100]}...")
        return
    
    print("\nCreating Cabrillo file...")
    cabrillo_content, unique_qsos = create_cabrillo_file(qsos, "K4GSX")
    
    print(f"After removing duplicates: {len(unique_qsos)} QSOs")
    
    # Show first few QSOs for verification
    print("\nFirst 5 QSOs:")
    for i, qso in enumerate(unique_qsos[:5]):
        print(f"{i+1:3d}: {qso['date']} {qso['time']} {qso['freq']:>5} {qso['mode']} {qso['their_call']:<12} RST:{qso['rst_rcvd']} {qso['rcvd_exchange']}")
    
    if len(unique_qsos) > 5:
        print(f"\nLast 5 QSOs:")
        for i, qso in enumerate(unique_qsos[-5:], len(unique_qsos)-4):
            print(f"{i:3d}: {qso['date']} {qso['time']} {qso['freq']:>5} {qso['mode']} {qso['their_call']:<12} RST:{qso['rst_rcvd']} {qso['rcvd_exchange']}")
    
    # Write Cabrillo file
    output_file = "/Users/rushealy/K4GSX_NY_QSO_PARTY_2025_CORRECTED.log"
    with open(output_file, 'w') as f:
        f.write(cabrillo_content)
    
    print(f"\nCabrillo file created: {output_file}")
    print(f"Total QSOs: {len(unique_qsos)}")
    print(f"Claimed Score: {calculate_score(unique_qsos)}")
    
    # Show summary by band
    bands = {}
    for qso in unique_qsos:
        freq = int(qso['freq'])
        if freq >= 21000:
            band = "15m"
        elif freq >= 14000:
            band = "20m"
        elif freq >= 7000:
            band = "40m"
        else:
            band = f"{freq}kHz"
        
        bands[band] = bands.get(band, 0) + 1
    
    print("\nQSOs by band:")
    for band, count in sorted(bands.items()):
        print(f"  {band}: {count}")
    
    # Show counties worked
    counties = set()
    for qso in unique_qsos:
        counties.add(qso['rcvd_exchange'])
    
    print(f"\nCounties worked: {len(counties)}")
    print("Counties:", ", ".join(sorted(counties)))
    
    # Show sample QSO lines from Cabrillo file
    print(f"\nSample QSO lines from Cabrillo file:")
    lines = cabrillo_content.split('\n')
    qso_lines = [line for line in lines if line.startswith('QSO:')]
    for i, line in enumerate(qso_lines[:3]):
        print(f"  {line}")
    
    print(f"\n" + "="*60)
    print("CABRILLO FILE READY FOR SUBMISSION!")
    print(f"File: {output_file}")
    print(f"QSOs: {len(unique_qsos)}")
    print(f"Counties: {len(counties)}")
    print("="*60)

if __name__ == "__main__":
    main()
