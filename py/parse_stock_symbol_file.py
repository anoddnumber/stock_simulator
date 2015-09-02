def parseLine(line):
    str = 'File Creation Time'
    lenth = len(str)
    if line == '' or line[:18] == str:
        return None
    index = line.find(' - ')
    if index > 0:
        return line[0:index].replace("|", ":") + ","
    return None
    
if __name__ == "__main__":    
    symbols = open('../stock_symbols.txt', 'r')
    newFile = open('../parsed_symbols.txt', 'w')
    
    newFile.write("{\n")
    
    for i, line in enumerate(symbols):
        if i == 0:
            continue
        parsedLine = parseLine(line)
        if parsedLine is not None:
            newFile.write(parsedLine + '\n')
    
    newFile.write("}")
    symbols.close()
    newFile.close()