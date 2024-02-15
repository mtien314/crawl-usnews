from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import chromedriver_binary

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("window-size = 1920x1080")

url = "https://www.usnews.com/best-colleges/rankings/national-universities"

names = []
links = []

#get url
for i in range(1,5):
    driver = webdriver.Chrome()
    url2 = url+f"?_page={i}"+"&_mode=table"
    driver.get(url2)
    element_name = driver.find_elements(By.TAG_NAME, "h3")
    name_page = [ele.text for ele in element_name]
    names +=name_page
    elems = driver.find_elements(By.TAG_NAME, "h3 [href]")
    links += [ele.get_attribute('href') for ele in elems]
    driver.quit()


names = list(filter(lambda x: x != '', names))
names = [x for i, x in enumerate(names) if names.index(x) == i]
names.remove('We and our partners process data to:')

overviews = []
costs = []
students = []
academics = []
aftercolleges = []
ranks = []
admissions = []
housing_and_dorms = []
activities = []
accepts = []
deadlines = []
data = []

for link in links:
    driver2 = webdriver.Chrome()
    driver2.get(str(link))
    #Get overview
    overview_element = driver2.find_element(By.CSS_SELECTOR,".mt2")
    overviews.append(overview_element.text)
    #get cost
    cost_element = driver2.find_element(By.CSS_SELECTOR, ".CostSection__DataHeader-coeai5-0")
    costs.append(cost_element.text)
    #get student
    student_element = driver2.find_element(By.CSS_SELECTOR, ".StudentsSection__DataHeader-sc-1tb3548-0")
    students.append(student_element.text)

    #get academic
    academic_element = driver2.find_elements(By.CSS_SELECTOR, ".m2")
    academic = [ele.text for ele in academic_element]
    academic = [x.replace('\n', ' ') for x in academic]
    academics.append(academic[2:])

    #deadline
    deadlines.append(academic[0])
    #accept
    accepts.append(academic[1])
    #get after college
    aftercollege_element = driver2.find_element(By.CSS_SELECTOR, ".AfterCollegeSection__DataHeader-czoza-1")
    aftercolleges.append(aftercollege_element.text)

    #get ranking
    ranking_element = driver2.find_elements(By.CSS_SELECTOR, ".RankList__List-sc-2xewen-0")
    ranking = [ele.text for ele in ranking_element]
    ranking = [x.replace('\n', ' ') for x in ranking]
    ranks.append(ranking)
    #Get admission
    admission_element = driver2.find_elements(By.CSS_SELECTOR, ".fQYHzS .kqzCwD")
    admission = ''
    count = 0
    for ele in admission_element:
        if count == 0:
            admission += 'SAT Range : ' + ele.text + ' , '
            count += 1
        elif count == 1:
            admission += 'ACT Range : ' + ele.text + ' , '
            count += 1
        elif count == 2:
            admission += 'High School GPA : ' + ele.text
            count += 1
        else:
            break

    admissions.append(admission)

    #get campus life
    campus_life_element = driver2.find_elements(By.CSS_SELECTOR, ".hXmjaP .bPrOzD")
    housing_and_dorm = ''
    for ele in campus_life_element:
        housing_and_dorm += ele.text + '\n'
    housing_and_dorms.append(housing_and_dorm)

    #get actitvities
    activities_element = driver2.find_element(By.CSS_SELECTOR, ".hXmjaP .lczeeQ")
    sport = activities_element.text + " Sports Teams"
    activities.append(sport)
    driver2.quit()


dict = {'Name':names,'Overview':overviews,'Rank':ranks,'Academics':academics,
        'Cost':costs,'Student':students,'Admission':admissions,'Deadline':deadlines,"Accept rate":accepts,
        'Housing and dorm':housing_and_dorms,'Student Activities':activities,
        'After college':aftercolleges,'Link':links}

df = pd.DataFrame(dict)
df.to_csv('crawl.csv')