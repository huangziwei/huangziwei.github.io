from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import datetime

# Read the content of index.html
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Initialize the RSS XML tree
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Ziwei Huang"
ET.SubElement(channel, "link").text = "https://hzwei.dev"
ET.SubElement(channel, "description").text = "SciDev @ Herti AI, Uni-Tü"

# Find the #news section
news_section = soup.find("section", {"id": "news"})
if news_section:
    # Loop through each blog post
    for details in news_section.find_all("details"):
        title = details.find("h4").encode_contents().decode("utf-8")
        date_time = details.find("time")["datetime"]
        description = details.find("p").encode_contents().decode("utf-8")

        # Add the blog post to the RSS feed
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = title
        ET.SubElement(item, "link").text = f"https://hzwei.dev#{details['id']}"
        ET.SubElement(item, "guid", isPermaLink="false").text = details["id"]
        ET.SubElement(item, "author").text = "Ziwei Huang"
        ET.SubElement(item, "pubDate").text = datetime.datetime.fromisoformat(date_time).strftime('%a, %d %b %Y %H:%M:%S GMT')
        ET.SubElement(item, "description").text = description

# Generate the RSS XML file
tree = ET.ElementTree(rss)
tree.write("rss.xml", encoding="utf-8", xml_declaration=True)
