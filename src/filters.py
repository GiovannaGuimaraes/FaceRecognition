from PIL import Image, ImageOps
from PIL import ImageFilter
import sys

def applyFilter(image, operation):
	options = {'blur': ImageFilter.BLUR,
			  'contour': ImageFilter.CONTOUR,
			  'detail': ImageFilter.DETAIL,
			  'edge_enhance': ImageFilter.EDGE_ENHANCE,
			  'edge_enhance_more': ImageFilter.EDGE_ENHANCE_MORE,
			  'emboss': ImageFilter.EMBOSS,
			  'find_edges': ImageFilter.FIND_EDGES,
			  'smooth': ImageFilter.SMOOTH,
			  'smooth_more': ImageFilter.SMOOTH_MORE,
			  'sharpen': ImageFilter.SHARPEN
			  }

	if operation not in options:
		raise ValueError("Unknown filter type.")

	return image.filter(options[operation])

image = Image.open(str(sys.argv[1])).convert("RGB") 
#filtered = applyFilter(image, str(sys.argv[2]))
#filtered.show()

#black = (255, 0, 0)
#white = (0, 255, 0)

bits = 3
opt = sys.argv[2]
# = input(); 

if(opt == 'autocontrast'):
	image2 = ImageOps.autocontrast(image, cutoff=0, ignore=None)
	image2.show()

'''if(opt == 'colorize'):
	image2 = ImageOps.colorize(image, black, white) 
	image2.show()'''

if(opt == 'crop'):
	image2 = ImageOps.crop(image, border=0)
	image2.show()

'''if(opt == 'deform'):
	image2 = ImageOps.deform(image, deformer, resample=2)
	image2.show()'''

if(opt == 'equalize'): 
	image2 = ImageOps.equalize(image, mask=None)
	image2.show()
	
if(opt == 'expand'): 
	image2 = ImageOps.expand(image, border=0, fill=0)
	image2.show()
	
'''if(opt == 'fit'): 
	image2 = ImageOps.fit(image, size, method=0, bleed=0.0, centering=(0.5, 0.5))
	image2.show()'''
	
if(opt == 'flip'):
	print ("testing flip") 
	image2 = ImageOps.flip(image)
	image2.show()
	
if(opt == 'grayscale'): 
	image2 = ImageOps.grayscale(image)
	image2.show()
	
if(opt == 'invert'): 
	image2 = ImageOps.invert(image)
	image2.show()
	
if(opt == 'mirror'):
	image2 = ImageOps.mirror(image)
	image2.show()
	
if(opt == 'posterize'): 
	image2 = ImageOps.posterize(image, bits)
	image2.show()
	
if(opt == 'solarize'): 
	image2 = ImageOps.solarize(image, threshold=128)
	image2.show()
	