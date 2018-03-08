import urllib
import urllib.request
import re
import os
import string

try:
	from bs4 import BeautifulSoup
except ImportError:
	from BeautifulSoup import BeautifulSoup


def write_text(col,target):
    col=re.sub("\d+", "#", col)
    col=col.split('#')
    no_sentences=0
    for l in range(len(col)):
        line=col[l].strip()
        if line!="":
            target.write(col[l].strip())
            target.write("\n")
            no_sentences+=1
    return no_sentences


def get_html(url_link):
	with urllib.request.urlopen(url_link) as url:
		return url.read()


def scrap_doc(url_chapter,name,book_name):
    html=get_html(url_chapter)
    soup = BeautifulSoup(html)
    for tag in soup.find_all('a'):
        tag.replaceWith('')
    tds = soup.find_all('td')
    col=tds[0].text
    folder=book_name[:-4]
    target = open("dataset/Bible/Hebrew/"+folder+"/"+name+".txt", 'w')
    write_text(col,target)
    print(name)


def get_chapter_links(link):
    directory="dataset/Bible/Hebrew/"+link[:-4]
    if not os.path.exists(directory):
        os.makedirs(directory)
    print (directory)
    book_name=link
    url="http://sacred-texts.com/bib/tan/"+link
    html=get_html(url)
    soup = BeautifulSoup(html)
    all_links = [tag['href'] for tag in soup.select('p a[href]')]
    for link in all_links:
        scrap_doc("http://sacred-texts.com/bib/tan/"+link,link,book_name)
    return book_name
    # print(h_tag.find_next_siblings())
    # for br in h_tag.find_next_siblings():
    #     link = br.get('href')
    #     if link!=None:
    #         print(link)


def get_links_books():
    directory="dataset/Bible/Hebrew/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    url="http://sacred-texts.com/bib/tan/index.htm"
    html=get_html(url)
    soup = BeautifulSoup(html)
    h_tag=soup.find('hr')
    book=[]
    # print(h_tag.find_next_siblings())
    for br in h_tag.find_next_siblings():
        link=br.get('href')
        if link!=None:
            book.append(get_chapter_links(link))
    return book

if __name__ == "__main__":
    book_list=get_links_books()
    print(book_list)
