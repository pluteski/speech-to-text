#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import os
import fnmatch
import argparse
import time
import shutil
import tempfile
from subprocess import Popen, PIPE

import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

from config import USER, PWD  # IBM Watson credentials
from config import STTCLIENT  # Full path to IBM Watson speech to text client sttclient.py
from config import GOOGLE_STTCLIENT # Google cloud api stt client grpc/transcribe_async.py
from config import IBM_QUEUE_FOLDER # Local temp folder for queuing audio files for upload to IBM audio.
from config import TMP_CONVERTED, TMP_CONVERTED_GOOGLE # Local temp folder for converted audio files
from config import GS_BUCKET  # Google Storage folder for uploaded audio, e.g., gs://<bucketname>/<folder>/<subfolder>/


__doc__ = "Basic wrapper for IBM Watson and Google Cloud speech-to-text APIs."

DEFAULT_NARROWBAND_MODEL = "en-US_NarrowbandModel"
DEFAULT_BROADBAND_MODEL = "en-US_BroadbandModel"
TYPES = ['flac','wav','mp3','m4a', 'ogg']
TYPE = 'flac'  # default audio format for upload to Watson
# TYPE='ogg' on Mac requires XCode update and ffmpeg reinstall:
# $ brew reinstall ffmpeg --with-libvorbis --with-opus --with-tools


def walk_files(folder=u'.', basepath='./', ext=".out", types=TYPES):
    """
    Locates audio files within a folder.
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
        fmatch = []
        for type in types:
            fmatch += fnmatch.filter(filenames, '*.%s' % type)
            fmatch += fnmatch.filter(filenames, '*.%s' % type.upper())
        for filename in fmatch:
           matches.append(os.path.join(root, filename))
    if matches:
        for filename in matches:
            filepath = os.path.realpath(filename)
            relpath = ((os.path.realpath(filename)).replace(basepath, '')+ext).lstrip('/')
            result.append((filepath, relpath,))
    return result

def make_dir(directory):
    if not os.path.exists(directory):
        logging.info("Creating directory: %s", directory)
        os.makedirs(directory)

def get_extension(filename):
    output = filename.split(".")
    extension = output[-1] if len(output)>1 else ''
    return extension if extension and extension.lower() in TYPES else None


def log_kv(key, value=''):
    """
    Helper to pretty print log statement with right hand side printed at fixed indent.
    :param key: left hand side of up to 30 characters
    :param value: right hand side
    """
    print "%-30s %s" % (key,value)


def convert_audio(filepath, type='flac', keep=False):
    if type in ["flac", "ogg"]:
        try:
            command = None
            make_dir(TMP_CONVERTED)
            logging.info("Converting to %s", type)
            if type == 'flac':
                new_filepath = os.path.join(TMP_CONVERTED, os.path.basename(filepath) + '.flac')
                command = 'ffmpeg -y -i "%s" -f flac "%s" ' % (filepath, new_filepath)
                if get_extension(filepath).lower() == 'mp3' :
                    command += ' -loglevel warning '
            elif type == 'ogg':
                new_filepath = os.path.join(TMP_CONVERTED, os.path.basename(filepath) + '.ogg')
                command = 'ffmpeg -y -i "%s" -acodec opus  "%s" ' % (filepath, new_filepath)
            if command:
                log_kv("command", command)
                if keep and os.path.isfile(new_filepath):
                    logging.info("Keeping previously converted file: %s", new_filepath)
                else:
                    os.system(command)
        except Exception as e:
            log_kv("While converting to %s" % type, e)
            raise
    else:
        log_kv("ERROR Unsupported type", type)
    if os.path.isfile(new_filepath):
        return new_filepath
    else:
        logging.error("Converted filepath not found: %s", new_filepath)
        return None



def convert_audio_to_linear16(filepath, keep=False):
    try:
        make_dir(TMP_CONVERTED_GOOGLE)
        logging.info("Converting to linear16: %s", filepath)
        new_filepath = os.path.join(TMP_CONVERTED_GOOGLE, os.path.basename(filepath) + '.pcm')
        if keep and os.path.isfile(new_filepath):
            logging.info("Keeping previously converted file: %s", new_filepath)
        else:
            command = 'ffmpeg -y -loglevel warning -i "%s" -f s16le -acodec pcm_s16le "%s" ' % (filepath, new_filepath)
            log_kv("command", command)
            os.system(command)
    except Exception as e:
        log_kv("While converting to linear 16", e)
        raise

    if os.path.isfile(new_filepath):
        return new_filepath
    else:
        logging.error("Converted filepath not found: %s", new_filepath)
        return None


def get_submit_command(sttclient_location,model,audio_format,full_output_folder,args,queue_file,threads=8):
    logpath = os.path.join(full_output_folder, "sttclient.log")
    return "python " \
              + sttclient_location \
              + " -noprompt" \
              + " -optout -threads=%d " % threads \
              + ' -model="%s" ' % model \
              + " -type=%s " % audio_format \
              + ' -out="%s" ' % full_output_folder \
              + " -credentials=%s:%s " % (args.user, args.pwd) \
              + ' -in="%s" ' % queue_file \
              + ' > "%s" ' % logpath, \
            logpath

def get_google_submit_command(gs_path, full_output_folder,sttclient_location=GOOGLE_STTCLIENT):
    return "python " + sttclient_location + " --encoding LINEAR16 " + '"%s"' % gs_path \
              + ' > "%s" ' % os.path.join(full_output_folder, "sttclient.log")

def replace_dictated(data):
    """
    This is a workaround to handle dictation (spoken word audio containing punctuation),
    in case the cloud api does not provide adequate support for properly converting dictation to punctuation.
    :param data:
    :return:
    """
    return data.replace(" period", ".") \
        .replace(" comma ", ", ") \
        .replace(" coma ", ",") \
        .replace(" colon ", ": ") \
        .replace(" exclamation mark ", "! ") \
        .replace(" question mark ", "? ") \
        .replace(" newline", "\n") \
        .replace(" new line", "\n") \
        .replace(" new paragraph", "\n\n") \
        .replace(" no paragraph", "\n\n") \
        .replace(" %HESITATION", "...") \
        .replace(" karma...", ",")


def process_ibm(audio_filepath, sttclient_location, full_output_folder, args, skipped, submitted):
    """
    :param filepath : audio filepath
    :param sttclient_location: filepath
    :param full_output_folder: filepath
    :param args:
    :param skipped: list
    :return: skipped, submitted : <skipped> is a list of filepaths, <submitted> is a list of filepaths.

    """

    # Skip if previous result already exists and args.keep
    if args.keep:
        previous = os.path.join(full_output_folder,"hypotheses.txt")
        if os.path.isfile(previous):
            log_kv("Keeping previous: ", previous)
            log_kv("Num processed: ", num_processed)
            skipped.append(audio_filepath)
            log_kv("Num skipped: ", len(skipped))
            return skipped, submitted


    # Convert audio format
    extension = get_extension(audio_filepath)
    extension1 = extension
    if not extension:
        logging.warn("skipping unsupported extension: %s", audio_filepath)
        skipped.append(audio_filepath)
        return skipped, submitted

    if extension.lower() in ['m4a', 'mp3', 'wav']:
        converted_filepath = convert_audio(audio_filepath, TYPE)
        log_kv("Converted audio:", converted_filepath)

    if converted_filepath is None:
        logging.error("bad audio file conversion.  Skipping: %s", audio_filepath)
        skipped.append(audio_filepath)
        return skipped, submitted

    # Set audio format
    extension = get_extension(converted_filepath)
    if extension == 'wav':
        audio_format = 'audio/wav'
    elif extension == 'flac':
        audio_format = 'audio/flac'
    elif extension == 'ogg':
        audio_format = '"audio/ogg; codecs=opus"'
    else:
        logging.warn("skipping file having bad extension: %s", audio_filepath)
        skipped.append(audio_filepath)
        return skipped, submitted


    logging.info("Queueing audio file")
    make_dir(IBM_QUEUE_FOLDER)
    temp_fp = tempfile.NamedTemporaryFile(prefix="ibm_tempq_", dir=IBM_QUEUE_FOLDER, mode='w+t')
    temp_fp.write(converted_filepath)
    temp_fp.flush()
    logging.info("Wrote '%s' to temp file %s", converted_filepath, temp_fp.name)


    try:
        print
        logging.info("Submitting audio file")
        model = DEFAULT_NARROWBAND_MODEL if args.narrowband else DEFAULT_BROADBAND_MODEL
        command,logpath = get_submit_command(sttclient_location,model,audio_format,full_output_folder,args,temp_fp.name,threads=8)
        if os.path.isfile(logpath):
            logging.warning("Removing previous log: %s", logpath)
            os.remove(logpath)
        log_kv("command", command)
        os.system(command)
        submitted.append(audio_filepath)

        hypotheses_filepath = os.path.join(full_output_folder,"hypotheses.txt")
        word_count = 0
        char_count = 0

        with open(hypotheses_filepath, 'r') as myfile:
            hypotheses_data = myfile.read()
            if hypotheses_data:
                word_count = len(hypotheses_data.split())
                char_count = len(hypotheses_data)

        if word_count < 5 or (extension1.lower()=='mp3' and word_count<50):
            logging.warn("low word count : %s  Number of characters: %s", word_count, char_count)
            # For WAV
            # if log contains a UpsamplingNotAllowed error message,
            # and failed run used broadband model, then rerun using narrowband model
            resubmit = False
            if extension1.lower() == "wav":
                err_msg = "('UpsamplingNotAllowed', 8000, 16000)"
                sttclient_log = os.path.join(full_output_folder,"sttclient.log")
                with open(sttclient_log, 'r') as myfile2:
                    sttclient_log_data = myfile2.read()
                    if sttclient_log_data and sttclient_log_data.find(err_msg) > -1:
                        resubmit = True
            # For other extensions always rerun using narrowband if low word count
            elif extension1.lower() == "mp3":
                logging.warn("=== ============================ ===")
                logging.warn("=== mp3 file with low word count ===")
                logging.warn("=== ============================ ===")
                resubmit = True
            elif extension1.lower() == "m4a":
                logging.warn("=== ============================ ===")
                logging.warn("=== m4a file with low word count ===")
                logging.warn("=== ============================ ===")
                resubmit = True
            else:
                logging.error("UNHANDLED CASE: %s", extension1)
                raise ValueError('An unhandled extension gave low word count.')
            if resubmit and not args.narrowband:
                print
                logging.info("ReSubmitting audio file using narrowband model")
                print
                command,logpath = get_submit_command(sttclient_location, DEFAULT_NARROWBAND_MODEL, audio_format,
                                                     full_output_folder, args, temp_fp.name, threads=8)
                if os.path.isfile(logpath):
                    logging.warning("Removing previous log: %s", logpath)
                    os.remove(logpath)
                log_kv("command", command)
                os.system(command)
                hypotheses_data = None
                with open(hypotheses_filepath, 'r') as file2:
                    hypotheses_data = file2.read()
                    if hypotheses_data:
                        word_count = len(hypotheses_data.split())
                        char_count = len(hypotheses_data)
                if word_count < 3:
                    logging.error("Still low word count : %s  Number of characters: %s  Data: %s",
                                    word_count, char_count, hypotheses_data)
            print
            logging.info("Words: %d  Characters: %d", word_count, len(hypotheses_data) if hypotheses_data else 0)
            if args.verbose:
                print
                logging.info("Hypotheses data: \n\n%s", hypotheses_data)
                print

            if word_count > 2 and char_count > 4 and hypotheses_data:
                hypotheses_data_edit = replace_dictated(hypotheses_data)
                if hypotheses_data != hypotheses_data_edit:
                    edit_filepath = hypotheses_filepath+".dictated"
                    "Dictation edits saved to ", edit_filepath
                    with open(edit_filepath, 'w') as file3:
                        file3.write(hypotheses_data_edit)
    finally:
        logging.info("Closing %s", temp_fp.name)
        temp_fp.close()

    return skipped, submitted



def process_google(audio_filepath, sttclient_location, full_output_folder, args, skipped, submitted):
    """
    :param audio filepath
    :param sttclient_location: filepath
    :param full_output_folder: filepath
    :param args:
    :param skipped: list
    :return: skipped, submitted
    where skipped is a list of filepaths, submitted is a list of filepaths.

    """
    stdout_filepath = os.path.join(full_output_folder, "sttclient.log")
    transcribed_filepath = os.path.join(full_output_folder, "transcript.txt")
    scored_filepath = os.path.join(full_output_folder, "scored.txt")

    # Skip if previous result already exists and args.keep
    if args.keep:
        # Look for transcript.txt and scored.txt
        logging.info("Checking for transcript")
        if os.path.isfile(transcribed_filepath) and os.path.isfile(scored_filepath):
            logging.info("Transcript exists ... skipping")
            skipped.append(audio_filepath)
            log_kv("Num processed: ", num_processed)
            log_kv("Num skipped: ", len(skipped))
            return skipped, submitted

    # Convert if necessary
    extension = get_extension(audio_filepath)
    if not extension:
        logging.warn("skipping unsupported extension: %s", audio_filepath)
        skipped.append(audio_filepath)
        return skipped, submitted

    if extension.lower() in ['m4a', 'mp3', 'wav']:
        # converted_filepath = convert_audio_to_linear16(audio_filepath, args.keep)
        converted_filepath = convert_audio_to_linear16(audio_filepath)
        log_kv("Converted audio:", converted_filepath)

    if converted_filepath is None:
        logging.error("bad audio file conversion.  Skipping: %s", audio_filepath)
        skipped.append(audio_filepath)
        return skipped, submitted

    gs_path = os.path.join(os.path.dirname(GS_BUCKET + audio_filepath.replace(basepath,'').lstrip("/")),os.path.basename(converted_filepath))
    do_upload = True

    if args.keep:
        log_kv("Checking cloud storage for pre-existing audio file.")
        process = Popen(["gsutil", "ls", gs_path], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        if err and err.strip() != "None":
            log_kv("err: ", err.strip())
        if output.strip() == gs_path:
            do_upload = False

    # Upload to Google Storage
    if do_upload:
        print
        logging.info("Uploading audio file")
        # command = "gsutil cp " + converted_filepath + " " + GS_BUCKET
        bucket_folder = os.path.dirname(gs_path)
        bucket_folder = bucket_folder if bucket_folder.endswith("/") else bucket_folder+"/"
        command = 'gsutil cp "%s" "%s" ' % (converted_filepath, bucket_folder)
        log_kv("command", command)
        log_kv("gs_path", '"%s"' % gs_path)
        os.system(command)
    else:
        logging.info('Using already uploaded: "%s"', gs_path)

    print
    logging.info("Transcribing audio file")
    command = get_google_submit_command(gs_path,full_output_folder)
    log_kv("command", command)
    transcript = ""
    scored_transcription = ""
    os.system(command)
    submitted.append(audio_filepath)
    word_count = 0
    char_count = 0
    if not os.path.isfile(stdout_filepath):
        logging.error("")
        logging.error("===   File not exists: %s   ===", stdout_filepath)
        logging.error("")
    else:
        with open(stdout_filepath, 'r') as myfile:
            data = myfile.read()
            if data:
                for line in data.split("\n"):
                    if line.startswith("Waiting for server processing") \
                            or line.startswith("name:") \
                            or line.startswith("Result:") \
                            or line.strip() == "" \
                            or not line.startswith("  ("):
                        continue
                    else:
                        text = line.split(":")
                        text = text[1] if len(text) > 1 else ""
                        scored_transcription += line.lstrip() + "\n"
                        transcript += text

                print
                if transcript:
                    word_count = len(transcript.split())
                    char_count = len(transcript)
                    with open(transcribed_filepath, 'w') as fp:
                        fp.write(transcript)
                        logging.info("Wrote transcript to %s", transcribed_filepath)
                if scored_transcription:
                    word_count = len(scored_transcription.split())
                    char_count = len(scored_transcription)
                    with open(scored_filepath, 'w') as fp:
                        fp.write(scored_transcription)
                        logging.info("Wrote scored transcript to %s", scored_filepath)
                if word_count > 0 and char_count > 0:
                    logging.info("Words: %d  Characters: %d", word_count, char_count)
                else:
                    print
                    logging.warn("===   No transcript   ===")
                    print
            else:
                logging.warn("No data at %s", stdout_filepath)

        if args.verbose:
            print
            logging.info("Hypotheses data: \n\n%s", data)
            print

        if word_count > 2 and char_count > 4 and transcript:
            data_edit = replace_dictated(transcript)
            if transcript != data_edit:
                edit_filepath = transcribed_filepath+".dictated"
                "Dictation edits saved to ", edit_filepath
                with open(edit_filepath, 'w') as fp2:
                    fp2.write(data_edit)

    return skipped, submitted


def list_walk(folder=u'.'):
    """
    Traverses folder's contents and prints the directories and files it contains.
    """
    for root_dir, sub_dirs, files in os.walk(folder):
        path = root_dir.split('/')
        if os.path.basename(root_dir) in ['.', '.DS_Store']:
            continue
        print (len(path) - 1) * '    ', os.path.basename(root_dir)+"/"
        for file in files:
            print len(path) * '    ', file


if __name__ == '__main__':

    start_time = time.time()

    # parse command line parameters
    parser = argparse.ArgumentParser(description='Speech to text batcher')

    parser.add_argument('--infolder','-i', action='store', default='.', help='folder containing audio files')
    parser.add_argument('--outfolder','-o', action='store', default='./output', help='output directory')
    parser.add_argument('--basefolder','-b', action='store', default='./output', help='prefix removed from path for indexing')
    parser.add_argument('--sttclient','-s', action='store', default=STTCLIENT, help='location of stt client')
    parser.add_argument('--user','-u', action='store', default=USER, help='IBM Watson api user')
    parser.add_argument('--pwd','-p', action='store', default=PWD, help='IBM Watson api password')
    parser.add_argument('--verbose','-v', action='store_true', help='Spew logs profusely.')
    parser.add_argument('--clean','-c', action='store_true', help='Clean %s' % TMP_CONVERTED)
    parser.add_argument('--max','-m', action='store', type=int, help='Quit after processing this many.')
    parser.add_argument('--keep','-k', action='store_true',
                        help='Do not overwrite previously converted audio files, or results folder already containing hypotheses.txt.')
    parser.add_argument('--narrowband','-n', action='store_true', help='Use model=en-US_NarrowbandModel instead of en-US_BroadbandModel')
    parser.add_argument('--google','-g', action='store_true', help='Use Google speech to text.')

    args = parser.parse_args()

    cwd = os.getcwd()
    original_cwd = cwd

    log_kv("Running", __file__)
    log_kv("From", os.path.dirname(os.path.realpath(__file__)))
    print
    log_kv("cwd", cwd)
    if args.infolder:
        log_kv("--infolder", args.infolder)
        os.chdir(args.infolder)
        cwd = os.getcwd()
        log_kv("new cwd", cwd)
    inpath = os.path.realpath(cwd)

    basefolder = u'/'
    if args.basefolder:
        basefolder = args.basefolder
        log_kv("--basefolder", basefolder)
    basepath = os.path.realpath(basefolder)
    log_kv("basepath", basepath)
    log_kv("log folder", cwd.replace(basefolder, ''))

    outfolder = u'./output'
    if args.outfolder:
        outfolder = args.outfolder
        log_kv("--outfolder", outfolder)
    outpath = os.path.realpath(outfolder)
    log_kv("outpath", outpath)
    make_dir(outpath)

    sttclient_location = os.path.realpath(os.path.expanduser(args.sttclient))

    if args.verbose:
        print
        list_walk()
        print

    if args.keep:
        logging.info("Keeping previous transcript, reusing previous converted audio.")

    if args.clean:
        print
        clean_exit = 0
        log_kv("Cleaning", TMP_CONVERTED)
        try:
            try:
                shutil.rmtree(TMP_CONVERTED)
                shutil.rmtree(IBM_QUEUE_FOLDER)
            except:
                pass
            make_dir(TMP_CONVERTED)


            if args.google:
                log_kv("Cleaning", TMP_CONVERTED_GOOGLE)
                try:
                    shutil.rmtree(TMP_CONVERTED_GOOGLE)
                except:
                    pass
                make_dir(TMP_CONVERTED_GOOGLE)

                log_kv("Cleaning", "Google cloud storage temp folder")
                # cf. https://cloud.google.com/storage/docs/gsutil/commands/rm
                log_kv("command", "gsutil rm -r %s*" % GS_BUCKET)

                process = Popen(["gsutil", "rm -r", "%s*" % GS_BUCKET], stdout=PIPE)
                (output, err) = process.communicate()
                exit_code = process.wait()
                if output.strip():
                    print output
                if err and err.strip() != "None":
                    log_kv("err: ", err.strip())
                    clean_exit = 1
        except Exception as e:
            log_kv("During clean", e)
            clean_exit = 1
        logging.info("Cleaning done")
        exit(clean_exit)


    print
    logging.info("Directing output to %s", outpath)
    skipped = []
    num_processed = 0
    submitted = []
    results = []
    file_list = walk_files(basepath=basepath)
    log_kv("Number Matching Files", len(file_list))

    for x in file_list:
        if args.max and num_processed >= args.max:
            log_kv("Max met", args.max)
            break
        audio_format = None
        file_time = time.time()
        num_processed += 1
        subpath = os.path.join(os.path.dirname(x[1]), os.path.basename(x[0]))
        print 75 * "=", "\n", subpath, "\n", 75 * "="
        if os.path.isfile(x[0]):
            full_output_folder = os.path.join(outpath, x[1])
            make_dir(full_output_folder)

            audio_file = x[0]

            num_submitted = len(submitted)
            if args.google:
                skipped, submitted = process_google(audio_file, sttclient_location, full_output_folder, args, skipped, submitted)
            else:
                skipped, submitted = process_ibm(audio_file, sttclient_location, full_output_folder, args, skipped, submitted)

            if len(submitted) > num_submitted:
                print
                log_kv("Result path", full_output_folder)
                results.append(full_output_folder)

        else:
            log_kv("ERROR: missing", x[0])

        print("Completed Item %d  (%.1f min)" % (len(results), (time.time() - file_time) / 60.0))

    print
    print

    #   Change back to original working directory
    if args.infolder:
        os.chdir(original_cwd)
        log_kv("cwd now", os.getcwd())

    if args.verbose:
        logging.info("%s", (105 * "="))
        logging.info("Results:")
        print("\n".join(results))
        print
        if skipped:
            print ("Skipped:\n")
            print ("\n".join(skipped))
            print

    logging.info("Processed: %d  Submitted: %d  Skipped: %d", num_processed, len(submitted), len(skipped))

    print("(%.1f min)" % ((time.time() - start_time) / 60.0))

    log_kv("Done:              ", __file__)


