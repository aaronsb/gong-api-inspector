# System Patterns

## Architecture
1. Two-Tool System:
   - Inspector: Main API exploration tool
   - Downloader: Dedicated spec retrieval

2. Design Principles:
   - Single Responsibility
   - Smart Defaults
   - Progressive Disclosure
   - User-Friendly Interface

## Technical Decisions
1. Language & Libraries:
   - Python for excellent JSON handling
   - Requests for HTTP operations
   - Argparse for CLI interface
   - Built-in modules for core functionality

2. File Organization:
   - Platform-specific naming ([platform]-openapi.json)
   - Automatic file detection
   - Clear separation of tools

## Key Patterns
1. Command Pattern:
   - Clear command hierarchy
   - Mutually exclusive options
   - Optional parameters
   - Smart defaults

2. Data Organization:
   - Category-based grouping
   - Path-based hierarchy
   - Method-based filtering
   - Search functionality

3. Output Formatting:
   - Summary views
   - Detailed specifications
   - Consistent styling
   - Clear separation of sections

## Error Handling
1. Robust Validation:
   - File existence checks
   - JSON parsing validation
   - Pattern matching
   - Input validation

2. Clear Error Messages:
   - Descriptive errors
   - Helpful suggestions
   - Proper exit codes
   - User guidance

## Best Practices
1. Code Organization:
   - Modular functions
   - Type hints
   - Clear documentation
   - Consistent formatting

2. User Experience:
   - Smart defaults
   - Progressive complexity
   - Clear help messages
   - Intuitive commands

3. Performance:
   - Efficient JSON parsing
   - Smart data structures
   - Minimal dependencies
   - Resource-conscious operations
