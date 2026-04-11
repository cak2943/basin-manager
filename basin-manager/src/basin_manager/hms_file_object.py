"""Base class for HMS file objects"""

from abc import ABC, abstractmethod
from typing import Optional


class HMSFileObject(ABC):
    """Abstract base class for objects in HMS files (basin, pdata, etc.)"""
    
    def __init__(self, object_type: str, name: str, metadata: str):
        """Initialize a file object.
        
        Args:
            object_type: Type of the object (e.g., 'Basin', 'Reach', 'Table')
            name: Name of the object
            metadata: Metadata content (lines between header and End:)
        """
        self.object_type = object_type
        self.name = name
        self.metadata = metadata
    
    def get_key_field(self, field_name: str) -> Optional[str]:
        """Extract a key field value from metadata.
        
        Args:
            field_name: The field name to search for (e.g., 'Downstream:', 'Table Type:')
            
        Returns:
            The field value if found, None otherwise
        """
        for line in self.metadata.split('\n'):
            if line.strip().startswith(field_name):
                parts = line.split(':', 1)
                if len(parts) > 1:
                    return parts[1].strip()
        return None
    
    def to_string(self) -> str:
        """Convert object back to file format.
        
        Returns:
            String representation of the object in HMS file format
        """
        return f"{self.object_type}: {self.name}\n{self.metadata}End:\n\n"
