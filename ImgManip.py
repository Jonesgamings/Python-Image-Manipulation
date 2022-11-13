from PIL import Image
import time as tm
import os
import random as rd

class Manip():

    def __init__(self, image):
        self.path = os.path.abspath(__file__).split(os.path.basename(__file__))[0]
        self.imageName = image
        self.scanData = {}
        self.chunks = {}
        self.divide = 10
        self.image = Image.open(self.path + self.imageName)
        self.x, self.y = self.image.size
        self.rgb = self.image.convert("RGB")
        self.scan()

    def Start(self):
        time = tm.time()
        return time

    def End(self, operation, time):
        dur = tm.time() - time
        self.startTime = 0
        print("{0} took {1} seconds".format(operation, dur))

    def scan(self):
        time = self.Start()
        for x in range(self.x):
            for y in range(self.y):
                self.scanData[x, y] = self.rgb.getpixel((x, y))

        self.End("Scanning Image", time)

    def scanchunk(self, divide):
        time = self.Start()
        for key in self.scanData.keys():
            x, y = key

            chunkY = y // divide
            chunkX = x // divide

            try:
                self.chunks[chunkX, chunkY] += [[x, y]]

            except:
                self.chunks[chunkX, chunkY] = [[x, y]]

        self.End("Scanning Chunks", time)

    def blur(self, percentage):
        divide = round((percentage / 100) * ((self.x + self.y) / 2))
        time = self.Start()
        im = self.rgb
        meanDIV = divide ** 2
        self.scanchunk(divide)
        for value in self.chunks.values():
            reds = 0
            greens = 0
            blues = 0
            for pixel in value:
                x, y = pixel
                r, g, b = self.scanData[x, y]
                reds += r
                greens += g
                blues += b

            newR = reds // meanDIV
            newG = greens // meanDIV
            newB = blues // meanDIV
            col = newR, newG, newB
            for pixel in value:
                im.putpixel(pixel, col)

        im.save("{0}{1}".format(self.path, "Output.jpg"))
        self.End("Blurring Image", time)

    def defocus(self):
        time = self.Start()
        im = self.rgb
        add = 1
        for key, value in self.scanData.items():
            x, y = key
            k1 = x + 1 * add, y
            k2 = x - 1 * add, y
            k3 = x, y + 1 * add
            k4 = x, y - 1 * add
            try:
                r1, g1, b1 = self.scanData[k1]
            except:
                r1, g1, b1 = value

            try:
                r2, g2, b2 = self.scanData[k2]
            except:
                r2, g2, b2 = value

            try:
                r3, g3, b3 = self.scanData[k3]
            except:
                r3, g3, b3 = value

            try: 
                r4, g4, b4 = self.scanData[k4]
            except:
                r4, g4, b4 = value

            Nr = (r1 + r2 + r3 + r4) // 4
            Ng = (g1 + g2 + g3 + g4) // 4
            Nb = (b1 + b2 + b3 + b4) // 4
            col = Nr, Ng, Nb
            try:
                im.putpixel(key, col)

            except:
                pass
            
        im.save("{0}{1}".format(self.path, "Output.jpg"))
        self.End("Defocusing Image", time)

    def invert(self):
        time = self.Start()
        im = self.rgb
        for key, value in self.scanData.items():
            r, g, b = value
            col = (255 - r, 255 - g, 255 - b)
            im.putpixel(key, col)

        im.save("{0}{1}".format(self.path, "Output.jpg"))
        self.End("Inverting image", time)

    def greyscale(self):
        time = self.Start()
        im = self.rgb
        for key, value in self.scanData.items():
            r, g, b = value
            medCOl = int((r + g + b) / 3)
            col = (medCOl, medCOl, medCOl)
            im.putpixel(key, col)

        im.save("{0}{1}".format(self.path, "Output.jpg"))
        self.End("Greyscaling image", time)

    def brighten(self, num):
        time = self.Start()
        im = self.rgb

        for key, value in self.scanData.items():
            r, g, b = value
            col = (r + num, g + num, b + num)
            im.putpixel(key, col)

        im.save("{0}{1}".format(self.path, "Output.jpg"))
        self.End("Brightning image", time)

    def saturate(self, num):
        time = self.Start()
        im = self.rgb

        for key, value in self.scanData.items():
            r, g, b = value
            maxV = max(r, g, b)

            if r == maxV:
                col = (r + num, g, b)

            elif g == maxV:
                col = (r, g + num, b)

            else:
                col = (r, g, b + num)

            im.putpixel(key, col)

        im.save("{0}{1}".format(self.path, "Output.jpg"))
        self.End("Saturating image", time)

    def AverageColumn(self):
        time = self.Start()
        im = self.rgb

        self.Columndata = {}

        for key, value in self.scanData.items():
            x, y = key
            r, g, b = value
            try:
                R, G, B = self.Columndata[x]
                self.Columndata[x] = (r + R, g + G, b + B)

            except Exception as e:
                self.Columndata[x] = value

        for key, value in self.Columndata.items():
            r, g, b = value
            Nvalue = (r // self.y, g // self.y, b // self.y)
            for _ in range(0, self.y + 1):
                pixel = (key, _)
                try:
                    im.putpixel(pixel, Nvalue)
                except:
                    pass


        im.save("{0}{1}".format(self.path, "Output.jpg"))
        self.End("Averaging columns of image", time)

    def AverageRow(self):
        time = self.Start()
        im = self.rgb

        self.Rowdata = {}

        for key, value in self.scanData.items():
            x, y = key
            r, g, b = value
            try:
                R, G, B = self.Rowdata[y]
                self.Rowdata[y] = (r + R, g + G, b + B)

            except Exception as e:
                self.Rowdata[y] = value

        for key, value in self.Rowdata.items():
            r, g, b = value
            Nvalue = (r // self.y, g // self.y, b // self.y)
            for _ in range(0, self.x + 1):
                pixel = (_, key)
                try:
                    im.putpixel(pixel, Nvalue)
                except:
                    pass


        im.save("{0}{1}".format(self.path, "Output.jpg"))
        self.End("Averaging rows of image", time)

    def AverageRowColumn(self):
        time = self.Start()
        im = self.rgb
        self.AverageRow()
        self.AverageColumn()

        for key, value in self.Rowdata.items():
            for key2, value2 in self.Columndata.items():
                r1, g1, b1 = value
                Ar1 = r1 // self.y
                Ag1 = g1 // self.y
                Ab1 = b1 // self.y

                r2, g2, b2 = value2
                Ar2 = r2 // self.x
                Ag2 = g2 // self.x
                Ab2 = b2 // self.x

                Nr = (Ar1 + Ar2) // 2
                Ng = (Ag1 + Ag2) // 2
                Nb = (Ab1 + Ab2) // 2

                col = (Nr, Ng, Nb)
                pixel = (key2, key)
                im.putpixel(pixel, col)

        im.save("{0}{1}".format(self.path, "Output.jpg"))
        self.End("Averaging rows/columns of image", time)

    def removeColour(self, col):
        time = self.Start()
        col = col.lower()
        im = self.rgb
        for key, value in self.scanData.items():
            if col == "red":
                colour = (0, value[1], value[2])

            elif col == "green":
                colour = (value[0], 0, value[2])

            elif col == "blue":
                colour = (value[0], value[1], 0)

            else:
                colour = value

            im.putpixel(key, colour)

        im.save("{0}{1}".format(self.path, "Output.jpg"))
        self.End("Removing colour from image", time)

    def onlyColour(self, col):
        time = self.Start()
        col = col.lower()
        im = self.rgb
        for key, value in self.scanData.items():
            if col == "red":
                colour = (value[0], 0, 0)

            elif col == "green":
                colour = (0, value[1], 0)

            elif col == "blue":
                colour = (0 , 0, value[2])

            else:
                colour = value

            im.putpixel(key, colour)

        im.save("{0}{1}".format(self.path, "Output.jpg"))
        self.End("Leaving colour from image", time)

    def splitColours(self):
        time = self.Start()
        im = self.rgb
        colours = ["red", "green", "blue"]
        for col in colours:
            for key, value in self.scanData.items():
                if col == "red":
                    colour = (value[0], 0, 0)

                elif col == "green":
                    colour = (0, value[1], 0)

                elif col == "blue":
                    colour = (0 , 0, value[2])

                else:
                    colour = value

                im.putpixel(key, colour)

            im.save("{0}{1}".format(self.path, "Output{0}.jpg").format(col.upper()))
        self.End("Splitting colour from image", time)

    def deleteOutputs(self):
        time = self.Start()
        openPath = os.listdir(self.path)
        for item in openPath:
            if item.endswith(".jpg"):
                if item.startswith("Image"):
                    pass

                else:
                    os.remove(os.path.join(self.path, item))

        self.End("Deleting Outputs", time)

image = Manip("Image.jpg")
image.deleteOutputs()
image.AverageColumn()
#image.AverageRow()
#image.AverageRowColumn()