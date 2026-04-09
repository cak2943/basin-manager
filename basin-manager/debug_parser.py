import sys
sys.path.insert(0, 'src')
from basin_manager.basins import BasinFile, ObjectType

f = r't:\SW\7-Hydrology\Milestone 3\_Submittal\Archive\Working_Basins\Existing_Conditions_002_.basin'
content = open(f, 'r', encoding='utf-8').read()
lines = content.split('\n')
print('lines', len(lines))
for i, l in enumerate(lines[:20]):
    print(i, repr(l), 'starts', l.startswith(' '), 'tab', l.startswith('\t'), 'colon', ':' in l)

current_object_lines = []
preamble_lines = []
in_object = False
i = 0
while i < len(lines):
    line = lines[i]
    if ':' in line and not line.startswith(' ') and not line.startswith('\t'):
        print('header candidate', i, repr(line), 'in_object', in_object, 'current_object', len(current_object_lines))
        if current_object_lines:
            print(' process prev object', current_object_lines[0])
            current_object_lines = []
        header_parts = line.split(':', 1)
        if header_parts[0].strip() in [obj_type.value for obj_type in ObjectType]:
            current_object_lines.append(line)
            in_object = True
            print('  start object', line)
        else:
            print('  non-object line', line)
            if in_object:
                current_object_lines.append(line)
            else:
                preamble_lines.append(line)
    else:
        if in_object:
            current_object_lines.append(line)
            if line.strip() == 'End:':
                print('  end object', current_object_lines[0])
                current_object_lines = []
                in_object = False
                if i + 1 < len(lines) and lines[i + 1].strip() == '':
                    print('   skip blank after end at', i + 1)
                    i += 1
        else:
            preamble_lines.append(line)
    i += 1

print('preamble', repr('\n'.join(preamble_lines)[:200]))
print('preamble lines', len(preamble_lines))
