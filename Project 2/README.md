# Project_ETL

ETL project based on womens education. 

## Extract

Specifically to see how many women make up the collegiate level students and graduates. The following sources were used:

* https://data.census.gov/
* https://nces.ed.gov/

The data includes:

* School year
* Total for each degree
* Total by gender for each degree
* Educational attainment for population between 18 to 24 and 25 and over
* Level of education
* Estimate by gender
* Race
* Poverty rate

Not all data was used.

## Transform

In order to use the public data, the following steps were taken to transform the information,

* Used pandas to import and read all CSV files.
* Reviewed files and converted column names in order to drop unwanted information.
* Removed irrelevant information such as years before 2014 and columns with missing information.
* Pandas DataFrames were created for each year since 2015. These DataFrames included the age group and level of education for each age group by gender.
* Pandas DataFrames were created for each degree type, for example: Associates, Bachelors, and Masters degrees. These DataFrames included actual degress granted by gender beween 2013-14 school year and estimated 2019-20 school year.

## Load
 
Finally, a womensEducation SQL Database was created in Postgres to store the cleaned data sets.

