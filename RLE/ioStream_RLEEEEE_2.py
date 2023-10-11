import sys

def encodeRLE(st, xCounter, xParent):

    # Count occurrences of current character
    count = 1
    i = xCounter
    blockLim = xParent - (xCounter % xParent)
    length = len(st) - 1
    eolCheck = count + xCounter
    if eolCheck == length:
        return count, st[eolCheck]

    while (i < length and
            st[i] == st[i + 1] and 
            count < blockLim):
            
        # increment count of current character
        count += 1
            
        # Increment index while character is still the same
        i += 1
        # print("current string character: ",st[i], "count: ", count, "length: ", length, "blockLim: ", blockLim, "i: ", i, "xCounter is: ",xCounter, "xParent is: ",xParent)
    return count, st[i - count + 1]

def outputRLE(xyzData, tagTableMap, xParent):
    global xCount
    # outputListZ = []
    # outputListY = []
    length = len(xyzData[0][0]) - 1
    totalEncodedBlocks = 0
    lineCount = 0
    # iterate z axis using zCounter to keep track of position
    for zCounter, z in enumerate(xyzData):
        
        # iterate y axis using yCounter to keep track of position
        for yCounter, y in enumerate(z):
            
            # set xCounter to 0 everytime yCounter increments by 1
            xCounter = 0
            lineCounter = 0
            # while loop to check condition of xCounter compared to current line length before proceeding with RLE encoding
            while xCounter <= length:
                
                # run RLE encoding
                xSize, tag = encodeRLE(xyzData[zCounter][yCounter], xCounter, xParent)
                # define output string format
                outputString = f"{xCounter},{yCounter},{zCounter},{xSize},{ySize},{zSize},{tagTableMap[tag]} \n"
                totalEncodedBlocks += xSize * ySize * zSize
                lineCounter += xSize * ySize * zSize
                lineCount += 1
                # if totalEncodedBlocks == 11063:
                #     print("tag: ",tag, "map value: ",tagTableMap[tag])
                if lineCount == 11064:
                    print("tag: ",tag, "map value: ",tagTableMap[tag])
                # increment xCounter by the amount of counts returned by the encode function
                xCounter += xSize
                # print(outputString)
                # outputListY.append(outputString)
            if ((lineCounter % xCount) != 0):
                print(totalEncodedBlocks, "\n")
                print(lineCounter, "\n")
                print(xCount, "\n")
                # print("Block position: ",zCounter, yCounter, xCounter, "\n")
                print("Block position: ",xCounter, yCounter, zCounter, xSize, ySize, zSize, tagTableMap[tag], "\n")
            # print()
        # outputListZ.append(outputListY)
        # outputListY = []
        # print("\n")
    print(totalEncodedBlocks)
    # return outputListZ
    pass

# Open/Create output file
outputFile = open("outputList.txt", "w")
output2File = open("outputList2.txt", "w")

# Initialise Variables
tagTableFound   = False
tagTableMap     = {}
outputList      = []
xData           = ''
xyData          = []
xyzData         = []
invertY         = False
counterToExit   = 0
counter         = 0
prevBlankLine   = False

# Testing variables
xSize           = 1
ySize           = 1
zSize           = 1
testLine        = ''
testingMode     = False
# Loop through each line of file
while True:
    line = sys.stdin.readline()

    # Get data dimensions from first line
    if counter == 0:
        dimensionList = line.split(',')
        xCount, yCount, zCount, xParent, yParent, zParent = map(int, dimensionList)

    # Get the tag table details
    elif counter > 0 and tagTableFound == False:

        # Detect end of line and set a flag to start processing data
        if line == '\n':
            tagTableFound = True
            continue
        
        # Build a map using the tag/label inputs
        tagParts = line.strip().split(',')
        if len(tagParts) == 2:
            tag, label = tagParts
            tagTableMap[tag] = label.strip()
    
    # Get data and store in a seperate variable
    else:
        # Remove leading/trailing spaces/end of line characters
        xData = line

        # Add to the 2d array when we dont have a blank line
        if line != '\n':

            # Validate number of characters in each line (x)
            if len(xData) - 1 != xCount:
                print (xData)
                print ('x size does not match, current: ' + str(len(xData) - 1) + ' expected: ' + str(xCount) + ' counter: ' + str(counter))
                quit()
            
            xyData.append(line.strip())

        # If we have a blank line, append 2d array to the 3d array and clear the 2d array
        else:
            # Validate number of lines in each slice (y)
            if len(xyData) != yCount:
                print ('y size does not match, current: ' + str(len(xyData)) + ' expected: ' + str(yCount) + ' counter: ' + str(counter))
                quit()

            # Reverse data for easier processing, as origin point is the bottom left instead of top left
            if invertY:
                xyzData.reverse()

            xyzData.append(xyData.copy())
            xyData.clear()
        
        # Increment counter to exit
        counterToExit = counterToExit + 1
        
        # If we reached the expected end of input file, exit
        if counterToExit > (yCount * zCount) + zCount - 1:
            break

    counter = counter + 1

# Validate number of slices (z)
if len(xyzData) != zCount:
    print ('z size does not match, current: ' + str(len(xyzData)) + ' expected: ' + str(zCount))
    quit()

# Close input file
# inputFile.close()

##################################################################
# Call algorithm here, output should be in outputList variable

outputRLE(xyzData, tagTableMap, xParent)
# outputList = outputRLE(xyzData, tagTableMap, xParent)

# print(outputList[0])
# print(outputList[len(outputList) - 1])
# print(len(outputList))
# print(len(outputList[0]))
# slice = 4
# for i in range(len(outputList[slice])):
#     print(outputList[slice][i])

##################################################################
# if testingMode == False:
#     for outputLine in outputList:
#         print(outputLine)

##################################################################
# Testing code below

##################################################################
if testingMode:
    # Build output string and add to outputList
    for zCounter, z in enumerate(xyzData):
        for yCounter, y in enumerate(z):
            for xCounter, x in enumerate(y):
                outputString = f"{xCounter},{yCounter},{zCounter},{xSize},{ySize},{zSize},{tagTableMap[x]} \n"
                print(outputString)
                #outputList.append(outputString)

    # Sample output file for testing
    for outputLine in outputList:
        outputFile.writelines(outputLine)

    outputFile.close()

    for z in xyzData:
        for y in z:
            for x in y:
                testLine = testLine + x
            output2File.write(testLine + "\n")
            testLine = ''
    output2File.close()