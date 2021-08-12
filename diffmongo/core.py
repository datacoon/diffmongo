#!/usr/bin/env python
# -*- coding: utf8 -*-
import click
import logging
from pprint import pprint

from .cmds.indexer import MongoIndexer
from .cmds.comparator import MongoComparator

# logging.getLogger().addHandler(logging.StreamHandler())
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)


def enableVerbose():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)


@click.group()
def cli1():
    pass


@cli1.command()
@click.option('--host', '-h', default='localhost', help="MongoDb hostname")
@click.option('--port', '-p', default=27017, help="MongoDb port")
@click.option('--db', '-d', default=None, help="Database name")
@click.option('--collection', '-c', default=None, help="Collection name")
@click.option('--idkey', '-i', default='_id', help="Unique records ID key")
@click.option('--output', '-o', default='table.csv', help="Output CSV file")
@click.option('--verbose', '-v', count=False, help='Verbose output. Print additional info')
def indexcoll(host, port, db, collection, idkey, output, verbose):
    """Index single collection"""
    if verbose:
        enableVerbose()
    acmd = MongoIndexer()
    acmd.indexcoll(host, int(port), db, collection, idkey, output)

@click.group()
def cli2():
    pass

@cli2.command()
@click.option('--fromhost', '-fh', default='localhost', help="Source MongoDb hostname")
@click.option('--fromport', '-fp', default=27017, help="Source MongoDb port")
@click.option('--fromdb', '-fd', default=None, help="Source database name")
@click.option('--fromcoll', '-fc', default=None, help="Source collection name")
@click.option('--tohost', '-th', default='localhost', help="Destination MongoDb hostname")
@click.option('--toport', '-tp', default=27017, help="Destination MongoDb port")
@click.option('--todb', '-td', default=None, help="Destination database name")
@click.option('--tocoll', '-tc', default=None, help="Destination collection name")
@click.option('--idkey', '-i', default='_id', help="Unique records ID key")
@click.option('--output', '-o', default='difftable.csv', help="Output CSV file")
@click.option('--verbose', '-v', count=False, help='Verbose output. Print additional info')
def compare(fromhost, fromport, fromdb, fromcoll, tohost, toport, todb, tocoll, idkey, output, verbose):
    """Compares to MongoDB collections and generates table of differences"""
    if verbose:
        enableVerbose()
    acmd = MongoComparator()
    acmd.compare(fromhost, fromport, fromdb, fromcoll, tohost, toport, todb, tocoll, idkey, output)

@click.group()
def cli3():
    pass

@cli3.command()
@click.option('--diffile', '-df', default='difftable.csv', help="File with actions list")
@click.option('--fromhost', '-fh', default='localhost', help="Source MongoDb hostname")
@click.option('--fromport', '-fp', default=27017, help="Source MongoDb port")
@click.option('--fromdb', '-fd', default=None, help="Source database name")
@click.option('--fromcoll', '-fc', default=None, help="Source collection name")
@click.option('--tohost', '-th', default='localhost', help="Destination MongoDb hostname")
@click.option('--toport', '-tp', default=27017, help="Destination MongoDb port")
@click.option('--todb', '-td', default=None, help="Destination database name")
@click.option('--tocoll', '-tc', default=None, help="Destination collection name")
@click.option('--verbose', '-v', count=False, help='Verbose output. Print additional info')
def apply(diffile, fromhost, fromport, fromdb, fromcoll, tohost, toport, todb, tocoll, verbose):
    """Apply diff table to the MongoDb collection"""
    if verbose:
        enableVerbose()
    acmd = MongoComparator()
    acmd.apply(diffile, fromhost, fromport, fromdb, fromcoll, tohost, toport, todb, tocoll)



cli = click.CommandCollection(sources=[cli1, cli2, cli3])

# if __name__ == '__main__':
#    cli()
