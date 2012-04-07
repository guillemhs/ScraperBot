#!/usr/bin/env python
# -*- coding: iso8859-1 -*-

# Copyright (C) 2004/08/20-25, Iñigo Serna <inigoserna@terra.es>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#
# DESCRIPTION:
#   a simple python script to retrieve news from the
#   http://news.google.com service.
#   Supported feeds: es, fr, de, it, nz, au, in, ca, uk, us
#   Can export to: rss2 xml and html files
#
# REQUIREMENTS:
#   It only works with Python 2.3+
#   The unique external dependancy is BeautifulSoup. which can be
#   downloaded from http://www.crummy.com/software/BeautifulSoup
#
# TODO:
#   - any ideas?


import os
import sys
import datetime
import time
import re
import urllib
import optparse

from bs4 import BeautifulSoup
from xml.sax.saxutils import escape


######################################################################
# default values
country = 'es'

# define some variables
PROGNAME = sys.argv[0]
AUTHOR = u'Iñigo Serna'.encode('utf-8')
VERSION = '0.3'

URL_BASE = 'http://news.google.com'
OUTPUT_HTML = 'news-%s-%s.html'
OUTPUT_RSS = 'news-%s-%s.xml'

CSS = """<style type="text/css">
  body { color: black; background: white; }
  a { color : #003399; text-decoration : none; }
  a:hover { color : #339900; text-decoration : none; }
  a.main { font-size : 100%; }
  span.text { font-size : 100%; }
  span.data { color : #666666; font-size : 80%; }
  a.other { color : #003366; font-size : 75%; }
  a.other:hover { color : #339900; font-size : 75%; }
</style>"""

urllib.URLopener.version = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0; T312461)'
urllib.FancyURLopener.prompt_user_passwd = lambda self, host, realm: (None, None)

categories = ['w', 'n', 'b', 't', 's', 'e', 'm']

LANGS = { 'nz': 'en', 'au': 'en', 'ca': 'en', 'in': 'en', 'uk': 'en', 'us': 'en',
          'es': 'es', 'fr': 'fr', 'de':'de', 'it': 'it' }
cats = {
    'nz': ('world', 'New Zealand', 'business', 'technology',
           'sports', 'entertainment', 'health'),
    'au': ('world', 'Australia', 'business', 'technology',
           'sports', 'entertainment', 'health'),
    'ca': ('world', 'Canada', 'business', 'technology',
           'sports', 'entertainment', 'health'),
    'in': ('world', 'India', 'business', 'technology',
           'sports', 'entertainment', 'health'),
    'uk': ('world', 'United Kingdom', 'business', 'technology',
           'sports', 'entertainment', 'health'),
    'us': ('world', 'USA', 'business', 'technology',
           'sports', 'entertainment', 'health'),
    'es': (u'internacional', u'España', u'economía', u'ciencia',
           u'deportes', u'entretenimiento', u'salud'),
    'fr': (u'international', u'France', u'économie', u'science',
           u'sports', u'culture', u'santé'),
    'de': (u'international', u'Deutschland', u'wirtschaft', u'wissen',
           u'sport', u'unterhaltung', u'gesundheit'),
    'it': (u'dal mondo', u'Italia', u'economia', u'scienze',
           u'sport', u'spettacolo', u'salute'),
    'common': ('world', 'national', 'business', 'technology',
               'sports', 'entertainment', 'health')
}

date_res = {
    'en': re.compile('(?P<num>\d+) (?P<val>hour|minute)(s)? ago', re.I),
    'es': re.compile('hace (?P<num>\d+) (?P<val>hora|minuto)(s)?', re.I),
    'fr': re.compile('(publi.+ depuis|il y a) (?P<num>\d+) (?P<val>heure|minute)(s)?', re.I),
    'de': re.compile('vor (?P<num>\d+) (?P<val>stunde|minute)(n)?', re.I),
    'it': re.compile('(?P<num>\d+) (?P<val>ore|minuti) fa', re.I)
}

months_d = {
    'en': ['january', 'february', 'march', 'april', 'may', 'june',
           'july', 'august', 'september', 'october', 'november', 'december'],
    'es': ['enero', 'febrero', 'marzo', 'abril', 'mayo' 'junio',
           'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],
    'fr': ['janvier', 'février', 'marche', 'avril', 'mai', 'juin',
           'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'],
    'de': ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
           'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
    'it': ['gennaio', 'febbraio', 'procedere', 'aprile', 'maggio', 'giugno',
           'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
}
months_re = re.compile('(?P<day>\d+)(\.)? (?P<month>\S+)(\.)? (?P<year>\d+)', re.I)


######################################################################
def purify_link(link):
    link = link.replace('.3a', ':').replace('.2e', '.').replace('.2f', '/')
    link = link.replace('.5f', '_').replace('.2d', '-').replace('.3f', '?')
    link = link.replace('.26', '&').replace('.3d', '=')
    link = link.replace('.3A', ':').replace('.2E', '.').replace('.2F', '/')
    link = link.replace('.5F', '_').replace('.2D', '-').replace('.3F', '?')
    link = link.replace('.26', '&').replace('.3D', '=')
#     link = link.replace('%3a', ':').replace('%2e', '.').replace('%2f', '/')
#     link = link.replace('%5f', '_').replace('%2d', '-').replace('%3f', '?')
#     link = link.replace('%26', '&').replace('%3d', '=')
#     link = link.replace('%3A', ':').replace('%2E', '.').replace('%2F', '/')
#     link = link.replace('%5F', '_').replace('%2D', '-').replace('%3F', '?')
#     link = link.replace('%26', '&').replace('%3D', '=')
    link = urllib.unquote(link)
    return link


######################################################################
def write_html(filename, country_name, cat, entries):
    country_name = country_name.encode('utf-8', 'strict')
    cat = cat.encode('utf-8', 'strict').capitalize()
    f = open(filename, 'w')
    buf = """<html>
<head>
<meta HTTP-EQUIV="content-type" CONTENT="text/html; charset=UTF-8">
<title>Google News - %s - %s</title>
<hr width= 90%% />
%s
</head>
<body>
<h1><center>%s - %s</center></h1>
""" % \
    (country_name, cat, CSS, cat, country_name)

    for entry in entries:
        buf += entry.html()
        buf += '  <hr width=90% />  <br />'

    buf += """</body>
</html>"""
    f.write(buf)
    f.close()


def write_rss(filename, country_name, cat, entries):
    country_name = country_name.encode('utf-8', 'strict')
    cat = cat.encode('utf-8', 'strict').capitalize()
    if time.daylight:
        tz = '%2.2d%2.2d' % divmod(time.altzone, 3600)
    else:
        tz = '%2.2d%2.2d' % divmod(time.timezone, 3600)
    if tz[0] != '-':
        tz = '+' + tz
    f = open(filename, 'w')

    buf = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
<channel>
  <title>%s</title>
  <link>%s</link>
  <description>%s</description>
  <lastBuildDate>%s</lastBuildDate>
  <language>%s</language>
  <generator>%s</generator>
""" % \
    ('Google News - %s - %s' % (country_name, cat),
     URL_BASE2,
     'Google News - %s - %s' % (country_name, cat),
     datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S ') + tz,
     lang,
     ('%s, by %s' % (PROGNAME, AUTHOR)))

    for entry in entries:
        date_txt = entry['date'].strftime('%a, %d %b %Y %H:%M:%S ') + tz
        buf += """  <item>
    <title>%s</title>
    <link>%s</link>
    <guid>%s</guid>
    <pubDate>%s</pubDate>
    <description>\n%s\n    </description>
  </item>
""" % (entry['title'], escape(entry['link']), escape(entry['link']),
       date_txt, escape(entry.html()))

    buf += """</channel>
</rss>"""

    f.write(buf)
    f.close()


######################################################################
class Entry(dict):
    def __init__(self):
        dict.__init__(self)
        self.title = ''
        self.link = ''
        self.img = ''
        self.source = ''
        self.date = ''
        self.txt = ''
        self.other_links = []
        self.all_links = ''


    def __str__(self):
        buf = """Title: %(title)s'
Source: %(source)s
Date: %(date)s
Image: %(img)s
Link: %(link)s
Links: %(all_links)s
Contents: %(txt)s
Other Links:
""" % self
        for s, l in self['other_links']:
            buf += '\t' + s + ' => ' + l + '\n'
        return buf


    def html(self):
        buf = '<table border="0" width="100%" valign="top" cellpadding="5" cellspacing="0"><tbody><tr>\n'
        if self['img']:
            buf += '<td width="80" align="center" valign="top"><img src="%s" width="125px">' % self['img']
#             buf += '<td width="80" align="center" valign="top"><img src="%s">' % self['img']
        buf += '<td valign="top">\n'
        buf += '<a href="%s" class="main">%s</a><br />' % (self['link'], self['title'])
        d = self['date']
        if d.time() == datetime.time(0, 0, 0, 0):
            buf += '<span class="data">%s - %s</span><br />\n' % \
                   (self['source'], d.strftime('%A, %d %B %Y'))
        else:
            buf += '<span class="data">%s - %s</span><br />\n' % \
                   (self['source'], d.strftime('%A, %d %B %Y  %H:%M'))
        buf += '<span class="text">%s</span><br />\n' % (self['txt'],)
        for s, l in self['other_links']:
            buf += '<a href="%s" class="other">%s</a><br />' % (l, s)
        buf += '<a href="%s" class="other">All links</a><br />' % self['all_links']
        buf += '</td>\n'
        buf += '</tr></tbody></table>'
        return buf


######################################################################
def parse_entry(ent):
    entry = Entry()
    # image
    try:
        img = ent.first('img')['src']
    except:
        img = ''
    if img:
        img = img.split('imgurl=')[-1]
        img = 'http://' + img
#         img = purify_link(img)[:-4]
    entry['img'] = img

    body = ent.fetch('td')[-1]
    ahrefs = body.fetch('a')
    # title & main link
    try:
        a = ahrefs[0]
    except IndexError:
        return None
    entry['title'] = a.contents[0].string
    try:
        entry['title'] += a.contents[1].string # "..."
    except IndexError:
        pass
    st = a['href'].find('http')
    entry['link'] = a['href'][st:]
    # other links
    entry['other_links'] = []
    for a in ahrefs[1:3]:
        st = a['href'].find('http')
        link = a['href'][st:]
        link = purify_link(link)
        src = str(a.contents[0])
        entry['other_links'].append((src, link))
    # all links
    a = ahrefs[-1]
    entry['all_links'] = a['href']
    # source and date
    try:
        # get text
        try:
            txt = body.fetch('font')[2].contents[0].string
        except IndexError:
            txt = ''
        try:
            if txt[-1] == ' ':
                txt = txt[:-1]
                txt += body.fetch('font')[2].contents[1].string # "..."
        except IndexError:
            pass
        entry['txt'] = txt
        # get source
        bb = str(body.fetch('font')[1].contents[0])
        st = bb.find('>') + 1
        end = bb.find('&nbsp;')
        entry['source'] = bb[st:end]
        # get date
        now = datetime.datetime.now()
        date_txt = str(ent.fetch('nobr')[0].contents[0])
        res = date_re.match(date_txt)
        if res:
            if res.group('val')[0] in ('hour', 'hora', 'heure', 'stunde', 'ore'):
                h = int(res.group('num'))
                m = 0
            else:
                h = 0
                m = int(res.group('num'))
            entry['date'] = now + datetime.timedelta(hours= -h, minutes= -m)
        else:
            res = months_re.match(date_txt)
            if res:
                d = int(res.group('day'))
                month_str = res.group('month').lower()
                y = int(res.group('year'))
                try:
                    m = months.index(month_str) + 1
                except ValueError:
                    months2 = [m[:3] for m in months]
                    try:
                        m = months2.index(month_str) + 1
                    except ValueError:
                        m = now.month
                entry['date'] = datetime.datetime(year=y, month=m, day=d)
            else:
                entry['date'] = datetime.datetime.now()
    except:
        if options.verbose:
            print '+' * 50
            print body.contents[2]
        raise

    return entry


######################################################################
def parse_category(cat):
    # read url
    page = urllib.urlopen(URL_CAT % cat).read()
    bs = BeautifulSoup(page)
    ents = bs.fetch('table')
    # only select the articles
    ents = ents[7:-2]
    cat2 = cats[country][categories.index(cat)]
    if options.verbose:
        print 'Category: %s - %d articles' % \
                (cat2.encode('utf-8'), len(ents))
    # parse entries
    entries = []
    for ent in ents:
        entry = parse_entry(ent)
        if entry != None:
            entries.append(entry)
    # sort entries by date
    entries.sort(lambda e1, e2: cmp(e1['date'], e2['date']))
    entries.reverse()
    return entries


######################################################################
def main():
    nation = cats[country][1]
    if options.verbose:
        print 'Google News - %s' % nation.encode('utf-8')
    for cat in categories_to_get:
        entries = parse_category(cat)
        idx = categories.index(cat)
        cat_translated = cats[country][idx]
        cat2 = cats['common'][categories.index(cat)]
        if options.html:
            if options.html_path != None:
                filename = os.path.join(options.html_path,
                                        OUTPUT_HTML % (country, cat2))
            else:
                filename = OUTPUT_HTML % (country, cat2)
            write_html(filename, nation, cat_translated, entries)
        if options.rss:
            if options.rss_path != None:
                filename = os.path.join(options.rss_path,
                                        OUTPUT_RSS % (country, cat2))
            else:
                filename = OUTPUT_RSS % (country, cat2)
            write_rss(filename, nation, cat_translated, entries)


######################################################################
if __name__ == '__main__':
    # handle args & options
    country_help = ' | '.join(LANGS.keys())

    cats_help = ', '.join(['%c: %s' % (c, c2) for c, c2 in zip(categories, cats['common'])])
    version_help = '%prog v' + VERSION + ' - (C) 2004, by ' + AUTHOR

    usage = """usage: %prog [options] [country]

where:
\tcountry = """ + country_help + """
\tdefault is '""" + country + """'."""
    parser = optparse.OptionParser(usage=usage,
                                   version=version_help)
    parser.add_option('-c', '--categories',
                      action='store', dest='categories', type='string',
                      default='wnbtsem',
                      help='select categories to retrieve news (' + \
                      cats_help + '. f.e. "wts", default=wnbtsem)',
                      metavar='CATEGORIES')
    parser.add_option('-n', '--no-rss',
                      action='store_false', dest='rss', default=True,
                      help='don\'t create rss feed file (default=YES)')
    parser.add_option('--rss-path',
                      action='store', dest='rss_path', type='string',
                      help='write rss feed to PATH (default=current directory)',
                      metavar='FILE')
    parser.add_option('-w', '--no-html',
                      action='store_false', dest='html', default=True,
                      help='don\'t create html file (default=YES)')
    parser.add_option('--html-path',
                      action='store', dest='html_path', type='string',
                      help='write html output to PATH (default=current directory)',
                      metavar='FILE')
    parser.add_option('-q', '--quiet',
                      action='store_false', dest='verbose', default=True,
                      help='don\'t output messages to terminal (default=YES)')

    (options, args) = parser.parse_args()
    # parse args
    if len(args) == 0:
        pass # country defined by default
    elif len(args) == 1:
        if args[0] in LANGS.keys():
            country = args[0]
        else:
            parser.error('"%s" is not a valid country.' % args[0])
    else:
        parser.error('Invalid number of arguments.')
    # validate categories
    for c in options.categories:
        if c not in categories:
            parser.error('"%s" is not a valid category.' % c)
    # set country values
    categories_to_get = list(options.categories)
    lang = LANGS[country]
    date_re = date_res[lang]
    months = months_d[lang]
    URL_BASE2 = URL_BASE + '/news?ned=%s' % country
    URL_CAT = URL_BASE2 + '&topic=%s'
    # process
    main()