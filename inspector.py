#!/usr/bin/env python3
import json
import sys
import argparse
import os
from typing import Dict, Any, List
from collections import defaultdict

def parse_openapi_spec(file_path: str) -> Dict[str, Any]:
    """Parse OpenAPI specification from JSON file."""
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
    """Extract and organize API endpoints from the OpenAPI specification."""
    endpoints = {}
    
    for path, path_data in spec.get('paths', {}).items():
        endpoints[path] = {}
        
        for method, operation in path_data.items():
            if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                endpoints[path][method] = {
                    'summary': operation.get('summary', ''),
                    'description': operation.get('description', ''),
                    'parameters': operation.get('parameters', []),
                    'requestBody': operation.get('requestBody', {}),
                    'responses': operation.get('responses', {}),
                    'tags': operation.get('tags', []),
                    'operationId': operation.get('operationId', '')
                }
    
    return endpoints

def group_by_path(endpoints: Dict[str, Any]) -> Dict[str, Any]:
    """Group endpoints by their path hierarchy."""
    grouped = defaultdict(dict)
    for path, methods in endpoints.items():
        parts = path.strip('/').split('/')
        current = grouped
        for part in parts:
            if part not in current:
                current[part] = defaultdict(dict)
            current = current[part]
        current['_methods'] = methods
    return grouped

def group_by_method(endpoints: Dict[str, Any]) -> Dict[str, List[str]]:
    """Group endpoints by HTTP method."""
    grouped = defaultdict(list)
    for path, methods in endpoints.items():
        for method in methods:
            grouped[method.upper()].append(path)
    return grouped

def group_by_tag(endpoints: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """Group endpoints by their tags."""
    grouped = defaultdict(list)
    for path, methods in endpoints.items():
        for method, details in methods.items():
            tags = details.get('tags', ['untagged'])
            for tag in tags:
                grouped[tag].append({
                    'path': path,
                    'method': method.upper(),
                    'summary': details['summary']
                })
    return grouped

def print_api_info(spec: Dict[str, Any]) -> None:
    """Print basic API information."""
    info = spec.get('info', {})
    print("\nAPI Information:")
    print(f"Title: {info.get('title', '')}")
    print(f"Version: {info.get('version', '')}")
    print(f"\nDescription:")
    print(info.get('description', ''))

def print_auth_info(spec: Dict[str, Any]) -> None:
    """Print authentication information."""
    security = spec.get('security', [])
    components = spec.get('components', {})
    security_schemes = components.get('securitySchemes', {})
    
    print("\nAuthentication Requirements:")
    if not security and not security_schemes:
        print("No authentication information specified")
        return
        
    for scheme_name, scheme in security_schemes.items():
        print(f"\n{scheme_name}:")
        print(f"Type: {scheme.get('type', '')}")
        print(f"Description: {scheme.get('description', '')}")
        if scheme.get('scheme'):
            print(f"Scheme: {scheme['scheme']}")
        if scheme.get('bearerFormat'):
            print(f"Bearer Format: {scheme['bearerFormat']}")

def print_schema(spec: Dict[str, Any], schema_name: str) -> None:
    """Print details of a specific schema."""
    schemas = spec.get('components', {}).get('schemas', {})
    if schema_name not in schemas:
        print(f"Schema '{schema_name}' not found", file=sys.stderr)
        return
        
    schema = schemas[schema_name]
    print(f"\nSchema: {schema_name}")
    print(json.dumps(schema, indent=2))

def search_endpoints(endpoints: Dict[str, Any], pattern: str) -> None:
    """Search endpoints by pattern."""
    import re
    pattern = re.compile(pattern, re.IGNORECASE)
    
    print("\nMatching Endpoints:")
    for path, methods in endpoints.items():
        if pattern.search(path):
            print(f"\n{path}")
            for method, details in methods.items():
                print(f"  {method.upper()}: {details['summary']}")
                continue
                
        for method, details in methods.items():
            if (pattern.search(details['summary']) or 
                pattern.search(details['description'])):
                print(f"\n{path}")
                print(f"  {method.upper()}: {details['summary']}")
                break

def print_grouped_endpoints(grouped: Dict[str, Any], indent: int = 0) -> None:
    """Print endpoints in a hierarchical structure."""
    for key, value in sorted(grouped.items()):
        if key == '_methods':
            for method, details in value.items():
                print(f"{'  ' * indent}{method.upper()}: {details['summary']}")
        else:
            print(f"{'  ' * indent}{key}/")
            print_grouped_endpoints(value, indent + 1)

def show_endpoint_details(endpoints: Dict[str, Any], path: str) -> None:
    """Show detailed information about a specific endpoint."""
    if path not in endpoints:
        print(f"Endpoint {path} not found", file=sys.stderr)
        return

    print(f"\nEndpoint: {path}")
    for method, details in endpoints[path].items():
        print(f"\nMethod: {method.upper()}")
        print(f"Summary: {details['summary']}")
        print(f"Description: {details['description']}")
        
        if details['tags']:
            print(f"Tags: {', '.join(details['tags'])}")
        
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

def show_category_details(spec: Dict[str, Any], endpoints: Dict[str, Any], category: str) -> None:
    """Show all endpoints and their details for a specific category/tag."""
    grouped = group_by_tag(endpoints)
    
    # Handle case-insensitive matching and partial matches
    matches = [tag for tag in grouped.keys() 
              if category.lower() in tag.lower()]
    
    if not matches:
        print(f"No category found matching '{category}'")
        print("\nAvailable categories:")
        for tag in sorted(grouped.keys()):
            print(f"- {tag}")
        return

    # If multiple matches, show options
    if len(matches) > 1:
        print(f"Multiple categories match '{category}':")
        for tag in matches:
            print(f"- {tag}")
        return

    tag = matches[0]
    print(f"\n=== {tag} API Endpoints ===\n")
    
    # First show a summary
    print("Summary:")
    for endpoint in sorted(grouped[tag], key=lambda x: x['path']):
        print(f"{endpoint['method']} {endpoint['path']}")
        print(f"  {endpoint['summary']}\n")
    
    # Then show details for each endpoint
    print("\nDetailed Specifications:")
    for endpoint in sorted(grouped[tag], key=lambda x: x['path']):
        print("\n" + "="*80 + "\n")
        show_endpoint_details(endpoints, endpoint['path'])

def find_spec_file() -> str:
    """Find the first *-openapi.json file in the current directory."""
    import glob
    
    files = glob.glob('*-openapi.json')
    if not files:
        print("Error: No *-openapi.json file found in current directory", 
              file=sys.stderr)
        sys.exit(1)
    return files[0]

def print_endpoint_groups(spec: Dict[str, Any]) -> None:
    """Print all available endpoint groups (tags) from the API specification."""
    tags = spec.get('tags', [])
    if not tags:
        print("No endpoint groups found in the API specification")
        return

    print("\nAvailable Endpoint Groups:")
    for tag in tags:
        print(f"- {tag['name']}")

def print_endpoint_group_description(spec: Dict[str, Any], group_name: str) -> None:
    """Print detailed description for a specific endpoint group."""
    tags = spec.get('tags', [])
    
    # Case-insensitive matching
    matches = [tag for tag in tags if tag['name'].lower() == group_name.lower()]
    if not matches:
        # Try partial matching if no exact match
        matches = [tag for tag in tags if group_name.lower() in tag['name'].lower()]
        
    if not matches:
        print(f"No endpoint group found matching '{group_name}'")
        print("\nAvailable groups:")
        for tag in tags:
            print(f"- {tag['name']}")
        return
    
    if len(matches) > 1:
        print(f"Multiple endpoint groups match '{group_name}':")
        for tag in matches:
            print(f"- {tag['name']}")
        return

    tag = matches[0]
    print(f"\n=== {tag['name']} API Endpoints ===\n")
    
    # The description is in HTML format, but we'll display it as-is since
    # it's relatively readable even with HTML tags
    print(tag['description'])

def main():
    parser = argparse.ArgumentParser(
        description='''
API Inspector - A tool for exploring and understanding OpenAPI specifications

This tool helps you navigate and understand API documentation by providing:
- Category-based exploration of endpoints
- Detailed endpoint information and schemas
- Authentication requirements
- Search capabilities
- Multiple organization views
''',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('--spec-file', 
                       help='Path to the OpenAPI specification JSON file. If not provided, '
                            'uses the first *-openapi.json file in the current directory')
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list', action='store_true',
                      help='List all available endpoints with their summaries')
    group.add_argument('--info', action='store_true',
                      help='Display general API information including title, version, and description')
    group.add_argument('--auth', action='store_true',
                      help='Show API authentication requirements and security schemes')
    group.add_argument('--endpoint',
                      help='Show detailed information about a specific endpoint (e.g., "/users/{id}")')
    group.add_argument('--schema',
                      help='Display a specific schema definition from the API specification')
    group.add_argument('--search',
                      help='Search endpoints by pattern in path, summary, or description')
    group.add_argument('--category',
                      help='Show all endpoints and details for a specific category/tag (e.g., "users", "calls")')
    group.add_argument('--list-groups', action='store_true',
                      help='List all available endpoint groups')
    group.add_argument('--describe-group',
                      help='Show detailed description for a specific endpoint group')
    
    parser.add_argument('--grouped-by',
                       choices=['path', 'method', 'tag'],
                       help='Group endpoints by: path (hierarchical), method (GET/POST/etc), or tag (functional category)')
    parser.add_argument('--method',
                       help='Filter endpoints by HTTP method (GET, POST, PUT, DELETE, PATCH)')
    
    args = parser.parse_args()

    # Use provided spec file or find one automatically
    spec_file = args.spec_file or find_spec_file()

    # Validate spec file follows naming convention
    if not spec_file.endswith('-openapi.json'):
        print("Warning: Spec file should follow the naming pattern: "
              "[platform]-openapi.json", file=sys.stderr)

    # Parse the specification
    spec = parse_openapi_spec(spec_file)
    endpoints = extract_endpoints(spec)

    # Handle different display options
    if args.info:
        print_api_info(spec)
    elif args.auth:
        print_auth_info(spec)
    elif args.schema:
        print_schema(spec, args.schema)
    elif args.endpoint:
        show_endpoint_details(endpoints, args.endpoint)
    elif args.search:
        search_endpoints(endpoints, args.search)
    elif args.category:
        show_category_details(spec, endpoints, args.category)
    elif args.list_groups:
        print_endpoint_groups(spec)
    elif args.describe_group:
        print_endpoint_group_description(spec, args.describe_group)
    elif args.list:
        if args.grouped_by == 'path':
            grouped = group_by_path(endpoints)
            print("\nEndpoints by Path:")
            print_grouped_endpoints(grouped)
        elif args.grouped_by == 'method':
            grouped = group_by_method(endpoints)
            print("\nEndpoints by Method:")
            for method, paths in sorted(grouped.items()):
                if not args.method or args.method.upper() == method:
                    print(f"\n{method}:")
                    for path in sorted(paths):
                        print(f"  {path}")
        elif args.grouped_by == 'tag':
            grouped = group_by_tag(endpoints)
            print("\nEndpoints by Tag:")
            for tag, endpoints in sorted(grouped.items()):
                print(f"\n{tag}:")
                for endpoint in sorted(endpoints, key=lambda x: x['path']):
                    print(f"  {endpoint['path']} [{endpoint['method']}]")
        else:
            print("\nAvailable Endpoints:")
            for path, methods in sorted(endpoints.items()):
                print(f"\n{path}")
                for method, details in sorted(methods.items()):
                    if not args.method or args.method.upper() == method.upper():
                        print(f"  {method.upper()}: {details['summary']}")
    else:
        # If no arguments provided, show help
        parser.print_help()
        sys.exit(0)

if __name__ == '__main__':
    main()
