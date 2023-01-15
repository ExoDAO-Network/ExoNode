import feedparser
import xml.etree.ElementTree as ET

txt = open('/Users/yoel/Downloads/subscriptions.txt', "r").read()

feed_urls = txt.split("\n")
feed_urls = [url for url in feed_urls if url != ""]

root = ET.Element("root")

for url in feed_urls:
    feed = feedparser.parse(url)
    feed_name = feed.feed.title
    feed_element = ET.SubElement(root, "feed")
    ET.SubElement(feed_element, "title").text = feed_name

    for entry in feed.entries:
        print(entry.keys())
        #entry_element = ET.SubElement(root, "entry")
        entry_element = ET.SubElement(feed_element, "entry")
        ET.SubElement(entry_element, "title").text = entry.title
        ET.SubElement(entry_element, "link").text = entry.link
        try:
            ET.SubElement(entry_element, "description").text = entry.description
        except:
            print("no description")
        try:
            ET.SubElement(entry_element, "published").text = entry.published
        except:
            print("no published")

tree = ET.ElementTree(root)
tree.write("articles.xml")

