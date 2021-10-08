from PIL import Image, ImageDraw, ImageFont
import sys
import argparse


# Get our parameters from the command line
parser = argparse.ArgumentParser(description='Turns an image into coloured BB-Code.')
parser.add_argument("image", help="path to image file")
parser.add_argument("outfile", help="path to output file")
parser.add_argument("--text", help="text to repeat", default="MESH")
parser.add_argument("--scale", help="factor to scale image by", default=1.0)
parser.add_argument("--alpha", help="whether to use transparency", action="store_true")
args = parser.parse_args()


def scale_image(image, new_width=100, new_height=0):
    (original_width, original_height) = image.size
    
    if new_height == 0:
        aspect_ratio = original_height/float(original_width)
        new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image

# Open the image
im = None
try:
    im = Image.open(args.image).convert('RGBA')
except Exception as e:
    print("Unable to open image file {}.".format(args.image))
    print(e)
    sys.exit(1)

# Get the amount of text required to cover the image
drawer = ImageDraw.Draw(im)
font = ImageFont.truetype('Verdana.ttf', 14)
fontSize = drawer.textsize(args.text, font=font)
fontOffset = font.getoffset(args.text)

charsAcross = int((im.size[0]/(fontSize[0]+fontOffset[0]))*len(args.text)*float(args.scale))
charsHigh = int((im.size[1]/(fontSize[1]+fontOffset[1]))*float(args.scale))

# Scale the image to one pixel per character
image = scale_image(im, charsAcross, charsHigh)

char_count = 0
current_line = ""
image_ascii = []
previous = (0, 0, 0, 1)

# Iterate over the pixels in the image
for pixel_value in image.getdata():
    r,g,b,a = pixel_value

    if char_count % charsAcross == 0: # start of the line
        previous = ((r * a), (g * a), (b * a), a)
        begin = True
    elif (abs(previous[0] - (r * a)) < 5) and (abs(previous[1] - (g * a)) < 5) and (abs(previous[2] - (b * a)) < 5) and (abs(previous[3] - a) < 5): # somewhere in the middle, check difference with previous char
        # no difference so don't end or start again
        begin = False
    else: # too large difference, we end and begin a new one
        previous = ((r * a), (g * a), (b * a), a)
        current_line += "[/color]"
        begin = True
	
	# Get the individual colour components as hexadecimal strings
    a = a/float(255)
    r = hex(int(r * a)).split('x')[1].zfill(2)
    g = hex(int(g * a)).split('x')[1].zfill(2)
    b = hex(int(b * a)).split('x')[1].zfill(2)

    color = "#" + str(r) + str(g) + str(b)

    # If we have set the --alpha parameter and the alpha is less than 10%
    if a < 0.1 and args.alpha:
        color = "transparent"

	# Choose the character we need from the string
    character = args.text[char_count % len(args.text)]

    if begin:
        current_line += "[color=" + color + "]"

    current_line += character 

    if char_count % charsAcross == (charsAcross-1):
        current_line += "[/color]"
        image_ascii.append(current_line)
        current_line = ""
    char_count += 1

# Write the output to the file
f = open(args.outfile, 'w')
f.write("\n".join(image_ascii))
f.close()
