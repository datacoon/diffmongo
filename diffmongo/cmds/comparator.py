# -* coding: utf-8 -*-

from pymongo import MongoClient
from xxhash import xxh64
import bson
import csv
import logging
from pprint import pprint


from .indexer import MongoIndexer
from datadiff.diff import compare_index

class MongoComparator:
    """Comparator class used to identify differences between tables"""
    def __init__(self):
        pass

    def compare(self, fromhost, fromport, fromdb, fromcoll, tohost, toport, todb, tocoll, idkey, output):
        indexer = MongoIndexer()
        right_index = indexer.indexcoll(fromhost, fromport, fromdb, fromcoll, idkey, output=None)
        left_index = indexer.indexcoll(tohost, toport, todb, tocoll, idkey, output=None)
        results = compare_index(left_index, right_index)
        if output:
            f = open(output, 'w', encoding='utf8')
            writer = csv.DictWriter(f, fieldnames=['idkey', 'key', 'action'])
            writer.writeheader()
            for action in ['a', 'd', 'c']:
                for key in results[action]:
                    writer.writerow({'idkey' : idkey, 'key' : key, 'action' : action})
            f.close()
            print('Generated %s file with list of actions' % (output))

    def apply(self, difffile, fromhost, fromport, fromdb, fromcoll, tohost, toport, todb, tocoll):
        f = open(difffile, 'r', encoding='utf8')
        reader = csv.DictReader(f)
        diffdata = {'a' : [], 'd' : [], 'c' : []}
        idkey = None
        for r in reader:
            idkey = r['idkey']
            diffdata[r['action']].append(r['key'])

        right = MongoClient(tohost, toport)
        r_db = right[todb]
        r_coll = r_db[tocoll]

        left = MongoClient(fromhost, fromport)
        l_db = left[fromdb]
        l_coll = l_db[fromcoll]

        n = 0
        for key in diffdata['d']:
            n += 1
            if n % 100 == 0:
                logging.info('Processed %d' % (n))
            r_coll.delete_one({idkey : key})

        for key in diffdata['a']:
            n += 1
            if n % 100 == 0:
                logging.info('Processed %d' % (n))
            record = l_coll.find_one({idkey : key})
            r_coll.insert_one(record)

        for key in diffdata['c']:
            n += 1
            if n % 100 == 0:
                logging.info('Processed %d' % (n))
            record = l_coll.find_one({idkey : key})
            del record['_id']
            r_coll.replace_one({idkey : key}, record)
        logging.info('Data updated. Total altered records %d' % (n))

