import os
import sys
from pathlib import Path
from basin_manager.basins import BasinFile, ObjectType

def flag_reach_junction_reach_pattern(basin_file: BasinFile) -> list:
    """
    Find Junction objects where the downstream chain is: Reach -> Junction -> Reach
    
    Args:
        basin_file: BasinFile instance with parsed objects
        
    Returns:
        List of tuples (junction_name, downstream_reach, intermediate_junction, final_reach)
    """
    flagged_junctions = []
    
    # Get all junctions
    junctions = basin_file.list_objects_by_type(ObjectType.JUNCTION)
    
    for junction_name in junctions:
        junction = basin_file.get_object(junction_name)
        
        # Step 1: Junction's downstream should be a Reach
        if not junction.downstream:
            continue
            
        downstream_reach_name = junction.downstream
        downstream_reach = basin_file.get_object(downstream_reach_name)
        
        # Check if downstream is a Reach
        if not downstream_reach or downstream_reach.object_type != ObjectType.REACH:
            continue
        
        # Step 2: That Reach's downstream should be a Junction
        if not downstream_reach.downstream:
            continue
            
        intermediate_junction_name = downstream_reach.downstream
        intermediate_junction = basin_file.get_object(intermediate_junction_name)
        
        # Check if that is a Junction
        if not intermediate_junction or intermediate_junction.object_type != ObjectType.JUNCTION:
            continue
        
        # Step 3: That Junction's downstream should be a Reach
        if not intermediate_junction.downstream:
            continue
            
        final_reach_name = intermediate_junction.downstream
        final_reach = basin_file.get_object(final_reach_name)
        
        # Check if that is a Reach
        if not final_reach or final_reach.object_type != ObjectType.REACH:
            continue
        
        # Found the pattern! Flag this junction
        flagged_junctions.append((
            junction_name,
            downstream_reach_name,
            intermediate_junction_name,
            final_reach_name
        ))
    
    return flagged_junctions


def main():
    """Main function to process basin files and output flagged junctions"""
    base_path = r"T:\SW\7-Hydrology\Milestone 3\_Submittal\Archive\Working_Basins"
    basin_list = ["Existing_Conditions_002_", "Existing_Conditions_02_"]
    
    # Set up output file
    output_file = r"flagged_junctions_output.txt"
    
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
            flagged = flag_reach_junction_reach_pattern(basin_file)
            
            # Write results
            outf.write(f"\n{'='*80}\n")
            outf.write(f"Basin: {basin_name}\n")
            outf.write(f"{'='*80}\n")
            outf.write(f"Total junctions flagged: {len(flagged)}\n\n")
            
            if flagged:
                outf.write(f"{'Junction Name':<20} {'-> Reach':<20} {'-> Junction':<20} {'-> Reach':<20}\n")
                outf.write("-" * 80 + "\n")
                
                for junction_name, reach1, junction2, reach2 in flagged:
                    outf.write(f"{junction_name:<20} {reach1:<20} {junction2:<20} {reach2:<20}\n")
            else:
                outf.write("No junctions found with the Reach -> Junction -> Reach pattern.\n")
            
            print(f"  Found {len(flagged)} flagged junctions")
    
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
