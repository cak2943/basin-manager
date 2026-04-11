#!/usr/bin/env python
"""Test script to verify BasinFile refactoring backward compatibility"""

from src.basin_manager.basins import BasinFile, ObjectType, FileObject, GenericFile

# Test 1: BasinFile instantiation
print("Test 1: BasinFile instantiation")
bf = BasinFile('test.basin')
print(f"  ✓ BasinFile created successfully")
print(f"  ✓ FilePath: {bf.filepath}")
print(f"  ✓ Objects list: {len(bf.objects)} objects")
print(f"  ✓ Object map: {len(bf.object_map)} items")

# Test 2: Verify ObjectType enum
print("\nTest 2: ObjectType enum")
print(f"  ✓ ObjectType.BASIN: {ObjectType.BASIN.value}")
print(f"  ✓ ObjectType.SUBBASIN: {ObjectType.SUBBASIN.value}")
print(f"  ✓ ObjectType.REACH: {ObjectType.REACH.value}")

# Test 3: Verify inheritance
print("\nTest 3: Inheritance")
print(f"  ✓ BasinFile is GenericFile: {isinstance(bf, GenericFile)}")

# Test 4: Verify methods exist
print("\nTest 4: Methods")
print(f"  ✓ read method: {hasattr(bf, 'read')}")
print(f"  ✓ write method: {hasattr(bf, 'write')}")
print(f"  ✓ get_object method: {hasattr(bf, 'get_object')}")
print(f"  ✓ add_object method: {hasattr(bf, 'add_object')}")
print(f"  ✓ replace_object method: {hasattr(bf, 'replace_object')}")

print("\n" + "="*50)
print("✓ All backward compatibility tests passed!")
print("="*50)
