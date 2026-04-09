import os
import sys
from pathlib import Path
from basin_manager.basins import BasinFile, ObjectType

def flag_subbasin_junction_missing_reach(basin_file: BasinFile) -> list:
    """
    Find Junction objects where:
    1. All upstream elements are Subbasins (no other types)
    2. The junction does NOT have a Reach as their downstream element
    
    Args:
        basin_file: BasinFile instance with parsed objects
        
    Returns:
        List of tuples (upstream_subbasins, junction_name, junction_downstream, downstream_type)
    """
    flagged_junctions = []
    
    # Build a reverse mapping: what flows into each element
    upstream_map = {}  # element_name -> list of (upstream_element_name, upstream_element_type)
    
    for obj_name, obj_type in basin_file.list_objects():
        obj = basin_file.get_object(obj_name)
        if obj.downstream:
            downstream_name = obj.downstream
            if downstream_name not in upstream_map:
                upstream_map[downstream_name] = []
            upstream_map[downstream_name].append((obj_name, obj_type))
    
    # Get all junctions
    junctions = basin_file.list_objects_by_type(ObjectType.JUNCTION)
    
    for junction_name in junctions:
        junction = basin_file.get_object(junction_name)
        
        # Get all upstream elements for this junction
        upstream_elements = upstream_map.get(junction_name, [])
        
        # Skip if junction has no upstream elements
        if not upstream_elements:
            continue
        
        # Check if ALL upstream elements are Subbasins
        all_subbasins = all(upstream_type == ObjectType.SUBBASIN for _, upstream_type in upstream_elements)
        
        # Skip if not all upstream are subbasins
        if not all_subbasins:
            continue
        
        # Check if the junction's downstream is a Reach
        if not junction.downstream:
            # Junction has no downstream element - flag it
            flagged_junctions.append((
                [upstream_name for upstream_name, _ in upstream_elements],
                junction_name,
                None,  # No downstream
                "MISSING"
            ))
        else:
            # Check what the junction's downstream is
            junction_downstream_obj = basin_file.get_object(junction.downstream)
            
            # If junction's downstream is NOT a Reach, flag it
            if not junction_downstream_obj or junction_downstream_obj.object_type != ObjectType.REACH:
                downstream_type = junction_downstream_obj.object_type.value if junction_downstream_obj else "UNKNOWN"
                flagged_junctions.append((
                    [upstream_name for upstream_name, _ in upstream_elements],
                    junction_name,
                    junction.downstream,
                    downstream_type
                ))
    
    return flagged_junctions


def main():
    """Main function to process basin files and output flagged junctions"""
    base_path = r"T:\SW\7-Hydrology\Milestone 3\_Submittal\Archive\Working_Basins"
    basin_list = ["Existing_Conditions_002_", "Existing_Conditions_02_"]
    
    # Set up output file
    output_file = r"flagged_missing_reach_junctions_output.txt"
    
    with open(output_file, 'w', encoding='utf-8') as outf:
        for basin_name in basin_list:
            input_file = os.path.join(base_path, f"{basin_name}.basin")
            
            # Check if file exists
            if not os.path.exists(input_file):
                print(f"File not found: {input_file}")
                outf.write(f"File not found: {input_file}\n")
                continue
            
            print(f"Processing {input_file}...")
            basin_file = BasinFile(input_file)
            basin_file.read()
            
            # Flag junctions
            flagged = flag_subbasin_junction_missing_reach(basin_file)
            
            # Write results
            outf.write(f"\n{'='*120}\n")
            outf.write(f"Basin: {basin_name}\n")
            outf.write(f"{'='*120}\n")
            outf.write(f"Total junctions flagged: {len(flagged)}\n")
            outf.write(f"(Junctions with ONLY Subbasins as upstream that do NOT have a Reach as downstream)\n\n")
            
            if flagged:
                outf.write(f"{'Junction Name':<25} {'Upstream Subbasins':<50} {'Junction Downstream':<25} {'Type':<15}\n")
                outf.write("-" * 120 + "\n")
                
                for upstream_subbasins, junction_name, junction_downstream, downstream_type in flagged:
                    upstream_display = ", ".join(upstream_subbasins) if upstream_subbasins else "(NONE)"
                    downstream_display = junction_downstream if junction_downstream else "(NONE)"
                    
                    outf.write(f"{junction_name:<25} {upstream_display:<50} {downstream_display:<25} {downstream_type:<15}\n")
            else:
                outf.write("No issues found. All junctions with only subbasin inputs have reaches as their downstream element.\n")
            
            print(f"  Found {len(flagged)} flagged junctions")
    
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
