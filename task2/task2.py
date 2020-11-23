from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

cap = cv2.VideoCapture(0)


def gen_frames(cap):  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        _,img = cap.read()  # read the camera frame
   
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, 1.1, 4)
        for (x, y, w, h) in faces:
        	cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/webcam')
def webcam():
    #Video streaming route. Put this in the src attribute of an img tag
    global cap
    return Response(gen_frames(cap), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """ home page."""
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)
