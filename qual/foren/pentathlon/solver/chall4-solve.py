from PIL import Image

image = Image.open("chall4.png")
pixels = image.load()

message = ""
for i in range(0, image.width, 3):
    mg, gb, b = pixels[i, 0]
    m = mg ^ gb ^ b
    message += chr(m)

print(message)