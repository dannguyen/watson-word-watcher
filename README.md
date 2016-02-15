# Using IBM Watson's Speech-to-Text API to Transcribe Really Long, Talky Videos such as Presidential Debates


Note: I don't actually know how to structure Python projects or do basic object-oriented programming. This code is not finalized and may not make any sense.

Also, this repo doesn't yet have the (relatively trivial) code to parse the Watson API's JSON responses. Or to make hilarious supercuts from the data.

# Requirements


## IBM Watson

The transcription power comes from IBM Watson's Speech-to-Text REST API. After cutting up a video into 5-minute segments, I then upload all of the audio files in parallel to Watson, which can complete the entire batch in nearly just 5 minutes.

- [Live Watson Speech-to-Text demo](https://speech-to-text-demo.mybluemix.net/)
- [Watson's Speech-to-Text documentation](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/speech-to-text/index.shtml)
- [API reference](https://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/speech-to-text/api/v1/)

### Getting started with IBM Bluemix

You have to sign up for an [IBM Bluemix account](http://www.ibm.com/cloud-computing/bluemix/), which is free and doesn't require a credit card for the first month.

After signing up for Bluemix, you can find the console page for the speech-to-text API here, [where you can get user credentials](https://console.ng.bluemix.net/catalog/services/speech-to-text). This repo contains a sample file: [credsfile_watson.SAMPLE.json](credsfile_watson.SAMPLE.json)

The [pricing is pretty generous, in terms of testing things out](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/speech-to-text.html#pricing-block): 1,000 minutes free __each month__. Every additional minute is __$0.02__ -- i.e. transcribing an hour's worth of audio will cost $1.20.



## Python stuff

This project uses:

- Anaconda 3-2.4.0
- Python 3.5.1
- Requests
- [moviepy](https://github.com/Zulko/moviepy) - currently, just being used as a very nice wrapper around ffmpeg, to do audio-video conversion and extraction. But has a lot of potential for laughter and games via programmatic editing.
  - moviepy will install __ffmpeg__ if you don't already have it installed

# Demonstration

Right now there's just a bunch of sloppy scripts that need to be refactored. There's a script named [go.py](go.py) that you can run from the command-line that will read an existing video file, create a project folder, cut up the audio, and do the transcriptions. It assumes that you have a file named `credsfile_watson.json` relative to `go.py`.


~~~sh
$ curl -o "/tmp/obama-weekly-address-2015-10-31.mp4" \
  https://www.whitehouse.gov/WeeklyAddress/2015/103115-QREDSC/103115_WeeklyAddress.mp4

$ python go.py /tmp/obama-weekly-address-2015-10-31.mp4
~~~
