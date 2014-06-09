__author__ = 'claire'
import string
import re
import subprocess
import os


def segmentcount(text):
    splitter = re.compile('\r|\.\s|\?\s|!\s')
    # text= re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", text)  # remove digits
    text = re.sub('\d', '', text)
    segments = re.split(splitter, text)
    segments = [s for s in segments if s != '']  # remove blanks
    return segments


def wordcount(text):
    '''
    split text string into words
    :param text: string of text
    :return: list of words in text
    '''
    replace_punctuation = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
    text = text.translate(replace_punctuation)
    return text.split()


def parse_text(filename):
    """
    use tika to turn file into utf8 string
    :param filename: name of file to scrape
    :return: string of text contained it file
    """
    cmd = "java -jar /Users/claire/Desktop/tika-app-1.5.jar --text " + filename
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, errors = p.communicate()
    print errors  # debug
    return output


def main(f):
    '''
    for testing
    :param f: filename
    :return: list of words and segments
    '''
    # file='test.txt'
    # file=sys.argv[1]
    file = os.path.abspath(f)
    print file
    text = parse_text(file)
    print text
    words = wordcount(text)
    print 'no. of words:', len(words)
    segments = segmentcount(text)
    print 'no. of segments:', len(segments)
    return words, segments


def quote(w, pair):
    '''
    return quote based on word count and language pair
    ?currency
    language pair lookup from an excel sheet (maybe)

    :param w: words
    :param pair: rate
    :return: quote
    '''
    pass


if __name__ == "__main__":
    file = 'trados_test/trados_segment_test.docx'
    # file='test.txt'
    #file=sys.argv[1]
    file = os.path.abspath(file)
    print file
    text = parse_text(file)
    print text
    words = wordcount(text)
    print 'no. of words:', len(words)
    segments = segmentcount(text)
    print 'no. of segments:', len(segments)


    # TODO read rates from file