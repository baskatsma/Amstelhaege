# Amstelhaege
#### Introductie
Wij, Felicia, Amy en Bas, zijn door de gemeente aangewezen om een nieuwe woonwijk in de **Duivendrechtse polder** in te richten. Voor de gemeente zullen wij een **20-, 40- en 60-huizenvariant** opleveren.

Echter, omdat dit *ooit in het verre verleden* een beschermd natuurgebied was, zijn er een aantal strenge restricties gesteld.

#### Restricties
* De wijk bestaat voor **60%** uit eengezinswoningen, **25%** uit bungalows en **15%** uit maisons
* De huizen hebben ieder een voorafbepaalde hoeveelheid vrijstand; een vergroting van de vrijstand levert extra waarde op
* De wijk moet voor **20%** uit oppervlaktewater bestaan, opgedeeld in **niet meer dan vier lichamen** die rechthoekig of ovaal van vorm zijn
* Deze lichamen hebben hoogte-breedteverhoudingen die **tussen de 1:1 en 1:4** liggen


## Status
- [x] Datastructures geïnitialiseerd
- [x] Basale functies toegevoegd
- [x] Random grid X, Y functie
- [x] Huizen kunnen op het grid worden geplaatst
- [x] Grid en huizen worden correct gescaled
- [x] Anti-overlap functies toegevoegd
- [x] Verplichte vrijstand toegevoegd (zonder pythagoras)
- [X] Extra vrijstand calculator functie toegevoegd
- [X] Water toegevoegd
- [ ] Random algoritme optimaliseren
- [ ] Nieuwe algoritmes toepassen


## Vereisten
Dit project is geschreven in Python 3.6.5. In requirements.txt staan de benodigde packages om de code uit te voeren. Deze packages zijn te installeren door het runnen van de volgende command:
```
pip3 install -r requirements.txt
```

## Gebruik
```
python3 main.py '#HOUSES' 'ALGORITHM'
```
**Voorbeelden:**
```
python3 main.py 40 random
python3 main.py 60 hillclimber
```

## Dankwoord
Wij willen graag onze assistent Nicole Silverio bedanken voor de assistentie, hulp en mentale support!
