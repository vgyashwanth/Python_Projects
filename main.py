
import tkinter as tk
import binascii
from tkinter import filedialog

def reflect(data, bits):
    reflection = 0
    for i in range(bits):
        if data & (1 << i):
            reflection |= (1 << (bits - 1 - i))
    return reflection

# Function to calculate CRC16/ARC
def crc16_arc(data):
    # CRC16/ARC uses 0x8005 polynomial and initial CRC of 0x0000
    crc = 0x0000
    poly = 0x8005
    
    for byte in data:
        byte = reflect(byte, 8)  # Reflect each byte before processing
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFF  # Ensure CRC remains within 16 bits
    
    return reflect(crc, 16)  # Reflect the final CRC value

# Function to parse SREC file (address + data fields for CRC calculation)
def parse_srec_file_for_crc(file_path):
    data = bytearray()

    with open(file_path, 'r') as f:
        for line in f:
            # Only process data records (S1, S2, S3) and exclude S0, S5, S7, S8, S9.
            if line.startswith('S1') or line.startswith('S2') or line.startswith('S3'):
                byte_count = int(line[2:4], 16)  # Byte count field
                
                # Extract address and data fields
                if line.startswith('S1'):
                    address_length = 4  # S1: 2-byte (4 hex characters) address
                elif line.startswith('S2'):
                    address_length = 6  # S2: 3-byte (6 hex characters) address
                elif line.startswith('S3'):
                    address_length = 8  # S3: 4-byte (8 hex characters) address
                
                # Extract the address field
                address_field = line[4:4 + address_length]
                address_data = binascii.unhexlify(address_field)
                
                # Extract data field (excluding checksum byte)
                data_length = (byte_count - (address_length // 2) - 1) * 2
                data_field = line[4 + address_length:4 + address_length + data_length]
                data_bytes = binascii.unhexlify(data_field)
                
                # Add both address and data to the CRC calculation
                data.extend(address_data)
                data.extend(data_bytes)
    
    return data



# Parse the SREC file and calculate CRC16



def merge_files(input_files, output_file_path, output_file, root):
    """Merges the contents of multiple files into a single output file.

    Args:
        input_files (list): A list of input file paths.
        output_file (str): The path of the output file.
    """
    #checking whether the inputs and outputs are correctly entered

    for file in input_files:
        if(file == ""):
            GenerateError(root)
            return

    if(output_file_path == ""):
        GenerateError(root)
        return 

    if(output_file == ""):
        GenerateError(root)
        return 
    #compute CRC for the Firmware file          
    output_file_path = output_file_path + "/" + output_file + ".srec" #creating the file path
    output_file = output_file_path #copying back to variable
    #flags to record the repetitions
    first_time_string1 = True
    first_time_string2 = True
    first_time_string3 = True
    string1 = "S0"
    string2 = "S3150100A150FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF08"
    string3 = "S7"
    with open(output_file, 'w') as outfile:
        for input_file in input_files:
            with open(input_file, 'r') as infile:
                for line in infile: #monitoring each line in file

                    if((string1 in line) and first_time_string1):
                        outfile.write(line)     #first time writing string1
                        first_time_string1 = False
                        continue

                    if(line.strip() == string2 and first_time_string2):
                        first_time_string2 = False #avoid first time writing string2
                        continue

                    if((string1 in line) and not first_time_string1):
                        continue    #avoid second time writing string1

                    if((string3 in line) and first_time_string3):
                        first_time_string3 = False #avoid first writing string3
                        continue
               

                    outfile.write(line)
                
    FilesMergeSucess(root)

def GenerateSrecString(CRC16_Value):
    str = f"S3XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    return str
def FilesMergeSucess(root):
        # Create a new top-level window for the error
    error_window = tk.Toplevel(root)
    error_window.title("Success")
    
    # Set the size of the window
    error_window.geometry("300x100")
    
    # Create a frame with a red background to represent the red box
    red_box = tk.Frame(error_window, bg="white", padx=10, pady=10)
    red_box.pack(fill="both", expand=True)
    
    # Add a label inside the red box to display the error message
    error_label = tk.Label(red_box, text="Merged Successfully !", bg="light green", fg="black", font=("Arial", 14))
    error_label.pack(padx=10, pady=20)

def select_file():
    """Opens a file dialog to select a single file."""
    file_path = filedialog.askopenfilename(filetypes=[("SREC Files", "*.srec")])
    if file_path:
        return file_path
def select_folder():

    dir_path = filedialog.askdirectory()
    if dir_path:
        return dir_path    
    
def GenerateError(root):
    # Create a new top-level window for the error
    error_window = tk.Toplevel(root)
    error_window.title("Error")
    
    # Set the size of the window
    error_window.geometry("300x100")
    
    # Create a frame with a red background to represent the red box
    red_box = tk.Frame(error_window, bg="white", padx=10, pady=10)
    red_box.pack(fill="both", expand=True)
    
    # Add a label inside the red box to display the error message
    error_label = tk.Label(red_box, text="Please select the requried files !", bg="red", fg="white", font=("Arial", 14))
    error_label.pack(padx=10, pady=20)

  

def update_latest_entry(entry,path):
    if path:
        entry.delete(0,tk.END)
        entry.insert(0,path)

def create_ui():
    """Creates a simple GUI for selecting files."""

    window = tk.Tk()
    window.title(".srec Files Merger")
    window.geometry("400x200")
   

    # Input file labels and entry fields
    input_file1_label = tk.Label(window, text="Boot Loader:")
    input_file1_label.grid(row=0, column=0)
    input_file1_entry = tk.Entry(window)
    input_file1_entry.grid(row=0, column=1)

    input_file2_label = tk.Label(window, text="Firmware:")
    input_file2_label.grid(row=1, column=0)
    input_file2_entry = tk.Entry(window)
    input_file2_entry.grid(row=1, column=1)

    # Program name label and entry field
    output_file_path_label = tk.Label(window, text="Output File Location:")
    output_file_path_label.grid(row=2, column=0)
    output_file_path_entry = tk.Entry(window)
    output_file_path_entry.grid(row=2, column=1)

    # Program name label and entry field
    output_file_label = tk.Label(window, text="File name:")
    output_file_label.grid(row=3, column=0)
    output_file_entry = tk.Entry(window)
    output_file_entry.grid(row=3, column=1)


    # Browse buttons
    input_file1_button = tk.Button(window, text="Browse", command=lambda: update_latest_entry(input_file1_entry, select_file()))
    input_file1_button.grid(row=0, column=2)

    input_file2_button = tk.Button(window, text="Browse", command=lambda: update_latest_entry(input_file2_entry, select_file()))
    input_file2_button.grid(row=1, column=2)

    output_file_path_button = tk.Button(window, text="Browse", command=lambda: update_latest_entry(output_file_path_entry, select_folder()))
    output_file_path_button.grid(row=2, column=2)
    
    # Process button
    process_button = tk.Button(window, text="Process Files", command=lambda: merge_files([input_file1_entry.get(), input_file2_entry.get()],output_file_path_entry.get(), output_file_entry.get(),window))
    process_button.grid(row=4, columnspan=3)

    window.mainloop()
                       


if __name__ == "__main__":
    
    create_ui()
    print("Files merged successfully!")