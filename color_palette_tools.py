
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import color
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

from typing import Union, Callable

def rgb2hex(c):
    c = c*255
    return "{:02x}{:02x}{:02x}".format(int(c[0]),int(c[1]),int(c[2]))

def read_image(path: Union[str,Path]) -> np.ndarray:
    with open(path,"rb") as f:
        return np.array(Image.open(f))

def get_kmeans_centers(img: np.ndarray, nclusters: int) -> np.ndarray:
    return KMeans(n_clusters=nclusters).fit(img).cluster_centers_

def get_gaussian_mixture_centers(img,nclusters):
    return GaussianMixture(n_components=nclusters).fit(img).means_
    
def rgb2hsv(dat: np.ndarray) -> np.ndarray:
    return color.rgb2hsv(dat)

def hsv2rgb(dat: np.ndarray) -> np.ndarray:
    return color.hsv2rgb(dat)

def preprocess_image(img: np.ndarray) -> np.ndarray:
    return img.reshape((-1,3)).astype("float32") / 255

def make_palette(path: Union[str,Path], palette_to_do = 1, nclusters: int = 8, filter_fn: Callable[[np.ndarray],np.ndarray] = None, ):
    # Load the image
    img = read_image(path)
    
    # Reshape and set range
    rgb_pixels = preprocess_image(img)
    
    # If filter_fn is set, filter pixels
    if filter_fn is not None:
        rgb_pixels = filter_fn(rgb_pixels)


    # Cluster the pixels
    if palette_to_do == 1:
        palette_centers = get_kmeans_centers(rgb_pixels,nclusters)
        title = "KMeans in RGB color space"

    if palette_to_do == 2:
        # Convert RGB to HSV
        hsv_pixels = rgb2hsv(rgb_pixels)

        palette_centers = get_kmeans_centers(hsv_pixels,nclusters)
        palette_centers = hsv2rgb(palette_centers)
        title = "KMeans in HSV color space"

    if palette_to_do == 3:
        palette_centers = get_gaussian_mixture_centers(rgb_pixels, nclusters)
        title = "GaussianMixture in RGB color space"

    if palette_to_do == 4:
        # Convert RGB to HSV
        hsv_pixels = rgb2hsv(rgb_pixels)
        palette_centers = get_gaussian_mixture_centers(hsv_pixels,nclusters)
        palette_centers = hsv2rgb(palette_centers)
        title = "GaussianMixture in HSV color space"

    # Plot the image
    plt.rcParams["axes.grid"] = False
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize = (16,9), sharex=False, sharey=False, gridspec_kw={'height_ratios': [10, 1]})
    ax[0].imshow(img)
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    # Plot the palette

    ax[1].imshow(palette_centers[np.concatenate([[i] * 4000 for i in range(len(palette_centers))]).reshape((-1,40)).T])
    ax[1].set_xticks([])
    ax[1].set_yticks([])
    plt.show()
    print("\n" + "=" * 100 + "\n")

    return palette_centers, title

def filter_pixels(pixels: np.ndarray, low = 0.0, high = 1.0) -> np.ndarray:
    pix_mean = pixels.mean(1)
    mask = (low <= pix_mean) & (pix_mean <= high)
    idx = np.arange(len(pixels))
    return pixels[idx[mask]]


def get_url_from_palette(palette):
    hex_colors = []
    for color in palette:
        hex_colors.append(rgb2hex(color))

    url = "https://coolors.co/" + "-".join(hex_colors)
    return url



