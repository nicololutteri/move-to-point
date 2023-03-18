from PIL import Image, ImageDraw, ImageFont
import os
import sys

const = 90

def getext(s : str) -> str:
    v = s.split(".")
    return v[len(v) - 1]

def getname(s : str) -> str:
    v = s.split(".")
    return v[0]

def create_directory(l):
    for x in l:
        name = getname(x)

        if os.path.exists(name):
            os.rmdir(name)

        os.mkdir(name)

def create_movie(folder : str, history : str(), episode : int):
    frame = 1

    historyone = history[0].split(";")
    x = historyone[1].split("-")[0]
    y = historyone[1].split("-")[1]

    brainx = historyone[0].split("-")[0]
    brainy = historyone[0].split("-")[1]

    img = create_image_base(episode, 0, 0, int(x), int(y), int(brainx), int(brainy))
    img.save(folder + "episode." + str(episode) + "." + str(number_convert(frame)) + ".png")
    frame = frame + 1

    for i in range(2, len(history)):
        v = history[i].split(";")
        rew = history[i].split(";")[3]

        brainx = v[1].split("-")[0]
        brainy = v[1].split("-")[1]

        img = create_image_base(episode, i - 1, int(rew), int(x), int(y), int(brainx), int(brainy))
        img.save(folder + "episode." + str(episode) + "." + str(number_convert(frame)) + ".png")
        frame = frame + 1

        print(str(frame))

def create_image_base(episodio : int, step : int, reward : int, x : int, y : int, brainx : int, brainy : int) -> Image:
    im = Image.new('RGB', (1920, 1080), color = 'white')
    draw = ImageDraw.Draw(im)

    color = 128

    for i in range(const, const * 12, const):
        draw.line((const, i, const * 11, i), fill = color, width = 5)
        draw.line((i, const, i, const * 11), fill = color, width = 5)
     
    draw.line(create_x_one(x, y), fill = color, width = 10)
    draw.line(create_x_two(x, y), fill = color, width = 10)

    fnt = ImageFont.truetype('arial.ttf', 72)
    draw.text((1100, 100), "Episodio: " + str(episodio), font = fnt, fill = color)
    draw.text((1100, 200), "Step: " + str(step), font = fnt, fill = color)
    draw.text((1100, 300), "Reward: " + str(reward), font = fnt, fill = color)

    brain = Image.open("brain.png", "r")
    im.paste(brain, create_brain(brainx, brainy))

    return im

def create_x_one(x, y) -> (int, int, int, int):
    return ((x + 1) * const, (y + 1) * const, (x + 1) * const + const, (y + 1) * const + const)
def create_x_two(x, y) -> (int, int, int, int):
    return ((x + 1) * const + const, (y + 1) * const, (x + 1) * const, (y + 1) * const + const)
def create_brain(x, y) -> (int, int):
    return ((x + 1) * const + 9, (y + 1) * const + 9)

def number_convert(x : int) -> str:
    l = len(str(x))

    if l == 1:
        return "000" + str(x)
    elif l == 2:
        return "00" + str(x)
    elif l == 3:
        return "0" + str(x)
    else:
        return str(x)

def procedure(i):
        f = open(i, "r+")

        l = list()
        for j in f:
            l.append(j)
        create_movie(getname(i) + "\\", l, getname(i))

        f.close()

if __name__ == "__main__":
    percorso = os.getcwd()
    #l = [f for f in listdir(percorso) if isfile(join(percorso, f))]

    l = list()
    for f in os.listdir(percorso):
        if os.path.isfile(f):
            extv = f.split(".")
            ext = extv[len(extv) - 1]

            if ext == "txt":
                l.append(f)

    create_directory(l)
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for out1, out2, out3 in executor.map(procedure, range(0, len(l))):
            pass
