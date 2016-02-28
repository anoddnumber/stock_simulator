def parse_line(line):
    string = 'File Creation Time'
    if line == '' or line[:18] == string:
        return None
    index = line.find(' - ')
    if index > 0:
        return '"' + line[0:index].replace('|',  '":"') +  '"'
    return None
    
if __name__ == "__main__":    
    symbols = open('../../stock_symbols.txt', 'r')
    newFile = open('../../static/parsed_symbols.json', 'w')
    
    newFile.write("{\n")

    lastLine = None
    for i, line in enumerate(symbols):
        if i == 0:
            continue
        parsedLine = parse_line(line)
        if parsedLine is not None:
            if lastLine is not None:
                newFile.write(lastLine + ',\n')
            lastLine = parsedLine
    newFile.write(lastLine + '\n')
    newFile.write("}")
    symbols.close()
    newFile.close()