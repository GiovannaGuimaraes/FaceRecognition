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

def quad_as_rect(quad):
    if quad[0] != quad[2]: return False
    if quad[1] != quad[7]: return False
    if quad[4] != quad[6]: return False
    if quad[3] != quad[5]: return False
    return True

def quad_to_rect(quad):
    assert(len(quad) == 8)
    assert(quad_as_rect(quad))
    return (quad[0], quad[1], quad[4], quad[3])

def rect_to_quad(rect):
    assert(len(rect) == 4)
    return (rect[0], rect[1], rect[0], rect[3], rect[2], rect[3], rect[2], rect[1])

def shape_to_rect(shape):
    assert(len(shape) == 2)
    return (0, 0, shape[0], shape[1])

def griddify(rect, w_div, h_div):
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]
    x_step = w / float(w_div)
    y_step = h / float(h_div)
    y = rect[1]
    grid_vertex_matrix = []
    for _ in range(h_div + 1):
        grid_vertex_matrix.append([])
        x = rect[0]
        for _ in range(w_div + 1):
            grid_vertex_matrix[-1].append([int(x), int(y)])
            x += x_step
        y += y_step
    grid = np.array(grid_vertex_matrix)
    return grid

def distort_grid(org_grid, max_shift):
    new_grid = np.copy(org_grid)
    x_min = np.min(new_grid[:, :, 0])
    y_min = np.min(new_grid[:, :, 1])
    x_max = np.max(new_grid[:, :, 0])
    y_max = np.max(new_grid[:, :, 1])
    new_grid += np.random.randint(- max_shift, max_shift + 1, new_grid.shape)
    new_grid[:, :, 0] = np.maximum(x_min, new_grid[:, :, 0])
    new_grid[:, :, 1] = np.maximum(y_min, new_grid[:, :, 1])
    new_grid[:, :, 0] = np.minimum(x_max, new_grid[:, :, 0])
    new_grid[:, :, 1] = np.minimum(y_max, new_grid[:, :, 1])
    return new_grid

def grid_to_mesh(src_grid, dst_grid):
    assert(src_grid.shape == dst_grid.shape)
    mesh = []
    for i in range(src_grid.shape[0] - 1):
        for j in range(src_grid.shape[1] - 1):
            src_quad = [src_grid[i    , j    , 0], src_grid[i    , j    , 1],
                        src_grid[i + 1, j    , 0], src_grid[i + 1, j    , 1],
                        src_grid[i + 1, j + 1, 0], src_grid[i + 1, j + 1, 1],
                        src_grid[i    , j + 1, 0], src_grid[i    , j + 1, 1]]
            dst_quad = [dst_grid[i    , j    , 0], dst_grid[i    , j    , 1],
                        dst_grid[i + 1, j    , 0], dst_grid[i + 1, j    , 1],
                        dst_grid[i + 1, j + 1, 0], dst_grid[i + 1, j + 1, 1],
                        dst_grid[i    , j + 1, 0], dst_grid[i    , j + 1, 1]]
            dst_rect = quad_to_rect(dst_quad)
            mesh.append([dst_rect, src_quad])
    return mesh

im = Image.open('./old_driver/data/train/c0/img_292.jpg')
dst_grid = griddify(shape_to_rect(im.size), 4, 4)
src_grid = distort_grid(dst_grid, 50)
mesh = grid_to_mesh(src_grid, dst_grid)
im = im.transform(im.size, Image.MESH, mesh)
im.show()	