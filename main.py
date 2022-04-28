import json
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random

with open("verses.json", "r", encoding="utf8") as f:
    data = json.load(f)


def wordWrapper(text):
    fontSize = 0
    textBoxGap = 0
    startingHeight = 0
    wordBreak = 0
    print(len(text))
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
    if 150 < len(text) < 200:
        fontSize = 55
        textBoxGap = 80
        startingHeight = -20
        wordBreak = 25
    if 100 < len(text) <= 150:
        fontSize = 60
        textBoxGap = 90
        startingHeight = 0
        wordBreak = 25
    if 50 < len(text) <= 100:
        fontSize = 75
        textBoxGap = 110
        startingHeight = +40
        wordBreak = 20
    if 20 < len(text) <= 50:
        fontSize = 80
        textBoxGap = 120
        startingHeight = +40
        wordBreak = 15
    return (fontSize, textBoxGap, startingHeight, wordBreak)
    # long = 250 fontsize = 50, textBox gap = 75, startingHeight = - 10, wordBreak = 30
    # middle = 150 fontsize = 55, textBox gap = 80, startingHeight = - 20, wordBreak = 25
    # small = 150 fontsize = 65, textBox gap = 90, startingHeight = + 10, wordBreak = 20
    # xs = 50 fontsize = 75, textBox gap = 110, startingHeight = + 40, wordBreak = 20
    # xss = 20 fontsize = 80, textBox gap = 120, startingHeight = + 40, wordBreak = 15


def logVerse(cleanedData):
    for verse in cleanedData:
        del verse['verse']
        del verse['caption']
    print(cleanedData)
    json_object = json.dumps(cleanedData, indent=4)
    with open("mapped.json", "w") as outfile:
        outfile.write(json_object)


def createImage(text):
    fontSize, textBoxGap, startingHeight, wordBreak = wordWrapper(text)

    image = Image.new('RGBA', (1080, 1080), '#EDCFCF')
    font = ImageFont.truetype('fonts/Bogart-Bold-trial.ttf',
                              size=fontSize)  # adjust the font size
    font2 = ImageFont.truetype('fonts/AnonymousPro-Regular.ttf', size=32)
    draw = ImageDraw.Draw(image)
    totalCircle = 3

    background_shape = Image.open('assets/x-bg.png')
    background_shape.convert('RGBA')

    image.paste(background_shape, (0, 0), background_shape)

    def drawFrame():
        shape = (76, 107, 940 + 76, 870 + 107)
        shadowShape = (76 + 25, 107 + 25, 940 + 76 + 25, 870 + 107 + 25)
        draw.rounded_rectangle(shadowShape, fill='black',
                               outline='black', width=4, radius=25)

        draw.rounded_rectangle(shape, fill='#EDCFCF',
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
        word_list = wrapper.wrap(text)

        def printText(line, x, y):
            color = '#FFF890'
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
                x = (1080 / 2) - (textX / 2) - 20
                height = 250 + startingHeight  # adjust starting height point
                y = height + (count * textBoxGap)  # adjust the text box gap
                secondX = (1080 / 2) + (textX / 2) + 20
                secondY = y + averageTextBoxHeight
                shape = (x, y, secondX, secondY)
                draw.rectangle(shape, fill='#F53D3D')
                count += 1
                print('thiss isss the yy ---- > ', textY)
                printText(line, x, y)

        def printVerse():
            text = '1 Corinthians 6:14'
            textX, textY = font2.getsize(text)
            x = 977 - textX
            y = 133
            color = '#000000'
            draw.text((x, y), text, fill=color, font=font2,  align='right')

        drawVerseBox()
        printVerse()

    def drawFooter():
        x = (1080 / 2) - (190 / 2)
        y = 1022
        secondX = (1080 / 2) + (190 / 2)
        secondY = 1022 + 40
        shape = (x, y, secondX, secondY)
        draw.rectangle(shape, fill='#F53D3D')

    def drawFooterText():
        text = '@myf.tac'
        textX, textY = font2.getsize(text)
        x = (1080 / 2) - (textX / 2)
        y = 1023
        color = '#FFF890'
        draw.text((x, y), text, fill=color, font=font2)

    drawFrame()
    drawCircleButtons()
    drawVerse()
    drawFooter()
    drawFooterText()

    image.save('verses-new.png', quality=100)


def writeMergedData(cleanData):
    # shuffledData = cleanData
    shuffledData = random.sample(cleanData, len(cleanData))
    json_object = json.dumps(shuffledData, indent=4)
    print('****************** Writing Cleaned Unique Verse in Json File ******************')
    with open("unique-verses.json", "w") as outfile:
        outfile.write(json_object)
    print('****************** Finished Writing Cleaned Unique Verse in Json File ******************')
    text = 'Finally, be strengthened by the Lord and his powerful strength'
    print('shufff ----- > ', shuffledData)
    # logVerse(cleanData)
    createImage(text)


def filterDuplicates(mergedData):
    uniqueData = []
    nonDuplicate = []
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
    writeMergedData(uniqueData)


def mergeData():
    mergedData = []
    for i in data.values():
        mergedData = mergedData + i
    filterDuplicates(mergedData)


def greetStart():
    print('******************-----------Starting the verse generator function-----------******************')
    print('***********************************************************************************************\n')
    print('there are total ', len(data.keys()), 'contributors')
    print('This is the list of contributors : ')
    for key, values in data.items():
        print(key)


greetStart()
mergeData()
f.close()
