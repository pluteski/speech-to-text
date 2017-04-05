#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import os
import fnmatch
import argparse
import time
import shutil
import json
import logging
import sys
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
from speech2text import log_kv

"""
What it does:

Counts number of :
- transcripts (including dictated as well as raw)
- dictated transcripts
- unique transcripts
- transcripts that were already analyzed previously

Calculates average word count and average character count

Estimates transcription processing time

"""

IBM_TRANSCRIPT_STATS_FILENAME = "file_stats.json" # transcript stats for ibm
GOOGLE_TRANSCRIPT_STATS_FILENAME = "gfile_stats.json" # transcript stats for google
IBM_PROCESSED_STATS_FILENAME = "processed.json" # transcribe time for ibm
GOOGLE_PROCESSED_STATS_FILENAME = "gprocessed.json" # transcribe time for google
TRANSCRIPTION_FILENAMES = ['hypotheses.txt','hypotheses.txt.dictated']
GOOGLE_TRANSCRIPTION_FILENAMES = ['transcript.txt','transcript.txt.dictated']
PROCESSED_FILENAME = "sttclient.log"

def get_uniques(filename, set_, pref='.dictated'):
    """
    Add unique X.txt or X.txt.dictated,
    where X = 'transcript' if args.google else 'hypotheses'

    Note:
    .txt.dictated trumps .txt
    """
    if filename+pref in set_:
        pass
    elif filename.endswith(pref): # incoming is trump card
        stripped = (''.join(filename.rsplit(pref, 1)))
        if stripped in set_:
            set_.discard(stripped)
            set_.add(filename)
    else:
        set_.add(filename)
    return set_


    if filename in set:
        for ff in allowed:
            if filename.endswith(ff):
                ''.join(filename.rsplit(ff, 1))
    for ff in allowed:
        if filename.endswith(ff):
            return ''.join(filename.rsplit(ff, 1))
    return filename


def calc_transcription_counts(filepath, basepath, args):
    word_count = 0
    char_count = 0
    subpath = filepath.replace(basepath, '')
    if args.verbose:
        print 75 * "=", "\n", subpath, "\n", 75 * "="
    if os.path.isfile(filepath):
        with open(filepath, 'r') as myfile:
            hypotheses_data = myfile.read()
            if hypotheses_data :
                word_count = len(hypotheses_data.split())
                char_count = len(hypotheses_data)
    else:
        logging.error("Not a file: %s", filepath)
    return word_count, char_count


def walk_logs(folder, basepath, match="sttclient.log"):
    """
    Locates files within a folder matching pattern.
    Returns a list of 2-tuples each containing a filepath of a file matching one of specified types,
    and a path relative to the basepath.
    :param folder:
    :param basepath: is stripped off the prefix of each filepath.
    :param ext: appends to each logpath in result
    :param types: accepted file types
    :return: list of 2-tuples: (filepath, logpath)
    """
    matches = []
    result = []
    for root, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            if filename == match:
               matches.append(os.path.join(root, filename))
    if matches:
        for filename in matches:
            filepath = os.path.realpath(filename)
            relpath = ((os.path.realpath(filename)).replace(basepath, '')).lstrip('/')
            result.append((filepath, relpath,))
    return result


def process_transcript_stats(inpath, basepath, outpath, args):

    file_stats_path = os.path.join(outpath, IBM_TRANSCRIPT_STATS_FILENAME)
    if args.google:
        file_stats_path = os.path.join(outpath, GOOGLE_TRANSCRIPT_STATS_FILENAME)

    log_kv("file stats", file_stats_path)
    previous_results = {}
    result_dict={}
    if os.path.exists(file_stats_path):
        log_kv("Loading file", file_stats_path)
        with open(file_stats_path) as file1:
            previous_results = json.load(file1)
            log_kv("Count(previous)", len(previous_results))
            for xx in previous_results:
                result_dict[xx] = previous_results[xx]

    print
    print 105 * "="
    print
    num_processed = 0
    num_skipped = 0
    num_done = 0

    # Gets list of transcript filepaths
    file_list = walk_files(folder=inpath+"/", basepath=basepath)
    uniques = set()
    for x,y in file_list:
        uniques = get_uniques(x,uniques)
    log_kv("Number Transcriptions", len(file_list))
    log_kv("Unique Transcriptions", len(uniques))
    print
    print 105 * "="
    print
    num_dictated = 0
    sum_word_count = 0
    sum_char_count = 0
    for uu in uniques:
        id = uu.replace(basepath, '').lstrip("/")
        if args.max and num_processed >= args.max:
            log_kv("Max met", args.max)
            break
        num_dictated += 1 if uu.endswith(".dictated") else 0
        num_processed += 1
        if id in previous_results:
            num_skipped += 1
            logging.debug("Skipping %s", uu)
            if result_dict[id] != previous_results[id] :
                logging.error("Mismatch")
                raise Exception('Expected %s , but encountered %s', result_dict[id], previous_results[id])
            sum_word_count += result_dict[id]["word_count"]
            sum_char_count += result_dict[id]["char_count"]
        else:
            num_done += 1
            logging.debug("Doing %s", uu)
            word_count, char_count = calc_transcription_counts(uu, basepath, args)
            sum_word_count += word_count
            sum_char_count += char_count
            result_dict[id] = {"word_count": word_count, "char_count": char_count}

    log_kv("Previous", len(previous_results))
    log_kv("Processed", num_processed)
    log_kv("Dictated", num_dictated)
    log_kv("Done", num_done)
    log_kv("Skipped", num_skipped)
    log_kv("Result count", len(result_dict))

    print
    running_avg_word_count = (float(sum_word_count) / len(result_dict))
    running_avg_char_count = (float(sum_char_count) / len(result_dict))
    log_kv("Avg Word count", "%.1f" % running_avg_word_count)
    log_kv("Avg Char count", "%.1f" % running_avg_char_count)

    log_kv("Writing", file_stats_path)
    with open(file_stats_path, 'w') as outfile:
        json.dump(result_dict, outfile, indent=2)


def analyze_transcribe_time(inpath, basepath, outpath, ext=".out", logname="sttclient.log"):
    result = {}
    if args.google:
        processed_filepath = os.path.join(outpath, GOOGLE_PROCESSED_STATS_FILENAME)
    else:
        processed_filepath = os.path.join(outpath, IBM_PROCESSED_STATS_FILENAME)
    if os.path.isfile(processed_filepath):
        with open(processed_filepath) as file1:
            loaded = json.load(file1)
            log_kv("Loaded", processed_filepath)
            if loaded and type(loaded) is dict:
                result = loaded
            log_kv("Count(previous)", len(result))
    logs = walk_logs(inpath, basepath, logname)
    cumulative_time = 0.0
    count = 0
    prev = 0
    skipped = 0
    total = 0
    for xx, yy in logs:
        total += 1
        # The actual key used to store the result.
        # If basepath==inpath, then keys in google result match keys in ibm result for easier cross-reference.
        # If basepath<inpath, then keys in google and ibm results retain their distinction for easier merge and safety
        id = yy.replace((ext + "/" + logname), '')
        if args.keep and id in result:
            prev += 1
            count += 1
            cumulative_time += result[id]["transcribe_seconds"]
            continue
        unixmtime = os.path.getmtime(xx)
        birthtime = os.stat(xx).st_birthtime
        diff = unixmtime - birthtime
        if unixmtime:
            if id not in result:
                result[id] = {"unixmtime": unixmtime}
            else:
                result[id]["unixmtime"] = unixmtime

        if diff > 3600 or diff < 10:
            logging.warn("Skipped transcription time: %s", id)
            skipped += 1
            continue
        else:
            cumulative_time += diff
            count += 1
            if id not in result:
                result[id] = {"transcribe_seconds": diff}
            else:
                result[id]["transcribe_seconds"] = diff

    log_kv("Skipped", skipped)
    log_kv("Result size", len(result))
    if result:
        if DRYRUN:
            log_kv("Warning", "Dry run only")
        else:
            log_kv("Writing", processed_filepath)
            with open(processed_filepath, 'w') as outfile:
                json.dump(result, outfile, indent=2)
    print "\n\n"
    print "Transcription Processing Time (estimated) \n"
    if skipped:
        print "Previous: %d  Skipped: %d   Total: %d" % (prev, skipped, total)
    print "Count:    %s  Avg transcribe time: %.2f minutes" % (count, float(cumulative_time)/60.0/count if count else 0)
    print


def list_walk(folder=u'.'):
    """
    traverse root directory, and list directories as dirs and files as files.
    """
    for root_dir, sub_dirs, files in os.walk(folder):
        path = root_dir.split('/')
        if os.path.basename(root_dir) in ['.', '.DS_Store']:
            continue
        print (len(path) - 1) * '    ', os.path.basename(root_dir)+"/"
        for file in files:
            try:
                print len(path) * '    ', file
            except Exception as e:
                logging.error("%s : bad filename: %s",e,file)
                raise
            if args.clean:
                try:
                    filepath = os.path.join(root_dir,file)
                    if not os.path.isfile(filepath) and not os.path.isdir(filepath):
                        logging.warn("Possible corrupted file: %s", filepath)
                        if raw_input("Confirm remove: (y/n) ?: ") in ["Y","y"]:
                            full_path = os.path.join(os.getcwd(), root_dir.strip(".").strip("/"),file)
                            logging.warn("Removing: %s", full_path)
                            os.remove(full_path)
                            logging.info("Removed: %s", file)
                except Exception as e:
                    logging.error("%s : bad filename: %s", e, file)
                    raise


def walk_files(folder=u'.', basepath='./'):
    """
    Locates transcripts within a folder.
    Returns a list of 2-tuples containing the file's full path,
    and a path relative to the basepath.

    :param folder:
    :param basepath: is stripped off the prefix of each filepath.
    :return: list of 2-tuples: (filepath, logpath)
    """
    matches = []
    result = []
    for root, dirnames, filenames in os.walk(folder):
        if not filenames:
            continue
        fmatch = []
        if args.google:
            for name in GOOGLE_TRANSCRIPTION_FILENAMES:
                fmatch += fnmatch.filter(filenames, name)
        else:
            for name in TRANSCRIPTION_FILENAMES:
                fmatch += fnmatch.filter(filenames, name)
        for filename in fmatch:
           matches.append(os.path.join(root, filename))
    if matches:
        for filename in matches:
            filepath = os.path.realpath(filename)
            outdir = ((os.path.realpath(filename)).replace(basepath, '')+".out").lstrip('/')
            result.append((filepath, outdir,))
    return result

def make_dir(directory):
    if not os.path.exists(directory):
        print "Creating directory: ", directory
        os.makedirs(directory)


DRYRUN = False # Runs without overwriting any previous results, safer than --keep
if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser(description='Tally stats from transcripts')
    parser.add_argument('--infolder','-i', action='store', default='.', help='folder containing audio files')
    parser.add_argument('--outfolder','-o', action='store', default='./output', help='output directory')
    parser.add_argument('--basefolder','-b', action='store', help='base directory containing all')
    parser.add_argument('--verbose','-v', action='store_true', help='Spew logs profusely.')
    parser.add_argument('--clean','-c', action='store_true', help='Clean munged data.')
    parser.add_argument('--max','-m', action='store', type=int, help='Quit after processing this many.')
    parser.add_argument('--keep','-k', action='store_true',
                        help='Do not overwrite previously converted audio files, or results folder already containing hypotheses.txt.')
    parser.add_argument('--google','-g', action='store_true', help='Analyze Google transcripts instead of IBM Watson.')
    args = parser.parse_args()

    if not args.basefolder:
        args.basefolder = args.infolder

    log_kv("Running", __file__)
    log_kv("From", os.path.dirname(os.path.realpath(__file__)))
    print

    inpath = os.path.realpath(args.infolder if args.infolder else os.getcwd())
    log_kv("inpath", inpath)

    basepath = os.path.realpath(args.basefolder if args.basefolder else u'/')
    log_kv("basepath", basepath)

    if inpath.startswith(basepath):
        if inpath == basepath:
            logging.warn("inpath == basepath.  Are you sure?  [Y/n]")
            choice = raw_input().lower()
            if choice not in set(['yes','y']):
                logging.info("Quitting")
                sys.exit(1)
    else:
        logging.error("Expected basepath (%s) to be prefix for inpath (%s)", basepath, inpath)
        sys.exit(1)

    outpath = os.path.realpath(args.outfolder if args.outfolder else u'.output')
    log_kv("outpath", outpath)
    make_dir(outpath)

    analyze_transcribe_time(inpath, basepath, outpath, ext=".out", logname="sttclient.log")
    if DRYRUN:
        log_kv("Dry run", "skipping main processing step")
    else:
        log_kv("Processing transcripts. Output:", outpath)
        process_transcript_stats(inpath, basepath, outpath, args)

    log_kv("Done:              ", __file__)
    print("(%.1f min)" % ((time.time() - start_time) / 60.0))



"""
Tested filepaths supported by command options.

--infolder

    "/Volumes/Samsung USB/AudioJournals/ibm_stt/ICD-BP100 2003/"
    'ibm_stt/ICD-BP100 2005'
    "AudioJournal/ibm_stt/ICD-BP100 2005"
    AudioJournal/ibm_stt/2006/2006\ MP3/Family\ Journal


--basefolder

    /Volumes/Samsung\ USB/AudioJournals/ibm_stt
    /AudioJournal
    /Users/mark/temp/transcription/
    ~/temp/transcription/


--outfolder

    /Volumes/Samsung\ USB/AudioJournals/ibm_stt
    /tmp/transcription/stt_stats/

"""
