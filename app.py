#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
from flask import Flask, render_template, request
import os
import urllib2
import json

# Charles Weng, Taylor Wong
# SoftDev2 pd7
# 06: Ay Mon, Go Git It From Yer Flask
# 2018-02-27


'''
================================================================================
                                set up & functions
================================================================================
'''

c = MongoClient('lisa.stuy.edu', 27017)
db = c[u'+X米X+']
p = db['pokedex']
url = 'https://raw.githubusercontent.com/Biuni/PokemonGO-Pokedex/master/pokedex.json'


# does data already exist
if(p.count() == 0):
    resp = urllib2.urlopen(url)
    dex = json.loads(resp.read())
    # print dex
    for poke in dex['pokemon']:
        p.insert_one(poke)


# searches by type
def find_t(t):
    d = p.find({"type": t})
    return d


# searches by weaknesses
def find_w(w):
    d = p.find({"weaknesses": w})
    return d


# searches by type and weaknesses
def find_tw(t, w):
    d = p.find({"$and": [{"type": t}, {"weaknesses": w}]})
    return d


# searches by average spawns
def find_s(s):
    d = p.find({"avg_spawns": {"$lt": s}})
    return d


'''
================================================================================
                                    tests
================================================================================
'''

# pokedex tests
if(False):
    find_t('Water')
    find_w('Fire')
    find_tw('Grass', 'Poison')
    find_s(2)


'''
================================================================================
                                    app stuffs
================================================================================
'''

app = Flask(__name__)
app.secret_key = os.urandom(32)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/process', methods=["POST"])
def do_stuffs():
    op = request.form.get('option')
    inputt = request.form.get('input')
    if op == 'type':
        result = find_t(inputt)
    elif op == 'weakness':
        result = find_w(inputt)
    else:
        result = find_s(int(inputt))
    if result.count() == 0:
        return render_template("results.html", message="no pokemon found")
    else:
        final = []
        for pokemon in result:
            final.append(pokemon)
        print len(final)
        return render_template('results.html', message="your " + op + " input returned these pokemon", list=final)


if __name__ == "__main__":
    app.debug = True
    app.run()
