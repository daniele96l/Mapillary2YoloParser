# www.danieleligato.com

import json
import os, os.path
from tqdm import tqdm

#Dir = '/Users/danieleligato/PycharmProjects/Mapillary2YoloParser/mtsd_v2_fully_annotated/lightannotation'
Dir = '/Users/danieleligato/Desktop/annotationsOld'
SaveFolder = '/Users/danieleligato/Desktop/untitled/'
ListOfLabels = "/Users/danieleligato/PycharmProjects/Mapillary2YoloParser/NewList"
path, dirs, files = next(os.walk(Dir))



def openFile(filename):
    f = os.path.join(Dir, filename)
    t = open(f)
    return t


def parse(t,filename,number):
    global imageHeight, imageWidth
    labels,xmin,xmax,ymax,ymin =  ([] for i in range(5)) #just declare 5 list
    data = json.load(t)

    for key in data:  # take the keys and values of the jsom file
        value = data[key]
        # ------------image properties
        if (key == "width"):  # could be written better
            imageWidth = value
        if (key == "height"):
            imageHeight = value
            # ---------single object inside the image

        if (key == 'objects'):
            for object in value:  # each sigle object
                for key2 in object:  # dentro le proprietà dell'oggetto
                    if(key2 == 'bbox'):
                        bbox = object.get(key2, 'key not exist') #i take the boundign box
                        for key3 in bbox:
                            if (key3 == 'xmin'):
                                xmin.append(bbox.get(key3,'key not exist'))
                            if (key3 == 'xmax'):
                                xmax.append(bbox.get(key3,'key not exist'))
                            if (key3 == 'ymin'):
                                ymin.append(bbox.get(key3,'key not exist'))
                            if (key3 == 'ymax'):
                                ymax.append(bbox.get(key3,'key not exist'))
                    if (key2 == 'label' and object.get(key2) != "other-sign"):
                        if(str(search_string_in_file(ListOfLabels,object.get(key2))) == "None"):
                            print(object.get(key2))
                            number += 1
                            print(number)
                            complete_file(str(number) + " " + object.get(key2))

                        myline = search_string_in_file(ListOfLabels,object.get(key2)) -1
                        labels.append(myline)  # i take the label
   # print(labels,xmin)

    xmin_n, xmax_n, ymax_n, ymin_n = normalize(imageWidth, imageHeight, xmin, ymin, xmax, ymax)
    # class x_center y_center width height f
    #flip


    widht, height, center_x, center_y = ([] for i in range(4))
    for i in range(len(xmin)):
        widht.append((xmax_n[i]-xmin_n[i]))
        height.append((ymax_n[i]-ymin_n[i]))
        center_x.append(xmin_n[i] + ((xmax_n[i]-xmin_n[i])/2))
        center_y.append((ymin_n[i] + ((ymax_n[i]-ymin_n[i])/2)))



    saveFile(labels,center_x, center_y, widht, height,filename)
    return number

def complete_file(newString):
    with open("/Users/danieleligato/PycharmProjects/Mapillary2YoloParser/NewList", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(newString)


def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
                return line_number

    # Return list of tuples containing line numbers and lines where string is found


def saveFile(labels, center_x, center_y, widht, height,filename):
    with open(SaveFolder + filename.replace(".json",".txt") , 'w') as file:
        for i in range(len(labels)):
            file.write(str(labels[i]) + " " + str(center_x[i])+ " " + str(center_y[i])+ " " +  str(widht[i])+ " " + str(height[i]) + "\n")


def normalize(imageWidth,imageHeight,xmin,ymin,xmax,ymax):
    xmin_n,xmax_n,ymax_n,ymin_n =  ([] for i in range(4)) #just declare 5 list
    for i in range(len(xmin)):
        xmin_n.append(xmin[i]/imageWidth)
        ymin_n.append(ymin[i]/imageHeight)
        xmax_n.append(xmax[i]/imageWidth)
        ymax_n.append(ymax[i]/imageHeight)

    return  xmin_n,xmax_n,ymax_n,ymin_n



def main():
    global number
    number = 1537
    LENGTH = len(os.listdir(Dir))  # Number of iterations required to fill pbar
    pbar = tqdm(total=LENGTH)  # Init pbar

    for filename in os.listdir(Dir):
        if (filename.endswith(".json")):
            pbar.update(n=1)  # Increments counter
            t = openFile(filename)  # open the n-file and return the content inside
            number = parse(t,filename,number)  # parse the content of the file
            t.close()  # close the n-file


if __name__ == "__main__":
    main()


