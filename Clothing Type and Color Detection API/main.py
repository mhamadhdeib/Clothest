from flask import  jsonify, request, Flask
import numpy as np
import tensorflow as tf
from color_detection import  getItemColors
import cv2
from variables import category_index

headers = {
    'Access-Control-Allow-Origin': '*'
}

config = tf.compat.v1.ConfigProto()

def loadModel(PATH_TO_CKPT):
    # Load the Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.compat.v2.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        return detection_graph, tf.compat.v1.Session(graph=detection_graph,config=config)

def process_prediction(boxes,classes,scores,max_boxes_to_draw=20, min_score_thresh=0.70):
    articlesInImg = []
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores[i] > min_score_thresh:
            box = tuple(boxes[i].tolist())
            article_type = ''
            if classes[i] in category_index:
                class_name = category_index[classes[i]]
            else:
                class_name = 'N/A'
            article_type = str(class_name)

            item = {"Type": article_type,
                "Color": "Blue",
                "BndBox": {
                    "TopLeft": (box[1], box[0]),
                    "BottomRight": (box[3], box[2])
                    },
                "Confidence": int(scores[i]*100)
                }
            articlesInImg.append(item)
    return articlesInImg

detection_graph, sess = loadModel("./frozen_inference_graph.pb")
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
num_detections = detection_graph.get_tensor_by_name('num_detections:0')
detection_array = [detection_boxes,
                   detection_scores,
                   detection_classes,
                   num_detections]

        
def detect(request):
    if request.method != 'POST':
        return "Error 405: Method should be post"
    else:
        imagefile = request.files['File']
        image = cv2.imdecode(np.fromfile(imagefile, np.uint8), cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_expanded = np.expand_dims(image_rgb, axis=0)
        (boxes, scores, classes, num) = sess.run(detection_array, feed_dict={image_tensor: image_expanded})

        predictions = process_prediction(np.squeeze(boxes),np.squeeze(classes).astype(np.int32),np.squeeze(scores))
        predictions = getItemColors(image_rgb, predictions)
        result = jsonify({"Items": predictions})
        return (result,200,headers)
            