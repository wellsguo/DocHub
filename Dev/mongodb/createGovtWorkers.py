import pymongo
import pprint
import numpy as np
import datetime

from pymongo import MongoClient

np.random.seed(2)  # set seed so everybody running it gets the same data

client = MongoClient()  # connects on default host
# client = MongoClient('localhost',27017))  # explicit connect command

db = client.db_people    


# remove entire collection, i.e. all docs in peopleDB.thePeople 
db.thePeople.remove()

# create UNIQUE INDEX
# db.thePeople.create_index( [('pid', pymongo.ASCENDING)], unique=True )

# the collection we will create
peeps = db.thePeople  


states = ["AL","AK","AZ","AZ","AR","CA","CO","CT","DE","FL","GA", "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD", "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ", "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC", "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]

fNames = ["Bob","Mary","Isabella","Santiago","Valentina","Daniella","Alejandro","Diego","Victoria","Sofia","John","Paul","Peter","Joseph","Vicky","David","Jeffrey","William","Jennifer","Linda","Sarah","Ashley","Michelle","Amy","Julie","Julia","Hannah","Jayden","Noah","Demarco","Madison","Ava","Kayla","Jayla","Priya","Tanya","Neha","Rahul","Raj","Amit","Mohammed","Mohammad","Vivek","Fatimah","Hasan"]

mNames = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

lNames = ["Garcia","Martinez","Gonzalez","Lopez","Torres","Ramirez","Hernandez","Baker","Jackson","Brown","Smith","Jones","Miller","White","Johnson","Wilson","Williams","Anderson","Das","Mukherjee","Simha","Liu","Li","Zhao","Zhang","Wu","Chen","Chan","Lee","Wong","Park","Kim","Ngyuen","Le","Tran","Dang","Sato","Tanaka","Takahashi"]

timeStartInsert = datetime.datetime.now()
numDocs = 2000
print("\nStart inserting " + str(numDocs) + " documents at: " + str(timeStartInsert) )
for i in range(0,numDocs):
	aPid = i
	aFName = fNames[ np.random.randint(len(fNames)) ]
	aMName = mNames[ np.random.randint(len(mNames)) ]
	aLName = lNames[ np.random.randint(len(lNames)) ]
	aName = aFName + " " + aMName + " " + aLName
	print(aName)
	aAge = np.random.randint(100) + 18
	aWeight = np.random.randint(100) + 40 # in Kilos
	aHeight = np.random.randint(150,200)  # in centimeters
	aBirth = 2019 - aAge
	aSalary = np.random.randint(100000) + 30000  # lowests paid is 30K
	aState = states[ np.random.randint( len(states) ) ]
	aChildren = []
	if (aAge > 20):
		aNumChildren = np.random.binomial(8,0.40)  # 0..8 children, binomially distributed with probability p = 0.40
		for j in range (0,aNumChildren):
			aChildren.append( fNames[ np.random.randint(len(fNames)) ] + " " + mNames[ np.random.randint(len(mNames)) ] + " " + aLName)
	else:
		aNumChildren = 0
	newPerson = {"pid":aPid,"firstName":aFName, "MI":aMName, "lastName":aLName, "state":aState, "age":aAge,"birth":aBirth, "salary":aSalary, "numChildren":aNumChildren,"children":aChildren, "weight":aWeight, "height":aHeight}
	print(newPerson)
	peeps.insert_one(newPerson)

timeEndInsert = datetime.datetime.now()
timeElapsedInsert = timeEndInsert - timeStartInsert
timeStartQueries = datetime.datetime.now()

print("\nNumber of docs in db.thePeople = " + str(db.thePeople.count()))
# print("\nAt start, output from peeps.find():")
# for objs in peeps.find():
# 	print(objs)

numQueries = 4
print("\nStart " + str(numQueries) + " random queries at: ")
print(datetime.datetime.now())
for i in range(1,numQueries):
	randPID = np.random.randint(numDocs)
	anObject = db.thePeople.find_one( {"pid":randPID} )
	print(anObject)

timeEndQueries = datetime.datetime.now()
timeElapsedQueries = timeEndQueries - timeStartQueries
	
'''
print("\nFinished random queries at: ")
print(datetime.datetime.now())


print("\nElapsed time for inserts = " + str(timeElapsedInsert) ) ;
print("\nElapsed time for queries = " + str(timeElapsedQueries) ) ;

'''
