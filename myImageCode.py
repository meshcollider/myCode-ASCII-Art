from PIL import Image, ImageDraw, ImageFont
import sys

# Get our parameters from the command line
if len(sys.argv) == 6:
	image_file_path = sys.argv[1]
	out_file_path = sys.argv[2]
	repeat_text = sys.argv[3]
	scale = float(sys.argv[4])
	alpha = int(sys.argv[5])
elif len(sys.argv) == 5:
	image_file_path = sys.argv[1]
	out_file_path = sys.argv[2]
	repeat_text = sys.argv[3]
	scale = float(sys.argv[4])
	alpha = 0
elif len(sys.argv) == 4:
	image_file_path = sys.argv[1]
	out_file_path = sys.argv[2]
	repeat_text = sys.argv[3]
	scale = 1
	alpha = 0
elif len(sys.argv) == 3:
	image_file_path = sys.argv[1]
	out_file_path = sys.argv[2]
	repeat_text = "MESH"
	scale = 1
	alpha = 0
else:
	print("USAGE: <IMAGE PATH> <OUTFILE> [TEXT] [SCALE FACTOR] [USE TRANSPARENT]")
	sys.exit(0)

repeat_text_array = list(repeat_text)
	
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
    im = Image.open(image_file_path).convert('RGBA')
except Exception as e:
    print("Unable to open image file {image_filepath}.".format(image_filepath=image_file_path))
    print(e)
    sys.exit(1)

# Get the amount of text required to cover the image
drawer = ImageDraw.Draw(im)
font = ImageFont.truetype('Verdana.ttf', 14)
fontSize = drawer.textsize(repeat_text, font=font)
fontOffset = font.getoffset(repeat_text)

charsAcross = int((im.size[0]/(fontSize[0]+fontOffset[0]))*len(repeat_text)*scale)
charsHigh = int((im.size[1]/(fontSize[1]+fontOffset[1]))*scale)

# Scale the image to one pixel per character
image = scale_image(im, charsAcross, charsHigh)
pixels_in_image = list(image.getdata())
count = 0

output = ""
image_ascii = []
previous = (0, 0, 0, 1)
color = "#000000"
transparent = False

# Iterate over the pixels in the image
for pixel_value in pixels_in_image:
    r,g,b,a = pixel_value
    bbcode = ""
    
    if count % charsAcross == 0: # start of the line
        previous = ((r * a), (g * a), (b * a), a)
        begin = True
        end = False
    elif (abs(previous[0] - (r * a)) < 5) and (abs(previous[1] - (g * a)) < 5) and (abs(previous[2] - (b * a)) < 5) and (abs(previous[3] - a) < 5): # somewhere in the middle, check difference with previous char
        end = False # no difference so don't end or start again
        begin = False
    else: # too large difference, we end and begin a new one
        previous = ((r * a), (g * a), (b * a), a)
        end = True
        begin = True
	
	# Get the individual colour components as hexadecimal strings
    a = a/255
    r = hex(int(r * a)).split('x')[1].zfill(2)
    g = hex(int(g * a)).split('x')[1].zfill(2)
    b = hex(int(b * a)).split('x')[1].zfill(2)

    color = "#" + str(r) + str(g) + str(b)
	
	# If we have set the USE ALPHA parameter and the alpha is less than 10%
    if a < 0.1 and alpha == 1:
        color = "transparent"
		
	# Choose the character we need from the string
    character = repeat_text_array[count % len(repeat_text)]
    
    if end:
        bbcode += "[/color]"
    if begin:
        bbcode += "[color=" + color + "]"
        
    bbcode += character 

    output += bbcode
    
    if count % charsAcross == (charsAcross-1):
        output += "[/color]"
        image_ascii.append(output)
        output = ""

    count += 1

# Write the output to the file
f = open(out_file_path, 'w')
f.write("\n".join(image_ascii))
f.close()
