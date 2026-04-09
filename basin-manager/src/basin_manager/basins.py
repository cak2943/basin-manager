from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import warnings


class ObjectType(Enum):
    """Enumeration of basin object types"""
    BASIN = "Basin"
    SUBBASIN = "Subbasin"
    REACH = "Reach"
    JUNCTION = "Junction"
    DIVERSION = "Diversion"
    RESERVOIR = "Reservoir"
    SOURCE = "Source"


@dataclass
class BasinObject:
    """Base class for all basin objects"""
    object_type: ObjectType
    name: str
    metadata: str
    
    @property
    def downstream(self) -> Optional[str]:
        """Extract the downstream element name from metadata.
        
        Returns:
            The downstream element name if found, None otherwise
        """
        for line in self.metadata.split('\n'):
            if line.strip().startswith('Downstream:'):
                parts = line.split(':', 1)
                if len(parts) > 1:
                    return parts[1].strip()
        return None
    
    def to_string(self) -> str:
        """Convert object back to basin file format"""
        return f"{self.object_type.value}: {self.name}\n{self.metadata}End:\n\n"
    
    @staticmethod
    def from_string(content: str) -> Optional['BasinObject']:
        """Parse a basin object from string content"""
        lines = content.strip().split('\n')
        if not lines or ':' not in lines[0]:
            return None
        
        # Parse header
        header_parts = lines[0].split(':', 1)
        if len(header_parts) != 2:
            return None
        
        object_type_str = header_parts[0].strip()
        name = header_parts[1].strip()
        
        # Find matching object type
        try:
            object_type = ObjectType(object_type_str)
        except ValueError:
            return None
        
        # Extract metadata (everything between header and End:)
        metadata_lines = lines[1:-1]  # Exclude header and End:
        metadata = '\n'.join(metadata_lines) + '\n' if metadata_lines else ''
        
        return BasinObject(object_type, name, metadata)


class Subbasin(BasinObject):
    """Represents a Subbasin object"""
    def __init__(self, name: str, metadata: str):
        super().__init__(ObjectType.SUBBASIN, name, metadata)


class Reach(BasinObject):
    """Represents a Reach object"""
    def __init__(self, name: str, metadata: str):
        super().__init__(ObjectType.REACH, name, metadata)


class Junction(BasinObject):
    """Represents a Junction object"""
    def __init__(self, name: str, metadata: str):
        super().__init__(ObjectType.JUNCTION, name, metadata)


class Diversion(BasinObject):
    """Represents a Diversion object"""
    def __init__(self, name: str, metadata: str):
        super().__init__(ObjectType.DIVERSION, name, metadata)


class Reservoir(BasinObject):
    """Represents a Reservoir object"""
    def __init__(self, name: str, metadata: str):
        super().__init__(ObjectType.RESERVOIR, name, metadata)


class Source(BasinObject):
    """Represents a Source object"""
    def __init__(self, name: str, metadata: str):
        super().__init__(ObjectType.SOURCE, name, metadata)


class Basin(BasinObject):
    """Represents a Basin object"""
    def __init__(self, name: str, metadata: str):
        super().__init__(ObjectType.BASIN, name, metadata)


class BasinFile:
    """Class to manage .basin files"""
    
    def __init__(self, filepath: str):
        """Initialize BasinFile with path to .basin file"""
        self.filepath = filepath
        self.objects: List[BasinObject] = []
        self.object_map: Dict[str, BasinObject] = {}
        self.preamble = ""  # Content before first object
        self.postamble = ""  # Content after last object
        
    def read(self) -> None:
        """Read and parse the .basin file"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self._parse_content(content)
    
    def _parse_content(self, content: str) -> None:
        """Parse basin file content into objects"""
        lines = content.split('\n')
        
        current_object_lines = []
        preamble_lines = []
        postamble_lines = []
        in_object = False
        found_first_object = False
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Handle End: inside an object first so it is not treated as a header.
            if in_object and line.strip() == 'End:':
                current_object_lines.append(line)
                self._add_parsed_object('\n'.join(current_object_lines))
                current_object_lines = []
                in_object = False
                found_first_object = True
                # Skip the empty line after End: if it exists
                if i + 1 < len(lines) and lines[i + 1].strip() == '':
                    i += 1
                i += 1
                continue

            # Check if this line starts a new object
            if ':' in line and not line.startswith(' ') and not line.startswith('\t'):
                # This might be an object header
                if current_object_lines:
                    # Process previous object (if file is malformed and no End:)
                    self._add_parsed_object('\n'.join(current_object_lines))
                    current_object_lines = []
                
                # Check if it's a valid object type
                header_parts = line.split(':', 1)
                if header_parts[0].strip() in [obj_type.value for obj_type in ObjectType]:
                    current_object_lines.append(line)
                    in_object = True
                    found_first_object = True
                else:
                    if in_object:
                        current_object_lines.append(line)
                    elif found_first_object:
                        postamble_lines.append(line)
                    else:
                        preamble_lines.append(line)
            else:
                if in_object:
                    current_object_lines.append(line)
                elif found_first_object:
                    postamble_lines.append(line)
                else:
                    preamble_lines.append(line)
            
            i += 1
        
        # Handle any remaining content
        if current_object_lines:
            self._add_parsed_object('\n'.join(current_object_lines))
        
        self.preamble = '\n'.join(preamble_lines)
        self.postamble = '\n'.join(postamble_lines)

    def _add_parsed_object(self, object_str: str) -> None:
        """Parse and add a single object to the collection"""
        lines = object_str.split('\n')
        if not lines or ':' not in lines[0]:
            return
        
        # Parse header
        header_parts = lines[0].split(':', 1)
        if len(header_parts) != 2:
            return
        
        object_type_str = header_parts[0].strip()
        name = header_parts[1].strip()
        
        # Find matching object type
        try:
            object_type = ObjectType(object_type_str)
        except ValueError:
            return
        
        # Extract metadata (everything between header and End:)
        # Find the End: line and include everything between header and End:
        end_index = -1
        for idx in range(len(lines) - 1, -1, -1):
            if lines[idx].strip() == 'End:':
                end_index = idx
                break
        
        if end_index == -1:
            return
        
        # Get all lines between header and End:
        metadata_lines = lines[1:end_index]
        
        metadata = '\n'.join(metadata_lines) + '\n' if metadata_lines else ''
        
        # Create appropriate object type
        if object_type == ObjectType.SUBBASIN:
            obj = Subbasin(name, metadata)
        elif object_type == ObjectType.REACH:
            obj = Reach(name, metadata)
        elif object_type == ObjectType.JUNCTION:
            obj = Junction(name, metadata)
        elif object_type == ObjectType.DIVERSION:
            obj = Diversion(name, metadata)
        elif object_type == ObjectType.RESERVOIR:
            obj = Reservoir(name, metadata)
        elif object_type == ObjectType.SOURCE:
            obj = Source(name, metadata)
        elif object_type == ObjectType.BASIN:
            obj = Basin(name, metadata)
        else:
            return
        
        self.objects.append(obj)
        self.object_map[name] = obj

    def replace_object(self, object_name: str, metadata: str) -> bool:
        """
        Replace an existing object's metadata
        
        Args:
            object_name: Name of the object to replace
            metadata: New metadata string (should not include "End:")
            
        Returns:
            True if replacement was successful, False if object not found
        """
        if object_name not in self.object_map:
            return False
        
        obj = self.object_map[object_name]
        
        # Only strip leading and trailing whitespace, preserve internal whitespace
        metadata = metadata.strip()
        
        # Ensure all metadata lines are properly indented
        metadata_lines = metadata.split('\n')
        indented_lines = []
        for line in metadata_lines:
            # Preserve empty lines but indent non-empty lines
            if line.strip():  # Non-empty line
                indented_lines.append('     ' + line.strip())
            else:  # Empty line
                indented_lines.append('')
        
        metadata = '\n'.join(indented_lines) + '\n' if indented_lines else ''
        
        obj.metadata = metadata
        
        return True

    def add_object(self, object_type: ObjectType, name: str, metadata: str, 
                after_object: str) -> bool:
        """
        Add a new object to the basin file
        
        Args:
            object_type: Type of object to create
            name: Name of the new object
            metadata: Metadata string (should not include "End:")
            after_object: Name of existing object to place new object after
            
        Returns:
            True if object was added successfully, False if after_object not found
        """
        if after_object not in self.object_map:
            return False
        
        # Check if object already exists in target file
        if name in self.object_map:
            warnings.warn(f"Object '{name}' already exists in {self.filepath}. Not adding duplicate.", UserWarning)
            return False
        
        # Only strip leading and trailing whitespace, preserve internal whitespace
        metadata = metadata.strip()
        
        # Ensure all metadata lines are properly indented
        metadata_lines = metadata.split('\n')
        indented_lines = []
        for line in metadata_lines:
            # Preserve empty lines but indent non-empty lines
            if line.strip():  # Non-empty line
                indented_lines.append('     ' + line.strip())
            else:  # Empty line
                indented_lines.append('')
        
        metadata = '\n'.join(indented_lines) + '\n' if indented_lines else ''
        
        # Create appropriate object type
        if object_type == ObjectType.SUBBASIN:
            new_obj = Subbasin(name, metadata)
        elif object_type == ObjectType.REACH:
            new_obj = Reach(name, metadata)
        elif object_type == ObjectType.JUNCTION:
            new_obj = Junction(name, metadata)
        elif object_type == ObjectType.DIVERSION:
            new_obj = Diversion(name, metadata)
        elif object_type == ObjectType.RESERVOIR:
            new_obj = Reservoir(name, metadata)
        elif object_type == ObjectType.SOURCE:
            new_obj = Source(name, metadata)
        elif object_type == ObjectType.BASIN:
            new_obj = Basin(name, metadata)
        else:
            return False
        
        # Find index of after_object
        after_index = -1
        for i, obj in enumerate(self.objects):
            if obj.name == after_object:
                after_index = i
                break
        
        if after_index == -1:
            return False
        
        # Insert new object after the found object
        self.objects.insert(after_index + 1, new_obj)
        self.object_map[name] = new_obj
        
        return True
    
    def replace_object_from_parent(self, parent: 'BasinFile', object_name: str) -> bool:
        """
        Replace an existing object's metadata using metadata from a parent basin file
        
        Args:
            parent: Parent BasinFile object to copy metadata from
            object_name: Name of the object to find in parent and replace in current file
            
        Returns:
            True if replacement was successful, False if object not found in parent or current file
        """
        # Get object from parent file
        parent_obj = parent.get_object(object_name)
        if parent_obj is None:
            return False
        
        # Replace object in current file using parent's metadata
        return self.replace_object(object_name, parent_obj.metadata)
    
    def add_object_from_parent(self, parent: 'BasinFile', object_name: str) -> bool:
        """
        Add a new object to the basin file using metadata from a parent basin file
        
        Args:
            parent: Parent BasinFile object to copy object from
            object_name: Name of the object to find in parent and add to current file
            
        Returns:
            True if object was added successfully, False if object not found in parent or anchor object not found in current file
        """
        # Get object from parent file
        parent_obj = parent.get_object(object_name)
        if parent_obj is None:
            return False
        
        # Check if object already exists in target file
        if object_name in self.object_map:
            warnings.warn(f"Object '{object_name}' already exists in {self.filepath}. Not adding duplicate.", UserWarning)
            return False
        
        # Find what object comes before this one in the parent file
        after_index = -1
        for i, obj in enumerate(parent.objects):
            if obj.name == object_name:
                if i == 0:
                    # Object is at the beginning, can't add without an anchor
                    return False
                after_index = i - 1
                break
        
        if after_index == -1:
            return False
        
        after_object = parent.objects[after_index].name
        
        # Add object to current file using parent's object type and metadata
        return self.add_object(parent_obj.object_type, object_name, parent_obj.metadata, 
                              after_object)
    
    def update_downstream_from_parent(self, parent: 'BasinFile', object_name: str) -> bool:
        """
        Update an object's downstream reference using data from a parent basin file
        while preserving all other metadata. Updates Last Modified Date and Time.
        
        Args:
            parent: Parent BasinFile object to copy downstream from
            object_name: Name of the object to update
            
        Returns:
            True if update was successful, False if object not found in parent or current file
        """
        # Get object from parent file
        parent_obj = parent.get_object(object_name)
        if parent_obj is None:
            return False
        
        # Get object from current file
        target_obj = self.get_object(object_name)
        if target_obj is None:
            return False
        
        # Extract downstream from parent
        downstream_value = parent_obj.downstream
        if downstream_value is None:
            return False
        
        # Get current date and time in the format from the basin file
        now = datetime.now()
        day = now.day
        month = now.strftime("%B")
        year = now.year
        date_str = f"{day} {month} {year}"
        time_str = now.strftime("%H:%M:%S")
        
        # Update metadata: replace Downstream and update timestamps
        metadata_lines = target_obj.metadata.split('\n')
        new_metadata_lines = []
        
        downstream_found = False
        date_found = False
        time_found = False
        
        for line in metadata_lines:
            stripped = line.strip()
            if stripped.startswith('Downstream:'):
                new_metadata_lines.append(f"     Downstream: {downstream_value}")
                downstream_found = True
            elif stripped.startswith('Last Modified Date:'):
                new_metadata_lines.append(f"     Last Modified Date: {date_str}")
                date_found = True
            elif stripped.startswith('Last Modified Time:'):
                new_metadata_lines.append(f"     Last Modified Time: {time_str}")
                time_found = True
            else:
                new_metadata_lines.append(line)
        
        # If Downstream wasn't found, add it
        if not downstream_found:
            new_metadata_lines.insert(1, f"     Downstream: {downstream_value}")
        
        # If date wasn't found, add it (after first line if it has content)
        if not date_found:
            new_metadata_lines.insert(1, f"     Last Modified Date: {date_str}")
        
        # If time wasn't found, add it after date
        if not time_found:
            # Find where we just inserted date or where it already is
            insert_pos = 1
            for i, line in enumerate(new_metadata_lines):
                if line.strip().startswith('Last Modified Date:'):
                    insert_pos = i + 1
                    break
            new_metadata_lines.insert(insert_pos, f"     Last Modified Time: {time_str}")
        
        target_obj.metadata = '\n'.join(new_metadata_lines) + '\n'
        
        return True
        
    def get_object(self, name: str) -> Optional[BasinObject]:
        """Get an object by name"""
        return self.object_map.get(name)
    
    def remove_object(self, name: str) -> bool:
        """Remove an object by name"""
        if name not in self.object_map:
            return False
        
        obj = self.object_map[name]
        self.objects.remove(obj)
        del self.object_map[name]
        
        return True
    
    def write(self, filepath: Optional[str] = None) -> None:
        """Write the basin file"""
        if filepath is None:
            filepath = self.filepath
        
        content = self.preamble
        if content and not content.endswith('\n'):
            content += '\n'
        
        for obj in self.objects:
            content += obj.to_string()
        
        content += self.postamble
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            f.close()
    
    def list_objects(self) -> List[Tuple[str, ObjectType]]:
        """List all objects in the file"""
        return [(obj.name, obj.object_type) for obj in self.objects]
    
    def list_objects_by_type(self, object_type: ObjectType) -> List[str]:
        """List all objects of a specific type"""
        return [obj.name for obj in self.objects if obj.object_type == object_type]