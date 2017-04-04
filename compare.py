#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import os
import argparse
import time
import json
from collections import defaultdict
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

from speech2text import log_kv
from text2stats import IBM_TRANSCRIPT_STATS_FILENAME, GOOGLE_TRANSCRIPT_STATS_FILENAME
from text2stats import IBM_PROCESSED_STATS_FILENAME, GOOGLE_PROCESSED_STATS_FILENAME
from tally_audio import RESULT_FILENAME, time_string_to_decimal_minutes

GOOGLE_PATH = "google_stt/"
IBM_PATH = "ibm_stt/"
BASE_PATH = "/temp/stt/AudioJournals/"

"""
Run Dependencies:
- text2stats.py
- tally_audio.py


Compares IBM vs Google on the basis of the following summary stats :
- Number of transcripts generated
- Portion of IBM transcripts that have Google transcript, and vice versa.
- The transcription rate: ratio of number of transcripts to the number of audio files processed
- Transcript words per minute of audio
- Processing time (seconds) per minute of audio

Counts total number of audio files.

"""

def load_json(path):
    result = {}
    log_kv("Loading", path)
    if os.path.exists(path):
        with open(path) as file1:
            result = json.load(file1)
    else:
        logging.error("Not exist: %s", path)
    return result


def calc_transcript_counts(ibm_stats_path, google_stats_path):
    """
    :param ibm_stats_path: to file containing index of IBM transcripts
    :param google_stats_path: to file containing index of Google transcripts
    :return:
      Counts number of IBM transcripts
      Counts number of Google transcripts
      Counts portion of IBM transcripts within processed folders that have Google transcript
      Counts portion of Google transcripts within processed folders that have IBM transcript
    """
    ibm_stats = load_json(ibm_stats_path)
    google_stats = load_json(google_stats_path)
    log_kv("Number of IBM Transcripts", len(ibm_stats))
    log_kv("Numberof Google Transcripts", len(google_stats))
    i_set = set([os.path.dirname(x).replace(IBM_PATH,'').replace(BASE_PATH,'') for x in ibm_stats])
    g_set = set([os.path.dirname(x).replace(GOOGLE_PATH,'').replace(BASE_PATH,'') for x in google_stats])

    print
    i_top_level_folders = sorted(set([xx.split("/")[0] for xx in i_set]))
    print "IBM folders in %s :\n%s " % (ibm_stats_path, i_top_level_folders)
    print
    g_top_level_folders = sorted(set([xx.split("/")[0] for xx in g_set]))
    print "Google folders in %s :\n%s" % (google_stats_path, g_top_level_folders)

    i_count = 0
    i_in_g = 0
    for xx in i_set:
        if xx.split("/")[0] not in g_top_level_folders:
            continue
        i_count += 1
        if xx in g_set:
            i_in_g += 1
    i_portion = float(i_in_g) / i_count

    g_count = 0
    g_in_i = 0
    for xx in g_set:
        if xx.split("/")[0] not in i_top_level_folders:
            continue
        g_count += 1
        if xx in i_set:
            g_in_i += 1
    g_portion = float(g_in_i) / g_count

    print;print
    print "IBM also in Google: %d/%d  (%.2f) " % (i_in_g, i_count, i_portion)
    print "Google also in IBM: %d/%d  (%.2f) " % (g_in_i, g_count, g_portion)



def calc_stat_per_minute(stats, audio_stats, prefix, suffix, suffix2, fieldname,
                         out_fieldname=None, duration_threshold = (3.0/60)):
    """

    :param stats: dict containing field "stat"
    :param audio_stats: dict containing field "duration"
    :param prefix: string to be stripped from each key of stats
    :param suffix: string to be stripped from each key of stats
    :param suffix2: string to be stripped from each key of stats
    :param duration_threshold: minimum minutes of audio duration required to admit item into sample.
    :return: dict
    """
    if not out_fieldname:
        out_fieldname = fieldname + "_per_minute"
    word_count_stats = defaultdict(dict)
    no_duration = 0
    count = 0
    skipped = 0
    sum_stat = 0
    sum_duration = 0
    for transcript in stats:
        count += 1
        # Strip down to filepath
        basepath = transcript.replace(prefix, '').replace(suffix,'').replace(suffix2,'')
        if basepath in audio_stats:
            stat = stats[transcript].get(fieldname)
            duration = time_string_to_decimal_minutes(audio_stats[basepath]["duration"])
            if duration and stat and duration > duration_threshold:
                stat_per_minute = float(stat)/duration
                word_count_stats[basepath][out_fieldname] = stat_per_minute
                sum_stat += stat
                sum_duration += duration
                logging.debug("%.0f %s/minute", stat_per_minute, fieldname)
            else:
                skipped += 1
                no_duration += 0 if duration else 1
    print
    if sum_duration > 0:
        logging.info("Average %s per minute: %.1f", fieldname, (sum_stat/sum_duration))
    else:
        logging.error("Expected sum duration > 0")
    if skipped > 0:
        logging.warn("Skipped %d", skipped)
    if no_duration > 0:
        logging.warn("Had no duration: %d", no_duration)
    return word_count_stats


def calc_transcript_words_per_minute(ibm_stats_path, google_stats_path, ibm_pstats_path, google_pstats_path, audio_stats_path):

    ibm_stats = load_json(ibm_stats_path)
    google_stats = load_json(google_stats_path)
    ibm_pstats = load_json(ibm_pstats_path)
    google_pstats = load_json(google_pstats_path)
    audio_stats = load_json(audio_stats_path)

    count_processed_ibm = len(ibm_pstats)
    count_processed_google = len(google_pstats)
    count_transcribed_ibm = len(ibm_stats)
    count_transcribed_google = len(google_stats)
    print
    if count_processed_ibm < count_transcribed_ibm :
        logging.error("count_processed_ibm < count_transcribed_ibm")
    log_kv("IBM Transcribed/Processed", "%d/%d" % (count_transcribed_ibm, count_processed_ibm))
    if count_processed_google < count_transcribed_google:
        logging.error("count_processed_google < count_transcribed_google")
    log_kv("Google Transcribed/Processed", "%d/%d" % (count_transcribed_google, count_processed_google))
    print
    log_kv("Num audio files", len(audio_stats))
    print
    print "==============================================================="
    print "Calculating number of IBM transcript words per minute of audio"
    print "==============================================================="
    suffix = ".out/hypotheses.txt.dictated"
    suffix2 = ".out/hypotheses.txt"
    prefix = "ibm_stt/"
    i_words_per_min = calc_stat_per_minute(ibm_stats, audio_stats, prefix, suffix, suffix2, "word_count")
    print "==============================================================="
    print "IBM wpm tallied: %d" % len(i_words_per_min)
    print "==============================================================="
    print
    print "==============================================================="
    print "Calculating IBM processing time per minute of audio"
    print "==============================================================="
    i_proc_per_min = calc_stat_per_minute(ibm_pstats, audio_stats, prefix, suffix, suffix2, "transcribe_seconds")
    print "==============================================================="
    print "IBM ppm tallied: %d" % len(i_proc_per_min)
    print "==============================================================="
    print
    print "==============================================================="
    print "Calculating number of Google transcript words per minute of audio"
    print "==============================================================="
    suffix = ".out/transcript.txt.dictated"
    suffix2 = ".out/transcript.txt"
    prefix = "google_stt/"
    g_words_per_min = calc_stat_per_minute(google_stats, audio_stats, prefix, suffix, suffix2, "word_count")
    print "==============================================================="
    print "Google wpm tallied: %d" % len(g_words_per_min)
    print "==============================================================="
    print
    print "==============================================================="
    print "Calculating Google processing time per minute of audio"
    print "==============================================================="
    i_proc_per_min = calc_stat_per_minute(google_pstats, audio_stats, prefix, suffix, suffix2, "transcribe_seconds")
    print "==============================================================="
    print "Google ppm tallied: %d" % len(i_proc_per_min)
    print "==============================================================="
    print



    print


if __name__ == '__main__':

    start_time = time.time()
    parser = argparse.ArgumentParser(description='Compare Google STT vs IBM STT')
    parser.add_argument('--folder','-f', action='store', default='/tmp/transcription/text2stats', help='text2stats.py output directory')
    parser.add_argument('--verbose','-v', action='store_true', help='Spew logs profusely.')
    args = parser.parse_args()

    if args.verbose:
        print "Relies on the following intermediate result files under %s :" % args.folder
        print ", ".join([IBM_TRANSCRIPT_STATS_FILENAME, GOOGLE_TRANSCRIPT_STATS_FILENAME, IBM_PROCESSED_STATS_FILENAME,
                         GOOGLE_PROCESSED_STATS_FILENAME, RESULT_FILENAME])

    log_kv("Running", __file__)
    log_kv("From", os.path.dirname(os.path.realpath(__file__)))
    folder = args.folder
    log_kv("--folder", folder)
    path = os.path.realpath(folder)

    if not os.path.isdir(path):
        raise IOError("Path not found: %s" % path)


    ibm_stats_path = os.path.join(path, IBM_TRANSCRIPT_STATS_FILENAME)
    google_stats_path = os.path.join(path, GOOGLE_TRANSCRIPT_STATS_FILENAME)
    ibm_pstats_path = os.path.join(path, IBM_PROCESSED_STATS_FILENAME)
    google_pstats_path = os.path.join(path, GOOGLE_PROCESSED_STATS_FILENAME)
    audio_stats_path = os.path.join(path, RESULT_FILENAME)

    calc_transcript_counts(ibm_stats_path, google_stats_path)
    calc_transcript_words_per_minute(ibm_stats_path, google_stats_path, ibm_pstats_path, google_pstats_path, audio_stats_path)


    log_kv("Done", __file__)
    print("(%.2f sec)" % (time.time() - start_time))


# python compare.py -f /tmp/transcription/text2stats
