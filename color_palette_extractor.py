import seaborn as sns
sns.set()
from functools import partial
import color_palette_tools

#KEY 1 = KMEANS + RGB
#KEY 2 = KMEANS + HSV
#KEY 3 = GAUSSIANMIXTURE + RGB
#KEY 4 = GAUSSIANMIXTURE + HSV

low_cutoff = 0.1
high_cutoff = 0.8
n_colors = 15

key_palette = 3

# img_path = input("Please, enter the image path: ")
img_path = "./pictures/int2.jpg"


print("Filtering pixels outside the range [{},{}]...".format(low_cutoff, high_cutoff))
print("-" * 65 + "\n")

palette, title = color_palette_tools.make_palette(
    img_path,
    nclusters=n_colors,
    palette_to_do = key_palette,
    filter_fn=partial(
        color_palette_tools.filter_pixels,
        low=low_cutoff,
        high=high_cutoff,

    )
)


url = color_palette_tools.get_url_from_palette(palette)
print("Here it is your palette using {}: {}".format(title,url))


exit()
