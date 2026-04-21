def rand_val():
    global rnd
    rnd = (rnd * 1103515245 + 12345) & 0xFFFFFFFF
    return rnd & 0xFF  # Return byte value

def native_check(input_string):
    global rnd
    rnd = 31337
    if len(input_string) != 39:
        return False
    input_bytes = input_string.encode('utf-8')
    cumulative = 0
    
    for i in range(39):
        rand_byte = rand_val()
        constants = [
            0xA3, 0xCA, 0x4C, 0x4D, 0xB3, 0xD0, 0x6D, 0x96, 0xA2, 0xB6,
            0xD7, 0xE9, 0x6B, 0x12, 0x46, 0xE1, 0xA9, 0x1A, 0x7C, 0xF3,
            0xCC, 0xFA, 0x0B, 0x23, 0x4F, 0x11, 0xD2, 0x78, 0x37, 0x24,
            0x68, 0x79, 0x7D, 0x0D, 0x1A, 0x36, 0x69, 0xB8, 0x15
        ]
        
        current = rand_byte ^ input_bytes[i] ^ constants[i]
        cumulative |= current
        
        if i == 38:
            return cumulative == 0
    
    return cumulative == 0


def native_check_clean(input_string):
    global rnd
    rnd = 31337
    
    if len(input_string) != 39:
        return False
    
    input_bytes = input_string.encode('utf-8')
    constants = [
        0xA3, 0xCA, 0x4C, 0x4D, 0xB3, 0xD0, 0x6D, 0x96, 0xA2, 0xB6,
        0xD7, 0xE9, 0x6B, 0x12, 0x46, 0xE1, 0xA9, 0x1A, 0x7C, 0xF3,
        0xCC, 0xFA, 0x0B, 0x23, 0x4F, 0x11, 0xD2, 0x78, 0x37, 0x24,
        0x68, 0x79, 0x7D, 0x0D, 0x1A, 0x36, 0x69, 0xB8, 0x15
    ]
    
    cumulative = 0
    
    for i in range(39):
        rand_byte = rand_val()
        current = rand_byte ^ input_bytes[i] ^ constants[i]
        cumulative |= current
    return cumulative == 0

# Testing function
def test_flag_candidate(flag):
    """
    Test if a flag candidate passes the check
    """
    result = native_check(flag)
    if result:
        print(f"✓ Valid flag: {flag}")
    else:
        print(f"✗ Invalid flag: {flag}")
    return result

# Brute force helper to find the flag (conceptually)
def brute_force_reconstruction():
    """
    This function demonstrates how to reconstruct the flag 
    by working backwards from the condition that cumulative must be 0
    """
    global rnd
    rnd = 31337
    
    constants = [
        0xA3, 0xCA, 0x4C, 0x4D, 0xB3, 0xD0, 0x6D, 0x96, 0xA2, 0xB6,
        0xD7, 0xE9, 0x6B, 0x12, 0x46, 0xE1, 0xA9, 0x1A, 0x7C, 0xF3,
        0xCC, 0xFA, 0x0B, 0x23, 0x4F, 0x11, 0xD2, 0x78, 0x37, 0x24,
        0x68, 0x79, 0x7D, 0x0D, 0x1A, 0x36, 0x69, 0xB8, 0x15
    ]
    
    
    flag_chars = []
    for i in range(39):
        rand_byte = rand_val()
        flag_byte = rand_byte ^ constants[i]
        flag_chars.append(chr(flag_byte))
    
    flag = ''.join(flag_chars)
    print(f"Reconstructed flag: {flag}")
    return flag

if __name__ == "__main__":
    flag = brute_force_reconstruction()