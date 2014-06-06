__author__ = 'claire'
import string
import sys
import re
import subprocess
import zipfile
import os

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML


WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'


def get_docx_text(path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        texts = [node.text
                 for node in paragraph.getiterator(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))

    return '\n\n'.join(paragraphs)

def binary2utf8(infile):
    text = open(infile, 'rb').read()
   # text = text.replace(u'\ufeff', ' ')  #replace with space
    return text


def sentencecount(text):
    splitter=re.compile('\r|\.\s|\?\s|!\s')
    #text= re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", text)  # remove digits
    text= re.sub('\d','',text)
    sentences=re.split(splitter,text)
    sentences=[s for s in sentences if s!=''] #remove blanks
    print 'no. of sentences:', len(sentences)


def wordcount(text):
    exclude = set(string.punctuation)
    text=text.replace('\r',' ')
    x=''.join(ch for ch in text if ch not in exclude) #remove punctuation
    #x= re.sub("^\d+\s|\s\d+\s|\s\d+$|\s\d+,\d+|\s\d+\.\d+", " ", x)  # remove digits
    x= x.lower().split()
    print 'no. of words:',len(x)
    #print 'set of words:',len(set(x))

    #print re.split('w')


def parse_text(filename):
    """
    use tika to turn file into utf8 string
    :param filename: name of file to scrape
    :return: string of text contained it file
    """
    cmd="java -jar /Users/claire/Desktop/tika-app-1.5.jar --text "+filename
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    output, errors = p.communicate()
    return output


if __name__ == "__main__":

    file='trados_test/trados_testing_6.docx'
    #file='test.txt'
    #file=sys.argv[1]
    file= os.path.abspath(file)
    print file
    text=parse_text(file)
    print text
    wordcount(text)
    sentencecount(text)
