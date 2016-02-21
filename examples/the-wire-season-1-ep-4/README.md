# Watson's transcription performance on The Wire Season 1 Episode 4 "Old Cases"

Sadly, Watson may not be up to doing supercuts of the vivid dialogue found in The Wire. For example, "Old Cases", [the first season's 4th episode](https://en.wikipedia.org/wiki/Old_Cases), is famous for having a scene in which [two detectives successfully investigate a murder scene while communicating almost exclusively with the word "fuck"](https://www.youtube.com/watch?v=1lElf7D-An8).

Running Watson's speech-to-text API on the entire episode yields only __59 profanities__. I've uploaded the [result to YouTube](https://youtu.be/muP5aH1aWUw):

[https://youtu.be/muP5aH1aWUw](https://youtu.be/muP5aH1aWUw)


There's a couple of problems that arise:

__One:__ Even though Watson has a [profanity_filter parameter](https://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/speech-to-text/using.shtml#profanity_filter), which can be set to `false`, it apparently will still filter for `"fuck"` and `"bitch"` and even `"scrotum"` (as you can see in the uploaded [YouTube clip](https://youtu.be/muP5aH1aWUw)). In the transcription file ([line-by-line](https://github.com/dannguyen/watson-word-watcher/blob/master/examples/the-wire-season-1-ep-4/lines-transcript.csv), [word-by-word](https://github.com/dannguyen/watson-word-watcher/blob/master/examples/the-wire-season-1-ep-4/words-transcript.csv), [full json](https://github.com/dannguyen/watson-word-watcher/blob/master/examples/the-wire-season-1-ep-4/full-transcript.json)), these filtered words are transcribed as `"****"`, although  `"shit"` escapes the filter:

https://github.com/dannguyen/watson-word-watcher/blob/master/examples/the-wire-season-1-ep-4/lines-transcript.csv#L148 

__Two:__ 59 profanities is not very much for an entire episode of The Wire. In fact, in the [aforementioned investigative scene](https://www.youtube.com/watch?v=1lElf7D-An8), has [30+ "fucks" in the span of a few minutes](http://genius.com/The-wire-cursing-scene-annotated). Some of the utterances may be too quiet or too ambiguous for Watson (the API returns tokens like `'nbsp'` and `'fn'` in cases where the word is untranslatable)

You can see the word-by-word transcription in this file: the investigative scene starts at around the 47th minute (i.e. 2,800 seconds in):

https://github.com/dannguyen/watson-word-watcher/blob/master/examples/the-wire-season-1-ep-4/words-transcript.csv#L4157


It's possible I'm setting the `profanity_filter` parameter incorrectly:

~~~
API_DEFAULT_PARAMS = {
    'continuous': True,
    'timestamps': True,
    'word_confidence': True,
    'profanity_filter': False,
    'word_alternatives_threshold': 0.4
}
~~~
