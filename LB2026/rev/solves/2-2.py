import struct 


s1 = 0x48195163427A6F67
s2 = 0x4E1A1D4E1C4C1218
s3 = 0x1D4B124E4F494E49
s4 = 0x1E124C1E4F1D1B13
s5 = 0x5713131E4E1F1C1E

data = b""

data += struct.pack('<Q', s1)
data += struct.pack('<Q', s2)
data += struct.pack('<Q', s3)
data += struct.pack('<Q', s4)
data += struct.pack('<Q', s5)[1:]


print(''.join([chr(elem ^ 0x2A) for elem in data]))