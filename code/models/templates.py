# Grid dimensions in meters
# gridXLength = 18
# gridYLength = 16
gridXLength = 23
gridYLength = 20

# Define house templates (in dictionary format) to create class instances
eengezinswoningTemplate = {"type": "eengezinswoning",
                            # "houseDimensions": (8, 8),
                            "houseDimensions": (3, 2),
                            "freeArea": 2,
                            "extraFreeArea": 5,
                            "value": 285000,
                            "valueIncrease": float(0.03),
                            "positionX": 0,
                            "positionY": 0,
                            "gridXLength": gridXLength,
                            "gridYLength": gridYLength,
                            "uniqueID": 0}

bungalowTemplate = {"type": "bungalow",
                    # "houseDimensions": (10, 7.5),
                    "houseDimensions": (4, 3),
                    "freeArea": 3,
                    "extraFreeArea": 0,
                    "value": 399000,
                    "valueIncrease": float(0.04),
                    "positionX": 0,
                    "positionY": 0,
                    "gridXLength": gridXLength,
                    "gridYLength": gridYLength,
                    "uniqueID": 0}

maisonTemplate = {"type": "maison",
                    # "houseDimensions": (11, 10.5),
                    "houseDimensions": (5, 4),
                    "freeArea": 6,
                    "extraFreeArea": 0,
                    "value": 610000,
                    "valueIncrease": float(0.06),
                    "positionX": 0,
                    "positionY": 0,
                    "gridXLength": gridXLength,
                    "gridYLength": gridYLength,
                    "uniqueID": 0}
