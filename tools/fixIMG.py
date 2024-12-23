from PIL import Image

numbers = ["_0", "_1", "_2", "_3", "_4", "_5", "_6", "_7", "_8", "_9"]
colours = ["red", "blue", "green", "yellow"]

for colour in colours:
    for number in numbers:
        img = Image.open(f"uno_cards/{colour}{number}.png")
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255,255,255,0))
            else:
                newData.append(item)
        img.putdata(newData)
        img.save(f"uno_cards/{colour}{number}.png", "PNG")