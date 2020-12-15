import png
import argparse


parser = argparse.ArgumentParser()
#parser.add_argument("type", help = "read or write [ -r | -w ]")
#parser.add_argument("datatype", help = "file or text [ -f | -t ]")
parser.add_argument("-w", help = "switch to writing mode", action = "store_true")
parser.add_argument("data", help = "file name or text", type = str )

def text_to_bin(text):
    ''' convert text into arrays of bins:
        Input:
            - text (str)

        Ouput:
            - Binary arrays
    '''
    chars = bytearray(text, "utf8")
    bins = []

    for char in chars:
        bin_char = bin(char)
        bin_char = bin_char[2:]
        bin_char = list(bin_char)
        bins += bin_char

    return bins

def read(file_encrypted):
    ''' Read encrypted message in png image : 
        Input:
            - filename_encrypted (str)
        Output:
            - Message (str)
    '''
    f1 = png.Reader(file_encrypted)

    flatImg1 = f.read_flat()


def write(file,bins):
    ''' Write ASCII message in png image :
        input:
            - filename (str)
            - array of ASCII in bin 
        output:
            - True or False (if code was written)
        
        errors:
            - code is to long too fit in image
    '''

    f = png.Reader(file)
    f = f.asRGBA()
    RGBA = True if f[3]["alpha"] else False
    list_binaries_of_files = []
    for x in f[2]:
        list_binaries_of_files += list(x)

    if len(list_binaries_of_files) < len(bins):
        SystemError("Message is too long in order to fit in this image.")

    for img_value, encrypted_value  in zip(list_binaries_of_files, bins):
        bin_value = '{0:08b}'.format(img_value)
        list_bins_values = list(bin_value)
        
        print(list_bins_values)
        print(encrypted_value)
        if encrypted_value == '1':
            list_bins_values[7] = '1'
        elif list_bins_values[7] == '1' and encrypted_value == '0':
            list_bins_values[7] = '0'
        
        print(list_bins_values)
        
        break




    
def main():
    ''' Main function '''
    args = parser.parse_args()

    if args.w:
        bins = text_to_bin("test")
        write(args.data,bins)
    else:
        read(args.data)


if __name__ == '__main__':
    main()
