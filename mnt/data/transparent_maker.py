import cv2

# Read the stone texture image
image = cv2.imread("./mnt/data/minecraft_stone_texture.webp", cv2.IMREAD_UNCHANGED)

# Check if the image has an alpha channel
if image.shape[2] < 4:
    # Add an alpha channel to the image if it doesn't have one
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

# Set the alpha channel to 128
image[:, :, 3] = 128

# Save the modified image with the new alpha value
cv2.imwrite("./mnt/data/minecraft_stone_texture_transparent.png", image)