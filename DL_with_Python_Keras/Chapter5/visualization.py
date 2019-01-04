from keras import models
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

model = models.load_model('../model/cat_and_dogs_small_2.h5')
model.summary()

img_path = '/home/xingyu/Downloads/Dogvscat/train/cats_and_dogs_small/test/cats/cat.1500.jpg'

img = image.load_img(img_path, target_size=(150, 150))
img_tensor = image.img_to_array(img)
img_tensor = np.expand_dims(img_tensor, axis=0)
img_tensor /= 255

print(img_tensor.shape)
# plt.imshow(img_tensor[0])
# plt.show()

# Extracts the outputs of the top 8 layers
layer_outputs = [layer.output for layer in model.layers[:8]]
# Creates a model that will return these outputs, given the model input
activation_model = models.Model(inputs=model.input, outputs=layer_outputs)

activations = activation_model.predict(img_tensor)
first_layer_activation = activations[0]

print(first_layer_activation.shape)

# plotting all features
layer_names = []
for layer in model.layers[:8]:
    layer_names.append(layer.name)

images_per_row = 16

for layer_name, layer_activation in zip(layer_names, activations):
    # the number of features in this feature map
    n_features = layer_activation.shape[-1]
    # shape (1, size, size, n_features)
    size = layer_activation.shape[1]

    n_cols = n_features // images_per_row
    display_grid = np.zeros((size * n_cols, images_per_row * size))

    for col in range(n_cols):
        for row in range(images_per_row):
            channel_image = layer_activation[0, :, :, col * images_per_row + row]
            # Post-process the feature to make it visually palatable
            channel_image -= channel_image.mean()

            if channel_image.std() != 0:
                channel_image /= channel_image.std()

            channel_image *= 64
            channel_image += 128
            channel_image = np.clip(channel_image, 0, 255).astype('uint8')
            display_grid[col * size:(col + 1) * size, row * size: (row + 1) * size] = channel_image

    scale = 1./size
    plt.figure(figsize=(scale * display_grid.shape[1],
                        scale * display_grid.shape[0]))
    plt.title(layer_name)
    plt.grid(False)
    plt.imshow(display_grid, aspect='auto', cmap='viridis')
    plt.show()

