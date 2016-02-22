#!/usr/bin/env python
import os
from urllib2 import Request, urlopen
import gzip
import csv

'''
See https://inventory.data.gov/dataset/public-elementary-secondary-school-universe-survey-2009-10
Data: https://inventory.data.gov/dataset/c325a86a-a0da-479d-bb87-cdbf88833b25/resource/102fd9bd-4737-401b-b88f-5c5b0fab94ec/download/userssharedsdfpublicelementarysecondaryunivsrvy200910.csv
Attribute Dictionary: http://nces.ed.gov/ccd/data/txt/psu091alay.txt
'''

FIELD_MAP = {'NCESSCH': 1, 'FIPST': 2, 'LEAID': 3, 'SCHNO': 4, 'STID09': 5, 'SEASCH09': 6, 'LEANM09': 7, 'SCHNAM09': 8,
            'PHONE09': 9, 'MSTREE09': 10, 'MCITY09': 11, 'MSTATE09': 12, 'MZIP09': 13, 'MZIP409': 14, 'LSTREE09': 15,
            'LCITY09': 16, 'LSTATE09': 17, 'LZIP09': 18, 'LZIP409': 19, 'TYPE09': 20, 'STATUS09': 21, 'ULOCAL09': 22,
            'LATCOD09': 23, 'LONCOD09': 24, 'CONUM09': 25, 'CONAME09': 26, 'CDCODE09': 27, 'FTE09': 28, 'GSLO09': 29,
            'GSHI09': 30, 'LEVEL09': 31, 'TITLEI09': 32, 'STITLI09': 33, 'MAGNET09': 34, 'CHARTR09': 35, 'SHARED09': 36,
            'BIES09': 37, 'FRELCH09': 38, 'REDLCH09': 39, 'TOTFRL09': 40, 'RACECAT09': 41, 'PK09': 42, 'AMPKM09': 43,
            'AMPKF09': 44, 'ASPKM09': 45, 'ASPKF09': 46, 'HIPKM09': 47, 'HIPKF09': 48, 'BLPKM09': 49, 'BLPKF09': 50,
            'WHPKM09': 51, 'WHPKF09': 52, 'HPPKM09': 53, 'HPPKF09': 54, 'TRPKM09': 55, 'TRPKF09': 56, 'KG09': 57,
            'AMKGM09': 58, 'AMKGF09': 59, 'ASKGM09': 60, 'ASKGF09': 61, 'HIKGM09': 62, 'HIKGF09': 63, 'BLKGM09': 64,
            'BLKGF09': 65, 'WHKGM09': 66, 'WHKGF09': 67, 'HPKGM09': 68, 'HPKGF09': 69, 'TRKGM09': 70, 'TRKGF09': 71,
            'G0109': 72, 'AM01M09': 73, 'AM01F09': 74, 'AS01M09': 75, 'AS01F09': 76, 'HI01M09': 77, 'HI01F09': 78,
            'BL01M09': 79, 'BL01F09': 80, 'WH01M09': 81, 'WH01F09': 82, 'HP01M09': 83, 'HP01F09': 84, 'TR01M09': 85,
            'TR01F09': 86, 'G0209': 87, 'AM02M09': 88, 'AM02F09': 89, 'AS02M09': 90, 'AS02F09': 91, 'HI02M09': 92,
            'HI02F09': 93, 'BL02M09': 94, 'BL02F09': 95, 'WH02M09': 96, 'WH02F09': 97, 'HP02M09': 98, 'HP02F09': 99,
            'TR02M09': 100, 'TR02F09': 101, 'G0309': 102, 'AM03M09': 103, 'AM03F09': 104, 'AS03M09': 105,
            'AS03F09': 106, 'HI03M09': 107, 'HI03F09': 108, 'BL03M09': 109, 'BL03F09': 110, 'WH03M09': 111,
            'WH03F09': 112, 'HP03M09': 113, 'HP03F09': 114, 'TR03M09': 115, 'TR03F09': 116, 'G0409': 117,
            'AM04M09': 118, 'AM04F09': 119, 'AS04M09': 120, 'AS04F09': 121, 'HI04M09': 122, 'HI04F09': 123,
            'BL04M09': 124, 'BL04F09': 125, 'WH04M09': 126, 'WH04F09': 127, 'HP04M09': 128, 'HP04F09': 129,
            'TR04M09': 130, 'TR04F09': 131, 'G0509': 132, 'AM05M09': 133, 'AM05F09': 134, 'AS05M09': 135,
            'AS05F09': 136, 'HI05M09': 137, 'HI05F09': 138, 'BL05M09': 139, 'BL05F09': 140, 'WH05M09': 141,
            'WH05F09': 142, 'HP05M09': 143, 'HP05F09': 144, 'TR05M09': 145, 'TR05F09': 146, 'G0609': 147,
            'AM06M09': 148, 'AM06F09': 149, 'AS06M09': 150, 'AS06F09': 151, 'HI06M09': 152, 'HI06F09': 153,
            'BL06M09': 154, 'BL06F09': 155, 'WH06M09': 156, 'WH06F09': 157, 'HP06M09': 158, 'HP06F09': 159,
            'TR06M09': 160, 'TR06F09': 161, 'G0709': 162, 'AM07M09': 163, 'AM07F09': 164, 'AS07M09': 165,
            'AS07F09': 166, 'HI07M09': 167, 'HI07F09': 168, 'BL07M09': 169, 'BL07F09': 170, 'WH07M09': 171,
            'WH07F09': 172, 'HP07M09': 173, 'HP07F09': 174, 'TR07M09': 175, 'TR07F09': 176, 'G0809': 177,
            'AM08M09': 178, 'AM08F09': 179, 'AS08M09': 180, 'AS08F09': 181, 'HI08M09': 182, 'HI08F09': 183,
            'BL08M09': 184, 'BL08F09': 185, 'WH08M09': 186, 'WH08F09': 187, 'HP08M09': 188, 'HP08F09': 189,
            'TR08M09': 190, 'TR08F09': 191, 'G0909': 192, 'AM09M09': 193, 'AM09F09': 194, 'AS09M09': 195,
            'AS09F09': 196, 'HI09M09': 197, 'HI09F09': 198, 'BL09M09': 199, 'BL09F09': 200, 'WH09M09': 201,
            'WH09F09': 202, 'HP09M09': 203, 'HP09F09': 204, 'TR09M09': 205, 'TR09F09': 206, 'G1009': 207,
            'AM10M09': 208, 'AM10F09': 209, 'AS10M09': 210, 'AS10F09': 211, 'HI10M09': 212, 'HI10F09': 213,
            'BL10M09': 214, 'BL10F09': 215, 'WH10M09': 216, 'WH10F09': 217, 'HP10M09': 218, 'HP10F09': 219,
            'TR10M09': 220, 'TR10F09': 221, 'G1109': 222, 'AM11M09': 223, 'AM11F09': 224, 'AS11M09': 225,
            'AS11F09': 226, 'HI11M09': 227, 'HI11F09': 228, 'BL11M09': 229, 'BL11F09': 230, 'WH11M09': 231,
            'WH11F09': 232, 'HP11M09': 233, 'HP11F09': 234, 'TR11M09': 235, 'TR11F09': 236, 'G1209': 237,
            'AM12M09': 238, 'AM12F09': 239, 'AS12M09': 240, 'AS12F09': 241, 'HI12M09': 242, 'HI12F09': 243,
            'BL12M09': 244, 'BL12F09': 245, 'WH12M09': 246, 'WH12F09': 247, 'HP12M09': 248, 'HP12F09': 249,
            'TR12M09': 250, 'TR12F09': 251, 'UG09': 252, 'AMUGM09': 253, 'AMUGF09': 254, 'ASUGM09': 255, 'ASUGF09': 256,
            'HIUGM09': 257, 'HIUGF09': 258, 'BLUGM09': 259, 'BLUGF09': 260, 'WHUGM09': 261, 'WHUGF09': 262,
            'HPUGM09': 263, 'HPUGF09': 264, 'TRUGM09': 265, 'TRUGF09': 266, 'MEMBER09': 267, 'AM09': 268,
            'AMALM09': 269, 'AMALF09': 270, 'ASIAN09': 271, 'ASALM09': 272, 'ASALF09': 273, 'HISP09': 274,
            'HIALM09': 275, 'HIALF09': 276, 'BLACK09': 277, 'BLALM09': 278, 'BLALF09': 279, 'WHITE09': 280,
            'WHALM09': 281, 'WHALF09': 282, 'PACIFIC09': 283, 'HPALM09': 284, 'HPALF09': 285, 'TR09': 286,
            'TRALM09': 287, 'TRALF09': 288, 'TOTETH09': 289, 'PUPTCH09': 290}
SCHOOL_DATA_URL = 'https://inventory.data.gov/dataset/c325a86a-a0da-479d-bb87-cdbf88833b25/resource/102fd9bd-4737-401b-b88f-5c5b0fab94ec/download/userssharedsdfpublicelementarysecondaryunivsrvy200910.csv'
CSV_FILE = 'userssharedsdfpublicelementarysecondaryunivsrvy200910.csv'
GZIP_FILE = '%s.gz' % CSV_FILE

if not os.path.isfile(CSV_FILE) and not os.path.isfile(GZIP_FILE):
    req = Request(SCHOOL_DATA_URL)
    connection = urlopen(req, timeout=5)
    with gzip.open(GZIP_FILE, 'wb') as gzfile:
        gzfile.write(connection.read())

def create_school_suggestion(row):
    suggestion = {
        'phrases': [],
        'rank': 1,
        'suggestion': None
    }

    return suggestion
data = None
if os.path.isfile(GZIP_FILE):
    with gzip.open(GZIP_FILE, 'rb') as f:
        csvreader = csv.reader(f, delimiter=',', quotechar='"')
        for row in csvreader:
            pass

elif os.path.isfile(CSV_FILE):
    with open(CSV_FILE, 'rb') as f:
        csvreader = csv.reader(f, delimiter=',', quotechar='"')
        for row in csvreader:
            pass
