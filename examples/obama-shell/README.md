# Using the shell to testing out the Watson API with President Obama

Before going full Python, which drastically increases the number of ways your system can throw an error, let's just do some basic shell-level scripting to make sure you can even contact IBM Watson.


## Setting up the environment

Open up your __Terminal__/command-line prompt. Assuming you don't want to litter your Desktop with Obama video clips, you can create a temp directory to work from if you want:



~~~sh
mkdir -p /tmp/obama-watson
cd /tmp/obama-watson
~~~

## Download a movie file with cURL

Let's pick a movie file your (American) tax dollars have paid for: one of President Obama's weekly video addresses: [President Obama Says We Must Move Forward on Wall Street Reform (April 17, 2010)](https://www.whitehouse.gov/the-press-office/weekly-address-president-obama-says-we-must-move-forward-wall-street-reform).

The direct link to the movie file is here in MP4 format:

[https://www.whitehouse.gov/WeeklyAddress/2010/041710-LKXTMN/041710_WeeklyAddress.mp4](https://www.whitehouse.gov/WeeklyAddress/2010/041710-LKXTMN/041710_WeeklyAddress.mp4)

If for some reason, the White House goes out of business, you can try this mirror of mine:

[http://stash.compciv.org/multimedia/041710_WeeklyAddress.mp4](http://stash.compciv.org/multimedia/041710_WeeklyAddress.mp4)

### The curl command

If you're on a standard *nix system, e.g. OSX or Linux, then you have __cURL__ -- known as "[the hobby project with a billion users](http://www.meetup.com/Google-Tech-Talk-Meetup/events/223765176/)" -- which allows us to contact HTTP resources via the command-line, including downloading them.

The following command will download the file at this URL:

    https://www.whitehouse.gov/WeeklyAddress/2010/041710-LKXTMN/041710_WeeklyAddress.mp4

And save it relative to wherever you currently are in your file system. In other words, if you are inside `/tmp/obama-watson/`, then the movie file will be at:

    /tmp/obama-watson/041710_WeeklyAddress.mp4

~~~sh
curl -o "041710_WeeklyAddress.mp4" \
  "https://www.whitehouse.gov/WeeklyAddress/2010/041710-LKXTMN/041710_WeeklyAddress.mp4"
~~~

Try opening the file to see that it is indeed a normal movie file. On OSX, you can simply do this:

~~~sh
open 041710_WeeklyAddress.mp4
~~~

## Extract the audio with ffmpeg

This is where things start breaking down depending on how your system is configured. 

For my Python workflow, I use the [__moviepy__ library](https://github.com/Zulko/moviepy), which is a beautiful fun wrapper around the stalwart and ubiquitous [FFmpeg library](https://www.ffmpeg.org/). But FFmpeg can be used standalone.

What is FFMpeg? [FFmpeg](https://www.ffmpeg.org/) is a popular program that is used for converting video and audio formats, including the extraction of audio tracks from a video file. If you [can't get FFmpeg installed](https://www.ffmpeg.org/download.html) (I recommend doing it via homebrew if you're on OS X and are already using [Homebrew](http://brew.sh/)), you won't be able to do this next step...which is __fine__, because using the Watson API doesn't require dealing with video. You just need to have an audio file -- so if you need to transcribe an audio recording, you're still good to go.

(note: __moviepy__ will attempt to install FFmpeg when you first run __moviepy__...depending on how weird your system is, that might just work out for you to do things all in Python...)

If you can't use FFmpeg for whatever reason, go ahead and download the [WAV audio file here](http://stash.compciv.org/multimedia/041710_WeeklyAddress.wav) and continue to the next step, in which we actually send it to Watson's API via __curl__.


#### The ffmpeg command to extract audio

OK, so you got __ffmpeg__ installed? Run the following shell command, which will create `041710_WeeklyAddress.wav` from the `041710_WeeklyAddress.mp4` movie file you downloaded from the White House:


~~~sh
ffmpeg -i "041710_WeeklyAddress.mp4" \
  -vn -ar 16000 -acodec pcm_s16le \
  "041710_WeeklyAddress.wav"
~~~


In case you're wondering what those flags meant (because I sure as ---- don't remember, which is why I delegate the work to the __moviepy__ library):

- `-i` specifies the input file
- `-vn` disables video (i.e. we just want audio)
- `-ar` sets rate in Hz, e.g. `16000`
- `-acodec`  sets the audio codec: we want 16-bit WAV, i.e. `pcm_s16le`


Again, if you can't get ffmpeg to work, then go ahead and download the [WAV audio file here](http://stash.compciv.org/multimedia/041710_WeeklyAddress.wav) and move on to the next step.

## Send the audio to the Watson Speech-to-Text API

OK, so you've signed up for an IBM Developer account and a Bluemix account, right (the latter is a free offer when you sign up for a dev account)? If so, you should be able to get to the speech-to-text console here:

[https://console.ng.bluemix.net/catalog/services/speech-to-text](https://console.ng.bluemix.net/catalog/services/speech-to-text)

...and somewhere on there is a button to get credentials, which will be in this plaintext format:

~~~json
{
  "credentials": {
    "url": "https://stream.watsonplatform.net/speech-to-text/api",
    "username": "99999999-4aaa-b333-l335-999999999",
    "password": "ABCDEFGJIHK"
  }
}
~~~

(note that the credentials are __not__ your IBM developer account credentials -- each API you sign-up for will assign you a new username and password)

In your shell, set a couple of variables for convenient reference in the current session:

~~~sh
WATSON_USERNAME="your-user-name-credentials-here"
WATSON_PASSWORD="yourpasswordhere"
~~~

### Making a POST request to IBM Watson's API with curl

Let's hit up the API. Here's the curl call:

~~~sh
curl -X POST \
     -u "$WATSON_USERNAME":"$WATSON_PASSWORD"     \
     -o 041710_WeeklyAddress.json        \
     --header "Content-Type: audio/wav"    \
     --header "Transfer-Encoding: chunked" \
     --data-binary "@041710_WeeklyAddress.wav"        \
     "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?continuous=true&timestamps=true&word_confidence=true&profanity_filter=false"
~~~

Now, wait for about 5 to 10 minutes, depending on how long it takes for you to upload that ~20MB file to IBM.

When it's finished, and assuming there's no error message, the `curl` command should have dumped the data into a file named `041710_WeeklyAddress.json`. You can quickly output it to screen via the __cat__ command:

~~~sh
cat 041710_WeeklyAddress.json
~~~

And it's going to look like this at the top:

~~~
      {
   "results": [
      {
         "alternatives": [
            {
               "word_confidence": [
                  [
                     "there", 
                     0.9999999999999846
                  ], 
                  [
                     "were", 
                     0.6345875705460627
                  ], 
                  [
                     "many", 
                     0.9999999999999966
                  ], 
~~~

## Parsing the JSON response


So...we're reaching the limits of what can easily be done via just the command-line...

### Previewing the plaintext

Here's how to just see the raw text of the transcript, without the timestamp or word-level confidence scores, using basic Unix tools (ok, I admit, my parents never taught me awk, I'm a hoser):

~~~sh
cat 041710_WeeklyAddress.json | 
    grep '"transcript":' |
    sed 's/ *"transcript": *//' |
    tr -d '",'
~~~

Which gets you this plain output:

~~~
there were many causes the turmoil that ripped through our economy over the past two years  
but above all this crisis was caused by the failures in the financial industry  
what's clear is that this crisis could have been avoided  
if Wall Street firms were more accountable  
if financial dealings were more transparent  
if consumers and shareholders were given more information and authority to make decisions  
but that didn't happen  
and that's because special interests have waged a relentless campaign to thwart even basic common sense rules  
rules to prevent abuse and protect consumers  
~~~


### Converting JSON to PSV

OK, I don't know how to do this (easily) with just command-line utilities. I think it would honestly be easier to sit down and learn Python than to learn whatever parsing acrobatics it would take to do it from purely shell code.

The following script parses the JSON file and returns a simple __pipe-delimited-file__...i.e. a CSV file, except with pipes...because...no reason, really...I don't think the Watson API ever returns commas in the text values...but just to be safe...

~~~py
import json
import csv
INPUT_FILENAME = "041710_WeeklyAddress.json"
OUTPUT_FILENAME = "041710_WeeklyAddress.psv"
outfile = open(OUTPUT_FILENAME, 'w')
c = csv.writer(outfile, delimiter="|")
with open(INPUT_FILENAME) as f:
    data = json.load(f)
    for r in data['results']:
        alt = r['alternatives'][0]
        for t in alt['timestamps']:
            c.writerow(t)
outfile.close()
~~~


When back in the command-line prompt, you can use __head__ to view the top of the file:

~~~sh
head "041710_WeeklyAddress.psv"
~~~

~~~
there|5.85|5.97
were|5.97|6.06
many|6.06|6.28
causes|6.28|6.77
the|6.77|6.95
turmoil|6.95|7.42
that|7.42|7.56
ripped|7.56|7.8
through|7.8|8.01
~~~

Here's an HTML-formatted version:

|---------|------|------|
| there   | 5.85 | 5.97 |
| were    | 5.97 | 6.06 |
| many    | 6.06 | 6.28 |
| causes  | 6.28 | 6.77 |
| the     | 6.77 | 6.95 |
| turmoil | 6.95 | 7.42 |
| that    | 7.42 | 7.56 |
| ripped  | 7.56 |  7.8 |
| through |  7.8 | 8.01 |

The JSON data has been simplified so that each transcribed word occupies its own line. The text of the word is in the first column. The start and end time, in seconds, are in the second and third columns, respectively.

This means we can now filter the list for words that we want with a simple __grep__:

Note: OK, at this point, you know if Watson works for you. I don't have the chops to write out an elegant solution in Bash that won't accidentally wipe out your computer. Please proceed to the Python version.



# TODO How to use FFMPEG to split stuff

~~~sh
echo ffmpeg -y                          \
       -i 041710_WeeklyAddress.mp4  \
       -ss 10                       \
       -t 20                        \
       -vcodec libx264              \
       -acodec copy                 \
       whatever.mp4
~~~
```
