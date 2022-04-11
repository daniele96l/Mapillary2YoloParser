# Mapillary2YoloParser


# H1 What is this?
This is a parser that will translate the format of [mapillary dataset](https://www.mapillary.com/dataset/trafficsign)
to the format that is usable in the [YOLO network](https://github.com/ultralytics/yolov3/wiki/Train-Custom-Data) for object identification 

## H2 What we need
Other that obviusly the YOLO neural network and the annotate orgiginal .json files of mapillary we will need the [list of all roadsign present in the mapillary dataset](https://www.mapillary.com/developer/api-documentation/traffic-signs)

The translation will translate the relative pixe-wise position of each object in an absolute normalizate one, and the labels aka the name of the roadsign will be translated 
in their corrispective identification number from 0 to N.

After generating the new annotation files you will need to put them in the folder that your YOLO network uses and update the dataset.yaml file, as explained in the 2nd link. 
