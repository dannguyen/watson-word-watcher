# Trump Steaks commercial 

The Watson Speech to Text API does pretty well on the 90-second Trump Steaks commercial, [which can be viewed here on YouTube](https://www.youtube.com/watch?v=LyONt_ZH_aw). 

<a href="https://www.youtube.com/watch?v=LyONt_ZH_aw"><img src="https://i.ytimg.com/vi/LyONt_ZH_aw/hqdefault.jpg" alt="youtube still"></a>

Trump enunciates all of his words clearly, and Watson even is able to accurately disambiguate the homophone in the first phrase by recognizing the idiom:

> when it comes to great __steaks__ I just raise the __stakes__

At a quick glance, the transcription seems almost perfect. However, it doesn't quite get all the _steaks_:

> it's the best of the best until now you can only enjoy __stakes__ of this quality in one of my resort restaurants or America's finest __steak__ houses

Check out the [projects/trump-steaks](projects/trump-steaks) folder for the data files, including:

- [Full JSON response from Watson Speech-to-Text](projects/trump-steaks/full-transcript.json)
- [Word level transcription as CSV](projects/trump-steaks/words-transcripts.csv)


Here's the raw text of Watson's transcribed output:

> when it comes to great steaks I just raise the stakes the sharper image is one of my favorite stores with fantastic products of all kinds that's why I'm thrilled they agree with me trump steaks are the world's greatest steaks and I mean that in every sense of the word and the sharper image is the only store where you can buy them
>
> trump steaks are by far the best tasting most flavorful beef you've ever had truly in a league of their own
>
> trump steaks are five star gourmet quality that belong in a very very select category of restaurant and are certified Angus beef prime there's nothing better than that
>
> of all of the beef produced in America less than one percent qualifies for that category
> 
> it's the best of the best until now you can only enjoy stakes of this quality in one of my resort restaurants or America's finest steak houses
> 
> but now that's changed today through the sharper image you can enjoy the world's greatest stakes in your own home with family friends anytime
>
> trump steaks are aged to perfection to provide the ultimate in tenderness and flavor
> 
> if you like your steak you'll absolutely love trump steaks
>
> treat yourself to the very very best life has to offer and is a gift trump steaks are the best you can give one bite and you'll know exactly what I'm talking about and believe me I understand stakes
>
> it's my favorite food and these are the best

