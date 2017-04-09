#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import csv
import sqlite3
import os
import argparse
import time
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
from speech2text import log_kv, make_dir

"""
What it does:
Loads TSV data into sqlite in memory database and runs SQL analyses.
"""

TRANSCRIBED_STATS_TSV = "transcribed_stats.tsv"
AUDIO_STATS_TSV = "audio_table.tsv"


API_META = {"ibm" : {"base" : "ibm_stt", "transcripts" : ["hypotheses.txt", "hypotheses.txt.dictated"]},
            "google": {"base": "google_stt", "transcripts": ["transcript.txt", "transcript.txt.dictated"]}}


CREATE_AUDIO_STATS_SQL = """
CREATE TABLE audio_stats (
    path TEXT PRIMARY KEY NOT NULL,
    filename TEXT,
    folder TEXT,
    format TEXT,
    short_format TEXT,
    extension TEXT,
    bitrate_string TEXT,
    bitrate_int INT,
    duration TEXT,
    duration_min REAL,
    size_mb REAL,
    unixmtime REAL,
    localtime TEXT,
    audio_filename_date TEXT,
    etl_date TEXT
);
"""

CREATE_TRANSCRIPT_STATS_SQL = """
CREATE TABLE transcript_stats (
    etl_time TEXT,
    google_char_count INT,
    google_transcribe_seconds INT,
    google_unixmtime BIGINT,
    google_word_count INT,
    ibm_char_count INT,
    ibm_transcribe_seconds INT,
    ibm_unixmtime BIGINT,
    ibm_word_count INT,
    path TEXT PRIMARY KEY NOT NULL
);
"""

def insert_from_tsv(con, tablename, path):
    sql_insert = "insert into " + tablename + " %s "
    with open(path, 'r') as fp:
        log_kv("Loading %s from" % tablename, path)
        reader = csv.reader(fp, delimiter='\t')
        header = next(reader)
        query = sql_insert % str(tuple(header)) + " VALUES %s"
        for rec in reader:
            con.execute(query % str(tuple(rec)))


def load_data(con, cur, audio_stats_path, transcript_stats_path):
    cur.execute(CREATE_AUDIO_STATS_SQL)
    cur.execute(CREATE_TRANSCRIPT_STATS_SQL)
    insert_from_tsv(con, "audio_stats", audio_stats_path)
    insert_from_tsv(con, "transcript_stats", transcript_stats_path)
    con.commit()


def run_query(con,cur,query):
    log_kv("query", query)
    cur.execute(query)
    con.commit()
    return cur.fetchall()


def fetch_rows_for_column(con,cur,tablename, column, value):
    value = '"%s"' % value if type(value) is str else value
    query = 'SELECT * FROM {tn} WHERE {cc} = {val}'.format(tn=tablename, cc=column, val=value)
    log_kv("query", query)
    cur.execute(query)
    con.commit()
    return cur.fetchall()

def fetch_rows_columns_for_column(con,cur,columns, tablename, column, value):
    value = '"%s"' % value if type(value) is str else value
    columns_string = ",".join(columns)
    query = 'SELECT {xx} FROM {tn} WHERE {cc} = {val}'.format(xx=columns_string, tn=tablename, cc=column, val=value)
    log_kv("query", query)
    cur.execute(query)
    con.commit()
    return cur.fetchall()

def create_and_load_db(audio_stats_path, transcript_stats_path):
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    load_data(con, cur, audio_stats_path, transcript_stats_path)
    return con, cur

query1 = """
select count(*) from
audio_stats JOIN transcript_stats
using (path)
where size_mb > 200000000
and google_word_count > 50
"""

query2 = """
select
count(case when google_word_count > 100 and size_mb > 500000000 then 1 else null end) as gwc_100_200mb,
count(case when ibm_word_count > 100 and size_mb > 500000000 then 1 else null end) as iwc_100_200mb,
count(case when google_word_count > 500 and size_mb > 500000000 then 1 else null end) as gwc_500_200mb,
count(case when ibm_word_count > 500 and size_mb > 500000000 then 1 else null end) as iwc_500_200mb,
count(case when size_mb > 200000000 then 1 else null end) as over_200mb
from audio_stats JOIN transcript_stats using (path)
"""

query3 = """
select
count(case when google_word_count = ibm_word_count then 1 else null end)
from audio_stats JOIN transcript_stats using (path)
"""

query4 = """
select
path, google_word_count, ibm_word_count, size_mb/1000000.0 as mb
from audio_stats JOIN transcript_stats using (path)
where
google_word_count <> "" and ibm_word_count <> ""
and google_word_count = ibm_word_count
order by google_word_count asc
limit 100
"""


#   Tallies how many ibm transcripts are at least triple the size of corresponding google transcripts
query5 = """
select
path, ibm_word_count, google_word_count, size_mb/1000000.0 as mb
from audio_stats JOIN transcript_stats using (path)
where
ibm_word_count > 3*google_word_count
and ibm_word_count > 100
and google_word_count<>'' and ibm_word_count<>''
order by ibm_word_count desc, google_word_count desc
"""
# 2394


#   Tallies how many ibm transcripts are at least triple the size of corresponding google transcripts
#   where the google transcript is at least 100 words.
query6 = """
select
path, ibm_word_count, google_word_count, size_mb/1000000.0 as mb
from audio_stats JOIN transcript_stats using (path)
where
ibm_word_count > 3*google_word_count
and google_word_count > 100
and google_word_count<>'' and ibm_word_count<>''
order by ibm_word_count desc, google_word_count desc
"""
# 83


#   Tallies how many transcripts have a specified number of words.
query7 = """
select
'10000:',
count(case when google_word_count > 10000 and google_word_count <> '' then 1 else null end),
count(case when ibm_word_count > 10000 and ibm_word_count <> ''  then 1 else null end),
'5000:',
count(case when google_word_count > 5000 and google_word_count <> ''  then 1 else null end),
count(case when ibm_word_count > 5000 and ibm_word_count <> '' then 1 else null end),
'3000:',
count(case when google_word_count > 3000 and google_word_count <> ''  then 1 else null end),
count(case when ibm_word_count > 3000 and ibm_word_count <> '' then 1 else null end),
'2000:',
count(case when google_word_count > 2000 and google_word_count <> ''  then 1 else null end),
count(case when ibm_word_count > 2000 and ibm_word_count <> '' then 1 else null end),
'1000:',
count(case when google_word_count > 1000 and google_word_count <> ''  then 1 else null end),
count(case when ibm_word_count > 1000 and ibm_word_count <> '' then 1 else null end),
'500:',
count(case when google_word_count > 500 and google_word_count <> ''  then 1 else null end),
count(case when ibm_word_count > 500 and ibm_word_count <> '' then 1 else null end)
from audio_stats JOIN transcript_stats using (path)
"""
# (u'10000:', 0, 0, u'5000:', 0, 39, u'3000:', 8, 321, u'2000:', 29, 1603, u'1000:', 141, 4047, u'500:', 334, 5782)


#   Tallies longest transcripts
query8 = """
select max(google_word_count), max(ibm_word_count)
from audio_stats JOIN transcript_stats using (path)
where
google_word_count is not null and ibm_word_count is not null
and google_word_count <> '' and ibm_word_count <> ''

"""
# (4892, 8445)


#   Tallies how transcript rate drops as file size increases, for google only, which imposes a limit.
query9 = """
select
'500mb:',
count(case when size_mb > 500000000 and google_word_count > 10 then 1 else null end),
'100mb:',
count(case when size_mb > 100000000 and google_word_count >10 then 1 else null end),
'50mb:',
count(case when size_mb > 50000000 and google_word_count >10 then 1 else null end),
'10mb:',
count(case when size_mb > 10000000 and google_word_count >10 then 1 else null end)
from audio_stats JOIN transcript_stats using (path)
where google_word_count <> ''
"""
# (u'500mb:', 0, u'100mb:', 1, u'50mb:', 18, u'10mb:', 532)


#   Tallies how transcript rate drops as file size increases, for google only, which imposes a limit.
query10 = """
select
'500mb:',
count(case when size_mb > 500000000 and ibm_word_count > 10 then 1 else null end),
'100mb:',
count(case when size_mb > 100000000 and ibm_word_count >10 then 1 else null end),
'50mb:',
count(case when size_mb > 50000000 and ibm_word_count >10 then 1 else null end),
'10mb:',
count(case when size_mb > 10000000 and ibm_word_count >10 then 1 else null end)
from audio_stats JOIN transcript_stats using (path)
where ibm_word_count <> ''
"""
# (u'500mb:', 3, u'100mb:', 282, u'50mb:', 431, u'10mb:', 2123)



if __name__ == '__main__':

    start_time = time.time()

    parser = argparse.ArgumentParser(description='Sqlite Helper')
    parser.add_argument('--infolder','-i', action='store', default='.', help='folder containing previous ETL files')
    parser.add_argument('--outfolder','-o', action='store', default='./output', help='output directory')

    args = parser.parse_args()

    log_kv("Running", __file__)
    log_kv("From", os.path.dirname(os.path.realpath(__file__)))
    print

    inpath = os.path.realpath(args.infolder if args.infolder else os.getcwd())
    log_kv("inpath", inpath)
    outpath = os.path.realpath(args.outfolder if args.outfolder else u'./output')
    log_kv("outpath", outpath)
    make_dir(outpath)

    log_kv("")
    log_kv("Audio stats file", AUDIO_STATS_TSV)
    log_kv("Transcript stats", TRANSCRIBED_STATS_TSV)
    log_kv("")

    audio_stats_path = os.path.join(inpath,AUDIO_STATS_TSV)
    transcript_stats_path = os.path.join(inpath,TRANSCRIBED_STATS_TSV)

    con,cur = create_and_load_db(audio_stats_path, transcript_stats_path)

    # result = fetch_rows_for_column(con, cur, "audio_stats", "path", "2015/Journal/20150822 104100.m4a")
    # print "\nResult:\n", result
    #
    # result = fetch_rows_columns_for_column(con, cur,["filename","bitrate_int","duration_min","size_mb"],
    #                               "audio_stats", "path", "2015/Journal/20150822 104100.m4a")
    # print "\nResult:\n", result
    # print
    #
    # result = run_query(con, cur, "select path from audio_stats where size_mb is not null and size_mb <> '' ")
    # log_kv("len(result)", len(result))
    #
    # result = run_query(con, cur, "select path from audio_stats where size_mb is null or size_mb = '' ")
    # log_kv("len(result)", len(result))
    #
    # result = run_query(con, cur, "select path from audio_stats where size_mb is null ")
    # log_kv("len(result)", len(result))
    #
    # result = run_query(con, cur, "select path from audio_stats where size_mb is null ")
    # log_kv("len(result)", len(result))


    result = run_query(con, cur, query2)
    log_kv("result", result)

    result = run_query(con, cur, query3)
    log_kv("result", result)


    con.close()


    log_kv("Done:              ", __file__)
    print("(%.1f min)" % ((time.time() - start_time) / 60.0))






