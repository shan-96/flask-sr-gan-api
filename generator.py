import keras
import numpy as np
import io
import base64
from PIL import Image
import matplotlib.pyplot as plt
from libs.srgan import SRGAN
from libs.util import DataLoader


def generateSR(img_url):
    gan = SRGAN(upscaling_factor=4, training_mode=False)
    gan.load_weights('./model/gen4X.h5')

    img_lr = DataLoader.load_img(img_url).astype(np.uint8)

    # Resize image (you can skip this if you are doing it on original image)
    img_lr = np.array(Image.fromarray(img_lr).resize((50, 50), Image.BICUBIC))

    # Scale image
    img_lr = DataLoader.scale_lr_imgs(img_lr)

    # Predict high-resolution version (add batch dimension to image)
    img_sr = np.squeeze(
        gan.generator.predict(
            np.expand_dims(img_lr, 0),
            batch_size=1
        ),
        axis=0
    )

    # Unscale colors
    img_sr = DataLoader.unscale_hr_imgs(img_sr).astype(np.uint8)
    img_lr = DataLoader.unscale_lr_imgs(img_lr).astype(np.uint8)

    # Images and titles
    images = {
        'Original': img_lr,
        'SRGAN': img_sr,
    }

    # Plot the images. Note: rescaling and using squeeze since we are getting batches of size 1
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    for i, (title, img) in enumerate(images.items()):
        axes[i].imshow(img)
        axes[i].set_title("{} - {}".format(title, img.shape))
        axes[i].axis('off')

    i = io.BytesIO()
    plt.savefig(i, format='png', bbox_inches='tight')
    i.seek(0)
    # return plt.show()
    encode64 = base64.b64encode(i.getvalue())
    # return '<img src="data:image/png;base64, {}">'.format(encode64.decode('utf-8'))
    keras.backend.clear_session()
    return "data:image/png;base64, {}".format(encode64.decode('utf-8'))