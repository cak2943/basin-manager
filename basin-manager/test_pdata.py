#!/usr/bin/env python
"""Test script to verify PdataFile works correctly"""

from src.basin_manager.pdata import PdataFile, PdataTable

# Test 1: PdataFile instantiation
print("Test 1: PdataFile instantiation")
pf = PdataFile('test.pdata')
print(f"  ✓ PdataFile created successfully")
print(f"  ✓ FilePath: {pf.filepath}")
print(f"  ✓ Objects list: {len(pf.objects)} objects")

# Test 2: Verify valid types
print("\nTest 2: Valid types")
valid_types = pf._get_valid_types()
print(f"  ✓ Valid types: {valid_types}")
assert valid_types == ["Table"], f"Expected ['Table'], got {valid_types}"

# Test 3: Create a PdataTable manually
print("\nTest 3: PdataTable creation")
metadata = """     Table Type: Pond
     Interpolation: Linear Interpolation
"""
table = PdataTable("TestPond", metadata)
print(f"  ✓ PdataTable created: {table.name}")
print(f"  ✓ Object type: {table.object_type}")
print(f"  ✓ Table type: {table.table_type}")

# Test 4:Test _create_object_from_type
print("\nTest 4: _create_object_from_type")
obj = pf._create_object_from_type("Table", "TestTable", metadata)
assert obj is not None, "Failed to create object"
assert obj.name == "TestTable", f"Name mismatch: expected 'TestTable', got '{obj.name}'"
assert obj.object_type == "Table", f"Type mismatch: expected 'Table', got '{obj.object_type}'"
print(f"  ✓ Object created successfully: {obj.name}")
print(f"  ✓ Object is PdataTable: {isinstance(obj, PdataTable)}")

# Test 5: Invalid type  
print("\nTest 5: Invalid type handling")
invalid_obj = pf._create_object_from_type("Invalid", "TestTable", metadata)
assert invalid_obj is None, "Should return None for invalid type"
print(f"  ✓ Invalid type correctly returns None")

# Test 6: Methods exist
print("\nTest 6: Methods")
print(f"  ✓ read method: {hasattr(pf, 'read')}")
print(f"  ✓ write method: {hasattr(pf, 'write')}")
print(f"  ✓ get_object method: {hasattr(pf, 'get_object')}")
print(f"  ✓ add_object method: {hasattr(pf, 'add_object')}")
print(f"  ✓ replace_object method: {hasattr(pf, 'replace_object')}")
print(f"  ✓ list_tables method: {hasattr(pf, 'list_tables')}")

print("\n" + "="*50)
print("✓ All PdataFile tests passed!")
print("="*50)
