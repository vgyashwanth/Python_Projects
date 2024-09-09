

# Load .srec file content
srec_file_path = '/mnt/data/gc2k_pcbxxx.srec'
with open(srec_file_path, 'r') as file:
    srec_content = file.read()

# Function to reverse bits in a byte
def reverse_bits(byte, bit_count=8):
    result = 0
    for _ in range(bit_count):
        result = (result << 1) | (byte & 1)
        byte >>= 1
    return result

# Function to compute CRC16-IBM
def crc16_ibm(data):
    crc = INIT
    for byte in data:
        # Reverse bits if RefIn is True
        if REF_IN:
            byte = reverse_bits(byte)
        
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ POLY
            else:
                crc <<= 1
            crc &= 0xFFFF  # Ensure CRC is 16-bit

    # Reverse bits if RefOut is True
    if REF_OUT:
        crc = reverse_bits(crc, 16)
    
    # Apply XOR_OUT
    crc ^= XOR_OUT
    return crc

# Convert .srec file to binary data
srec_binary_data = b''
for line in srec_content.splitlines():
    # Only process data records starting with 'S1' (16-bit address, data)
    if line.startswith('S1'):
        byte_count = int(line[2:4], 16)
        address = line[4:8]  # Address is 4 characters (2 bytes)
        data = line[8:8 + (byte_count - 3) * 2]  # Data field (Byte count - 3 for address and checksum)
        
        # Convert data to bytes and append to binary data
        srec_binary_data += bytes.fromhex(data)

# Compute CRC16-IBM for the binary data
crc16_result = crc16_ibm(srec_binary_data)
crc16_result_hex = hex(crc16_result).upper()
crc16_result_hex
