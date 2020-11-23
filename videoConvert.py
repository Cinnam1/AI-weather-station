import ffmpeg
import subprocess
from os import path

def downsample(infile,outfile,bitrate):
    #set up variables for command processing
    aviConvert = str("ffmpeg -i " + infile + " out.mp4")
    reScale = str("ffmpeg -i out.mp4 -b " + bitrate + " " + outfile)
    cleanupOldout = str("rm out.mp4")
    cleanupOldReScaled = str("rm " + outfile)
    cleanupOldnoLip = str("rm " + infile)
    print(aviConvert)
    print(reScale)
    print(cleanupOldout)
    print(cleanupOldReScaled)
    print(cleanupOldnoLip)
    
    #check if previous outputs exists, and deleting old output to eliminate conflict during conversionk.
    if path.isfile('out.mp4') == True:
	    subprocess.call(cleanupOldout, shell=True)
    
    if path.isfile('reScaledOut.mp4') == True:
	    subprocess.call(cleanupOldReScaled, shell=True)

    
    #execute conversions and cleanup
    subprocess.call(aviConvert, shell=True)
    subprocess.call(reScale, shell=True)
    subprocess.call(cleanupOldout, shell=True)
    subprocess.call(cleanupOldnoLip, shell=True)

