# Using IBM Watson's Speech-to-Text API to do Multi-Threaded Transcription of Really Long and Talky Videos, Such as Presidential Debates

A demonstration of how to use Python and IBM Watson's Speech-to-Text API to do some decently accurate transcription of real-world video and audio, at amazingly fast speeds.



Note: I don't actually know how to structure Python projects or do basic object-oriented programming. This code is not finalized and is not guaranteed at all to work for you.

### How it works

After you've downloaded a video file to disk, the assorted scripts and commands in this repo will:

1. Convert the file to mp4 if necessary
2. Create a project subfolder to store the video file and all derived audio and transcripts file
3. Extract the audio from as 16-bit, 16khz WAV files
4. Split the audio into segments (300 seconds each, by default)
5. Send each of those segments to Watson's API to be analyzed and transcribed.
6. Saves the raw responses from Watson's API for each audio file
7. Compiles all of the resulting responses into one data file, as if you had sent the entire audio file to be analyzed in a single go.

The advantages of splitting up the audio is that it allows the transcription to be done in parallel. An hour-long audio track would take probably an hour to get a response back (if your internet connection doesn't fail), whereas 60 parallel requests to analyze 1-minute each will take roughly...1 minute to complete.

I haven't tested the upper-bounds in concurrent requests to Watson's API, though I was able to send around 30 5-minute requests all at once without getting an errors.


TODO: This repo doesn't yet have the (relatively trivial) code to parse the Watson API's JSON responses and create interesting visualizations. Or to make hilarious supercuts from the data. 

Here are some sample results in the [projects/](projects/) folder:

- [The Republican Presidential Debate, South Carolina, Feb. 13, 2016](#republican-debate-in-south-carolina-feb-13-2016)
- [Donald Trump's "Live Free or Die" commercial](#donald-trump-live-free-or-die-commercial-39-seconds)
- [President Obama's Weekly Video Address, Oct. 31, 2015](#president-obama-weekly-address-for-october-31-2015-3-minutes)




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


## Quickie Watson Testy!

Before you get into the Python stuff, you should see if you are properly initialized with Watson by making contact with it from the __command-line__ (i.e. __bash__, i.e. uh not sure if it will work on Windows like this):

If you don't have a WAV file at hand, you can install the [youtube-dl](https://rg3.github.io/youtube-dl/) command-line tool:

    $ pip install youtube-dl

And then download [Trump's Live Free or Die commercial](https://www.youtube.com/watch?v=bb4TxjvQlh0). The following command downloads a movie file, `bb4TxjvQlh0.mkv`, and extracts a WAV file named `bb4TxjvQlh0.wav`:


~~~sh
youtube-dl "https://www.youtube.com/watch?v=bb4TxjvQlh0" \
  --keep-video \
  --extract-audio \
  --audio-format wav \
  --audio-quality 16K \
  --id
~~~


In the next step, I assume you have a file named `bb4TxjvQlh0.wav`, but you are free to use any WAV audio file. 

*(Note: the whole movie-file thing is totally ancillary...Watson doesn't care if the audio file comes from a movie or you recording into your microphone or whatever. But people like to transcribe videos, which is why I include the step.)*

This next step is what contacts Watson's API. Replace `USERNAME` and `PASSWORD` with whatever credentials you got from the IBM Bluemix Developer Panel.

The `--data-binary` flag wants a file name (prepended with `@`).

When the audio file is uploaded and Watson returns a response, it will be saved to `transcript.json`

~~~sh
curl -X POST \
     -u USERNAME:PASSWORD     \
     -o transcript.json        \
     --header "Content-Type: audio/wav"    \
     --header "Transfer-Encoding: chunked" \
     --data-binary "@bb4TxjvQlh0.wav"        \
     "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?continuous=true&timestamps=true&word_confidence=true&profanity_filter=false"
~~~

If this doesn't work for you, then either your Internet is down, Watson is down, or you don't have the proper user/password credentials.







## Python stuff

This project uses:

- Anaconda 3-2.4.0
- Python 3.5.1
- Requests
- [moviepy](https://github.com/Zulko/moviepy) - currently, just being used as a very nice wrapper around ffmpeg, to do audio-video conversion and extraction. But has a lot of potential for laughter and games via programmatic editing.
  - moviepy will install __ffmpeg__ if you don't already have it installed

# Demonstrations

## Republican Debate in South Carolina, Feb. 13, 2016


Check out the [projects/republican-debate-sc-2016-02-13 folder](projects/republican-debate-sc-2016-02-13) in this repo to see the raw JSON response files and their corresponding .WAV audio, as extracted from the [Feb. 13, 2016 Republican Presidential Candidate debate in South Carolina](https://www.youtube.com/watch?v=OkSRfYeD7cQ):

<a href="https://www.youtube.com/watch?v=OkSRfYeD7cQ">
  <img src="https://i.ytimg.com/vi/OkSRfYeD7cQ/maxresdefault.jpg"
  alt="debate video on youtube">
</a>




## Donald Trump "Live Free or Die" commercial (39 seconds)

The commercial can be seen [here on YouTube](https://www.youtube.com/watch?v=bb4TxjvQlh0):

<a href="https://www.youtube.com/watch?v=bb4TxjvQlh0">
  <img src="https://i.ytimg.com/vi/bb4TxjvQlh0/maxresdefault.jpg" alt="trumpvideo">
</a>

The project directory generated: [projects/trump-nh/](projects/trump-nh/)

Because the video is so short, the directory includes the video file, the extracted audio, as well as the segmented audio and raw Watson JSON responses. For this example, I made the segments __10 seconds__ long.

To compile the transcript text:

~~~py
import json
from glob import glob
filenames = glob("./projects/trump-nh/transcripts/*.json")

for fn in filenames:
  with open(fn, 'r') as t:
      data = json.loads(t.read())
      for x in data['results']:
          best_alt = x['alternatives'][0]
          print(best_alt['transcript'])
~~~

The result:

> this great slogan of the Hampshire live free or die means so much 
>
> so many people all over the world they use that expression it means liberty it means freedom it means free enterprise 
>
>mean safe 
>
> the insecurity it means borders it means strong strong military where nobody's going to mess with us it means taking care of our vets 
>
> what a great slogan congradulations New Hampshire 

> wonderful job dnmt 
> I 
> and 

Note that the last 3 tokens, `dmnt I and`, are a result of the Watson API getting confused by the dramatic music that closes the commercial. Luckily, the JSON response includes, among timestamp data for each work, a confidence level as well.

It actually is spot on for Trump's full closing sentence (not sure why "congradulations" is used...)...the confidence levels for `dmnt I and` were very low comparatively...I think `dmnt` is some kind of code word used by the API to indicate something, not that Watson thought that `dmnt` was actually said (see the [full JSON response here](projects/trump-nh/transcripts/00030-00040.json))

~~~json
{
    "word_confidence": [
        [
            "what",
            0.9999999999999674
        ],
        [
            "a",
            0.9999999999999672
        ],
        [
            "great",
            0.999999999999967
        ],
        [
            "slogan",
            0.9964234383591973
        ],
        [
            "congradulations",
            0.7798716606178608
        ],
        [
            "New",
            0.9999999999999933
        ],
        [
            "Hampshire",
            0.9845177369977128
        ]
    ]
}
~~~


## President Obama weekly address for October 31, 2015 (3 minutes)

Here's a quick demonstration of Watson's accuracy given a weekly video address from President Obama (~3 minutes):

- [Video landing page at Whitehouse.gov](https://www.whitehouse.gov/the-press-office/2015/10/31/weekly-address-its-time-reform-our-criminal-justice-system)
- [Video file: 103115_WeeklyAddress.mp4](https://www.whitehouse.gov/WeeklyAddress/2015/103115-QREDSC/103115_WeeklyAddress.mp4)
- [Audio file: 00000-00190.wav](projects/obama-weekly-address-2015-10-31/audio-segments/00000-00190.wav)
- [Watson JSON response: 00000-00190.json](projects/obama-weekly-address-2015-10-31/transcripts/00000-00190.json)
- The produced file folder: [projects/obama-weekly-address-2015-10-31/](projects/obama-weekly-address-2015-10-31/)


(because President Obama's video address is just about 3 minutes long, only audio file is extracted, and only one call to Watson's API is made)


Right now there's just a bunch of sloppy scripts that need to be refactored. There's a script named [go.py](go.py) that you can run from the command-line that will read an existing video file, create a project folder, cut up the audio, and do the transcriptions. It assumes that you have a file named `credsfile_watson.json` relative to `go.py`.


Some code for the commandline, to download the file, then to run `go.py`:

~~~sh
curl -o "/tmp/obama-weekly-address-2015-10-31.mp4" \
  https://www.whitehouse.gov/WeeklyAddress/2015/103115-QREDSC/103115_WeeklyAddress.mp4

python go.py /tmp/obama-weekly-address-2015-10-31.mp4
~~~



The output produced by `go.py`:

~~~
[MoviePy] Writing audio in /Users/dtown/watson-word-watcher/projects/obama-weekly-address-2015-10-31/full-audio.wav
[MoviePy] Done.                                                                                            
[MoviePy] Writing audio in /Users/dtown/watson-word-watcher/projects/obama-weekly-address-2015-10-31/audio-segments/00000-00190.wav
[MoviePy] Done.                                                                                            
Sending to Watson API:
   /Users/dtown/watson-word-watcher/projects/obama-weekly-address-2015-10-31/audio-segments/00000-00190.wav
Transcribed:
   /Users/dtown/watson-word-watcher/projects/obama-weekly-address-2015-10-31/transcripts/00000-00190.json
~~~


And a quickie processing of the JSON transcript:

~~~py
import json
FILENAME = './projects/obama-weekly-address-2015-10-31/transcripts/00000-00190.json'

with open(FILENAME, 'r') as t:
    data = json.loads(t.read())
    for x in data['results']:
        best_alt = x['alternatives'][0]
        print(best_alt['transcript'])
~~~

The output:

> hi everybody today there are two point two million people behind bars in America and millions more on parole or probation 
> 
> every year we spend eighty billion 
> 
> in taxpayer dollars 
> 
> keep people incarcerated 
> 
> many are nonviolent offender serving unnecessarily long sentences 
> 
> I believe we can disrupt the pipeline from underfunded schools overcrowded jails 
> 
> I believe we can address the disparities in the application of criminal justice from arrest rates to sentencing to incarceration 
> 
> and I believe we can help those who have served their time and earned a second chance 
> 
> get the support they need to become productive members of society 
> 
> that's why over the course of this year I've been talking to folks around the country about reforming our criminal justice system 
> 
> to make it smarter fairer and more effective 
> 
> in February I sat down in the oval office with police officers from across the country 
> 
> in the spring 
> 
> I met with police officers and young people in Camden New Jersey where they're using community policing and data to drive down crime 
> 
> over the summer I visited a prison in Oklahoma to talk with inmates and correction officers about rehabilitating prisoners 
> 
> preventing more people from ending up there in the first place 
> 
> two weeks ago I visit West Virginia to meet with families battling prescription drug heroin abuse 
> 
> as well as people who are working on new solutions for treatment and rehabilitation 
> 
> last week I traveled to Chicago to thank police chiefs from across the country for all that their officers do to protect Americans 
> 
> to make sure they get the resources they need to get the job done 
> 
> and to call for common sense gun safety reforms that would make officers and their communities safe 
> 
> we know that having millions of people in the criminal justice system without any ability to find a job after release is unsustainable 
> 
> it's bad for communities and it's bad for our economy 
> 
> so on Monday I'll travel to Newark New Jersey to highlight efforts to help Americans 
> 
> paid their debt to society re integrate back into their communities 
> 
> everyone has a role to play for businesses that are hiring ex offenders 
> 
> to philanthropies they're supporting education and training programs 
> 
> and I'll keep working with people in both parties to get criminal justice reform bills to my desk 
> 
> including a bipartisan bill that would reduce mandatory minimums for nonviolent drug offenders and reward prisoners 
> 
> shorter sentences if they complete programs that make them less likely 
> 
> commit a repeat offense 
> 
> there's a reason good people across the country are coming together to reform our criminal justice system 
> 
> because it's not about politics 
> 
> it's about whether we as a nation live up to our founding ideals of liberty and justice for all 
> 
> and working together we can make sure that we do 
> 
> thanks everybody have a great weekend and have a safe and happy Halloween 

You [can compare it to the transcript here](https://www.whitehouse.gov/the-press-office/2015/10/31/weekly-address-its-time-reform-our-criminal-justice-system).



