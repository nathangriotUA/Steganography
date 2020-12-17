import png
import argparse
import subprocess


parser = argparse.ArgumentParser()
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
    # EOM (END OF MESSAGE) signals that it's the end of the message
    chars = bytearray(text+"EOM", "utf8")
    bins = []

    for char in chars:
        bin_char = bin(char)
        bin_char = bin_char[2:]
        bin_char = list(bin_char)
        bins += bin_char

    return bins

def check_conditions(ASCII,conditions):
    ''' This method checks if the conditions are met to stop reading the file
        input:
            ASCII char
        output:
            True if conditions are met
            False if conditions are not met
    '''
    keys = conditions.keys()
    for i in keys:
        if not conditions[i] and ASCII == i:
            conditions[i] = True
            break

        elif not conditions[i] and ASCII != i:
            for condition in conditions:
                condition = False
            break
       
    return conditions["F"]


def read(file_encrypted):
    ''' Read encrypted message in png image : 
        Input:
            - filename_encrypted (str)
        Output:
            - Message (str)
    '''
    f = png.Reader(file_encrypted)
    f = f.asRGBA() # Every png is converted in a RGBA format
    img= []
    list_binaries_of_files = []
    for x in f[2]:
        img.append(list(x))
        list_binaries_of_files += list(x)
    
    i = 0
    ASCIIS = []
    ASCII = []

    stop_Condition = {"E" : False, "O" : False, "F" : False}

    test = 0
    for img_value in list_binaries_of_files:
        value = '{0:08b}'.format(img_value)[-1:] # get low weight bit
        ASCII.append(value)
        i+=1

        if i == 8:
            i = 0
            ASCII = "".join(ASCII)
            ASCII_char = chr(int(ASCII, 2))
            ASCIIS.append(ASCII_char)
            ASCII = []

            test += 1
            if check_conditions(ASCII_char, stop_Condition) or test == 10:
                break

    return "".join(ASCIIS)

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
    f = f.asRGBA() # Every png is converted in a RGBA format
    list_binaries_of_files = []
    img= []
    for x in f[2]:
        img.append(list(x))
        list_binaries_of_files += list(x)

    if len(list_binaries_of_files) < len(bins):
        SystemError("Message is too long in order to fit in this image.")

    print(img[0][:10])
    newImg = []
    for img_value, encrypted_value  in zip(list_binaries_of_files, bins):
        bin_value = '{0:08b}'.format(img_value)
        list_bins_values = list(bin_value)
        
        if encrypted_value == '1':
            list_bins_values[7] = '1'
        elif list_bins_values[7] == '1' and encrypted_value == '0':
            list_bins_values[7] = '0'
        
        new_bin = ''.join(list_bins_values)
        newImg.append(int(new_bin, 2))

    i = 0
    for x in img:
        for value in x:
            print(value,newImg[i])
            value = newImg[i]
            i+=1
            if i == len(newImg):
                break
        if i == len(newImg):
            break
    print(img[0][:10])

    f_encrypted = open(file[:-4] + '_encrypted.png', 'wb')
    w = png.Writer(f[0], f[1], greyscale=False, bitdepth=f[3]["bitdepth"], alpha=True)
    w.write(f_encrypted, img)
    f_encrypted.close()
    


def main():
    ''' Main function '''
    args = parser.parse_args()

    if args.w:
        bins = text_to_bin("test"+"EOF")
        write(args.data,bins)
    else:
        read(args.data)


if __name__ == '__main__':
    main()
