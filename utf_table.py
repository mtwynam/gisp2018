'''Print Character table

Attempts to output representation of encoded characters in decimal range supplied by user. Encodings output determined
by list. Prints decimal value, hex equivalent, printable character (glyph) if possible and representation as bytes
object, which may render as "b'<glyph>'" or "b'<hex value>[<hex value>]...'" Bytes object can be represented as more
than one hex value.
'''

encodings = ['utf-8', 'ascii', 'latin_1', 'cp1252']
file_handles = []

for i in range(len(encodings)):
    try:
        # Note that we are opening the output files as binary because we are writing out bytes
        # not strings
        file_handles.append(open(encodings[i] + ".txt", "wb"))
    except IOError as e:
        print(e)
        quit()
    except IndexError as e:
        print(i, e)
        quit()

top_num = int(input("Enter max decimal : "))

for dec_num in range(top_num):
    print("| {} {} -".format(dec_num, hex(dec_num)), end="")
    for i in range(len(encodings)):
        try:
            # my_char is a bytes object
            # In this case we take a decimal number and compute its representation based on the value of encoding.
            # We then store the representation in bytes
            my_char = chr(dec_num).encode(encodings[i])
            file_handles[i].write(my_char)

            # my_print_char is a str object
            # In this case, we take a representation in bytes and decode it back to a string (a sequence of
            # unicode values)
            my_print_char = my_char.decode(encodings[i])

            # We make exceptions in the display of the tab, linefeed and carriage return characters because
            # they screw up the output formatting
            if dec_num == 9:
                my_print_char = 'TAB'
            if dec_num == 10:
                my_print_char = 'LF'
            if dec_num == 13:
                my_print_char = 'CR'
        except UnicodeEncodeError as e:
            # If we can't compute a representation it will be because it doesn't make sense. For example,
            # there are no valid ascii values beyond decimal 127 (hex 7f).
            my_char = ''
            my_print_char = 'UNDEF'
        print("- {}: {} {} -".format(encodings[i], my_print_char, my_char), end="")

    print("- |")

for i in range(len(encodings)):
    file_handles[i].close()
