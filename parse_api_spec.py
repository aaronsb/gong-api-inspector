#!/usr/bin/env python3
import json
import sys
import argparse
from typing import Dict, Any

def parse_openapi_spec(file_path: str) -> Dict[str, Any]:
    """
    Parse OpenAPI specification from JSON file.
    Returns the parsed data structure.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

def extract_endpoints(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract and organize API endpoints from the OpenAPI specification.
    Returns a simplified structure focusing on endpoints and their details.
    """
    endpoints = {}
    
    # Extract paths and their operations
    for path, path_data in spec.get('paths', {}).items():
        endpoints[path] = {}
        
        # Process each HTTP method (get, post, etc.)
        for method, operation in path_data.items():
            if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                endpoints[path][method] = {
                    'summary': operation.get('summary', ''),
                    'description': operation.get('description', ''),
                    'parameters': operation.get('parameters', []),
                    'requestBody': operation.get('requestBody', {}),
                    'responses': operation.get('responses', {})
                }
    
    return endpoints

def print_api_info(spec: Dict[str, Any]) -> None:
    """Print basic API information."""
    info = spec.get('info', {})
    print("API Information:")
    print(f"Title: {info.get('title', '')}")
    print(f"Version: {info.get('version', '')}")
    print("\nDescription:")
    print(info.get('description', ''))

def list_endpoints(endpoints: Dict[str, Any], method: str = None) -> None:
    """List all endpoints, optionally filtered by HTTP method."""
    print("Available Endpoints:")
    for path, methods in endpoints.items():
        if method:
            if method.lower() in methods:
                print(f"{path} [{method.upper()}]: {methods[method.lower()]['summary']}")
        else:
            print(f"\n{path}")
            for http_method, details in methods.items():
                print(f"  {http_method.upper()}: {details['summary']}")

def show_endpoint_details(endpoints: Dict[str, Any], path: str) -> None:
    """Show detailed information about a specific endpoint."""
    if path not in endpoints:
        print(f"Endpoint {path} not found", file=sys.stderr)
        return

    print(f"Endpoint: {path}")
    for method, details in endpoints[path].items():
        print(f"\nMethod: {method.upper()}")
        print(f"Summary: {details['summary']}")
        print(f"Description: {details['description']}")
        
        if details['parameters']:
            print("\nParameters:")
            for param in details['parameters']:
                print(f"  {param.get('name')} ({param.get('in')})")
                print(f"    Description: {param.get('description', '')}")
                print(f"    Required: {param.get('required', False)}")
        
        if details['requestBody']:
            print("\nRequest Body:")
            print(json.dumps(details['requestBody'], indent=2))
        
        if details['responses']:
            print("\nResponses:")
            for status, response in details['responses'].items():
                print(f"  {status}: {response.get('description', '')}")

def main():
    parser = argparse.ArgumentParser(description='Parse and display OpenAPI specification')
    parser.add_argument('file', help='Path to the OpenAPI specification JSON file')
    parser.add_argument('--info', action='store_true', help='Show API information')
    parser.add_argument('--list', action='store_true', help='List all endpoints')
    parser.add_argument('--method', help='Filter by HTTP method (GET, POST, etc.)')
    parser.add_argument('--endpoint', help='Show details for specific endpoint')
    
    args = parser.parse_args()

    # Parse the full specification
    spec = parse_openapi_spec(args.file)
    endpoints = extract_endpoints(spec)

    # Handle different display options
    if args.info:
        print_api_info(spec)
    elif args.endpoint:
        show_endpoint_details(endpoints, args.endpoint)
    elif args.list:
        list_endpoints(endpoints, args.method)
    else:
        # Default to showing API info and listing endpoints
        print_api_info(spec)
        print("\n" + "="*80 + "\n")
        list_endpoints(endpoints, args.method)

if __name__ == '__main__':
    main()
