import string, httplib2

# The following are the strings which define the basic HTML document. Later on we will make an HTML 'span' element for
# each word with an appropriate font size set. The resulting collection of 'span's is sandwiched between these two basic
# strings to form the final document.
HTML_START_TEXT = "<!DOCTYPE html>\n<html>\n<head lang=\"en\">\n<meta charset=\"UTF-8\">\n<title>Tag Cloud Generator</title>\n</head>\n<body>\n<div style=\"text-align: center; vertical-align: middle; font-family: arial; color: white; background-color:black; border:1px solid black\">\n"
HTML_END_TEXT = "</div>\n</body>\n</html>"

# These are the min/max allowable font sizes for the words
MIN_FONT_SIZE = 20
MAX_FONT_SIZE = 200

# IRLs for source data
SPEECH_URL = "http://mf2.dit.ie/gettysburg.txt"
STOPWORDS_URL = "http://mf2.dit.ie/stopwords.txt"


def makeWordList(speech, stopWords):
    # Take each line and strip whitespace, punctuation and stop words. Also ignore words smaller than three chars as
    # they're likely to be stop words not on the list

    speech_list = []

    for line in speech:
        line = line.strip(string.whitespace).split()
        for word in line:
            word = word.lower()
            word = word.strip(string.punctuation)
            if (word not in stopWords) and (word not in string.punctuation) and (len(word) > 3):
                speech_list.append(word)

    return speech_list


def countWords(speech):
    # Count occurrences of each word
    counts = {}
    for word in speech:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts


def main():
    try:
        # Get speech and stop word files from the net and store in local cache
        h = httplib2.Http(".cache")
        speech_headers, speech = h.request(SPEECH_URL)
        stopwords_headers, stopwords = h.request(STOPWORDS_URL)

        speech = speech.decode().split("\n")
        stopwords = tuple(stopwords.decode().strip().split(','))

        speech = makeWordList(speech, stopwords)
        counts = countWords(speech)

        span_strings = ""

        for k, v in counts.items():
            # Make an html 'span' element for each word including font size. Size is set as frequency * min size. Max
            # size is the upper limit.
            span_string = "<span style=\"font-size: {}px\"> {} </span>\n".format(
                int(min(v * MIN_FONT_SIZE, MAX_FONT_SIZE)), k)
            span_strings += span_string

        # Make final html document and write it to local cache
        html_final = HTML_START_TEXT + span_strings + HTML_END_TEXT

        with open(".cache/tag_cloud.html", "w") as fh:
            fh.write(html_final)


    except httplib2.HttpLib2Error as e:
        print(e)


if __name__ == "__main__":
    main()
