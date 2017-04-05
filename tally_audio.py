#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import os
import re
import argparse
import datetime
import time
import json
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
import subprocess
from collections import defaultdict
from speech2text import log_kv, walk_files, get_extension, make_dir

"""
What it does:

Tallies following information for each audio file and stores to file :
- create day of week
- creation date
- file extension
- duration (minutes)
- bitrate
- audio_type
- path relative to a base path

"""

DEFAULT_BASE_PATH = "/Volumes/AUDIOJ/AudioJournals/"
RESULT_FILENAME = "audio_stats.txt"
TSV_FILENAME = "audio_table.tsv"

def load_json(path):
    result = {}
    log_kv("Loading", path)
    if os.path.exists(path):
        with open(path) as file1:
            result = json.load(file1)
    else:
        logging.error("Not exist: %s", path)
    return result


def get_audio_metadata(filepath):
    result = {}
    result["extension"] = get_extension(filepath)
    pipe = subprocess.Popen(['ffmpeg', "-i", filepath],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pipe.stdout.readline()
    pipe.terminate()
    audio_info = pipe.stderr.read()
    duration_bitrate = audio_info.split("Duration: ")
    if duration_bitrate and len(duration_bitrate)>1:
        duration_bitrate = duration_bitrate[1]
        duration = duration_bitrate.split(",")
        duration = duration[0].strip() if duration and type(duration) is list and len(duration) > 0 else None
        result["duration"] = duration
        bitrate = duration_bitrate.split("bitrate: ")
        bitrate = bitrate[1] if bitrate and type(bitrate) is list and len(bitrate) > 1 else None
        bitrate = bitrate.split("\n")
        bitrate = bitrate[0].strip() if bitrate and type(bitrate) is list and len(bitrate) > 0 else None
        result["bitrate"] = bitrate
        audio = duration_bitrate.split("Audio: ")
        audio = audio[1] if audio and type(audio) is list and len(audio) > 1 else None
        audio = audio.split("\n")
        audio = audio[0] if audio and type(audio) is list and len(audio) > 0 else None
        result["audio"] = audio.strip()
    return result

def load_json_file(filepath):
    results = defaultdict(dict)
    if os.path.isfile(filepath):
        with open(filepath) as fp:
            try:
                loaded = json.load(fp)
                if type(loaded) is not dict and type(loaded) is not defaultdict:
                    logging.error("Expected a dict, got : %s", type(loaded))
                elif loaded:
                    results = loaded
            except:
                pass
    return results


def get_short_format(format_string):
    result = ''
    if format_string:
        if format_string.startswith('mp3'):
            result = 'mp3'
        elif format_string.startswith('pcm_s16le'):
            result = 'pcm_s16le'
        elif format_string.startswith('pcm_u8'):
            result = 'pcm_u8'
        elif format_string.startswith('aac') and 'mp4a' in format_string:
            result = 'mp4a'
        elif format_string.startswith('adpcm_ms'):
            result = 'adpcm_ms'
        else:
            logging.warn("Unsupported short format: %s", format_string)
    return result

def get_bitrate_int(bitrate_string):
    result = ''
    try:
        if 'kb/s' in bitrate_string:
            result = int(bitrate_string.split(" ")[0])
        else:
            logging.warn("bitrate string missing kb/s: %s", bitrate_string)
    except Exception as e:
        logging.error("%s: %s", e, bitrate_string)
    return str(result)

def get_duration_min(duration_string):
    result = ''
    minutes = time_string_to_decimal_minutes(duration_string)
    if minutes:
        result = '%.6f' % minutes
    else:
        logging.warn("Expected time string, encountered: %s", duration_string)
    return result



def time_string_to_decimal_minutes(time_string):
    minutes = None
    try:
        fields = time_string.split(":")
        hours = fields[0] if len(fields) > 0 else 0.0
        minutes = fields[1] if len(fields) > 1 else 0.0
        seconds = fields[2] if len(fields) > 2 else 0.0
        minutes = (int(hours) * 60.0) + float(int(minutes)) + (float(seconds) / 60.0)
        if minutes <= 0.01:
            logging.warn("Short duration: %.3f minutes. Time string: %s", minutes, time_string)
    except Exception as e:
        logging.error("time_string_to_decimal_minutes : %s : while converting time string: %s", time_string, e)
    return minutes

def get_audio_filename_date(filename):
    re1 = re.compile('2\d{3}[_/]\d{2}[_/]\d{2}')
    re2 = re.compile('2\d{3}[\./][01]\d[\./][0123]\d')
    re3 = re.compile('2\d{3}\d{2}\d{2} \d{6}')
    re4a = re.compile('2\d{3}[-/]\w{3}[-/]\d{2} \d{2}[-/]\d{2}[-/]\d{2}')
    re4b = re.compile('2\d{3}[-/]\d{2}[-/]\d{2} \d{2}[-/]\d{2}[-/]\d{2}')
    re4c = re.compile(' \w{3} \d{2} 2\d{3}')
    re5 = re.compile('_\d{2}[01]\d[0123]\d_\d{6}')
    re6 = re.compile('2\d{3}[-/]\d{2}[-/]\d{2}')
    re7 = re.compile('2\d{3}[-/]\w{3}[-/]\d{2}')
    re9 = re.compile('2\d{3}[01]\d[0123]\d')
    reY = re.compile('2\d{3}')

    patterns = [(re1, '%Y_%m_%d'),
                (re2, '%Y.%m.%d'),
                (re3, '%Y%m%d %H%M%S'),
                (re4a,'%Y-%b-%d %H-%M-%S'),
                (re4b, '%Y-%m-%d %H-%M-%S'),
                (re4c, ' %b %d %Y'),
                (re5, '_%y%m%d_%H%M%S'),
                (re6, '%Y-%m-%d'),
                (re7, '%Y-%b-%d'),
                (re9, '%Y%m%d'),
                (reY, None)]

    result = ''
    date_ = None
    filename_noext = os.path.splitext(filename)[0]
    if filename_noext:
        for regex, pattern in patterns:
            match = regex.findall(filename_noext)
            if match:
                if pattern:
                    date_ = datetime.datetime.strptime(match[0], pattern)
                    break
                else:
                    logging.warn("Encountered year but could not extract full date: %s", filename_noext)
                    break
    if date_:
        result = date_.isoformat()
    return result

def dump_to_tsv(path, results):
    logging.info("")
    logging.info("Writing tsv data..")
    logging.info("")
    count_warnings = 0
    rows = []
    for key in results:
        row = results[key]
        filename = os.path.basename(key)
        folder = os.path.dirname(key)
        format = row['audio'] if 'audio' in row else ''
        short_format = get_short_format(format) if format else ''
        extension = row['extension'] if 'extension' in row else ''
        bitrate_string = row['bitrate']
        bitrate_int = get_bitrate_int(row['bitrate'])
        duration = row['duration'] if 'duration' in row else ''
        duration_min = get_duration_min(duration) if duration else ''
        if not duration_min:
            logging.warn("No duration for audio file: %s", key)
            count_warnings += 1
        size_mb = str(row['size_mb']) if 'size_mb' in row else ''
        unixmtime = str(row['unixmtime']) if 'unixmtime' in row else ''
        localtime = str(row['localtime']) if 'localtime' in row else ''
        audio_filename_date = get_audio_filename_date(filename)
        now = datetime.datetime.now().isoformat()
        tsv_string = '"%s"\t"%s"\t"%s"\t"%s"\t%s\t%s\t"%s"\t%s\t"%s"\t%s\t%s\t%s\t%s\t%s\t%s' % \
                     (key,filename,folder,format,short_format,extension,bitrate_string,bitrate_int,
                      duration,duration_min,size_mb,unixmtime,localtime,audio_filename_date,now)
        rows.append(tsv_string)

    logging.warn("Number of warnings: %d", count_warnings)

    logging.info("Writing table data to %s", TSV_FILENAME)
    with open(path, 'w') as fp:
        fp.write('path\tfilename\tfolder\tformat\tshort_format\textension\tbitrate_string\tbitrate_int\tduration\tduration_min\tsize_mb\tunixmtime\tlocaltime\taudio_filename_date\tetl_date')
        fp.write("\n")
        for line in rows:
            fp.write(line)
            fp.write("\n")
    logging.info("")


if __name__ == '__main__':

    start_time = time.time()

    parser = argparse.ArgumentParser(description='Tally audio file specs')
    parser.add_argument('--infolder','-i', action='store', default='.', help='folder containing audio files')
    parser.add_argument('--basefolder','-b', action='store', default=DEFAULT_BASE_PATH, help='base directory')
    parser.add_argument('--outfolder','-o', action='store', default='/tmp/transcription/text2stats_dev', help='output directory')
    parser.add_argument('--verbose','-v', action='store_true', help='Spew logs profusely.')
    parser.add_argument('--keep','-k', action='store_true', help='Do not reprocess files already in previous result.')
    args = parser.parse_args()

    log_kv("Running", __file__)
    log_kv("From", os.path.dirname(os.path.realpath(__file__)))
    log_kv("--infolder", args.infolder)
    inpath = os.path.realpath(os.path.expanduser(args.infolder))
    inpath = inpath if inpath.endswith("/") else inpath+"/"
    log_kv("inpath", inpath)
    log_kv("--outfolder", args.outfolder)
    outpath = os.path.realpath(os.path.expanduser(args.outfolder))
    log_kv("outpath", outpath)
    log_kv("--basefolder", args.basefolder)
    basepath = os.path.realpath(os.path.expanduser(args.basefolder))
    log_kv("basepath", basepath)

    result_filepath = os.path.join(outpath, RESULT_FILENAME)
    log_kv('result_filepath', result_filepath)
    make_dir(outpath)

    logging.info("Loading previous audio stats file: %s", result_filepath)
    results = load_json_file(result_filepath)
    log_kv("Count(loaded)", len(results))

    logging.info("Searching for audio files")
    audio_files = walk_files(inpath, basepath, ext='')
    log_kv("Count(audio files)", len(audio_files))

    anydone = False
    if args.verbose:
        logging.info("day   date                  ext     duration  bitrate    audio_type  relative_path")
        logging.info("")

    for fullpath, relative_path  in audio_files:
        if args.keep and relative_path in results and results.get('size_mb'):
            continue

        if relative_path not in results:
            results[relative_path] = {}

        results[relative_path]['size_mb'] = os.path.getsize(fullpath)

        if args.keep and relative_path not in results:
            unixmtime = os.path.getmtime(fullpath)
            localtime_readable = time.ctime(unixmtime)
            localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unixmtime))
            day_of_week = localtime_readable.split()[0] \
                if localtime_readable and len(localtime_readable.split()) > 0 \
                else None
            results[relative_path]['unixmtime'] = unixmtime
            results[relative_path]['day'] = day_of_week
            results[relative_path]['localtime'] = localtime
            if day_of_week is None:
                logging.error("Day of week is none! unixtime: %s  localtime: %s ", unixmtime, localtime_readable)

            format_data = get_audio_metadata(fullpath)
            audio_shortened = format_data.get("audio").split()[0] if format_data.get("audio") and format_data.get("audio").split() else None

            if args.verbose:
                logging.info("%-4s  %19s   %3s  %11s  %9s  %9s   %s",
                             day_of_week, localtime, format_data.get("extension"), format_data.get("duration"),
                             format_data.get("bitrate"), audio_shortened, relative_path)

            for k,v in format_data.items():
                results[relative_path][k] = v

        anydone = True

    if args.verbose :
        logging.info("")
    if anydone:
        logging.info("Writing %d results to : %s", len(results), result_filepath)
        with open(result_filepath, 'w') as file:
            json.dump(results, file, indent=2)
        dump_to_tsv(os.path.join(outpath,TSV_FILENAME), results)
    else:
        logging.info("Nothing new here")

    logging.info("")
    logging.info("(%.2f min)" % ((time.time() - start_time) / 60.0))
    logging.info("Done: %s", __file__)

# Usage example:
# $ python ~/code/speech-to-text/tally_audio.py -o /temp/stt/AudioJournals/text2stats -i /Volumes/AUDIOJ/AudioJournals -k
