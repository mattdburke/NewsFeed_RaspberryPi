# This is a news feed for the unicornhathd running on Raspberry Pi and python 2
#!/usr/bin/env python
import time
time.sleep(30)

import colorsys
import signal
import datetime
import numpy
from sys import exit

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit("This script requires the pillow module\nInstall with: sudo pip install pillow")

import unicornhathd


print("""Unicorn HAT HD: Text
This example shows how to draw, display and scroll text in a regular TrueType font on Unicorn HAT HD.
It uses the Python Pillow/PIL image library, and all other drawing functions are available.
See: http://pillow.readthedocs.io/en/3.1.x/reference/
""")

############# Change the text you want to display, and font, here ################

#--------------
# FINANCE BIT

while True:

	import feedparser

	def fetch_TopNews():
		n = feedparser.parse('http://feeds.reuters.com/reuters/UKTopNews')
		return (n)

	def fetch_ScienceNews():		
		w = feedparser.parse('http://feeds.reuters.com/reuters/UKScienceNews')
		return (w)
	
	def fetch_BankingFinancial():
		y = feedparser.parse('http://feeds.reuters.com/reuters/UKBankingFinancial')
		return (y)
		
	n1 = fetch_TopNews()
	w1 = fetch_ScienceNews()
	y1 = fetch_BankingFinancial()

	a = int(len(n1['entries']))
	b = int(len(w1['entries']))
	c = int(len(y1['entries']))

	TEXT = []

	def text():
		localtime = datetime.datetime.now().strftime("%B %d %Y  %H:%M")
		TEXT.append("THE DATE AND TIME IS %s"%(localtime))
		#1
		TEXT.append("THE FEED IS PROVIDED TO YOU BY REUTERS")
		TEXT.append("REUTERS: TOP NEWS")
		for i in range(a):
			h1 = n1.entries[i].title
			TEXT.append(h1)
		#2
		TEXT.append("REUTERS: SCIENCE NEWS")
		for i in range(b):
			h2 = w1.entries[i].title
			TEXT.append(h2)
		#3
		TEXT.append("REUTERS: BANKING AND FINANCIAL NEWS")
		for i in range(c):
			h3 = y1.entries[i].title
			TEXT.append(h3)
		TEXT.append("---UPDATING FEED---")
		

	text ()

#--------------




	FONT = ("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 10)

	colours = [tuple([int(n * 255) for n in colorsys.hsv_to_rgb(x/float(len(TEXT)), 1.0, 1.0)]) for x in range(len(TEXT))]


# Use `fc-list` to show a list of installed fonts on your system,
# or `ls /usr/share/fonts/` and explore.

# sudo apt install fonts-droid
#FONT = ("/usr/share/fonts/truetype/droid/DroidSans.ttf", 12)

# sudo apt install fonts-roboto
#FONT = ("/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf", 10)

################# Now, let's draw some amazing rainbowy text! ####################

# Get the width/height of Unicorn HAT HD.
# These will normally be 16x16 but it's good practise not to hard-code such numbers,
# just in case you want to try and hack together a bigger display later.
	width, height = unicornhathd.get_shape()

	unicornhathd.rotation(180)
	unicornhathd.brightness(0.7)

# We want to draw our text 1 pixel in, and 2 pixels down from the top left corner
	text_x = width
	text_y = 2

# Grab our font file and size as defined at the top of the script
	font_file, font_size = FONT

# Load the font using PIL's ImageFont
	font = ImageFont.truetype(font_file, font_size)




# Make sure we accommodate enough width to account for our text_x left offset


# Now let's create a blank canvas wide enough to accomodate our text

	text_width, text_height = width, 0
# To draw on our image, we must use PIL's ImageDraw


# And now we can draw text at our desited (text_x, text_y) offset, using our loaded font
	for i in TEXT:
		w, h = font.getsize(i)
		text_width += w + width
		text_height = max(text_height, h)

	text_width += width + text_x + 1


	image = Image.new("RGB", (text_width,max(16, text_height)))

	draw = ImageDraw.Draw(image)

	offset_left = 0

	for index, line in enumerate(TEXT):
		draw.text((text_x + offset_left, text_y), line, colours[index], font=font)
		offset_left += font.getsize(line)[0] + width
	
# To give an appearance of scrolling text, we move a 16x16 "window" across the image we generated above
# The value "scroll" denotes how far this window is from the left of the image.
# Since the window is "width" pixels wide (16 for UHHD) and we don't want it to run off the end of the,
# image, we subtract "width".


	for scroll in range(text_width - width):
		for x in range(width):
			for y in range(height):
				pixel = image.getpixel((x+scroll, y))
            # Now we want to turn the colour of our text - shades of grey remember - into a mask for our rainbow.
            # We do this by dividing it by 255, which converts it to the range 0.0 to 1.0
				r, g, b = [int(n) for n in pixel]
            # We can now use our 0.0 to 1.0 range to scale our three colour values, controlling the amount
            # of rainbow that gets blended in.
            # 0.0 would blend no rainbow
            # 1.0 would blend 100% rainbow
            # and anything in between would copy the anti-aliased edges from our text
				
            # Finally we colour in our finished pixel on Unicorn HAT HD
				unicornhathd.set_pixel(width-1-x, y, r, g, b)
    # Finally, for each step in our scroll, we show the result on Unicorn HAT HD
		unicornhathd.show()
    # And sleep for a little bit, so it doesn't scroll too quickly!
		time.sleep(0.05)

unicornhathd.off()
