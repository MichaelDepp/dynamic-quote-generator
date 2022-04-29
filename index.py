# coding=utf-8

# ========================================
#   Modules
# ========================================
import datetime
from fileinput import filename
import json
import os
import random
import sys
import textwrap

# importing the Pillow module
from PIL import Image, ImageDraw, ImageFont

# global constants
postSize = 1080

lastThreeBg = []
lastThreeColor = []


def loadFileData():
    with open("verses.json", "r", encoding="utf8") as f:
        verseData = json.load(f)
    with open("colorConfig.json", "r", encoding="utf8") as j:
        colorConfig = json.load(j)
    return verseData, colorConfig


def greet(data):
    print('***************______Starting Verse Generator***************______\n')
    print('There are total ', len(data.keys()), 'contributors : ')
    print('Contributors List : \n')
    for key, values in data.items():
        print(key)


def filterDuplicates(data):
    mergedData = []
    uniqueData = []
    nonDuplicate = []

    for i in data.values():
        mergedData = mergedData + i

    for i in mergedData:
        verseText = ''
        try:
            verseText = i['verse'][:i['verse'].index('-')]
        except:
            verseText = i['verse']

        if verseText in nonDuplicate:
            print('\nWe just found a duplicate: ')
            print(i)
        else:
            nonDuplicate.append(verseText)
            uniqueData.append(i)

    return uniqueData


def shuffleNWrite(data):
    shuffledData = random.sample(data, len(data))
    json_object = json.dumps(shuffledData, indent=4)
    print('\nWriting Unique Data in Json File')
    with open("unique-verses.json", "w") as outfile:
        outfile.write(json_object)
    print('Finished Writing File\n')
    return shuffledData


def randomColorAsset(colors, fileName):
    randomColor = random.choice(colors)
    while randomColor in lastThreeColor:
        randomColor = random.choice(colors)

    if len(lastThreeColor) < 3:
        lastThreeColor.append(randomColor)
    else:
        del lastThreeColor[0]
        lastThreeColor.append(randomColor)

    randomBg = random.choice(os.listdir('./assets'))
    while randomBg in lastThreeBg:
        randomBg = random.choice(os.listdir('./assets'))

    if len(lastThreeBg) < 3:
        lastThreeBg.append(randomBg)
    else:
        del lastThreeBg[0]
        lastThreeBg.append(randomBg)

    return randomColor, randomBg


def wordWrapper(text):
    fontSize = 0
    textBoxGap = 0
    startingHeight = 0
    wordBreak = 0

    if len(text) >= 250:
        fontSize = 45
        textBoxGap = 70
        startingHeight = -10
        wordBreak = 35
    if 200 < len(text) < 250:
        fontSize = 50
        textBoxGap = 75
        startingHeight = -10
        wordBreak = 30
    if 160 < len(text) < 200:
        fontSize = 55
        textBoxGap = 80
        startingHeight = -20
        wordBreak = 25
    if 90 < len(text) <= 160:
        fontSize = 60
        textBoxGap = 90
        startingHeight = 0
        wordBreak = 25
    if 50 < len(text) <= 90:
        fontSize = 75
        textBoxGap = 110
        startingHeight = +40
        wordBreak = 20
    if 20 < len(text) <= 50:
        fontSize = 80
        textBoxGap = 120
        startingHeight = +40
        wordBreak = 15
    # Logic

    # long = 250 fontsize = 50, textBox gap = 75, startingHeight = - 10, wordBreak = 30
    # middle = 150 fontsize = 55, textBox gap = 80, startingHeight = - 20, wordBreak = 25
    # small = 150 fontsize = 65, textBox gap = 90, startingHeight = + 10, wordBreak = 20
    # xs = 50 fontsize = 75, textBox gap = 110, startingHeight = + 40, wordBreak = 20
    # xss = 20 fontsize = 80, textBox gap = 120, startingHeight = + 40, wordBreak = 15

    return (fontSize, textBoxGap, startingHeight, wordBreak)


def writeCaptionFile(filePath, fileName, caption):
    try:
        completeName = os.path.join(filePath, fileName + ".txt")
        file1 = open(completeName, "w")
        file1.write(caption)
        file1.close()
    except:
        print('Text file writing failed!')


def createPost(verse, verseDate, colorConfig):
    fileName = verseDate.strftime('%d-%m-%Y')
    randomColor, randomBg = randomColorAsset(colorConfig, fileName)

    postBgColor = randomColor['bg']
    postTextColor = randomColor['text']
    postTextBoxColor = randomColor['box']

    try:
        path1 = 'generated-verses'
        path2 = fileName
        if not os.path.exists(path1):
            os.makedirs(path1)
        if not os.path.exists(os.path.join(path1, path2)):
            os.makedirs(os.path.join(path1, path2))
    except:
        print('creating folder went wrong')
        sys.exit()

    fontSize, textBoxGap, startingHeight, wordBreak = wordWrapper(
        verse['text'])

    image = Image.new('RGBA', (postSize, postSize), postBgColor)
    font = ImageFont.truetype('fonts/Bogart-Bold-trial.ttf',
                              size=fontSize)  # adjust the font size
    font2 = ImageFont.truetype('fonts/AnonymousPro-Regular.ttf', size=32)
    draw = ImageDraw.Draw(image)
    totalCircle = 3

    background_shape = Image.open('assets/' + randomBg)
    background_shape.convert('RGBA')

    image.paste(background_shape, (0, 0), background_shape)

    def drawFrame():
        shape = (76, 107, 940 + 76, 870 + 107)
        shadowShape = (76 + 25, 107 + 25, 940 + 76 + 25, 870 + 107 + 25)
        draw.rounded_rectangle(shadowShape, fill='black',
                               outline='black', width=4, radius=25)

        draw.rounded_rectangle(shape, fill=postBgColor,
                               outline='black', width=4, radius=25)

        draw.line((76, 187, 940 + 76, 187), fill='black', width=4)

    def drawCircleButtons():
        for i in range(totalCircle):
            x = 98 + (i * 50)
            y = 133
            size = 30
            draw.ellipse((x, y, size + x, size + y), outline='black', width=4)

    def drawVerse():
        wrapper = textwrap.TextWrapper(
            width=wordBreak)  # adjust the text break
        (x, y) = (100, 400)
        word_list = wrapper.wrap(verse['text'])

        def printText(line, x, y):
            color = postTextColor
            draw.text((x + 20, y - 10), line, fill=color, font=font)

        def drawVerseBox():
            averageTextBoxHeight = 0
            for line in word_list:
                textX, textHeight = font.getsize(line)
                if averageTextBoxHeight < textHeight:
                    averageTextBoxHeight = textHeight

            count = 0
            for line in word_list:
                textX, textY = font.getsize(line)
                x = (postSize / 2) - (textX / 2) - 20
                height = 250 + startingHeight  # adjust starting height point
                y = height + (count * textBoxGap)  # adjust the text box gap
                secondX = (postSize / 2) + (textX / 2) + 20
                secondY = y + averageTextBoxHeight
                shape = (x, y, secondX, secondY)
                draw.rectangle(shape, fill=postTextBoxColor)
                count += 1
                printText(line, x, y)

        def printVerse():
            text = verse['verse']
            textX, textY = font2.getsize(text)
            x = 977 - textX
            y = 133
            color = '#000000'
            draw.text((x, y), text, fill=color, font=font2,  align='right')

        drawVerseBox()
        printVerse()

    def drawFooter():
        x = (postSize / 2) - (190 / 2)
        y = 1022
        secondX = (postSize / 2) + (190 / 2)
        secondY = 1022 + 40
        shape = (x, y, secondX, secondY)
        draw.rectangle(shape, fill=postTextBoxColor)

    def drawFooterText():
        text = '@myf.tac'
        textX, textY = font2.getsize(text)
        x = (postSize / 2) - (textX / 2)
        y = 1023
        color = postTextColor
        draw.text((x, y), text, fill=color, font=font2)

    drawFrame()
    drawCircleButtons()
    drawVerse()
    drawFooter()
    drawFooterText()

    filePath = 'generated-verses/'
    image.save(filePath + fileName +
               '/' + fileName + '.png', quality=100)

    print('Post ' + fileName + '.png' + ' generated!!')
    writeCaptionFile(filePath + fileName + '/', fileName, verse['caption'])


def generateArt(data, colorConfig):
    year = int(input('\nEnter a year (number) : '))
    month = int(input('\nEnter a month (number) : '))
    day = int(input('\nEnter a day (number) : '))
    startDate = datetime.date(year, month, day)
    endDate = startDate + datetime.timedelta(days=len(data))

    formatStyle = '%d %B %Y'
    formatStartDate = startDate.strftime(formatStyle)
    formatEndDate = endDate.strftime(formatStyle)

    input("You've choose " + formatStartDate +
          " as the starting date! (Enter any keyword to proceed) : ")
    input("There are total " + str(len(data)) +
          " verses that has been sorted, filtered, and shuffled and ready to be generated as bible verse posts! (Enter any keyword to proceed) : ")
    input("The verses post will be generated for each day until " +
          formatEndDate + ' (Enter any keyword to proceed) : ')

    answer = input("Enter y/Y to proceed generating the verses: ")

    if answer == 'y' or answer == 'Y':
        count = 0
        for verse in data:
            verseDate = startDate + datetime.timedelta(days=count)
            createPost(verse, verseDate, colorConfig)
            print('######## Created ' + count + ' post!! ########')
            count += 1
    else:
        print('Program ends!')


def main():
    verseData, colorConfig = loadFileData()
    greet(verseData)

    uniqueData = filterDuplicates(verseData)
    shuffledData = shuffleNWrite(uniqueData)

    generateArt(shuffledData, colorConfig)


main()
