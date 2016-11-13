from bs4 import BeautifulSoup
import urllib.request

def menu():
	caldining = BeautifulSoup(urllib.request.urlopen('http://caldining.berkeley.edu/menus/all-locations-d1'), "html.parser")
	restaurants = caldining.find_all("div", class_="meal_items")

	result = {"Cafe 3": {"Brunch": [], "Dinner": []}, 
	"Clark Kerr Campus": {"Breakfast":[], "Lunch":[],"Brunch": [], "Dinner": []}, 
	"Crossroads": {"Breakfast":[], "Lunch":[], "Brunch": [], "Dinner": []}, 
	"Foothill": {"Breakfast":[], "Lunch":[],"Brunch": [], "Dinner": []}}
	place = ""
	time = ""

	for restaurant in restaurants:
		for element in restaurant:
			if "bs4.element.NavigableString" not in str(type(element)):
				if (element.h3):
					for e in element:
						if "bs4.element.NavigableString" not in str(type(e)):
							if (e['class'][0] == "location_period"):
								time = e.get_text()
							else:
								result[place][time].append(e.get_text())
				elif (element.a):
					result[place][time].append(element.get_text())
				else:
					if (element['class'][0] == "location_name"):
						place = element.get_text()
					elif (element['class'][0] == "location_period"):
						time = element.get_text()

	result['cafe3'] = result.pop('Cafe 3')
	result['foothill'] = result.pop('Foothill')
	result['clarkkerr'] = result.pop('Clark Kerr Campus')
	result['crossroads'] = result.pop('Crossroads')
	return result

def filtered_menu():
	filtered_dict = {'cafe3':'', 'crossroads':'', 'foothill':'', 'clarkkerr':''}
	results = menu()
	for restaurant in results.keys():
		for time in results[restaurant].keys():
			if results[restaurant][time] != []:
				filtered_dict[restaurant] += time + '\n' + '\n'.join(results[restaurant][time]) + '\n\n'
	return filtered_dict



def info():
	items = {'cafe3': 'Hours: Mon-Sun (10AM-2PM, 5PM-9PM) \nLocation: 2400 Durant Ave.',
	'clarkkerr': 'Hours: Mon-Fri (7-9:30AM, 5:30PM-8PM), Sat-Sun (10am-2pm, 5:30pm-8pm) \nLocation: 2610 Warring St.',
	'crossroads': 'Hours: Mon-Fri (7-10AM, 11AM-2PM, 5PM-9PM), Sat-Sun (10am-3pm, 5pm-9pm) \nLocation: 2415 Bowditch St.',
	'foothill': 'Hours: Mon-Fri (7-9AM, 10:30AM-2PM, 5PM-8PM), Sat-Sun (10:30am-2pm, 5pm-8pm) \nLocation: 2700 Hearst Ave.',
	'bearwalk': 'Hours: Dusk-3AM \nPhone: 510-642-9255 \nSite: http://bearwalk.berkeley.edu/',
	'calcentral': 'Hours: Mon-Fri (9AM-4PM) \nLocation: Sproul Hall \nPhone: 510-664-9181 \nSite: https://calcentral.berkeley.edu/',
	'gbc': 'Hours: Mon-Th (7:30AM-8PM), Fr (7:30AM-6PM) \nLocation: Upper Sproul by Sather Gate',
	'browns': 'Hours: Mon-Th (7:30AM-6PM), Fri (7:30AM-6PM) \nLocation: Genetics & Plant Biology Rooftop',
	'qualcomm': 'Hours: Mon-Th (7:30AM-6PM), Fri (7:30AM-4PM) \nLocation: Sutardja Dai Hall',
	'ucpd': 'Phone: 510-642-3333 \nLocation: Sproul Hall \nSite: http://ucpd.berkeley.edu/'}
	return items

