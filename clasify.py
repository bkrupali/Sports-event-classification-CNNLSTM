import os
import sys
import cv2
import shutil
import numpy as np
from data import DataSet
from extractor import Extractor
from keras.models import load_model
from shutil import copyfile
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

if (len(sys.argv) == 5):
    seq_length = int(sys.argv[1])
    class_limit = int(sys.argv[2])
    saved_model = sys.argv[3]
    video_file = sys.argv[4]

else:
    print ("Usage: python clasify.py sequence_length class_limit saved_model_name video_file_name")
    print ("Example: python clasify.py 75 2 lstm-features.095-0.090.hdf5 some_video.mp4")
    exit (1)
clip = VideoFileClip("one.mp4")
for j in range(0,int(clip.duration),5):
    ffmpeg_extract_subclip("one.mp4", j, j+5, targetname="clip"+str(j)+".mp4")

    capture = cv2.VideoCapture(os.path.join("clip"+str(j)+".mp4"))
    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter("E:/LSTM-video-classification/result/"+"result"+str(j)+".avi", fourcc, 15, (int(width), int(height)))

# Get the dataset.
    data = DataSet(seq_length=seq_length, class_limit=class_limit, image_shape=(height, width, 3))

# get the model.
    extract_model = Extractor(image_shape=(height, width, 3))
    saved_LSTM_model = load_model(saved_model)

    frames = []
    frame_count = 0
    while True:
        ret, frame = capture.read()
    # Bail out when the video file ends
        if not ret:
            break

    # Save each frame of the video to a list
        frame_count += 1
        frames.append(frame)

        if frame_count < seq_length:
            continue # capture frames untill you get the required number for sequence
        else:
            frame_count = 0

    # For each frame extract feature and prepare it for classification
        sequence = []
        for image in frames:
            features = extract_model.extract_image(image)
            sequence.append(features)

    # Clasify sequence

        prediction = saved_LSTM_model.predict(np.expand_dims(sequence, axis=0))
        print(prediction)
        print("---------------------------")
        values = data.print_class_from_prediction(np.squeeze(prediction, axis=0))
        print ("***************")
        if ('six' in values[0]):
            print("its a six")
            f1 = os.path.abspath('F:/Six')
            dst = f1
        elif ('four' in values[0]):
            print("its a four")
            f2 = os.path.abspath('F:/Four')
            dst = f2
        else:
            print("its a wicket")
            f3 = os.path.abspath('F:/Wicket')
            dst = f3

    # Add prediction to frames and write them to new video
        for image in frames:
            for i in range(len(values)):
                cv2.putText(image, values[i], (40, 40 * i + 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
            video_writer.write(image)

        frames = []
    #print (j)
    video_writer.release()
    src = "E:/LSTM-video-classification/result/"+"result"+str(j)+".avi"
    shutil.move(src, dst)

    j = j+5
    print("continuing")
#shutil.copyfile('F:/LSTM-video-classification - Copy (2)', dst)
