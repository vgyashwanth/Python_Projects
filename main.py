import os

def merge_files(input_files, output_file):
    """Merges the contents of multiple files into a single output file.

    Args:
        input_files (list): A list of input file paths.
        output_file (str): The path of the output file.
    """
    avoid_writing = True
    with open(output_file, 'w') as outfile:
        for input_file in input_files:
            with open(input_file, 'r') as infile:
                outfile.write(infile.read())
               
                


if __name__ == "__main__":
    input_files = ['BL_RA6M2_GC2K_V1.28_CONTRAST50_PLM13200.srec', 'gc2k_pcbxxx.srec']  # Replace with your input files
    output_file = 'output.srec'

    merge_files(input_files, output_file)
    print("Files merged successfully!")