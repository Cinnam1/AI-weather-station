import requests
import cv2

#Generate face and put to file face.png
response = requests.get("https://thispersondoesnotexist.com/image")

file = open("face.png", "wb")
file.write(response.content)
file.close()


#GENERATE STILL VID

#Vid name, image name, seconds
video_name = "noLip.avi"
image = "face.png"
seconds = 5;

frame = cv2.imread("face.png")
height, width, layers = frame.shape
video = cv2.VideoWriter(video_name, 0, 30, (width, height))

for x in range(seconds*30):
    video.write(cv2.imread(image))

#Unidentify
cv2.destroyAllWindows()
video.release()