"""
TODO docs

High-level commands to execute tasks
"""

from foo.project_settings import *
from foo.audio_video import *
from foo.watson import *
from multiprocessing import Process
from os.path import exists


def init_project(video_filename):
    # creates a project directory and a copy of the file
    # returns the project slug
    project_slug = init_project_from_video_file(video_filename)
    return project_slug


def split_audio(project_slug):
    # extracts audio from existing video file
    # creates segments
    # yields filenames of segments
    vid_path = full_video_path(project_slug)
    audio_path = full_audio_path(project_slug)
    extract_audio_file(vid_path, audio_path)

    # segments the audio (via a generator)
    segments = segment_audio_file(audio_path, audio_segments_dir(project_slug))
    for seg_filename in segments:
        yield seg_filename

def transcribe_audio(project_slug, creds, overwrite=False):
    # Send each audio segment in a project to Watson Speech-to-Text API
    # with the POWER OF MULTITHREADED PRPOCESSINGASDF!!
    #
    # returns nothing...just prints to screen
    audio_segments_fnames = audio_segments_filenames(project_slug)
    watson_jobs = []
    for audio_fn in audio_segments_fnames:
        time_slug = make_slug_from_path(audio_fn)
        transcript_fn = join(transcripts_dir(project_slug), time_slug) + '.json'
        if not exists(transcript_fn):
            print("Sending to Watson API:\n\t", audio_fn)
            job = Process(target=process_transcript_call,
                          args=(audio_fn, transcript_fn, creds))
            job.start()
            watson_jobs.append(job)


    # Wait for all jobs to end
    for job in watson_jobs:
        job.join()


def compile_transcripts(project_slug):
    pass

def supercut(project_slug, regex_pattern):
    pass





def process_transcript_call(audio_filename, transcript_path, creds):
    resp = speech_to_text_api_call(
        audio_filename,
        username=creds['username'],
        password=creds['password'])
    with open(transcript_path, 'w') as t:
        t.write(resp.text)
        print("Transcribed:\n\t", transcript_path)
