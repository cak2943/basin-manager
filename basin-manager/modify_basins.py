import os
from basin_manager.basins import BasinFile, ObjectType

def modify_instructions(basin_file: BasinFile):

    #Read basin data
    basin_file.read()

    # Replace a junction's metadata
    new_metadata = """
    Last Modified Date: 8 April 2026
    Last Modified Time: 12:43:59
    Canvas X: 3029779.002806442
    Canvas Y: 1.0085744850310959E7
    From Canvas X: 3029759.49325904
    From Canvas Y: 1.0085691358231135E7
    Downstream: R_LBA120
    """
    basin_file.replace_object('J_LBA110', new_metadata)

    # Add a new junction after an existing one
    new_reach_metadata = """    
    Last Modified Date: 8 April 2026
     Last Modified Time: 12:43:59
     Canvas X: 3032015.0563074476
     Canvas Y: 1.0083641449600764E7
     From Canvas X: 3029779.002806442
     From Canvas Y: 1.0085744850310959E7
     Downstream: J_LBA120

     Route: Muskingum Cunge
     Channel: 8-point
     Length: 2431.613
     Energy Slope: 0.0165
     Mannings n: 0.05
     Left Mannings n: 0.08
     Right Mannings n: 0.08
     Cross Section Name: R_LBA120
     Initial Variable: Combined Inflow
     Space-Time Method: Automatic DX and DT
     Index Parameter Type: Index Celerity
     Index Celerity: 5
     Maximum Depth Iterations: 20
     Maximum Route Step Iterations: 30
     Channel Loss: None
    """
    basin_file.add_object(ObjectType.REACH, 'R_LBA120', new_reach_metadata, 'J_LBA120')

    # Replace a junction's metadata
    new_metadata = """
    Last Modified Date: 8 April 2026
     Last Modified Time: 12:28:48
     Latitude Degrees:  30.247484988000945
     Longitude Degrees: -97.85688307958125
     Canvas X: 3078836.8773487345
     Canvas Y: 1.0062294245578693E7
     Area: 0.059
     Downstream: R_GAI0040

     Discretization: None
     File: Existing_Conditions_01_.sqlite

     Canopy: None
     Allow Simultaneous Precip Et: No
     Plant Uptake Method: None

     Surface: None

     LossRate: SCS
     Percent Impervious Area: 31.0
     Curve Number: 76

     Transform: SCS
     Lag: 18.8
     Unitgraph Type: STANDARD

     Baseflow: None
    """
    basin_file.replace_object('GAI0030', new_metadata)

    # Add a new junction after an existing one
    new_reach_metadata = """    
    Last Modified Date: 8 April 2026
     Last Modified Time: 12:38:57
     Canvas X: 3079945.8693733234
     Canvas Y: 1.0060445460565975E7
     From Canvas X: 3078827.0804493707
     From Canvas Y: 1.006231383937742E7
     Downstream: J_GAI0040

     Route: Muskingum Cunge
     Channel: 8-point
     Length: 1935.88
     Energy Slope: 0.0253
     Mannings n: 0.05
     Left Mannings n: 0.08
     Right Mannings n: 0.08
     Initial Variable: Combined Inflow
     Space-Time Method: Automatic DX and DT
     Index Parameter Type: Index Celerity
     Index Celerity: 5
     Maximum Depth Iterations: 20
     Maximum Route Step Iterations: 30
     Channel Loss: None
    """

    basin_file.add_object(ObjectType.REACH, 'R_GAI0040', new_reach_metadata, 'J_GAI0040')

    # Write changes back to file
    basin_file.write()

def main():
    # Reading and modifying a basin file
    base_path = r"T:\SW\7-Hydrology\Milestone 3\_Submittal\Working_12182025\BAR\HEC-HMS_v4.12\BAR"
    basin_list = ["May_2015", "May_2019", "Oct_2015"]

    for basin_name in basin_list:
        input_file = os.path.join(base_path, f"{basin_name}.basin")
        basin_file = BasinFile(input_file)
        print()
        print(f"Reading and modifying {input_file}...")
        modify_instructions(basin_file)
        print(f"Finished modifying {input_file}.\n")

if __name__ == "__main__":
    main()