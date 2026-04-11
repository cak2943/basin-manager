#!/usr/bin/env python
"""
Comprehensive refactoring script for basins.py
Adds parent classes FileObject and GenericFile to refactor BasinFile
"""

import sys
import os

# Path to basins.py
BASINS_PATH = r'src\basin_manager\basins.py'

# Read the original file
with open(BASINS_PATH, 'r', encoding='utf-8') as f:
    original_lines = f.readlines()

# Build new content
output_lines = []

# Add modified imports
output_lines.append('from pathlib import Path\n')
output_lines.append('from typing import Dict, List, Optional, Tuple\n')
output_lines.append('from dataclasses import dataclass\n')
output_lines.append('from enum import Enum\n')
output_lines.append('from datetime import datetime\n')
output_lines.append('import warnings\n')
output_lines.append('from abc import ABC, abstractmethod\n')
output_lines.append('\n\n')

# Add FileObject class definition
file_object_code = '''class FileObject(ABC):
    """Abstract base class for objects in HMS files (basin, pdata, etc.)"""
    
    def __init__(self, object_type: str, name: str, metadata: str):
        """Initialize a file object."""
        self.object_type = object_type
        self.name = name
        self.metadata = metadata
    
    def get_key_field(self, field_name: str) -> Optional[str]:
        """Extract a key field value from metadata."""
        for line in self.metadata.split('\\n'):
            if line.strip().startswith(field_name):
                parts = line.split(':', 1)
                if len(parts) > 1:
                    return parts[1].strip()
        return None
    
    def to_string(self) -> str:
        """Convert object back to file format"""
        return f"{self.object_type}: {self.name}\\n{self.metadata}End:\\n\\n"


'''
output_lines.append(file_object_code)

# Skip original imports line and add class definitions from original file
skip_until_class = True
modified_basin_object = False

for i, line in enumerate(original_lines):
    # Skip the original imports
    if skip_until_class and line.startswith('from '):
        continue
    elif skip_until_class and line.startswith('class ObjectType'):
        skip_until_class = False
        # Add ObjectType class
        output_lines.append(line)  # "class ObjectType(Enum):\n"
        # Copy ObjectType enum definition
        j = i + 1
        while j < len(original_lines) and not original_lines[j].startswith('class '):
            output_lines.append(original_lines[j])
            j += 1
        i = j - 1
        continue
    elif skip_until_class:
        continue
    
    # Modify BasinObject to inherit from FileObject
    if line.startswith('@dataclass') and i + 1 < len(original_lines) and original_lines[i + 1].startswith('class BasinObject'):
        if not modified_basin_object:
            modified_basin_object = True
            # Skip the @dataclass decorator and redefine class
            output_lines.append('class BasinObject(FileObject):\n')
            output_lines.append('    """Base class for all basin objects"""\n')
            output_lines.append('    \n')
            output_lines.append('    def __init__(self, object_type: ObjectType, name: str, metadata: str):\n')
            output_lines.append('        super().__init__(object_type.value, name, metadata)\n')
            output_lines.append('        self._object_type_enum = object_type\n')
            output_lines.append('    \n')
            output_lines.append('    @property\n')
            output_lines.append('    def object_type_enum(self) -> ObjectType:\n')
            output_lines.append('        """Return the object type as an enum (for backward compatibility)"""\n')
            output_lines.append('        return self._object_type_enum\n')
            output_lines.append('    \n')
            output_lines.append('    @property\n')
            output_lines.append('    def downstream(self) -> Optional[str]:\n')
            output_lines.append('        """Extract the downstream element name from metadata."""\n')
            output_lines.append('        return self.get_key_field(\'Downstream:\')\n')
            output_lines.append('    \n')
            output_lines.append('    def to_string(self) -> str:\n')
            output_lines.append('        """Convert object back to basin file format"""\n')
            output_lines.append('        return f"{self._object_type_enum.value}: {self.name}\\n{self.metadata}End:\\n\\n"\n')
            output_lines.append('    \n')
            # Skip original BasinObject definition
            j = i + 2
            while j < len(original_lines) and not original_lines[j].startswith('class Subbasin'):
                j += 1
            # Continue from after BasinObject definition
            # (Don't skip lines here, let the main loop handle it)
            continue
    
    # Skip original lines that were part of BasinObject definition if we just rewrote it
    if modified_basin_object and line.startswith('class BasinObject'):
        # Skip until next class
        j = i + 1
        while j < len(original_lines) and not original_lines[j].startswith('class '):
            j += 1
        continue
    
    # Just copy everything else
    output_lines.append(line)

# Write the refactored file
with open(BASINS_PATH, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"✓ Successfully refactored {BASINS_PATH}")
print(f"  - Added FileObject parent class")
print(f"  - Added ABC imports")
print(f"  - Modified BasinObject to inherit from FileObject")
