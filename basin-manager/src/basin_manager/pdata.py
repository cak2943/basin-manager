"""Classes for managing HEC-HMS .pdata (Paired Data) files"""

from typing import Dict, List, Optional, Tuple
from .basins import GenericFile
from .hms_file_object import HMSFileObject


class PdataTable(HMSFileObject):
    """Represents a Table object in a .pdata file"""
    
    def __init__(self, name: str, metadata: str):
        """Initialize a PdataTable.
        
        Args:
            name: Name of the table
            metadata: Metadata content (lines between header and End:)
        """
        super().__init__("Table", name, metadata)
    
    @property
    def table_type(self) -> Optional[str]:
        """Extract the Table Type from metadata.
        
        Returns:
            The table type (e.g., 'Pond', 'Reservoir', etc.) if found, None otherwise
        """
        return self.get_key_field('Table Type:')


class PondTable(PdataTable):
    """Represents a Pond Table in a .pdata file"""
    
    def __init__(self, name: str, metadata: str):
        super().__init__(name, metadata)


class ReservoirTable(PdataTable):
    """Represents a Reservoir Table in a .pdata file"""
    
    def __init__(self, name: str, metadata: str):
        super().__init__(name, metadata)


class DiverSionTable(PdataTable):
    """Represents a Diversion Table in a .pdata file"""
    
    def __init__(self, name: str, metadata: str):
        super().__init__(name, metadata)


class PdataFile(GenericFile):
    """Class to manage .pdata (Paired Data) files"""
    
    def __init__(self, filepath: str):
        """Initialize PdataFile with path to .pdata file.
        
        Args:
            filepath: Path to the .pdata file
        """
        super().__init__(filepath)
    
    def _get_valid_types(self) -> List[str]:
        """Return list of valid pdata object types.
        
        Returns:
            List containing 'Table' as the only valid type
        """
        return ["Table"]
    
    def _create_object_from_type(self, type_str: str, name: str, metadata: str) -> Optional[PdataTable]:
        """Create a PdataTable object.
        
        Args:
            type_str: The object type (must be 'Table')
            name: The name of the table  
            metadata: The metadata content
            
        Returns:
            A PdataTable instance, or None if type_str is not 'Table'
        """
        if type_str != "Table":
            return None
        
        # Could extend this to create specific subclasses based on table type
        # For now, just use generic PdataTable
        return PdataTable(name, metadata)
    
    def replace_object(self, object_name: str, metadata: str) -> bool:
        """Replace an existing table's metadata.
        
        Args:
            object_name: Name of the table to replace
            metadata: New metadata string (should not include "End:")
            
        Returns:
            True if replacement was successful, False if table not found
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
    
    def add_object(self, name: str, metadata: str, after_object: str) -> bool:
        """Add a new table to the pdata file.
        
        Args:
            name: Name of the new table  
            metadata: Metadata string (should not include "End:")
            after_object: Name of existing table to place new table after
            
        Returns:
            True if table was added successfully, False otherwise
        """
        if after_object not in self.object_map:
            return False
        
        # Check if table already exists
        if name in self.object_map:
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
        
        # Create new table
        new_obj = PdataTable(name, metadata)
        
        # Find index of after_object
        after_index = -1
        for i, obj in enumerate(self.objects):
            if obj.name == after_object:
                after_index = i
                break
        
        if after_index == -1:
            return False
        
        # Insert new table after the found table
        self.objects.insert(after_index + 1, new_obj)
        self.object_map[name] = new_obj
        
        return True
    
    def list_tables(self) -> List[Tuple[str, Optional[str]]]:
        """List all tables in the file with their table types.
        
        Returns:
            List of (table_name, table_type) tuples
        """
        return [(obj.name, obj.table_type) for obj in self.objects if isinstance(obj, PdataTable)]
