# Rock Climbing Scraper and MySQL Database

- **Author**: Matthew Smith

- **Email**: mattsmith1652@gmail.com

## Background
There are many destination rock climbing areas across the United States containging hundreds of routes each. To better understand the nuances of each climbing area, climbers rely on grade distribution, route popularity, and route density to inform their decision to climb at certain destinations. To facilitate this process, this project constructs a MySQL database of climbing areas using Python with data gathered from [Mountain Project](https://www.mountainproject.com/), a user-driven repository of rock climbing routes worldwide, for further querying.

## Functionality
Comprised of two Python scripts, get_mpareas.py gathers data from [Mountain Project](https://www.mountainproject.com/) using BS4. The script reads from area_codes.txt, which is a set of nine digit area identifiers from Mountain Project comprised of areas the user wishes to explore. These indentifiers can be obtained for the URL of Mountain Project URLs. The script also cleans data to be stored in .csv files in the \areas folder (must be in the same directory), which csv_to_mysql.py reads and imports into a corresponding MySQL database it has created. Future users will need to add login details to their local MySQL instance. 

## Entity Relationship Diagram
![eer](/climbing_eer.png)
