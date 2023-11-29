# MY-Photo-Finish
A video processing app to determine race times.
This is an ongoing project, the app is not complete and new features are regularly going to be added.


The input video must be such that the camera is always still, on the finish line, alligned with the finish line.

The app produces a time-synchronized image of the finish line. Only what happens on the line gets into the picture, just like the real photo finish.

Tha app also imports the sound of the video, from which you can determine the start gun sound, and re-synchronize the image time axis.

You can add-edit athletes, names, lane numbes, ID, affiliation, and place; all in a table.

Determine the finish time by placing the curser on the image. The times will appear on each athlete's time entry as a combo box option.

Remember that you must also install the modules: cv2, tkinter, time, PIL, os, numpy, sounddevice, io, moviepy, soundfile
