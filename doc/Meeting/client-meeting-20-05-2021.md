<h1>Client Meeting</h1>

*Datum: 20 mei 2021 - 10:00*

<h4>Algemene mededelingen</h4>

- Project gaat goed; wat onduidelijkheden over wat er nog moet gebeuren
- Grote realistische datasets kunnen niet gestuurd worden wegens privacy redenenen
	- Kleine datasets die nu geleverd zijn kunnen wel handmatig opgeschaald worden tot grotere datasets door replicatie
- Communiceren mag frequenter

<h4>Demo</h4>

- Over het algemeen meer dan tevreden tot nu toe
- Continue waardes worden autmatisch omgezet in een heatmap
- Één patiënt/persoon staat gelijk aan één csv bestand

<h4>TODO</h4>

- Eigen filter:
	- Een eigen functie kunnen schrijven (in python)
	- Een selectie aan data doorgeven aan deze functie en het resultaat over de oude plot overlayen
	- Bij voorkeur is de input en output van deze zelfgeschreven functie een pandas dataFrame

- Nested Filerting:
	- Meerdere filters kunnen toepassen over de data die ook invloed hebben op de plot

- GUI rearrangen: De knoppen en menus links en de graphs rechts

- Een slider om het interval van tijd aan te passen van de graph

- Subplots met elkaar linken (_bonus_):
	- Als er een subplot word gemaakt dat bepaalde punten kunnen verwijzen naar een punt in de orignele plot of een regio daarvan