"""
A somewhat random collection of useful functions that are intended to be imported into other programs.

The 'main()' function is useful just to TEST these in stand-alone mode.

MF Feb 2018
"""

def get_textfile_from_web(file_url, encoding_scheme="utf-8"):
    """
    Call this function to get any TEXT file from the internet using a http 'get' request.

    :param file_url: The address of the file
    :param encoding_scheme: The text encoding scheme. Default is 'utf-8'
    :return: A string representing the file
    """
    try:
        import httplib2
        # The request method gives us http header information and the content as a bytes object.
        h = httplib2.Http(".cache")
        headers, body = h.request(file_url)

        # We don't know what we're getting. The content-type header might give us a clue. In this example
        # I'm just going to assume that we can correctly decode utf-8 (the default). I can do this because I know that
        # the file is just a short 'plain text' speech so I know that there won't be any oddities in there. This
        # is often a bit of a gamble for, as we know, there is no such thing as 'plain text'.

        # Make a list of lines by splitting on the newline character.
        body = body.decode(encoding_scheme)

        # Print the results
        print("Request for {} returned status of {}."
              .format(file_url, headers['status']))

        return (headers, body)

    except Exception as e:
        print(e)

def count_items_in_collection(collection):
    """
    Create a dictionary and count the occurrences of each item.
    If an item already exists in the dictionary, add 1 to its counter
    otherwise set a counter for to to an initial value of 1

    :param collection: The bunch of things to be counted.
    :return: A dictionary containing the counts
    """

    counts = {}
    for item in collection:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1

    return counts


def main():
    """
    This is for TEST only. It grabs a sample file, chops it up and counts the words.

    :return: Nothing
    """
    FILE_URL = "http://mf2.dit.ie/gettysburg.txt"

    textfile = get_textfile_from_web(FILE_URL)[1]
    textfile = textfile.strip().lower().split()

    print("Counts: {}".format(count_items_in_collection(textfile)))

if __name__ == "__main__":
    main()

