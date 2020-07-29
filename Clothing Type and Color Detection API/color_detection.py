from variables import  shoewear, topwear, long_bottomwear, short_bottomwear, headwear
import random 

def rgb_to_text(rgb):

    red,green,blue = rgb 

    similarity_average = (abs(125-red) + abs(125- green) + abs(125-blue))/3
    if(similarity_average < 20 ):
        return "Grey"

    colors = {
        "Black" : (0,0,0),
        "Dark" : (22,22,22),
        "Light Grey" : (192,192,192),
        "Dark Greeen" : (96,120,10),
        "White" : (255,255,255),
        "Karaka" : (51,51,0),
        "Brown" : (102,51,0),
        "Light Brown" : (185,177,164),
        "Bordeaux" : (51,0,0),
        "Red" :    (255,0,0),
        "Dark Red" : (153,0,0),
        "Cosmos Red" : (255,204,204),
        "Blaze Orange" : (255,102,102),
        "Beige" : (255,178,102),
        "Orange" : (255,128,0), 
        "Yellow" : (255,255,0),
        "Light Green"  : (128,255,0),
        "Green" : (0,255,0),
        "Dark Green" : (0,153,0),
        "Vine Green" : (0,255,128),
        "Myrtle Green" : (25,51,0),
        "Persian Blue": (0,153,153),
        "Pigment Green" : (0,153,76),
        "Islamic Green" : (0,153,0),
        "Cytrus" : (153,153,0),
        "Cyan": (0,255,255),
        "Light Blue" : (0 ,128, 255),
        "Light Blue " : (181, 198, 208),
        "Blue Romance" : (204,255,204),
        "Magic Mint Blue" : (153,205,204),
        "Dark Blue": (0,0,153),
        "Blue" : (0,0,255),
        "Cyprus Blue" : (0,51,51),
        "Black Pearl Blue" : (0,25,51),
        "Midnight Blue": (0,0,153),
        "Cobalt Blue" : (0,76,153),
        "Sky Blue" : (204,255,255),
        "Purple" : (127,0,255),
        "Blackcurrant Purple": (25,0,51),
        "Mardi Gras Purple": (51,0,51),
        "Jazberry Jam Purple" : (153,0,76),
        "Dark Magenta" : (153,0,153),
        "Dark Purple" : (76,0,153),
        "Fucshia" : (255,0,255),
        "Pink" : (255,0,125)
    }
    count = 0
    for c in colors :
        count += 1 
    print(count)
    best_similarity_avg , most_similar_color = 255 , ""

    for current_color in colors : 
        crrnt_red, crrnt_green, crrnt_blue = colors[current_color]
        similarity_average = (abs(crrnt_red-red) + abs(crrnt_green- green) + abs(crrnt_blue-blue))/3
        
        if(similarity_average < best_similarity_avg):
            best_similarity_avg, most_similar_color = similarity_average , current_color

    return most_similar_color

print(rgb_to_text((223,1,2)))

def getItemColors(image, items):
    width , height = image.shape[0], image.shape[1]
    for clothing_item in items:
        x_topLeft      =  int(clothing_item["BndBox"]["TopLeft"][0] * width)
        y_topleft      =  int(clothing_item["BndBox"]["TopLeft"][1] * height)
        x_bottomRight  =  int(clothing_item["BndBox"]["BottomRight"][0] * width)
        y_bottomrRight =  int(clothing_item["BndBox"]["BottomRight"][1] * height)
        item_colors_found = {}

        if clothing_item["Type"]  in topwear :
            x_margin = int((x_bottomRight - x_topLeft) /4)
            y_margin = int((y_bottomrRight - y_topleft)/5)
            x_centerred_left = x_topLeft + x_margin 
            x_centerred_right = x_bottomRight - x_margin
            y_centerred_left = y_topleft + y_margin 
            y_centerred_right = y_bottomrRight - y_margin
            numRandomCenterredPixels = 200 


        elif clothing_item["Type"] in short_bottomwear :
            x_margin = int((x_bottomRight - x_topLeft) /5)
            y_margin = int((y_bottomrRight - y_topleft)/5)
            x_centerred_left = x_topLeft  
            x_centerred_right = x_bottomRight 
            y_centerred_left = y_topleft  
            y_centerred_right = y_bottomrRight - y_margin
            numRandomCenterredPixels = 200 

        else :
            x_margin = 0
            y_margin = 0
            x_centerred_left = x_topLeft  
            x_centerred_right = x_bottomRight 
            y_centerred_left = y_topleft  
            y_centerred_right = y_bottomrRight - y_margin
            numRandomCenterredPixels = 200 

        for i in range(numRandomCenterredPixels):
            x = random.randint(x_centerred_left, x_centerred_right)
            y = random.randint(y_centerred_left, y_centerred_right)
            color_detected = rgb_to_text(tuple(image[x][y]))
            if color_detected not in item_colors_found :
                item_colors_found[color_detected] = 1 
            else :
                item_colors_found[color_detected] += 1 

        clothing_item["Color"] = getFinalColor(item_colors_found)
    return items 


def getFinalColor(item_colors_found):
    count , final_clr = 0 , ""
    for color in item_colors_found :
        if item_colors_found[color] > count :
            count = item_colors_found[color] 
            final_clr = color  
    return final_clr