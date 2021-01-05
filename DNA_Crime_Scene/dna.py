from sys import argv
import csv
import time

def Desired_Sequences(crimeDb):
  #Creates list of Desired STR's
  Headers=crimeDb[0]
  CS=[] 
  for x in Headers:
    if x!='CrimeID':
      CS.append(x)
  return CS

def sorted_sequence(suspect,crime_sequences):
  #Creates a list of occurnces for each desired sequence 
  sortedlist=[]
  Test_DNA=suspect['Sequence']

  for element in crime_sequences:
    count=1
    len_sequence=len(element)
    list1=[]
    
    #Goes through each letter and tests if substring equals desired sequence 
    for letter in range(len(Test_DNA)-len_sequence):
      if Test_DNA[letter:(letter+len_sequence)]==element and ((Test_DNA[letter+len_sequence:letter+(2*len_sequence)]==element)):
        count+=1
        letter+=len_sequence
        #if the following substring does not equal the current one, add that length of the run of consectuive sequences to a list 
        if (Test_DNA[letter:letter+len_sequence]!=Test_DNA[letter+len_sequence:letter+len_sequence+len_sequence]):
          list1.append(count)
          count=1
    #Adss the longest "runs" to a Final list that is used to compare to crime scenes
    if len(list1)!=0:
      sortedlist.append(max(list1))
    else:
      sortedlist.append(count)

  return sortedlist


def compare (CrimeData,current_suspect,suspect_sequences_num,newfile):
  Guilty_Crimes=[]
  for row in CrimeData[1:len(CrimeData)]:
    Crime_str_list=[]
    for i in range(1,len(row)):
      Crime_str_list.append(int(row[i]))   

    count=0
    for x in range(len(suspect_sequences_num)):
      if suspect_sequences_num[x]==Crime_str_list[x]:
        count+=1
      else:
        x=len(suspect_sequences_num)

    if count==len(suspect_sequences_num):
      Guilty_Crimes.append(row[0])
      
  newfile.writerow({'Suspect' : current_suspect['Suspect'], 'Crimes': ','.join(Guilty_Crimes)})
  return 


def run():
  if len(argv)<4:
    print(f"Usage: python 3 {argv[0]} crimedb suspectdb solutiondb")

  #opening Crime and Suspect files and creating Solutions file
  with open(argv[1], newline='') as crimes_csv:
    Crimes_Reader=list(csv.reader(crimes_csv))
    with open(argv[2], newline='') as suspect_csv:
      Suspects_Reader=csv.DictReader(suspect_csv)
      with open(argv[3], 'w', newline='') as solution_csv:
        Solutions_Writer=csv.DictWriter(solution_csv,('Suspect','Crimes'), delimiter=",",dialect='excel-tab')
        Solutions_Writer.writeheader()
        #Creates a list of the Sequence Headers
        list_of_desired_sequences=Desired_Sequences(Crimes_Reader)
        for S in Suspects_Reader:
          #Creates list of occurences for each sequence
          Sequences_Occurences=sorted_sequence(S,list_of_desired_sequences)
          print(Sequences_Occurences)
          #Compares the sequence list for the suspect and the sequences at the crime scenes and writes the soltuions to a new file
          comparison=compare(Crimes_Reader,S,Sequences_Occurences,Solutions_Writer)
  return 
  
if __name__ == "__main__":
  start = time.perf_counter()
  run()
  end = time.perf_counter()
  print(f"Time used: {end-start} seconds")



# python3 dna.py crimedb/crime_small.csv suspectdb/suspect_small.csv answer_small.csv

# python3 dna.py crimedb/crime_large.csv suspectdb/suspect_large.csv answer_large.csv

# python3 dna.py crimedb/crime_other.csv suspectdb/suspect_other.csv answer_other.csv

