# www.danieleligato.com

import json
import os, os.path
from tqdm import tqdm

Dir = '/Users/danieleligato/PycharmProjects/Mapillary2YoloParser/mtsd_v2_fully_annotated/lightannotation'
SaveFolder = '/Users/danieleligato/PycharmProjects/Mapillary2YoloParser/mtsd_v2_fully_annotated/newAnnotation/'
ListOfLabels = "/Users/danieleligato/PycharmProjects/Mapillary2YoloParser/NewList"
path, dirs, files = next(os.walk(Dir))


def openFile(filename):
    f = os.path.join(Dir, filename)
    t = open(f)
    return t


def parse(t,filename):
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
                    if (key2 == 'label'):
                        myline = search_string_in_file(ListOfLabels,object.get(key2)) -1
                        labels.append(myline)  # i take the label
   # print(labels,xmin)

    xmin_n, xmax_n, ymax_n, ymin_n = normalize(imageWidth, imageHeight, xmin, ymin, xmax, ymax)
    saveFile(labels,xmin_n, xmax_n, ymax_n, ymin_n,filename)

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


def saveFile(labels, xmin_n, xmax_n, ymax_n, ymin_n,filename):
    with open(SaveFolder + filename, 'w') as file:
        for i in range(len(xmin_n)):
            file.write(str(labels[i]) + " " + str(xmin_n[i])+ " " + str(xmax_n[i])+ " " +  str(ymax_n[i])+ " " + str(ymin_n[i]) + "\n")


def normalize(imageWidth,imageHeight,xmin,ymin,xmax,ymax):
    xmin_n,xmax_n,ymax_n,ymin_n =  ([] for i in range(4)) #just declare 5 list
    for i in range(len(xmin)):
        xmin_n.append(xmin[i]/imageWidth)
        xmax_n.append(ymin[i]/imageHeight)
        ymax_n.append(xmax[i]/imageWidth)
        ymin_n.append(ymax[i]/imageHeight)

    return  xmin_n,xmax_n,ymax_n,ymin_n



def main():
    LENGTH = len(os.listdir(Dir))  # Number of iterations required to fill pbar
    pbar = tqdm(total=LENGTH)  # Init pbar
    for filename in os.listdir(Dir):
        if (filename.endswith(".json")):
            pbar.update(n=1)  # Increments counter
            t = openFile(filename)  # open the n-file and return the content inside
            parse(t,filename)  # parse the content of the file
            t.close()  # close the n-file


if __name__ == "__main__":
    main()


