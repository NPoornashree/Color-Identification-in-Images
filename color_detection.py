#Importing libraries
import cv2
import numpy as np
import pandas as pd
import argparse

img_path='colorpic.jpg'
csv_path = 'colors.csv'


#Creating argument parser to take image path from command line
#argparse library is used to create an argument parser. 
#We can directly give an image path from the command prompt:
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']


#Reading the image with opencv
img = cv2.imread(img_path)

#declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

#The pandas library is very useful when we need to perform various operations on data files like CSV. 
#pd.read_csv() reads the CSV file and loads it into the pandas DataFrame. 
#I have assigned each column with a name for easy accessing.

#Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

#Calculate distance to get color 
#distance is calculated by this formula: d = abs(Red – ithRedColor) + (Green – ithGreenColor) + (Blue – ithBlueColor)

#function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

#Create draw function
#It will calculate the rgb values of the pixel which we double click

#function to get x,y coordinates of mouse double click
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
        
        
#Creat a window in which the input image will display. 
#Then,set a callback function which will be called when a mouse event happens.
       
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)


#Display image on the window
#Whenever a double click event occurs, it will update the color name and RGB values on the window.
#Using the cv2.imshow() function, draw the image on the window. 
#When the user double clicks the window, draw a rectangle and get the color name to draw text on the window 


while(1):

    cv2.imshow("image",img)
    if (clicked):
   
        #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        #Creating text string to display( Color name and RGB values )
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        #For very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

    #Break the loop when user hits 'esc' key    
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
