import clusters
import random
from PIL import Image,ImageDraw,ImageFont
blognames,words,data = clusters.readfile('blogdata1.txt')
coords=clusters.scaledown(data)
color=[[0,0,0],[0,0,255],[0,255,0],[255,0,0],[255,255,0],[255,0,255],[0,255,255],[128,0,0],[0,128,0],[0,0,128],[128,128,0]]
for k in range(2,11):
    kcluster=clusters.kcluster(coords,k)
    img = Image.new('RGB', (2000, 2000), (255, 255, 255))
    draw=ImageDraw.Draw(img)
    font = ImageFont.truetype('simsun.ttc', 24)
    for i in range(k):
        for j in range(len(kcluster[i])):
            x = int((coords[kcluster[i][j]][0] + 0.5) * 1000)
            y = int((coords[kcluster[i][j]][1] + 0.5) * 1000)
            print(x,y,blognames[kcluster[i][j]])
            draw.text((x, y), blognames[kcluster[i][j]], (color[i][0],color[i][1],color[i][2]), font)
            #draw.text((x, y), "o", (color[i][0], color[i][1], color[i][2]), font)
    img.save("test"+str(k)+".jpg", 'JPEG')