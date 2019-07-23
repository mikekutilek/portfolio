# My Portfolio
An online portfolio website built to showcase pieces of my life to anyone interested in getting to know me.

## Frameworks
* [Node.js] - the web framework used
* [Angular.js] - front end builder
* [Python] - data extraction, manipulation, and analysis

## Sections
The website is divided into 4 sections: Projects, Photography, Videography, and About Me. 

### Projects
An assortment of code projects I've worked on, primarily coded in python and focused around scraping and analyzing sports data, particularly MLB, NHL, and NFL. 
Each project has a back end data refresh and a front end application that is part of the website.
The code for these projects is in the /projects folder of this repository. 

### Photography
One of my favorite hobbies that has emerged over the past 3 years is photography. 
This section of the portfolio is dedicated to showcasing this work. I have an online gallery/store hosted at https://mikekutilek.zenfolio.com
and an Etsy store here: https://etsy.com/shop/MikeKutilekPhoto

### Videography
Along with photography comes videography. 
To get acclimated with editing software such as Adobe Premiere and After Effects, I spent a few years editing footage of Pittsburgh Penguins games into 2-3 minute montages in the style of Hockey Night in Canada. 
Following this mold, I built a YouTube channel called Hockey Night in Pittsburgh and produced these videos regularly during the playoffs. 
All of these videos are showcased in this section. Additionally, some time lapse projects of Pittsburgh that I've created are also shown here.

## Data Flow
All MLB, NHL, and NFL data is pulled from sites such as Baseball Savant, Fangraphs, etc. using a series of Beautiful Soup web scrapers.
The data is then dumped into a MongoDB Atlas database where it can be read by the front end Node application. 
This data is refreshed in MongoDB daily at 4AM EST. 

## Front End
The front end is built in Node.js with a heavy dose of Angular.js. 
Angular is primarily used to loop through configuration files that store the info to display photos and videos. 

## Deployment
The website is deployed using Heroku (https://heroku.com)

## Authors
* **Mike Kutilek** - *All work*
