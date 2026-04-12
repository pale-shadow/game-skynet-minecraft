#!/usr/bin/env python3
import sys
import os

def lint_conf(file_path):
    """
    Validates BlueMap HOCON structural integrity and flags version control conflicts.
    """
    if not os.path.exists(file_path):
        print(f"FATAL: Configuration file not found at {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    errors = []
    brace_count = 0
    bracket_count = 0

    for i, line in enumerate(lines):
        line_num = i + 1
        stripped = line.strip()

        # Catch unresolved Git merge conflicts present in the Bitsmasher repository
        if stripped.startswith("<<<<<<<") or stripped.startswith("=======") or stripped.startswith(">>>>>>>"):
            errors.append(f"Line {line_num}: Unresolved Git merge conflict marker.")

        # Ignore comments for structural balancing
        if not stripped.startswith("#"):
            brace_count += stripped.count('{') - stripped.count('}')
            bracket_count += stripped.count('[') - stripped.count(']')

            if brace_count < 0:
                errors.append(f"Line {line_num}: Unexpected closing brace '}}'.")
                brace_count = 0 
            
            if bracket_count < 0:
                errors.append(f"Line {line_num}: Unexpected closing bracket ']'.")
                bracket_count = 0

    if brace_count > 0:
        errors.append(f"EOF: Missing {brace_count} closing brace(s) '}}'.")
    if bracket_count > 0:
        errors.append(f"EOF: Missing {bracket_count} closing bracket(s) ']'.")

    if errors:
        print(f"LINTING FAILED for {file_path}:")
        for error in errors:
            print(f" - {error}")
        return False

    return True

def format_conf(file_path):
    """
    Applies standard 4-space indentation based on hierarchical depth.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    formatted_lines = []
    indent_level = 0
    indent_spaces = 4

    for line in lines:
        stripped = line.strip()
        
        # Decrease indent for closing boundaries
        if stripped.startswith("}") or stripped.startswith("]"):
            indent_level = max(0, indent_level - 1)

        if stripped:
            formatted_lines.append((" " * (indent_level * indent_spaces)) + stripped + "\n")
        else:
            formatted_lines.append("\n")

        # Increase indent for opening boundaries
        if not stripped.startswith("#"):
            if stripped.endswith("{") or stripped.endswith("["):
                indent_level += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(formatted_lines)
    print(f"SUCCESS: {file_path} validated and formatted.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 -m src.mapping.bluemap_linter <path_to_world.conf>")
        sys.exit(1)
        
    target_file = sys.argv[1]
    
    if lint_conf(target_file):
        format_conf(target_file)
    else:
        sys.exit(1)
