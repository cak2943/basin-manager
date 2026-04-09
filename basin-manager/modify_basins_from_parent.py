import os
from basin_manager.basins import BasinFile, ObjectType

def modify_instructions(basin_file: BasinFile, parent_file:BasinFile):

    #Read basin data
    basin_file.read()

    basin_file.replace_object_from_parent(parent_file, 'J_LBA110')

    basin_file.add_object_from_parent(parent_file,'R_LBA120')

    basin_file.update_downstream_from_parent(parent_file, 'GAI0030')

    basin_file.add_object_from_parent(parent_file,'R_GAI0040')

    # Write changes back to file
    basin_file.write()

def main():
    # Reading and modifying a basin file
    base_path = r"T:\SW\7-Hydrology\Milestone 3\_Submittal\Working_12182025\BAR\HEC-HMS_v4.12\BAR"
    basin_list = ["May_2015", "May_2019", "Oct_2015"]
    parent_path = r"T:\SW\7-Hydrology\Milestone 3\_Submittal\Working_12182025\BAR\HEC-HMS_v4.12\BAR\Existing_Conditions_01_.basin"
    parent_file = BasinFile(parent_path)
    parent_file.read()

    for basin_name in basin_list:
        input_file = os.path.join(base_path, f"{basin_name}.basin")
        basin_file = BasinFile(input_file)
        print()
        print(f"Reading and modifying {input_file}...")
        modify_instructions(basin_file, parent_file)
        print(f"Finished modifying {input_file}.\n")

if __name__ == "__main__":
    main()