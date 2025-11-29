from PIL import Image

def color_to_ps(colors,name,f):
    f.write(f"/{name} [\n")
    for y in range(len(colors)):
        f.write("    [")
        for x in range(len(colors[y])):
            f.write(f"{colors[x][y]} ")
        f.write("]\n")
    f.write("] def\n")

# CanvasSize will depend on the image u load
CanvasWidth = 280
CanvasHeight = 420

#PixelSize・・・Zoom rate
#PixelSize = 1
print("Zoom rate(default:1)")
PixelSize = input(">")
if not PixelSize:
    PixelSize = 1
else:
    PixelSize = int(PixelSize)
# WeightLevel・・・1:heavy~32:light(4 recommend,min:1,max:256)
#WeightLevel = 4
print("WeightLevel.  1:heavy~32:light(default:4,min:1,max:256)")
WeightLevel = input(">")
if not WeightLevel:
    WeightLevel = 4
else:
    WeightLevel = int(WeightLevel)

Div = 256 // WeightLevel
with open("main.ps", "w") as f:
    img = Image.open("image.bmp").convert("RGB")
    width, height = img.size
    f.write("%!PS-Adobe-3.0\n")
    f.write("% This file is created by python.\n")
    f.write("% source:https://github.com/kur0inusan/bmp_to_ps/blob/main/converter.py")
    CanvasHeight = height * PixelSize
    CanvasWidth = width * PixelSize
    f.write(f"<< /PageSize [{CanvasWidth} {CanvasHeight}] >> setpagedevice\n")
    # ここから本質の部分
    pixels = img.load()
    R = [[0] * width for _ in range(height)]
    G = [[0] * width for _ in range(height)]
    B = [[0] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            R[y][x] = r // WeightLevel    
            G[y][x] = g // WeightLevel
            B[y][x] = b // WeightLevel
    R.reverse()
    G.reverse()
    B.reverse()
    color_to_ps(R,"R",f)
    color_to_ps(G,"G",f)
    color_to_ps(B,"B",f)
    tmp = [
        f"/PixelSize {PixelSize} def\n",
        f"0 1 {height-1} {"{"}\n",
        f"    /i exch def\n",
        f"    0 1 {width-1} {"{"}\n",
        f"        /j exch def\n",
        f"        newpath\n",
        f"        R i get j get {Div} div\n",
        f"        G i get j get {Div} div\n",
        f"        B i get j get {Div} div\n",
        f"        setrgbcolor\n",
        f"        1 setlinewidth\n",
        f"        i PixelSize mul j PixelSize mul moveto\n",
        f"        i PixelSize mul j PixelSize mul PixelSize add lineto\n",
        f"        i PixelSize mul PixelSize add j PixelSize mul PixelSize add lineto\n",
        f"        i PixelSize mul PixelSize add j PixelSize mul lineto\n",
        f"        closepath\n",
        f"        stroke\n",
        f"        fill\n",
        f"    {"}"} for\n",
        f"{"}"} for\n"
    ]
    for i in tmp:
        f.write(i)
    f.write("showpage\n")
    print("all done!")
