import feedparser
import csv
import hashlib
import sys
import bencodepy
import base64
from requests import get
import tempfile

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
RSS_URL = 'https://ultrastar-es.org/en/canciones/rss/1186691/b0a1f6ba6fbf8b556f15ac0fe0c3e1146814be67a609cdf49faa09e099a895c3'

def make_magnet_from_file(file, name) :
    metadata = bencodepy.decode_from_file(file)
    print(metadata)
    subj = metadata[b'info']
    hashcontents = bencodepy.encode(subj)
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest).decode()
    return 'magnet:?'\
             + 'xt=urn:btih:' + b32hash\
             + '&dn=' + name\
             + '&tr=' + metadata[b'announce'].decode()\
             + '&xl=' + str(metadata[b'info'][b'length'])

def download_file(url, file_name):
  req = get(url)
  file = open(file_name, 'wb')
  for chunk in req.iter_content(100000):
      file.write(chunk)
  file.close()

#rss = open("test.rss", "r+")
#feed = feedparser.parse(rss.read())
feed = feedparser.parse(RSS_URL, referrer='https://ultrastar-es.org', agent=USER_AGENT)
feed_entries = feed.entries

if (len(feed_entries) == 0):
  print('No entries available')
  quit()

with open('ultrastar_songs.csv', 'w', newline='') as csvfile:
  fieldnames = ['title', 'language', 'year', 'album', 'song_type', 'torrent']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()

  for entry in feed.entries:
    split = entry.title.split("#")
    title = split[0].strip()
    language = split[1].strip()
    year = split[3].strip()
    album = split[5].strip()
    if (len(split) > 7):
      song_type = split[7].strip()
    else:
      song_type = ""
    torrent = entry.links[0].href.strip()
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    download_file(torrent, temp_file.name)
#    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
    print(make_magnet_from_file(temp_file.name))
    writer.writerow({'title': title, 'language': language, 'year': year, 'album': album, 'song_type': song_type, 'torrent': torrent})
    break
