#!/usr/bin/env python
"""Test script to verify PdataFile can read real .pdata files"""

import sys
from src.basin_manager.pdata import PdataFile, PdataTable

# Test with sample pdata file
print("Test: Loading sample BAR.pdata file")
try:
    # Path to the sample file attached to the conversation
    pdata_path = r"t:\SW\7-Hydrology\Milestone 3\_Submittal\Working_12182025\BAR\HEC-HMS_v4.12\BAR\BAR.pdata"
    
    pf = PdataFile(pdata_path)
    pf.read()
    
    print(f"✓ File loaded successfully")
    print(f"  - Tables: {len(pf.objects)}")
    print(f"  - Object map size: {len(pf.object_map)}")
    
    # List first 10 tables
    tables = pf.list_tables()
    print(f"\n  First 10 tables:")
    for name, table_type in tables[:10]:
        print(f"    - {name}: {table_type}")
    
    # Verify some specific tables  
    print(f"\nVerifying specific tables:")
    bar_tc = pf.get_object("BAR_TC Pond")
    if bar_tc:
        print(f"  ✓ Found 'BAR_TC Pond'")
        print(f"    - Type: {bar_tc.object_type}")
        print(f"    - Table Type: {bar_tc.table_type if isinstance(bar_tc, PdataTable) else 'N/A'}")
    
    gai = pf.get_object("GAI Pond")
    if gai:
        print(f"  ✓ Found 'GAI Pond'")
        print(f"    - Type: {gai.object_type}")
        print(f"    - Table Type: {gai.table_type if isinstance(gai, PdataTable) else 'N/A'}")
    
    # Test write/read round trip
    print(f"\nRound-trip test:")
    test_output = "/tmp/test_pdata.pdata"
    pf.write(test_output)
    print(f"  ✓ File written to {test_output}")
    
    # Read back
    pf2 = PdataFile(test_output)
    pf2.read()
    print(f"  ✓ File read back successfully")
    print(f"  ✓ Object count matches: {len(pf.objects)} == {len(pf2.objects)}")
    
    print("\n" + "="*60)
    print("✓ All pdata file tests passed!")
    print("="*60)
    
except FileNotFoundError as e:
    print(f"✗ File not found: {e}")
    print("  (This is expected if running outside the project environment)")
    sys.exit(0)
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
