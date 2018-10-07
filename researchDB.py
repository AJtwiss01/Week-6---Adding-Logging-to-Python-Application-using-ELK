import os
import sqlite3
import logging
import logstash
import sys

# setLogstash config
host = '18.237.228.31'

test_logger = logging.getLogger('My Reseach DB creation log with sqlite')
test_logger.setLevel(logging.DEBUG)
test_logger.addHandler(logstash.LogstashHandler(host, 5959, version=1))
test_logger.info('Database was open')

##create db research 
db = 'research.db'
con = sqlite3.connect(db)
if con.cursor(): 
    test_logger.debug('Database was open')
else:
    print('closed')



##create tabel if it does not exist and insert data
con.execute('''create table if not exists people
    ( id integer primary key,
    name varchar,
    position varchar,
    phone varchar,
    office varchar)''')

con.execute('''create table if not exists experiment (
   id integer primary key,
   name varchar,
   researcher integer,
   description text,
   foreign key(researcher) references people(id)
)''')
##insert into people table
con.execute("INSERT INTO people VALUES( 1,'Alice', 'Research Director', '555-123-0001', '4b')")

con.execute("INSERT INTO people VALUES(2, 'Bob', 'Research assistant', '555-123-0002', '17')")
con.execute("INSERT INTO people VALUES(3,'Charles', 'Research assistant', '555-123-0001', '24')")
con.execute("INSERT INTO people VALUES(4, 'David', 'Research assistant', '555-123-0001', '8')")
con.execute("INSERT INTO people VALUES(5,  'Edward', 'Toadie', 'None', 'Basement')")

##insert into experiments
##alices research projects
con.execute("INSERT INTO experiment VALUES( null, 'A Vacine', 1, 'for the B virus')")
con.execute("INSERT INTO experiment VALUES( null, 'B Vacine', 1, 'for the B virus')")

##bobs research projects
con.execute("INSERT INTO experiment VALUES( null, 'C Vacine', 2, 'for the C virus')")
con.execute("INSERT INTO experiment VALUES( null, 'D Vacine', 2, 'for the D virus')")

##Charles research projects
con.execute("INSERT INTO experiment VALUES( null, 'E Vacine', 3, 'for the E virus')")
con.execute("INSERT INTO experiment VALUES( null, 'F Vacine', 3, 'for the F virus')")

##David research projects
con.execute("INSERT INTO experiment VALUES( null, 'G Vacine', 4, 'for the G virus')")
con.execute("INSERT INTO experiment VALUES( null, 'H Vacine', 4, 'for the H virus')")

people = con.execute('select * from people')
experiment = con.execute('select * from experiment')

##print items from people table
for i in people:
   print(i)

##pirint print items from experiment table
for i in experiment:
   print(i)
   
##check name and research title before switch and deletion of alice
r = con.execute('select p.name, e.name from people as p join experiment as e where e.researcher == p.id')

for i in r:
   print('Name: %s\n\tExperiment: %s' % (i[0],i[1]))



##Add new user
newUserInsert = con.execute("INSERT INTO people VALUES(6,  'AJ', 'Intern', '7602241830', '4b')")
##show all people in table again

##selecting alices info
aliceSelect = con.execute('select c.position, c.id from people as c where c.id = 1')
for i in aliceSelect:
##    grab alice's position and make it a string 
    allicesPosition = str(i[0])
    allicesID = i[1]


#select new Reserach Director
ajSelect = con.execute('select c.id from people as c where c.id = 6')
for i in ajSelect:
##    grab aj's id
    ajID = i[0]

##asign to a array sor sqlite to see one object - error with 17 binds so consolitate to 1 object
##find the Research Director and delete previouse director
removeResearchDirector =  con.execute("DELETE FROM people WHERE position = ?",([str(allicesPosition)]))

##Update inter becuase he was impressive to Research director
updateInternToResearchDirector =  con.execute("UPDATE people set position = ? Where id = ?",( str(allicesPosition) ,"6"))


print('\n************************************************** \n \n NOW THE SWITCH of Position and Research Projects\n \n**************************************************\n')

##print new list to show alice is deleted an AJ is promoted 
selectPeople = con.execute('select * from people')
for i in selectPeople:
   print(i)
#    added logger to record researchers 
   test_logger.info('Researcher put into reasearcherDB: %s ', i)
   
##switch reseach projects to AJ id 
updateNewRDwithAlicesProjects =  con.execute("UPDATE experiment set researcher = ? Where researcher = ?",( ajID , allicesID))

##print out new positon list selecting table as p alias
updatePrint = con.execute('select p.name, e.name from people as p join experiment as e where e.researcher == p.id')
for i in updatePrint:
   print('Name: %s\n\tExperiment: %s' % (i[0],i[1]))
#    added logger ot record db experiments
   test_logger.info('tExperiments : %s ', i[1])

    
