# Watson's transcription performance on The Wire Season 1 Episode 4 "Old Cases"

Sadly, Watson may not be up to doing supercuts of the vivid dialogue found in The Wire. For example, "Old Cases", [the first season's 4th episode](https://en.wikipedia.org/wiki/Old_Cases), is famous for having a scene in which [two detectives successfully investigate a murder scene while communicating almost exclusively with the word "fuck"](https://www.youtube.com/watch?v=1lElf7D-An8).

Running Watson's speech-to-text API on the entire episode only yields 50 profanities. I've uploaded the result to YouTube:

[https://youtu.be/FoRnbbRAlko](https://youtu.be/FoRnbbRAlko)



There's a couple of problems that arise:

__One:__ Even though Watson has a [profanity_filter parameter](https://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/speech-to-text/using.shtml#profanity_filter), which can be set to `false`, it apparently will still filter for `"fuck"` and `"bitch"` and even `"scrotum"` (as you can see in the uploaded YouTube clip). But not `"shit"`. 

__Two:__ 50 profanities is not very much for an entire episode of The Wire. In fact, in the [aforementioned investigative scene](https://www.youtube.com/watch?v=1lElf7D-An8), has [30+ "fucks" in the span of a few minutes](http://genius.com/The-wire-cursing-scene-annotated).


