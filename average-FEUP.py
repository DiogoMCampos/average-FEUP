import re
import getpass
from robobrowser import RoboBrowser


def stringToFloat(str):
    return float(str.replace(',', '.'))


def gatherData(user, password):
    baseURL = 'https://sigarra.up.pt/feup/pt/'
    browser = RoboBrowser(history=True, parser='html.parser')
    browser.open(baseURL + 'web_page.Inicial')

    # Gets the login form
    form = browser.get_form(action=re.compile(r'validacao'))

    # Updates the login form with the user credentials
    form['p_user'].value = 'up' + user
    form['p_pass'].value = password

    browser.submit_form(form)

    # Goes to the user profile
    browser.open(baseURL + 'fest_geral.cursos_list?pv_num_unico=' + user)

    # Opens the extended view
    extended = browser.find(title='Visualizar informações no contexto do curso')
    browser.follow_link(extended)

    credits = []
    grades = []

    # For each html class containing grades ("i", "p" and "o"), gather data
    for i in browser.find_all(class_='i'):
        if i.find(class_='n aprovado'):
            credits.append(i.find(class_='k n').text)
            grades.append(i.find(class_='n aprovado').text)

    for j in browser.find_all(class_='p'):
        if j.find(class_='n aprovado'):
            credits.append(j.find(class_='k n').text)
            grades.append(j.find(class_='n aprovado').text)

    for k in browser.find_all(class_='o'):
        if k.find(class_='n aprovado'):
            credits.append(k.find(class_='k n').text)
            grades.append(k.find(class_='n aprovado').text)

    return credits, grades


def calculateAverage():
    print('Introduz o número de estudante (ex: 2014xxxxx):', end=' ')
    user = input()
    password = getpass.getpass()

    creditsSum = 0
    gradesSum = 0

    credits, grades = gatherData(user, password)

    # Calculate the weighted average
    for x in range(0, len(grades)):
        creditsSum += stringToFloat(credits[x])
        gradesSum += stringToFloat(grades[x]) * stringToFloat(credits[x])

    average = gradesSum / creditsSum

    print('A média é:', average, end='')

calculateAverage()
