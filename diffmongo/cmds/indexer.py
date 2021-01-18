# -* coding: utf-8 -*-

from pymongo import MongoClient
from xxhash import xxh64
import bson
import csv
import logging

MONGODB_UNIQKEY = '_id'


class MongoIndexer:
    """Indexer class generates CSV file with indexes of database collections and BSON files that speed up incremental DB updates"""
    def __init__(self):
        pass

    def indexcoll(self, host, port, dbname, collname, id=MONGODB_UNIQKEY, output='table.csv'):
        client = MongoClient(host=host, port=port)
        db = client[dbname]
        coll = db[collname]
        if output is not None:
            f = open(output, 'w', encoding='utf8')
            writer = csv.DictWriter(f, fieldnames=['id', 'hash'])
            writer.writeheader()
        else:
            f = None
        n = 0
        results = {}
        for o in coll.find_raw_batches():
            n += 1
            rows = []
            nx = 0
            for r in bson.decode_iter(o):
                nx += 1
                if id != MONGODB_UNIQKEY:
                    del r[MONGODB_UNIQKEY]
                rh = xxh64(bson.BSON.encode(r)).hexdigest()
                row = {'id' : str(r[id]), 'hash' : rh}
                results[row['id']] = rh
                if f:
                    rows.append(row)
            if f:
                writer.writerows(rows)
            logging.info('Processed bson batch %d with %d records' % (n, nx))
        if f:
            f.close()
        return results


    def indexbson(self, bsonfilename, id='_id', output='table.csv'):
        filein = open(bsonfilename, 'rb')
        if output is not None:
            f = open(output, 'w', encoding='utf8')
            writer = csv.DictWriter(f, fieldnames=['id', 'hash'])
            writer.writeheader()
        else:
            f = None
        nx = 0
        results = {}
        for r in bson.decode_file_iter(filein):
            nx += 1
            rh = xxh64(bson.BSON.encode(r)).hexdigest()
            row = {'id' : str(r[id]), 'hash' : rh}
            results[row[id]] = hash
            if f:
                writer.writerow(row)
        logging.info('Processed bson with %d records' % (nx))
        filein.close()
        if f:
            f.close()
        return results
