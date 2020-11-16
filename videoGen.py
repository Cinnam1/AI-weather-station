
import requests
import cv2
import math
import ffmpeg
import subprocess

#Generate face and put to file face.png
response = requests.get("https://thispersondoesnotexist.com/image")

file = open("face.png", "wb")
file.write(response.content)
file.close()
todaysTemp = [0, 0, 0]
def todays_forecast():
    #String generation
    speakString = "Welcome to the Cursed Weather forecast. "
    if todaysTemp[0]>=0:
        if todaysTemp[0]>20:
            if todaysTemp[0]>35:
                speakString += "The temperature this morning is extremely hot at "
            else:
                speakString += "The temperature this morning is hot at "
        else:
            speakString += "The temperature this morning is cold at "
    else:
        speakString += "The temperature this morning is freezing cold at "
    speakString += str(todaysTemp[0]) + " degrees. "

    if math.fabs(todaysTemp[0]-todaysTemp[1])>=7:
        speakString += "This will change throughout the day as "
    else:
        speakString += "This will keep on going where "
    speakString += "the temperature this afternoon is " + str(todaysTemp[1]) + " degrees. "

    speakString += "The temperature this evening will be "
    if math.fabs(todaysTemp[1]-todaysTemp[2]) == 0:
        "the same, where the temperature will be"
    else:
        if math.fabs(todaysTemp[1]-todaysTemp[2]) <= 3:
            speakString += "a bit "
        if todaysTemp[2]-todaysTemp[1] > 0:
            speakString += "hotter as the temperature will be "
        else:
            speakString += "colder as the temperature will be "
    speakString += str(todaysTemp[2]) + " degrees. "
    return speakString



def voice_gen(thing_to_say):
    session = requests.session()
    fakeHeader = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'referer' : "https://spik.ai/"}
    source = session.get("https://spik.ai/", headers = fakeHeader)
    csrf_token = source.cookies["csrftoken"]

    phpFormRequest = { 'csrfmiddlewaretoken': csrf_token, "text_to_generate" : speakString, "voice_type" : "en-US-Wavenet-A", "text_or_ssml" : "text"}
    r = session.post("https://spik.ai/generate/",cookies = {"csrftoken" : csrf_token}, data = phpFormRequest, headers = fakeHeader, allow_redirects = True)
    fileRedir = r.text[r.text.find('/media/'):]
    fileRedir = fileRedir[:fileRedir.find('" type="audio/mpeg">')]
    print(fileRedir)

    #Download wave file test
    waveRequest = requests.get("https://spik.ai" + fileRedir)
    waveFile = open("ForeCast.mp3", "wb")
    waveFile.write(waveRequest.content)
    waveFile.close()

def face_gen():
    #Generate face and put to file face.png
    response = requests.get("https://thispersondoesnotexist.com/image")
    file = open("face.png", "wb")
    file.write(response.content)
    file.close()


#GENERATE STILL VID
def vid_gen():
    #Vid name, image name, seconds
    video_name = "noLip.avi"
    image = "face.png"
    seconds = 5
    frame = cv2.imread("face.png")
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, 0, 30, (width, height))

#Vid name, image name, seconds
video_name = "noLip.avi"
image = "face.png"
seconds = 5;
    #Put in frames
    for x in range(seconds*30):
        video.write(cv2.imread(image))

frame = cv2.imread("face.png")
height, width, layers = frame.shape
video = cv2.VideoWriter(video_name, 0, 30, (width, height))
    #Close the stuffs
    cv2.destroyAllWindows()
    video.release()

for x in range(seconds*30):
    video.write(cv2.imread(image))

#Unidentify
cv2.destroyAllWindows()
video.release()


downsample("noLip.avi","out.mp4","800")