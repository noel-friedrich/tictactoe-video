from PIL import Image, ImageFont, ImageDraw, ImageColor
import random

random_file = lambda: f"outputs/boards/{random.randint(0, 421):0>5}.jpg"

background = Image.open("templates/background.jpg")

for i in range(1000):
    img = Image.open(random_file())
    img = img.crop((102, 77, 1028, 1005))

    size_factor = random.random() * 0.2 + 0.2
    img = img.resize((round(size_factor * img.width), round(size_factor * img.height)))

    mask = Image.new('L', img.size, 255)
    rotation_deg = random.random() * 360
    img = img.rotate(rotation_deg, expand=True)
    mask = mask.rotate(rotation_deg, expand=True)

    background.paste(img, (
        random.randint(0, background.width) - img.width // 2,
        random.randint(0, background.height) - img.height // 2
    ), mask)

    if i % 100 == 0:
        print(f"{round(i / 1000 * 100, 2)}%")

background.save("outputs/thumbnail/thumbnail-background.png")