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
De code wordt uitgevoerd door het runnen van de volgende command:
```
python3 main.py '#HOUSES' 'ALGORITHM'
```
In deze command staat #HOUSES voor het aantal huizen dat de woonwijk kan bevatten.
Dit kunnen er 20, 40 of 60 zijn. Verder staat ALGORITHM voor het gewenste algoritme waarmee de woonwijk gecreëerd wordt. Voor een random algoritme dient "random" te worden ingevoerd. Voor een hillclimber algoritme dient "hillSwaps" of "hillMoves" te worden ingevoerd. Voor een simulated annealing algoritme dient "simAnnealing" te worden ingevoerd.


**Voorbeelden:**
```
python3 main.py 20 simAnnealing
python3 main.py 40 random
python3 main.py 60 hillSwaps
```

## Dankwoord
Wij willen graag onze assistent Nicole Silverio bedanken voor de assistentie, hulp en mentale support!
