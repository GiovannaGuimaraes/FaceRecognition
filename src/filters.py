import numpy as np
from PIL import Image, ImageOps
from PIL import ImageFilter
import sys

# Filters
def applyFilter(image, operation):
	return image.filter(operation)

def autocontrast(img):
	return ImageOps.autocontrast(img, cutoff=0, ignore=None)

def equalize(img):
	return ImageOps.equalize(img, mask=None)
	
def flip(img):
	return ImageOps.flip(img)
	
def grayscale(img):
	return ImageOps.grayscale(img)
	
def invert(img):
	return ImageOps.invert(img)
	
def mirror(img):
	return ImageOps.mirror(img)
	
def posterize(img):
	return ImageOps.posterize(img, bits=3)
	
def solarize(img):
	return ImageOps.solarize(img, threshold=128)


# Distortion functions
def quad_as_rect(quad):
    if quad[0] != quad[2]: return False
    if quad[1] != quad[7]: return False
    if quad[4] != quad[6]: return False
    if quad[3] != quad[5]: return False
    return True

def quad2rect(quad):
    assert(len(quad) == 8)
    assert(quad_as_rect(quad))
    return (quad[0], quad[1], quad[4], quad[3])

def rect2quad(rect):
    assert(len(rect) == 4)
    return (rect[0], rect[1], rect[0], rect[3], rect[2], rect[3], rect[2], rect[1])

def createRect(shape):
    assert(len(shape) == 2)
    return (0, 0, shape[0], shape[1])

def griddify(rect, xRes, yRes):
    
    # Get width and height from original image
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]
    
    # Calculate step based on distortion resolution
    xStep = w / float(xRes)
    yStep = h / float(yRes)
    
    y = rect[1]
    vertexMat = []
    
    for _ in range(yRes + 1):
    
        vertexMat.append([])
        x = rect[0]

        for _ in range(xRes + 1):
            vertexMat[-1].append([int(x), int(y)])
            x += xStep

        y += yStep

    grid = np.array(vertexMat)

    return grid

def distort(org_grid, maxDistortion):

    newGrid = np.copy(org_grid)
    
    minX = np.min(newGrid[:, :, 0])
    minY = np.min(newGrid[:, :, 1])
    maxX = np.max(newGrid[:, :, 0])
    maxY = np.max(newGrid[:, :, 1])
    
    # Create a random matrix
    newGrid += np.random.randint(-maxDistortion, maxDistortion+1, newGrid.shape)

    # Populate it getting maximum and minimum inside original range
    newGrid[:, :, 0] = np.maximum(minX, newGrid[:, :, 0])
    newGrid[:, :, 1] = np.maximum(minY, newGrid[:, :, 1])
    newGrid[:, :, 0] = np.minimum(maxX, newGrid[:, :, 0])
    newGrid[:, :, 1] = np.minimum(maxY, newGrid[:, :, 1])
    
    return newGrid

def gridToMesh(src, dest):
    
    assert(src.shape == dest.shape)
    mesh = []
    
    for i in range(src.shape[0] - 1):
        for j in range(src.shape[1] - 1):
            
            srcQuad = [src[i    , j    , 0], src[i    , j    , 1],
                       src[i + 1, j    , 0], src[i + 1, j    , 1],
                       src[i + 1, j + 1, 0], src[i + 1, j + 1, 1],
                       src[i    , j + 1, 0], src[i    , j + 1, 1]]
            
            destQuad = [dest[i    , j    , 0], dest[i    , j    , 1],
                        dest[i + 1, j    , 0], dest[i + 1, j    , 1],
                        dest[i + 1, j + 1, 0], dest[i + 1, j + 1, 1],
                        dest[i    , j + 1, 0], dest[i    , j + 1, 1]]
            
            dst_rect = quad2rect(destQuad)
            mesh.append([dst_rect, srcQuad])

    return mesh
