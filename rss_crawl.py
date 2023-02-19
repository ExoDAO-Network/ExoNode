import os
import feedparser
import xml.etree.ElementTree as ET

#File with URL to feeds
try:
    txt = open('subscriptions.txt', "r").read()
except:
    print ("Provide valid file with URLs to RSS feeds")
    
feed_urls = txt.split("\n")
feed_urls = [url for url in feed_urls if url != ""]

all_feed_elements = []

# iterate over the feed URLs and parse them
for url in feed_urls:
    feed = feedparser.parse(url)
    feed_name = feed.feed.title
    print(feed_name)
    feed_element = ET.Element("feed")
    ET.SubElement(feed_element, "title").text = feed_name

    # iterate over the entries in the feed and add them to the feed element
    for entry in feed.entries:
        print(entry.keys())
        entry_element = ET.SubElement(feed_element, "entry")
        try:
            ET.SubElement(entry_element, "title").text = entry.title
        except:
            print("no title")
        try:
            ET.SubElement(entry_element, "link").text = entry.link
        except:
            print("no link")
        try:
            ET.SubElement(entry_element, "description").text = entry.description
        except:
            print("no description")
        try:
            ET.SubElement(entry_element, "published").text = entry.published
        except:
            print("no published")

    # add the feed_element to the list of feed elements
    all_feed_elements.append(feed_element)

# create a new ElementTree with each feed_element as the root, and write it to the output file
with open("articles.xml", "wb") as f:
    for feed_element in all_feed_elements:
        # write the XML for the feed_element to the file
        f.write(ET.tostring(feed_element, encoding="iso-8859-1", xml_declaration=False, with_tail=False))




