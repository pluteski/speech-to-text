# Introduction

by Mark Plutowski

I wrote this code to utilize the speech-to-text cloud APIs provided by
IBM and Google.  This is not intended for commercial use, I don't
expect to use it for commercial gain myself, frankly I don't see a
business opportunity here for myself although the reader is welcome to
apply this code to that aim under the MIT license.

I hope that other individuals or nonprofit organizations who have a similar
need will find this code useful, and that this use will encourage the
cloud API providers to improve their support for my use case.

## Background

I have accumulated many audio files containing spoken word audio.
This audio contains valuable data for me and my family, including
family journals, recordings of talks I've given,
dictation of stories I've written, health and fitness data.
The story behind the data and how I came to accumulate it is too long
to address here; however suffice it to say that there is enough of it
that it became too unwieldy to utilize in its audio form.
I needed to transcribe it to make it accessible. Over the years I
tried various speech-to-text transcription software.
I was able to successfully transcribe a small portion of it
using Dragon Naturally Speaking, and another small portion using the
speech-to-text capability built into Mac OS. However, neither of these
was suited to my task.  Neither one provided a means of processing
batches of audio files.  However in 2016 both IBM and Google made their
cloud APIs available at compelling price points.  Furthermore, each
one provided a generous allowance of free processing.  Also, each one
also offered an attractive trial period that offered an even more
generous allowance of unlimited free processing time.
This prompted me to consider each one.

It turned out that using each one wasn't exactly trivial.
While the cloud offerings provide the key functionality lacking by
commercial off-the-shelf (COTS) software, utilizing it also requires
some coding effort.
However, given the amount of data I've accumulated
the price point and accuracy of results reached the point
where this coding effort became worthwhile.

## What does it do?
This code locates the audio files that are contained in a folder and
submits them to a cloud api, and collects the output into another
folder.  The output consists of the transcribed text, as well as
other associated log data.

## Who might find this useful?
This is suitable for DIY users who have up to thousands of
audio files. I have tested it on thousands of my own files.

The cloud APIs I used are not yet suitable for transcribing
continuous speech collected using a mobile audio recorder especially
where there is substantial background noise.
Even audio that is obtained using a good microphone in a quiet
environment poses a difficult challenge. Transcribing
meeting minutes would still require a substantial amount of additional
processing. Furthermore, neither of these offerings can as yet
handle dictation as well as COTS software.  This means that to
obtain an accurate transcript would require not only correcting
the transcription errors, but inserting the punctuation even where
that is provided by dictation.  Furthermore, the ability to handle
dates and entity names is not (yet) as good as COTS software.

However, while the current accuracy limits the utility, I find it to be
adequate for indexing my audio files and rudimentary text analysis.


## What do I hope to gain by contributing this code?
These cloud APIs are evolving rapidly. I fully expect them to
improve to be able to handle low bitrate recordings and background
noise.  However, as a software developer myself I also expect these
cloud providers to adapt their product towards their best users.

## References
https://www.wired.com/2016/04/long-form-voice-transcription/
- claims current error rate is 4% to 12%.  The error rate is
 substantially higher on my audio, ranging from 15% to 100%.


