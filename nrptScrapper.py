#-------------------------------------------------------------------------------
# Name:        Email Scraper
# Purpose:      Create a that find email address by the domain name
#
# Author:      Beny-DZIENGUE
#
# Created:     03/01/2019
# Copyright:   (c) Beny-DZIENGUE 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#import needed object
import re
import os
import sys
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import http.client
import socket
from bs4 import BeautifulSoup

def getPage(page):
    try:
        # always set a timeout when you connect to an external server
        url =  "nrpt.co.uk"
        #coonect to the http server, return the object connection of type http.client.HTTPConnection
        connection = http.client.HTTPSConnection(url, timeout=10)
        #send request to the server, return an object of type NoneTYpe
        connection.request("GET", page)
        #get response from the server, return the object response of type http.client.HTTPResponse
        response = connection.getresponse()
        #read and reurn the response
        return response.read()
    except socket.timeout:
        # in a real world scenario you would probably do stuff if the
        # socket goes into timeout
        pass

def nbrPage ():
    #get the result of the research, return the object result of type bytes
    result = getPage(page)
    #create a beautifumsoup object, return the object soup of type bs4.BeautifulSoup
    soup = BeautifulSoup(result,features="html.parser")
    #get all link of the pagination, return the object pagination of type bs4.element.ResultSet
    pagination = soup.find('div', class_="pager").find_all('a')
    print(pagination)
    #create the object that will contain the href of all links, return the object paginationLinks
    paginationLinks = []
    #condition to read each element of pagination
    for link in pagination:
        if len(pagination) == 1:
            paginationLinks.append(link.get("href"))
        #condition to verify if the actual element is the last
        elif len(pagination) > 1 and link == pagination[-1]:
            #pass
            pass
        else:
            #add the href of the link in paginationLinks
            paginationLinks.append(link.get("href"))

    #return paginationLinks
    return paginationLinks

def getTrainersName(soup,trainersName):
    #get all h2 Tag, return the object h2Tag of type list
    h2Tag = soup.find('ul', class_="searchresults").find_all('h2')
    #condition to read each element of h2Tag
    for h2 in h2Tag:
        #add all link text in trainersName
        trainersName.append(h2.find('a').text)
    #return trainersName
    return trainersName

def getTrainersUrl(pageList):
    #create the object that will contain all trainersUrl href, return the object trainersHref of type list
    trainersHref = []
    #create the object that will contain all traners names, return the object trainersName of type list
    trainersName = []
    #excecute 7 instruction in same time
    with PoolExecutor(max_workers=7) as executor:
        #get the result of the research, return the object sourcePage of type bytes
        for sourcePage in executor.map(getPage, pageList):
            #create a beautifulsoup object, return the object soup of type bs4.BeautifulSoup
            soup = BeautifulSoup(sourcePage,features="html.parser")
            #get all trainers url, return the object trainersUrl of type list
            trainersUrl = soup.find_all("a", class_="wtrk-click")
            for link in trainersUrl:
                if link.get("href") not in trainersHref:
                    trainersHref.append(link.get("href"))
            trainersName = getTrainersName(soup,trainersName)

    #create the object that will contain trainersName and trainerHref
    trainerInfo = [trainersHref,trainersName]
    return trainerInfo

def getTrainersWebsite(trainerHref):
    #create the object that will contain all trainers Website url, return the object trainerWebsite of type list
    trainerWebsite = []
    #excecute 7 instruction in same time
    with PoolExecutor(max_workers=7) as executor:
        #get the result of the research, return the object sourcePage of type bytes
        for sourcePage in executor.map(getPage, trainerHref):
            #create a beautifulsoup object, return the object soup of type bs4.BeautifulSoup
            soup = BeautifulSoup(sourcePage,features="html.parser")
            #get trainers website link , return the object pageLink of type list
            pageLink = soup.find('div', class_="tab-website").find('p', class_='purpleblock').find_all('a')
            #condition to read element of pageLink
            for link in pageLink:
                #add the href of the link in trainerWebsite
                trainerWebsite.append(link.get('href'))
    #return trainerWebsite
    return trainerWebsite

def writeModel(trainersName,trainersWebsite):
    #create the object that will contain the final output, return the object finalOutput of type list
    finalOutput = []
    for name,websiteLink in zip(trainersName,trainersWebsite):
        #append name in finalOutput
        finalOutput.append(("   Name   :"+("{}".center(10," "))).format(name))
        #append websiteLink in finalOutput
        finalOutput.append(("        Website-link   :"+("{}".center(10," "))+"\n\n").format(websiteLink))
    #return finalOutput
    return finalOutput

def whriteInOuput(finalOutput):
    """
    Whrite the result in a file txt
    """

    os.chdir("D:/IIHT/Python/Project/NRPT scrapper/caches")
     #open text file, return  an object of type io.TextIOWrapper
    with open("Trainer----{}.txt".format(location), "w") as writ:
        #write each line in the object op, return an object of type int
        writ.write('\n'.join(finalOutput) + "\n")

#get location, return the object location of type str
location = input('Enter a location')

#initialise the object page, return the object page of type str
page = "/profiles/trainers/searchresults.htm?query={}&page=1".format(location)

paginationLinks = nbrPage()
trainerInfo = getTrainersUrl(paginationLinks)
trainersName = trainerInfo[1]
trainerHref = trainerInfo[0]
trainersWebsite = getTrainersWebsite(trainerHref)
finalOutput = writeModel(trainersName,trainersWebsite)
whriteInOuput(finalOutput)

