from foo.project_settings import *
from foo.audio_video import *
from foo.watson import *
from multiprocessing import Process
import sys
CREDS = get_watson_creds()


def process_transcript_callback(audio_filename, transcript_path):
    resp = speech_to_text_api_call(
        audio_filename,
        username=CREDS['username'],
        password=CREDS['password'])
    with open(transcript_path, 'w') as t:
        t.write(resp.text)
        print("Transcribed:\n\t", transcript_path)


if __name__ == '__main__':
    filepath = sys.argv[1].strip()
    print(filepath)

    # creates a project directory and a copy of the file
    pslug = init_project_from_video_file(filepath)

    # extracts the audio
    audio_fname = extract_audio_file(full_video_path(pslug), full_audio_path(pslug))

    # segments the audio (via a generator)
    audio_segments_fnames = segment_audio_file(audio_fname, audio_segments_dir(pslug))

    # Send each audio segment to Watson Speech-to-Text API
    # with the POWER OF MULTITHREADED PRPOCESSINGASDF!!
    watson_jobs = []
    for audio_fn in audio_segments_fnames:
        print("Sending to Watson API:\n\t", audio_fn)
        time_slug = make_slug_from_path(audio_fn)
        transcript_fn = join(transcripts_dir(pslug), time_slug) + '.json'
        job = Process(target=process_transcript_callback,
                    args=(audio_fn,transcript_fn))
        job.start()
        watson_jobs.append(job)


    # Wait for all jobs to end
    for job in watson_jobs:
        job.join()


