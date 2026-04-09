"""
Script to compare two .basin files and identify differences in basin objects.
Lists objects that exist in one file but not the other, and writes results to a text file.
"""

from basin_manager.basins import BasinFile, ObjectType
from pathlib import Path


def compare_basin_files(file1_path: str, file2_path: str, output_file: str = None) -> None:
    """
    Compare two basin files and write differences to a text file.
    Lists only objects that are not found in both files.
    
    Args:
        file1_path: Path to the first .basin file
        file2_path: Path to the second .basin file
        output_file: Path to output text file (optional, defaults to compare_results.txt)
    """
    if output_file is None:
        output_file = "compare_results.txt"
    
    print(f"\nComparing basin files:")
    print(f"  File 1: {file1_path}")
    print(f"  File 2: {file2_path}")
    print(f"  Output: {output_file}\n")
    
    # Load both files
    basin_file1 = BasinFile(file1_path)
    basin_file2 = BasinFile(file2_path)
    
    print("Reading File 1...")
    basin_file1.read()
    print(f"  Loaded {len(basin_file1.objects)} objects")
    
    print("Reading File 2...")
    basin_file2.read()
    print(f"  Loaded {len(basin_file2.objects)} objects\n")
    
    # Get object names from each file
    file1_objects = set(basin_file1.object_map.keys())
    file2_objects = set(basin_file2.object_map.keys())
    
    # Find differences
    only_in_file1 = file1_objects - file2_objects
    only_in_file2 = file2_objects - file1_objects
    
    # Write results to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("BASIN FILE COMPARISON RESULTS\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"File 1: {file1_path}\n")
        f.write(f"File 2: {file2_path}\n\n")
        
        # Objects only in File 1
        f.write("=" * 80 + "\n")
        f.write(f"Objects only in File 1 ({len(only_in_file1)}):\n")
        f.write("=" * 80 + "\n")
        if only_in_file1:
            for obj_name in sorted(only_in_file1):
                obj = basin_file1.get_object(obj_name)
                f.write(f"  {obj.object_type.value:12} | {obj_name}\n")
        else:
            f.write("  (none)\n")
        
        # Objects only in File 2
        f.write("\n" + "=" * 80 + "\n")
        f.write(f"Objects only in File 2 ({len(only_in_file2)}):\n")
        f.write("=" * 80 + "\n")
        if only_in_file2:
            for obj_name in sorted(only_in_file2):
                obj = basin_file2.get_object(obj_name)
                f.write(f"  {obj.object_type.value:12} | {obj_name}\n")
        else:
            f.write("  (none)\n")
        
        # Summary
        f.write("\n" + "=" * 80 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 80 + "\n")
        f.write(f"  Total in File 1:     {len(basin_file1.objects)}\n")
        f.write(f"  Total in File 2:     {len(basin_file2.objects)}\n")
        f.write(f"  Only in File 1:      {len(only_in_file1)}\n")
        f.write(f"  Only in File 2:      {len(only_in_file2)}\n")
        f.write("=" * 80 + "\n")
    
    print(f"Results written to: {output_file}")
    print(f"  Objects only in File 1: {len(only_in_file1)}")
    print(f"  Objects only in File 2: {len(only_in_file2)}\n")


def main():
    """Main function - compare two specified basin files."""
    # Example comparison - update these paths as needed
    file1 = r"T:\SW\7-Hydrology\Milestone 3\_Submittal\Working_12182025\BAR\HEC-HMS_v4.12\BAR\Existing_Conditions_01_.basin"
    file2 = r"T:\SW\7-Hydrology\Milestone 3\_Submittal\Working_12182025\BAR\HEC-HMS_v4.12\BAR\May_2015.basin"
    output = "compare_results.txt"
    
    compare_basin_files(file1, file2, output)


if __name__ == "__main__":
    main()
