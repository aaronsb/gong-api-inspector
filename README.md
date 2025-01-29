# API Inspector

A command-line tool for efficiently exploring and understanding OpenAPI specifications. Particularly useful for coding agents and developers working with API documentation.

## Features

- Taxonomically organized API exploration
- Multiple grouping options (by path, method, or tag)
- Search functionality for finding specific endpoints
- Detailed endpoint information
- Authentication requirements inspection
- Schema definition viewing
- Support for multiple API platforms

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install requests
   ```
3. Make the scripts executable:
   ```bash
   chmod +x inspector.py download_gong_api_spec.py
   ```

## Downloading API Specifications

Use the `download_gong_api_spec.py` script to download the Gong API specification:

```bash
# Download Gong API spec
./download_gong_api_spec.py

# Specify custom output file (optional)
./download_gong_api_spec.py --output custom-openapi.json
```

## Usage

The inspector provides simple commands to explore the API:

```bash
# List all endpoint groups (e.g., Users, Calls, Stats)
./inspector.py --list-groups

# View detailed description of a specific endpoint group
./inspector.py --describe-group users

# View all endpoints in a category
./inspector.py --category users

# Search across all endpoints
./inspector.py --search "recording"

# View API overview
./inspector.py --info

# Check authentication requirements
./inspector.py --auth

# View data models
./inspector.py --schema "Call"
```

For more detailed organization:
```bash
# List all endpoints with grouping
./inspector.py --list --grouped-by tag   # Group by category
./inspector.py --list --grouped-by path  # Group by URL structure
./inspector.py --list --grouped-by method # Group by HTTP method

# View specific endpoint details
./inspector.py --endpoint "/v2/calls"

# Use a specific spec file (optional)
./inspector.py --spec-file custom-openapi.json --category users
```

The inspector automatically uses the first `*-openapi.json` file it finds in the current directory, so you don't need to specify the file unless you want to use a different one.

## File Naming Convention

API specification files should follow the naming pattern:
```
[platform]-openapi.json
```

For example:
- gong-openapi.json
- salesforce-openapi.json
- github-openapi.json

## Error Handling

The tool includes robust error handling for:
- File not found
- Invalid JSON
- Invalid endpoint paths
- Missing authentication
- Memory constraints

## For Coding Agents

The taxonomic organization makes it easy to:
1. Get an overview of available endpoints (--list)
2. Understand the API structure (--grouped-by)
3. Find specific functionality (--search)
4. Get detailed specifications (--endpoint)
5. Verify authentication requirements (--auth)
6. Access data models (--schema)

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

## License

MIT License
