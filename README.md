# OpenAPI Spec Parser

A command-line tool for efficiently parsing and exploring OpenAPI specifications. Particularly useful for coding agents and developers working with API documentation.

## Features

- List all available API endpoints
- Filter endpoints by HTTP method
- View detailed endpoint specifications
- Access API overview and authentication details
- Efficient handling of large API specifications
- Clean, structured output format

## Usage

```bash
# Show all endpoints
./parse_api_spec.py api_specs.json --list

# Filter endpoints by HTTP method
./parse_api_spec.py api_specs.json --method GET

# Show details for a specific endpoint
./parse_api_spec.py api_specs.json --endpoint "/v2/calls"

# View API overview and authentication details
./parse_api_spec.py api_specs.json --info
```

## Requirements

- Python 3.x
- No external dependencies

## Installation

1. Clone the repository
2. Make the script executable:
   ```bash
   chmod +x parse_api_spec.py
   ```

## Error Handling

The tool includes robust error handling for:
- File not found
- Invalid JSON
- Invalid endpoint paths
- Memory constraints

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

## License

MIT License
