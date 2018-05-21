# Grid dimensions in meters
# Total oppervlak: 320 * 360 = 115.200
# 20% oppervlak = 0.2 * 115.200 = 23.040
# sqrt(23.040) = 151,7893276881
# 300 x 76,8
gridXLength = 180 * 2
gridYLength = 160 * 2

# Define object templates (in dictionary format) to create class instances
waterTemplate = {
    "type": "water",
    "freeArea": 0,
    "extraFreeArea": 0,
    "xBegin": 0,
    "xEnd": 0,
    "yBegin": 0,
    "yEnd": 0,
    "gridXLength": gridXLength,
    "gridYLength": gridYLength,
    "uniqueID": 0
}

eengezinswoningTemplate = {
    "type": "eengezinswoning",
    "objectDimensions": (8, 8),
    "freeArea": 2,
    "extraFreeArea": 0,
    "value": 285000,
    "valueIncrease": float(0.03),
    "xBegin": 0,
    "xEnd": 0,
    "yBegin": 0,
    "yEnd": 0,
    "gridXLength": gridXLength,
    "gridYLength": gridYLength,
    "uniqueID": 0
}

bungalowTemplate = {
    "type": "bungalow",
    "objectDimensions": (10, 7.5),
    "freeArea": 3,
    "extraFreeArea": 0,
    "value": 399000,
    "valueIncrease": float(0.04),
    "xBegin": 0,
    "xEnd": 0,
    "yBegin": 0,
    "yEnd": 0,
    "gridXLength": gridXLength,
    "gridYLength": gridYLength,
    "uniqueID": 0
}

maisonTemplate = {
    "type": "maison",
    "objectDimensions": (11, 10.5),
    "freeArea": 6,
    "extraFreeArea": 0,
    "value": 610000,
    "valueIncrease": float(0.06),
    "xBegin": 0,
    "xEnd": 0,
    "yBegin": 0,
    "yEnd": 0,
    "gridXLength": gridXLength,
    "gridYLength": gridYLength,
    "uniqueID": 0
}

# Set result template
resultsTemplate = {
    "algorithm": "",
    "maxHouses": 0,
    "rounds": 0,
    "roundsCounter": 0,
    "swaps": 0,
    "moves": 0,
    "allScores": 0,
    "highestScore": 0,
    "highestScoreMap": [],
    "numpyGrid": 0,
    "lowestScore": 1000000000,
    "averageScore": 0,
    "fastestRuntime": 1000000000,
    "slowestRuntime": 0,
    "totalRuntime": 0
}
