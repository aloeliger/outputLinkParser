from rich.console import Console
from rich.table import Table
import argparse
import re

console = Console()

def splitListIntoEvents(lines, eventSize=6):
    return [lines[i:i+eventSize] for i in range(0, len(lines), eventSize)]

def parseWords(event):
    resultWords = []
    for line in event:
        lineTokens = re.split("\s", line)
        lineTokens = [token for token in lineTokens if token != '']
        lineTokens = lineTokens[1:] #get rid of the word count
        #we take the first word that isn't 0x00000000... unless that's the only thing in there
        word = '0x00000000'
        for token in lineTokens:
            if token != '0x00000000':
                word = token
                break
        resultWords.append(word)
    return resultWords

def parseCICADAHexString(eventWords, cicadaHexLocation=7):
    result = ''
    for i in range(4):
        result += eventWords[i][cicadaHexLocation+2]
    return result

def hexStringToDecimal(hexString):
    firstChar = int(hexString[0], 16)
    firstChar = firstChar << 4
    secondChar = int(hexString[1], 16)
    thirdChar = float(int(hexString[2],16))
    thirdChar = thirdChar * (2**-4)
    fourthChar = float(int(hexString[3],16))
    fourthChar = fourthChar * (2**-8)

    result = float(firstChar)+float(secondChar)+thirdChar+fourthChar
    return result

def main(args):
    with open(args.fileName) as theFile:
        fileContents = theFile.readlines()
        
    #the first few lines are blank or contain space marking information only
    fileContents = fileContents[args.headerLines:]

    #if we have incomplete events at the start, we can also get rid of those
    if args.skipLines != 0:
        console.log(f"Skipping the first {args.skipLines} link lines.")
        fileContents = fileContents[args.skipLines:]

    numLines = len(fileContents)
    excessEventLines = numLines % 6
    console.log(f"Number of lines: {numLines}")
    if excessEventLines != 0:
        console.log(f"The lines were not perfectly divisible by 6 (a standard CaloSummary event), I am discarding the last {excessEventLines} lines.")
        fileContents = fileContents[:-excessEventLines]
    numEvents = numLines//6
    console.log(f"Number of events: {numEvents}")

    events = splitListIntoEvents(fileContents)
    #console.print(events)

    resultTable = Table(title="CICADA Results")
    resultTable.add_column("Event #", justify='left', style='cyan', no_wrap=True)
    resultTable.add_column("CICADA (decimal)", justify='right', style='green')
    resultTable.add_column("CICADA (hex)", justify='right', style='green')
    resultTable.add_column("Event words")

    for index, event in enumerate(events):
        eventWords = parseWords(event)
        wordString = ' '.join(eventWords)
        cicadaHexString = parseCICADAHexString(eventWords, cicadaHexLocation=0)
        cicadaDecimal = hexStringToDecimal(cicadaHexString)
        cicadaDecimalString = str(cicadaDecimal)
        resultTable.add_row(f'{index}', cicadaDecimalString, cicadaHexString, wordString)
    console.print(resultTable)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check an output reference for the CICADA scores")
    
    parser.add_argument(
        '-f',
        '--fileName',
        required=True,
        nargs='?',
        help="file with output link hexes",
    )
    parser.add_argument(
        '--headerLines',
        default=3,
        type=int,
        nargs='?',
        help='Number of lines in the header describing links',
    )
    parser.add_argument(
        '-s',
        '--skipLines',
        default=0,
        type=int,
        nargs='?',
        help='Number of link lines to skip at the beginning due to incomplete events',
    )

    args = parser.parse_args()

    main(args)
