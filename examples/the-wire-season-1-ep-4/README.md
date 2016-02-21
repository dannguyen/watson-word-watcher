# Watson's transcription performance on The Wire Season 1 Episode 4 "Old Cases"

Sadly, while Watson does a [decent job with presidential debates](https://www.youtube.com/watch?v=K41miubs1eE&list=PLLrlUAN-LoO73FrSa6yn8gsPpi7J9TJb7&index=1), it may not be up to doing supercuts of the vivid dialogue found in The Wire. For example, "Old Cases", [the first season's 4th episode](https://en.wikipedia.org/wiki/Old_Cases), is famous for having a scene in which [two detectives successfully investigate a murder scene while communicating almost exclusively with the word "fuck"](https://www.youtube.com/watch?v=1lElf7D-An8).

Running Watson's speech-to-text API on the entire episode yields only __59 profanities__. I've uploaded the [result to YouTube](https://youtu.be/muP5aH1aWUw):

__[https://youtu.be/muP5aH1aWUw](https://youtu.be/muP5aH1aWUw)__


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


After the Watson transcription is made, I run it through my `supercut.py` script; 

      python supercut.py projects/the-wire-ep-4 '\*{4}|shit' 


which generates the video and this output:



~~~
Extracting case-insensitive pattern: \*{4}|shit
  from project: projects/the-wire-ep-4
  with a minimum confidence of: 0.0
   0: **** 0.329 71.47 71.84
   1: **** 0.537 109.55 109.94
   2: **** 0.615 139.11 139.49
   3: **** 0.76 284.94 285.37
   4: **** 0.962 359.03 359.29
   5: **** 0.199 369.2 369.53
   6: **** 0.635 390.37 390.74
   7: **** 1.0 410.65 410.93
   8: **** 0.727 433.94 434.47
   9: **** 0.565 648.45 648.84
   10: **** 0.577 655.64 655.96
   11: shit 0.733 667.34 667.65
   12: **** 0.993 673.11 673.51
   13: **** 0.233 687.86 688.13
   14: **** 0.402 696.56 697.08
   15: **** 0.157 700.63 701.06
   16: **** 0.501 708.65 709.12
   17: **** 0.353 825.54 825.79
   18: **** 0.697 837.19 837.56
   19: **** 0.284 854.37 854.78
   20: **** 0.279 917.14 917.74
   21: **** 0.97 925.58 926.12
   22: **** 0.988 957.11 957.41
   23: **** 0.226 1045.88 1046.47
   24: **** 0.362 1214.74 1215.26
   25: **** 0.494 1216.28 1216.67
   26: bullshit 0.59 1484.25 1484.81
   27: **** 0.53 1511.39 1511.7
   28: shit 0.801 1587.41 1587.73
   29: shit 0.208 1589.62 1589.91
   30: shit 0.357 1590.68 1590.96
   31: **** 0.494 1617.27 1617.6
   32: shit 0.52 1636.46 1636.6399999999999
   33: **** 0.654 1666.07 1666.44
   34: **** 0.49 1782.65 1783.01
   35: **** 0.849 1907.16 1907.44
   36: **** 0.229 2031.83 2032.13
   37: **** 0.366 2032.94 2033.38
   38: **** 0.61 2035.41 2035.81
   39: **** 0.622 2051.88 2052.45
   40: **** 0.368 2074.85 2075.2799999999997
   41: **** 0.366 2081.41 2081.65
   42: **** 0.617 2089.69 2090.08
   43: **** 0.114 2090.56 2090.98
   44: **** 0.513 2102.93 2103.3
   45: **** 0.897 2103.45 2103.81
   46: **** 0.876 2112.43 2113.04
   47: bullshit 0.433 2143.98 2144.39
   48: **** 0.854 2454.0 2454.32
   49: shit 0.331 2709.5 2709.76
   50: **** 0.385 2774.53 2775.52
   51: **** 0.312 2888.81 2889.15
   52: **** 0.504 2930.44 2930.88
   53: **** 0.561 2964.2200000000003 2964.74
   54: **** 0.253 3068.55 3068.85
   55: **** 1.0 3182.23 3182.68
   56: **** 0.387 3233.14 3233.65
   57: **** 0.368 3264.3 3264.65
   58: shit 0.114 3284.77 3285.19
~~~
