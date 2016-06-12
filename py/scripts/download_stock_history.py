import urllib2


# global f

url_part1 = 'http://ichart.finance.yahoo.com/table.csv?s='
url_part2 = ''

print "Starting"

f = open('./../../static/parsed_symbols.json', 'r')
file_content = f.readlines()
count = 1;
print "About %d tickers will be downloaded" % len(file_content)

for line in file_content:
    print "line: " + str(line)
    try:
        ticker = line[1: line.index('"', 1)]  # from the first " (quote) to the 2nd " is the ticker symbol
    except:
        print "failed to download line: " + str(line)
        continue

    # ticker = ticker.strip()
    url = url_part1 + ticker + url_part2

    try:
        # This will cause exception on a 404
        response = urllib2.urlopen(url)

        print "Downloading ticker %s (%d out of %d)" % (ticker, count, len(file_content))

        count = count + 1
        history_file = open(ticker + '.csv', 'w')
        history_file.write(response.read())
        history_file.close()

    except Exception, e:
        pass

f.close()