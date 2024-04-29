from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re
import string
import csv
import os

# Extracts boulder area from URL
def get_sub_area(j):
    link = rs_location[j].findNext('a')['href'].split('/')[-1].split('-')
    return string.capwords(" ".join(link))

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#open and reads .txt for areas to be scraped
area_codes = open('area_codes.txt', 'r')
area_list = area_codes.readlines()
for i in range(len(area_list)):
    try:
        id = int(area_list[i].strip())
    except:
        print('Ensure area_codes.txt entries are int type only')
        exit()
    if len(str(id)) != 9 or id < 0:
        print(f'Area code {i+1} out of range')
        exit()

    #read bouldering area overview page to gather data for iteration counts, and get area name
    link_num = 1
    init_id = f'https://www.mountainproject.com/route-finder?selectedIds={id}&type=boulder&diffMinrock=1800&diffMinboulder=20000&diffMinaid=70000&diffMinice=30000&diffMinmixed=50000&diffMaxrock=5500&diffMaxboulder=21700&diffMaxaid=75260&diffMaxice=38500&diffMaxmixed=60000&is_trad_climb=1&is_sport_climb=1&is_top_rope=1&stars=0&pitches=0&sort1=area&sort2=rating&page{link_num+1}'
    try:
        html = urlopen(init_id, context=ctx).read()
        soup = BeautifulSoup(html, "html.parser")
        area_count = soup.find_all(string=re.compile("Results 1 to"))
        area = soup.find('div', class_='float-md-left').contents[5].text
    except:
        print("Unable to open URL")

    #calculate number of iterations
    route_count = int(re.findall(('\d+'), area_count[0])[2])
    page_length = int(re.findall(('\d+'), area_count[0])[1])
    iter_count = route_count//page_length
    last_iter_count = route_count%page_length

    # Calculates iterations needed to record all routes
    route_lst = []
    for page in range(1, iter_count+2):
        if page < iter_count:
            rep = 50
        elif page == iter_count:
            rep = int(last_iter_count)

        # New URL to iterate through successive pages
        f_id = f'https://www.mountainproject.com/route-finder?diffMaxaid=75260&diffMaxboulder=21700&diffMaxice=38500&diffMaxmixed=60000&diffMaxrock=5500&diffMinaid=70000&diffMinboulder=20000&diffMinice=30000&diffMinmixed=50000&diffMinrock=1800&is_sport_climb=1&is_top_rope=1&is_trad_climb=1&page7=&pitches=0&selectedIds={id}&sort1=area&sort2=rating&stars=0&type=boulder&page={page}'

        # URL is open and contents parsed using BS4
        html = urlopen(f_id, context=ctx).read()
        soup = BeautifulSoup(html, "html.parser")
        area_count = soup.find_all(string=re.compile("Results 1 to"))

        # Finds relevant tags where data is located
        rs_name = soup.find_all('div', class_="text-truncate")
        rs_location = soup.find_all('div', class_="small text-warm")
        rs_grade = soup.find_all('span', class_='rateYDS')
        rs_stars = soup.find_all('span', class_='scoreStars')
        rs_popular = soup.find_all('span', class_='text-muted small')

        # Using above ResultSets, gathers and cleans data for route name,
        # sub-area, grade, star count/rating, and popularity
        for j in range(rep):
            name = rs_name[j].findNext('strong').text
            sub_area = get_sub_area(j)
            try:
                grade = re.search('(\d+)(?!.*\d)', rs_grade[j].text).group()
            except: #if grade is Veasy, substitutes in a 0 for grade
                grade = 0
            popular = rs_popular[j].text.strip()
            star_imgs = [str(i) for i in rs_stars[j] if i != '\n']
            star_count = 0
            for star in star_imgs:
                if 'starBlue.' in star:
                    star_count += 1
                elif 'starBlueH' in star:
                    star_count += 0.5
            # Route data stored in a list of dictionaries to work with csv.DictWriter
            route_lst.append({'name': name, 'sub_area': sub_area, 'area': area, 'grade': grade, 'star_count': star_count, 'popular': popular})

    # Creates .csv for climbing areas if not present in directory and writes to it using csvwriter
    try:
        if os.path.isfile(rf'C:\Users\smitt\PycharmProjects\pythonProject\areas\{area}.csv') is False:
            with open(os.path.join(r'C:\Users\smitt\PycharmProjects\pythonProject\areas', f'{area}.csv'), 'w') as file:
                fields = ['name', 'sub_area', 'area', 'grade', 'star_count', 'popular']
                csvwriter = csv.DictWriter(file, fieldnames=fields, lineterminator='\n')
                csvwriter.writeheader()
                csvwriter.writerows(route_lst)
        elif os.path.isfile(rf'C:\Users\smitt\PycharmProjects\pythonProject\areas\{area}.csv') is True:
            print(f'{area}.csv already exists')
    except:
        print(f'Unable to create {area}.csv')
