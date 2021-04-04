import numpy as np
from PIL import Image
import time

for i in range(2320):

    imageArray = np.random.rand(400, 400, 3) * 255

    image = Image.fromarray(imageArray.astype("uint8")).convert("RGBA")

    image.save("/Users/anonymousvikram/recyclingVision/downloads/not drink can single/notCan" + str(i) + ".png")

    print(str(i) + "/2320")

    time.sleep(0.05)