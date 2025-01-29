#!/usr/bin/env python3
import argparse
import json
import os
import sys
import requests
from typing import Optional

def download_gong_spec() -> dict:
    """
    Download the Gong API specification.
    
    Returns:
        The API specification as a dictionary.
    """
    url = "https://gong.app.gong.io/ajax/settings/api/documentation/specs?version="
    
    try:
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading API spec: {e}", file=sys.stderr)
        sys.exit(1)

def save_spec(spec: dict, output_file: str) -> None:
    """
    Save the API specification to a file.
    
    Args:
        spec: The API specification dictionary
        output_file: Path to save the file
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(spec, f, indent=2)
        print(f"Saved API specification to {output_file}")
    except IOError as e:
        print(f"Error saving API spec: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Download Gong API specification')
    parser.add_argument('--output', default='gong-openapi.json',
                       help='Output file (default: gong-openapi.json)')
    
    args = parser.parse_args()
    
    print("Downloading Gong API specification...")
    spec = download_gong_spec()
    save_spec(spec, args.output)

if __name__ == '__main__':
    main()
