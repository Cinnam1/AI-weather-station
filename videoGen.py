from videoConvert import downsample
import requests
import cv2
import math
import ffmpeg
import subprocess
from pydub import AudioSegment

#Generate face and put to file face.png
response = requests.get("https://thispersondoesnotexist.com/image")
file = open("face.png", "wb")
file.write(response.content)
file.close()

def parseApiTemperature():
    data = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=56.162937&lon=10.203921&exclude=current,minutely,hourly,alerts&appid=7311d6fc621b3fc343a5d5e87c3530eb")
    return data.json()




def todays_forecast(todaysTemp):
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



def voice_gen(thing_to_say, name):
    session = requests.session()
    fakeHeader = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 'referer' : "https://spik.ai/"}
    source = session.get("https://spik.ai/", headers = fakeHeader)
    csrf_token = source.cookies["csrftoken"]

    phpFormRequest = { 'csrfmiddlewaretoken': csrf_token, "text_to_generate" : thing_to_say, "voice_type" : "en-US-Wavenet-A", "text_or_ssml" : "text"}
    r = session.post("https://spik.ai/generate/",cookies = {"csrftoken" : csrf_token}, data = phpFormRequest, headers = fakeHeader, allow_redirects = True)
    fileRedir = r.text[r.text.find('/media/'):]
    fileRedir = fileRedir[:fileRedir.find('" type="audio/mpeg">')]
    print(fileRedir)

    #Download wave file test
    waveRequest = requests.get("https://spik.ai" + fileRedir)
    waveFile = open(name + ".mp3", "wb")
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


        #Put in frames
    for x in range(seconds*30):
        video.write(cv2.imread(image))



    #Unidentify
    cv2.destroyAllWindows()
    video.release()

#Joins audio, inputnames are a list (WITH filetype), outputname is a single string
def joinAudio(inputNames, outputName):
    HELPME = AudioSegment.from_mp3("today.mp3")
    print("HELPED ME:" + str(HELPME))
    formattedInputNames = [AudioSegment.from_file(mp3_file, format="mp3") for mp3_file in inputNames]
    AudioSegment.from_mp3("today.mp3")
    output = AudioSegment.empty()
    for files in formattedInputNames:
        output += files
    output.export(outputName, format="mp3")



#Run the functions

temperatures = {'lat': 56.16, 'lon': 10.2, 'timezone': 'Europe/Copenhagen', 'timezone_offset': 3600, 'daily': [{'dt': 1605524400, 'sunrise': 1605509957, 'sunset': 1605539343, 'temp': {'day': 283.26, 'min': 281.71, 'max': 283.26, 'night': 282.35, 'eve': 282.63, 'morn': 282.31}, 'feels_like': {'day': 278.27, 'night': 277.77, 'eve': 278.6, 'morn': 275.65}, 'pressure': 1001, 'humidity': 84, 'dew_point': 280.68, 'wind_speed': 6.31, 'wind_deg': 225, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'clouds': 47, 'pop': 0.71, 'rain': 2.4, 'uvi': 0.44}, {'dt': 1605610800, 'sunrise': 1605596480, 'sunset': 1605625644, 'temp': {'day': 284.69, 'min': 281.59, 'max': 285.25, 'night': 285.01, 'eve': 284.83, 'morn': 282.04}, 'feels_like': {'day': 280.3, 'night': 280.15, 'eve': 279.91, 'morn': 277.2}, 'pressure': 1014, 'humidity': 92, 'dew_point': 283.56, 'wind_speed': 6.45, 'wind_deg': 227, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'clouds': 100, 'pop': 1, 'rain': 2.33, 'uvi': 0.47}, {'dt': 1605697200, 'sunrise': 1605683003, 'sunset': 1605711948, 'temp': {'day': 284.6, 'min': 282.47, 'max': 285.35, 'night': 282.54, 'eve': 282.47, 'morn': 285.08}, 'feels_like': {'day': 278.51, 'night': 276.23, 'eve': 276.4, 'morn': 280.95}, 'pressure': 1018, 'humidity': 83, 'dew_point': 281.99, 'wind_speed': 8.27, 'wind_deg': 220, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'clouds': 100, 'pop': 0, 'uvi': 0.47}, {'dt': 1605783600, 'sunrise': 1605769525, 'sunset': 1605798254, 'temp': {'day': 282.41, 'min': 276.15, 'max': 284.74, 'night': 276.15, 'eve': 278.12, 'morn': 284.74}, 'feels_like': {'day': 274.61, 'night': 268.04, 'eve': 269.99, 'morn': 278.39}, 'pressure': 1005, 'humidity': 64, 'dew_point': 276.02, 'wind_speed': 8.95, 'wind_deg': 240, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 'clouds': 56, 'pop': 1, 'rain': 4.88, 'uvi': 0.38}, {'dt': 1605870000, 'sunrise': 1605856045, 'sunset': 1605884563, 'temp': {'day': 278.06, 'min': 274.79, 'max': 278.06, 'night': 274.79, 'eve': 275.33, 'morn': 275.13}, 'feels_like': {'day': 272.8, 'night': 269.76, 'eve': 270.03, 'morn': 269.2}, 'pressure': 1022, 'humidity': 64, 'dew_point': 267.96, 'wind_speed': 4.41, 'wind_deg': 336, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'clouds': 45, 'pop': 0.19, 'uvi': 0.36}, {'dt': 1605956400, 'sunrise': 1605942564, 'sunset': 1605970875, 'temp': {'day': 278.05, 'min': 274.28, 'max': 278.23, 'night': 278.19, 'eve': 278.21, 'morn': 274.35}, 'feels_like': {'day': 272.53, 'night': 270.34, 'eve': 270.54, 'morn': 270.63}, 'pressure': 1024, 'humidity': 68, 'dew_point': 271.64, 'wind_speed': 4.95, 'wind_deg': 192, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'clouds': 100, 'pop': 0.8, 'rain': 0.66, 'uvi': 0.37}, {'dt': 1606042800, 'sunrise': 1606029082, 'sunset': 1606057190, 'temp': {'day': 281.54, 'min': 278.37, 'max': 281.54, 'night': 278.51, 'eve': 278.37, 'morn': 279.43}, 'feels_like': {'day': 277.17, 'night': 274.26, 'eve': 274.19, 'morn': 276.3}, 'pressure': 1016, 'humidity': 72, 'dew_point': 276.95, 'wind_speed': 4.26, 'wind_deg': 276, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 'clouds': 21, 'pop': 1, 'rain': 4.13, 'uvi': 0.36}, {'dt': 1606129200, 'sunrise': 1606115598, 'sunset': 1606143507, 'temp': {'day': 281.23, 'min': 277.77, 'max': 281.23, 'night': 277.82, 'eve': 278.41, 'morn': 277.77}, 'feels_like': {'day': 276.51, 'night': 274.28, 'eve': 274.11, 'morn': 273.39}, 'pressure': 1025, 'humidity': 75, 'dew_point': 277.09, 'wind_speed': 4.83, 'wind_deg': 281, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'clouds': 0, 'pop': 0, 'uvi': 0.33}]}

morning = int(temperatures["daily"][0]["temp"]["morn"] - 273.15)
day = int(temperatures["daily"][0]["temp"]["day"]-273.15)
eve = int(temperatures["daily"][0]["temp"]["eve"]-273.15)
thisTodaysTemp = [morning, day, eve]

morning = int(temperatures["daily"][1]["temp"]["morn"] - 273.15)
day = int(temperatures["daily"][1]["temp"]["day"]-273.15)
eve = int(temperatures["daily"][1]["temp"]["eve"]-273.15)
tommorowsTemp = [morning, day, eve]


voice_gen(todays_forecast(thisTodaysTemp), "today")
voice_gen(todays_forecast(tommorowsTemp), "tomorrow")

joinAudio(["today.mp3", "tomorrow.mp3"] , "ForeCast.mp3")

vid_gen()

print("Downsampling video file")

downsample("noLip.avi","reScaledOut.mp4","32000")

