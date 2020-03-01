import feedparser
import csv

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
RSS_URL = 'https://ultrastar-es.org/en/canciones/rss/1186691/b0a1f6ba6fbf8b556f15ac0fe0c3e1146814be67a609cdf49faa09e099a895c3'

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
    writer.writerow({'title': title, 'language': language, 'year': year, 'album': album, 'song_type': song_type, 'torrent': torrent})

