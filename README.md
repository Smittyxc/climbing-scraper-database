# Rock Climbing Scraper and MySQL Database

- **Author**: Matthew Smith

- **Email**: mattsmith1652@gmail.com

## Background
There are many destination rock climbing crags across the United States; the goal of this project was to build a MySQL database using Python, consisting of a list of user-defined crags with information on every boulder located in specified areas.

## Functionality
Comprised of two Python scripts, get_mpareas.py gathers data from [Mountain Project](https://www.mountainproject.com/), a user-driven repository of rock climbing routes, using BS4. The script reads from area_codes.txt, which is a set of nine digit area identifiers from Mountain Project comprised of areas the user wishes to explore. The script also cleans data to be stored in .csv files in the \areas folder (must be in the same directory), which csv_to_mysql.py reads and imports into a corresponding MySQL database it has created. Future users will need to add login details to their local MySQL instance. 

## Entity Relationship Diagram
![eer](/climbing_eer.png)
