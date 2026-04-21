import pefile

pe = pefile.PE('/media/azakharova/KINGSTON/LB2026/rev/win.exe')

if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
    for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        # Type level (e.g., RT_ICON, RT_STRING)
        for resource_id in resource_type.directory.entries:
            # Name/ID level
            for resource_lang in resource_id.directory.entries:
                if resource_type.id == 10  and resource_id.id == 101:
                    data_rva = resource_lang.data.struct.OffsetToData
                    size = resource_lang.data.struct.Size
                    
                    # Extract the raw binary data
                    data = pe.get_data(data_rva, size)
                    print(''.join([chr(~b & 0xFF) for b in data]))
                    break
