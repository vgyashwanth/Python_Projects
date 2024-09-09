import binascii

# CRC parameters for CRC16-IBM
POLY = 0x8005
INIT = 0x0000
XOR_OUT = 0x0000
REF_IN = True
REF_OUT = True

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


def parse_srec_file(file_path):
    srec_binary_data = b''
    data = bytearray()
    with open(file_path, 'r') as f:
        for line in f:
            # Only process data records (S1, S2, S3) and exclude S0, S5, S7, S8, S9.
            if line.startswith('S1') or line.startswith('S2') or line.startswith('S3'):
                byte_count = int(line[2:4], 16)  # Byte count field converting hex to int
                # Convert hex data from S-record to binary data
                record_data = line[12:(12+(byte_count-5)*2)]  # Skip address bytes and checksumbytes
                data_bytes = binascii.unhexlify(record_data)
                data.extend(data_bytes)
                srec_binary_data += bytes.fromhex(record_data)
    
    return data

# File path to the SREC file
file_path = 'gc2k_pcbxxx.srec'

# Parse the SREC file and calculate CRC16
srec_data = parse_srec_file(file_path)
crc16_value = crc16_ibm((srec_data))
hex_value = hex(crc16_value)
print(hex_value)


