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