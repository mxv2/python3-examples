#!/usr/bin/env python3
import sys
import xml.sax.saxutils


def print_start():
    print("<table border='1'>")


def print_end():
    print("</table>")


def extract_fields(line):
    fields = []
    field = ""
    quote = None
    for c in line:
        if c in "\"'":
            if quote is None:  # start quoted string
                quote = c
            elif quote == c:  # end quoted string
                quote = None
            else:
                field += c  # other quote inside quoted string
            continue
        if quote is None and c == ",":  # end of a field
            fields.append(field)
            field = ""
        else:
            field += c  # accumulating a field
    if field:
        fields.append(field)  # add last field
    return fields


def print_line(line, color, maxwidth, format):
    print("<tr bgcolor='{}'>".format(color))
    fields = extract_fields(line)
    for field in fields:
        if not field:
            print("<td></td>")
        else:
            number = field.replace(",", "")
            try:
                x = float(number)
                print("<td align='right'>{number:{format}}</td>".format(
                    number=round(x), format=format)
                )
            except ValueError:
                field = field.title()
                field = field.replace(" And ", " and ")
                if len(field) <= maxwidth:
                    field = xml.sax.saxutils.escape(field)
                else:
                    field = "{0} ...".format(
                        xml.sax.saxutils.escape(field[:maxwidth])
                    )
                print("<td>{0}</td>".format(field))
    print("</tr>")


def print_usage():
    print("usage:")
    print("csv2html.py [maxwidth=int] [format=str] < infile.csv > outfile.html")
    print("\nmaxwidth is an optional integer; if specified, it sets the maximum")
    print("number of characters that can be output for string fields,")
    print("otherwise a default of 100 characters is used.")
    print("\nformat is the format to use for numbers; if not specified it")
    print("defaults to \".0f\".")


def process_options():
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h", "--help"):
            print_usage()
            return None, None

        maxwidth = None
        format = None
        for arg in sys.argv[1:]:
            opt_name, eq, opt_value = arg.partition("=")
            if opt_name == "maxwidth" and eq == "=":
                try:
                    maxwidth = int(opt_value)
                except ValueError:
                    print("error: maxwidth value should be int")
                    return None, None
            elif opt_name == "format" and eq == "=":
                format = opt_value
            else:
                print("error: unrecognized option {}".format(opt_name))
                return None, None
        return maxwidth or 100, format or ".0f"

    return 100, ".0f"


def main():
    maxwidth, format = process_options()
    if maxwidth is None or format is None:
        return

    print_start()
    count = 0
    while True:
        try:
            line = input()
            if count == 0:
                color = "lightgreen"
            elif count % 2 == 0:
                color = "white"
            else:
                color = "lightyellow"
            print_line(line, color, maxwidth, format)
            count += 1
        except EOFError:
            break
    print_end()


main()
