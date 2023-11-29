# MY-Photo-Finish
A video processing app to determine race times.
This is an ongoing project, the app is not complete and new features are regularly going to be added.


The input video must be such that the camera is always still, on the finish line, alligned with the finish line.

The app produces a time-synchronized image of the finish line. Only what happens on the line gets into the picture, just like the real photo finish.

Tha app also imports the sound of the video, from which you can determine the start gun sound, and re-synchronize the image time axis.

You can add-edit athletes, names, lane numbes, ID, affiliation, and place; all in a table.

Determine the finish time by placing the curser on the image. The times will appear on each athlete's time entry as a combo box option.

Remember that you must also install the modules: cv2, tkinter, time, PIL, os, numpy, sounddevice, io, moviepy, soundfile

# How to Use

-open the app (xd)

-click 'import video'
  the video must be recorded such that timewise: from before the gunshot to after everyone have passed the finish line, placewise: vertically aligned with the finish line, so that the middle of the display coincides with the finish line.
  it creates a time-wise synchronized image of the finish line: takes the middle vertical line of the video from every frame and unifies them back to back.

-hit the gun button. at the top of the display, you have to see the wave of the sound of the video file. after you have determined where the gun shot happened by the sound, click there. now the time scale at the bottom changed so that 0.00 is where you clicked.

-hit the first button on top "add cursor"

-add cursors (vertical photo finish line) on the picture. place the curser so thet it is aligned with the forewardmost point of the torso of the athlete. place as many cursor as the number of athletes.

-after you have done adding cursor, click the yellow tick button, just next to "add cursor" button.

-now click the reults button, the button with clock image. there you can add athleted and edit attributes. the times, according to the cursor placements, automatically appears on the time column of the athlete as a choice (combobox)
