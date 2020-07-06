from os import _exit as exit

def get_image_dimensions_string(file_name):
    '''
    Given the file name for a valid PPM file, this function will return the
    image dimensions as a string. For example, if the image stored in the
    file is 150 pixels wide and 100 pixels tall, this function should return
    the string '150 100'.
    file_name: A string. A PPM file name.
    '''
    image_file = open(file_name, 'r')
    image_file.readline()
    return image_file.readline().strip('\n')

def load_image_pixels(file_name):
    ''' Load the pixels from the image saved in the file named file_name.
    The pixels will be stored in a 3d list, and the 3d list will be returned.
    Each list in the outer-most list are the rows of pixels.
    Each list within each row represents and individual pixel.
    Each pixels is representd by a list of three ints, which are the RGB values of that pixel.
    '''
    pixels = []
    image_file = open(file_name, 'r')

    image_file.readline()
    image_file.readline()
    image_file.readline()

    width_height = get_image_dimensions_string(file_name)
    width_height = width_height.split(' ')
    width = int(width_height[0])
    height = int(width_height[1])

    for line in image_file:
        line = line.strip('\n ')
        rgb_row = line.split(' ')
        row = []
        for i in range(0, len(rgb_row), 3):
            pixel = [int(rgb_row[i]), int(rgb_row[i+1]), int(rgb_row[i+2])]
            row.append(pixel)
        pixels.append(row)

    return pixels, width, height

def main():
    '''The main function loads the pixels from the file,
    uses an algorithm to generate a new image based on the
    users two input values, and opens and writes the file.
    f.write: writes the user file after implementation of algorithm
    '''
    channel = input(str('Enter color channel\n'))
    if channel not in ('r','g','b'):
        print('Channel must be r, g, or b. Will exit.')
        exit(0)
    channel_difference = float(input('Enter color channel difference\n'))
    if channel_difference <= 1.0 or channel_difference > 12.0:
        print('Invalid channel difference. Will exit.')
        exit(0)
    gs_file = input('Enter greenscreen image file name\n')
    fi_file = input('Enter fill image file name\n')

    #loads pixels
    gs_file_pixels,gs_width,gs_height = load_image_pixels(gs_file)
    fi_file_pixels,fi_width,fi_height = load_image_pixels(fi_file)
    if gs_width != fi_width or gs_height!=fi_height:
        print('Images not the same size. Will exit.')
        exit(0)
    out_file = input('Enter output file name\n')
    out_file_pixels = list()
    cd = float(channel_difference)

    #greenscreen algorithm: generates a new image
    #based on two input values
    for row in range(len(gs_file_pixels)):
        out_pixels_row = list()
        for column in range(len(gs_file_pixels[row])):
            pixels = gs_file_pixels[row][column]
            r = pixels[0]
            g = pixels[1]
            b = pixels[2]
            if(channel == 'r'):
               if(r > g*cd and r > b*cd):
                   out_pixels_row.append(fi_file_pixels[row][column])
               else:
                   out_pixels_row.append(pixels)
            elif(channel == 'g'):
               if(g > r*cd and g > b*cd):
                   out_pixels_row.append(fi_file_pixels[row][column])
               else:
                   out_pixels_row.append(pixels)
            else:
                if(b > r*cd and b > g*cd):
                   out_pixels_row.append(fi_file_pixels[row][column])
                else:
                   out_pixels_row.append(pixels)

        out_file_pixels.append(out_pixels_row)

   #opens and writes the file
    f = open(out_file, 'w')
    f.write('P3\n')
    f.write('%d %d\n255\n' % (len(out_file_pixels[0]), len(out_file_pixels)))
    for i in out_file_pixels:
        for j in i:
            for k in j:
                f.write(str(k))
                f.write(' ')
            f.write('')
        f.write('\n')

    f.close()
    print('Output file written. Exiting.')

main()
