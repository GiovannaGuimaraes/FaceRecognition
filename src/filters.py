import PIL
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
filtered = applyFilter(image, str(sys.argv[2]))
filtered.show()

'''
image2 = PIL.ImageOps.autocontrast(image, cutoff=0, ignore=None)

#black = (255, 0, 0)
#white = (0, 255, 0)
#image2 = PIL.ImageOps.colorize(image, black, white)

image2 = PIL.ImageOps.crop(image, border=0)

#image2 = PIL.ImageOps.deform(image, deformer, resample=2)

image2 = PIL.ImageOps.equalize(image, mask=None)

image2 = PIL.ImageOps.expand(image, border=0, fill=0)

#image2 = PIL.ImageOps.fit(image, size, method=0, bleed=0.0, centering=(0.5, 0.5))

image2 = PIL.ImageOps.flip(image)

image2 = PIL.ImageOps.grayscale(image)

image2 = PIL.ImageOps.invert(image)

image2 = PIL.ImageOps.mirror(image)

#image2 = PIL.ImageOps.posterize(image, bits)

image2 = PIL.ImageOps.solarize(image, threshold=128)'''