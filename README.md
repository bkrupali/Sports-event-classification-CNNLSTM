# Video classification example with Inception and LSTM:

Video classification with Inception and LSTM.

1. Place the videos from your dataset in data/train and data/test folders. Each video type should have its own folder

>	| data/test
> >		| Four
> >		| Six
> >		| Wicket
>	| data/train
> >		| Four
> >		| Six
> >		| Wicket

2. Extract frames from video with script extract_files.py. Pass video files extenssion as a parameter

`	$ python extract_files.py mp4`

3. Check the data_file.csv and choose the acceptable sequence length of frames. It should be less or equal to lowest one if you want to process all videos in dataset.
4. Extract sequence for each video with InceptionV3 and train LSTM. Run train.py script with sequence_length, class_limit, image_height, image_width args

`	$ python train.py 150 3 404 720`

5. Save your best model file. (For example, lstm-features.hdf5)
6. Use clasify.py script to clasify your video. Args sequence_length, class_limit, saved_model_file, video_filename

`	$ python classify.py 150 3 lstm-features.hdf5 video_file.mp4`

The result will be placed in result.avi file.

## Requirements

This code requires you have Keras 2 and TensorFlow 1 or greater installed. Please see the `requirements.txt` file. To ensure you're up to date, run:

`pip install -r requirements.txt`

You must also have `ffmpeg` installed in order to extract the video files.
