#!/usr/bin/env python3
"""
Script to extract all Reservoir objects from basin files and output to a txt file.
"""

from pathlib import Path
from src.basin_manager.basins import BasinFile, ObjectType


def extract_reservoirs(basin_file: str, output_file: str = "reservoirs_output.txt") -> None:
    """
    Extract all Reservoir objects from a single basin file.
    
    Args:
        basin_file: Path to the .basin file to process
        output_file: Path to output txt file
    """
    basin_file_path = Path(basin_file)
    
    if not basin_file_path.exists():
        print(f"Error: File not found: {basin_file_path}")
        return
    
    if not basin_file_path.suffix.lower() == '.basin':
        print(f"Warning: File does not have .basin extension: {basin_file_path}")
    
    print(f"Processing: {basin_file_path.name}")
    
    reservoirs = []
    
    # Process the basin file
    try:
        basin_obj = BasinFile(str(basin_file_path))
        basin_obj.read()
        
        # Get all Reservoir objects
        reservoir_names = basin_obj.list_objects_by_type(ObjectType.RESERVOIR)
        
        for name in reservoir_names:
            reservoir_obj = basin_obj.get_object(name)
            reservoirs.append({
                'file': basin_file_path.name,
                'name': name,
                'object': reservoir_obj
            })
    except Exception as e:
        print(f"Error reading {basin_file_path}: {e}")
        return
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Reservoir Objects Summary\n")
        f.write(f"{'=' * 50}\n\n")
        f.write(f"Total Reservoirs Found: {len(reservoirs)}\n\n")
        
        if not reservoirs:
            f.write("No reservoir objects found.\n")
        else:
            # Group by file
            by_file = {}
            for res in reservoirs:
                if res['file'] not in by_file:
                    by_file[res['file']] = []
                by_file[res['file']].append(res)
            
            # Write grouped output
            for filename in sorted(by_file.keys()):
                f.write(f"\nFile: {filename}\n")
                f.write(f"{'-' * 50}\n")
                
                for res in by_file[filename]:
                    f.write(f"\nReservoir: {res['name']}\n")
                    f.write(f"Metadata:\n{res['object'].metadata}")
                    f.write(f"{'.' * 50}\n")
    
    print(f"Successfully extracted {len(reservoirs)} reservoir(s)")
    print(f"Output written to {output_file}")

def main():
    basin_file = r"T:\SW\7-Hydrology\Milestone 3\_Submittal\Working_12182025\BAR\HEC-HMS_v4.12\BAR\Existing_Conditions_01_.basin"
    output_file = r"T:\SW\7-Hydrology\Milestone 3\_Submittal\Archive\Reservoirs.txt"
    extract_reservoirs(basin_file, output_file)

if __name__ == "__main__":
   main() 