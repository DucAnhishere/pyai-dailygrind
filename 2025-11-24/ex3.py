from PIL import Image, ImageFilter

def blur(img):          # simple average blur
    img = img.filter(ImageFilter.BLUR)
    return img

def sharpen(img):       # classic sharpening kernel
    img = img.filter(ImageFilter.SHARPEN)
    return img

def edge_detect(img):   # Sobel or Laplacian
    img = img.filter(ImageFilter.FIND_EDGES)
    return img