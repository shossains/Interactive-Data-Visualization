<h1>Client Meeting</h1>

*Datum: woensdag 21 april 2021 - 14:00*

<h4>Algemene mededelingen</h4>

- Casus: Veel data over gezondheid met het oog op hartritmestoornissen
- Meehelpen met code is mogelijk
- Basis/voorbeeld is al een keer gemaakt (in R), maar voorkeur gaat naar Python en één abstractielaag hoger
- [Demo](https://heartpr.shinyapps.io/tsne_pcas_removed/)


<h4>Requirement questions</h4>

**General**

What do you mean by a top-down approach regarding the engineering process?
> Work in blocks, adding to the GUI piece-by-piece

On the project forum, we read software architecture is very important for this project, but what do mean by that exactly?
What architectural patterns do you propose we use? (Client/server, MVC, Micro-services etc?)
> Pick the (useful) functionalities from the libraries. Make sure to build upon already existing functionalities. Furthermore the application should be extendable 

Can workspace be provided?
> With current measures this will not be possible. The SP-staff however is looking for possibilities to arrange such needs in the near future

What are your working hours, to reach you for questions?
> Email is always possible at all times. Mattermost is preferred as most conversations will be back-and-forth

How often would you like to meet us?
> Once every 2 weeks, if necessary once a week; preferably Monday morning or after 14:00 || Friday whole day. These meetings can be arranged whenever needed through Mattermost

What mode of communication should we use to reach you?
> Mattermost/Email

---
**GUI**

Should we create our own design for the GUI, or do you have a design in mind?
> No particular preference. The given demo can be used as a guideline

What is the order of prioritization regarding GUI components (GUI, plotter, data selection, thumbnail, caching)?
> 1. Data selection (nested filtering): Including and excluding several variables and using that as a filter to narrow the scatter further (eg. Selecting a specific person in the plot and change a variable to years and select a specific year for that specific person).
> 2. Plotter: This will mainly be a scatterplot with an option to select a certain interval on top of the scatterplot. A possible option to smooth the scatterplot is possible
> 3. Thumbnail: Every point will contain meta-data and will create a small thumbnail displaying how the scatterplot will look like for that specific point (meta-data of specific point)
> 4. GUI: If possible, try to abstract a much a possible in such a way that the program can be expanded easily (API)

Do you have any tips on which GUI builder we should use?
> [Ploty](https://plotly.com/), [Dash](https://dash.plotly.com/introduction) or [Bokeh](https://bokeh.org/) are good libraries to build upon

---
**Type Data**

Should the end product be able to convert data to a useful format itself, or will only converted data be provided (e.g. pictures to numbers etc.)?
> Data will always be delivered by us in the correct format. Coverting is not needed. Furthermore is you prefer the data to be in a (slightly) different format that is also possible.

Are we getting a specific data format?
> The data delivered will be time-dependant. It will be delivered in a table or CSV-like format. Metadata will be in a different table.

What data set sizes can we expect? 
> Data are quite big and in the size of several Gigabytes. It might be possible to make the user preselect certain variable to plot and preload the remaining variable in the background to save memory, increase efficiency and decrease overhead (lazy loading)

For visualization, how many dimensions will the data generally have? 
(How) should we handle (attempt to visualize) >3 dimensional data?
> Data will be preprocessed and converted in such a way that it will only have 3 or less dimensions.

~~How many dimensions should the end product be able to handle?~~

Besides graphs, should there also be an option to display the data in a table?
> Data will be visualized in a scatterplot. If possible continious variables could be plotted in a heatmap.


---
**Client/server division**

Data only local or should it be taken from a server? Or Both?
> The program and the data will be local. In case of expansion to a WebApp is will be online. However, if that happens necessary administrative measures must be taken to preserve the anonimity and security of the data

~~In case of a server: Can we use your servers or do we need to make one of our own?~~

~~In case of a server: Will you provide/recommend a server framework w.r.t. Data protection and/or security~~

---
**Non-functional**

How user-friendly should the GUI be? Accessible for people without ML background?
> The only user that will be using the program will have a background in machine learing

Should there be an explanation of what the tools do?
> Documentation of how the program work back-end as well as front-end is recommended

Should users be able to have an account?
> Such thing is no necessary

Should users be able to save presets of settings (ticked boxes etc.)?
> An expansion that would be nice to have

~~Should we make some kind of .exe such that users without programming experience are able to run this?~~

In what format must the final product be in? (eg. .exe, .py2exe)
> The final deliverable should be an executable runnable in Linux

---
**Webapp (extra)**

How important is a web app?
Should we prioritize it over some of the other requirements or treat it as the last requirement?
> This should be the biggest priority after the main program is finished. A very big wish, but not a requirement

---
**Machine learning**

~~Which machine learning tools are mandatory to have in our visualiser or are there any preference on tools?~~

~~What tools should we prioritize over others?~~

What are the minimum amount of tools we should have in our visualiser?
> The use of numPy and sciPy is definetely necessary since most of the data is also generated with datastructeres from these libraries


