import requests
from bs4 import BeautifulSoup

def get_project_details(url):
    response = requests.get(url, verify=False)  # Disable SSL certificate verification
    soup = BeautifulSoup(response.text, 'html.parser')

    projects = []
    for i, project_row in enumerate(soup.select('table#tableRegisteredProjects tbody tr')):
        if i >= 6:  # Limiting to the first 6 projects
            break
        
        project = {}
        columns = project_row.find_all('td')
        project['Name'] = columns[0].get_text(strip=True)
        project['Promoter Type'] = columns[1].get_text(strip=True)
        project['Registration No.'] = columns[2].find('a').get_text(strip=True)
        detail_url = 'https://hprera.nic.in' + columns[2].find('a')['href']
        
        # Get details from the detail page
        detail_response = requests.get(detail_url, verify=False)  # Disable SSL certificate verification
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
        details_table = detail_soup.find('table', {'id': 'DataGrid1'})

        for row in details_table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                if key in ['GSTIN No.', 'PAN No.', 'Name', 'Permanent Address']:
                    project[key] = value

        projects.append(project)

    return projects

url = 'https://hprera.nic.in/PublicDashboard'
projects = get_project_details(url)

for i, project in enumerate(projects, 1):
    print(f"Project {i}:")
    for key, value in project.items():
        print(f"{key}: {value}")
    print()
