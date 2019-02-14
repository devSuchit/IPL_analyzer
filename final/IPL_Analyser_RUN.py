import pandas as pd
import numpy as np
import operator
import csv
file={}
bats={}
yrs=[12,13,15,16,17,18]
bats_final={}

bowls={}
bowls_final={}

def processor_bat():

   
    for i in yrs:
        file[i]=pd.read_csv("20{}_batsman_ranked.csv".format(i))
    
    basefile=pd.read_csv("2012_batsman_ranked.csv")
    
    for i in range(basefile.shape[0]):
        name=(basefile.iloc[i])["Player's Name"]
        val=[]
        for n in yrs:
            temp=file[n].iloc[i]
            if(temp["Ball"]==0):
                val.append(0)
            else:
                temp_value=temp["Strike Rate"]*temp["Ball"]
                val.append(temp_value)
        bats[name]=val
        
        
 
def predictor_bat():
     yr=np.asarray(yrs)
     basefile=pd.read_csv("2012_batsman_ranked.csv")  
     for i in range(basefile.shape[0]):
         name=(basefile.iloc[i])["Player's Name"]
         z=np.polyfit(yr,np.asarray(bats[name]),5)
         z1=np.poly1d(z)
         bats_final[name]=abs(z1(19))
         
    
         
         
def analyser_bat():
    processor_bat() 
    predictor_bat()
    final_bats= sorted(bats_final.items(), key=operator.itemgetter(1),reverse=True)
    return(final_bats)
        
#======================#


def processor_bowl():

    
    for i in yrs:
        file[i]=pd.read_csv("20{}_bowlers_ranked.csv".format(i))
    
    basefile=pd.read_csv("2012_bowlers_ranked.csv")
    
    for i in range(basefile.shape[0]):
        name=(basefile.iloc[i])["Player's Name"]
        val=[]
        for n in yrs:
            temp=file[n].iloc[i]
            if(temp["Balls Bowled"]==0):
                val.append(0)
            else:
                temp_value=(1/(float(temp["Economy"])))*temp["Matches Played"]
                val.append(temp_value)
        bowls[name]=val
        
        
 
def predictor_bowl():
     yr=np.asarray(yrs)
     basefile=pd.read_csv("2012_bowlers_ranked.csv")  
     for i in range(basefile.shape[0]):
         name=(basefile.iloc[i])["Player's Name"]
         z=np.polyfit(yr,np.asarray(bowls[name]),5)
         z1=np.poly1d(z)
         bowls_final[name]=abs(z1(18))
         
    
         
         
def analyser_bowl():
    processor_bowl() 
    predictor_bowl()
    final_bowlers= sorted(bowls_final.items(), key=operator.itemgetter(1),reverse=True)
    return(final_bowlers)
        
    


def main():
    final_batsmen_ranklist=analyser_bat()  #list of all batsmen
    final_bowlers_ranklist=analyser_bowl() #list of all bowlers
    
        
    f = open('2019_ipl_allrounders.rtf','r')
    hold_ar=[]
    all_rounders = list(f.readlines())
    for word in all_rounders:
        word=word.replace("\n","")
        word=word.replace("\\","")
        word=word.replace(" ","")
        word=word.replace("}","")
        word.rstrip()
        if(len(word) < 20):
            hold_ar.append(word)
            
    g = open('2019_ipl_wk.rtf','r')
    hold_wk=[]
    wicket_keepers = list(g.readlines())
    for word in wicket_keepers:
        word=word.replace("\n","")
        word=word.replace("\\","")
        word=word.replace("}","")
        word=word.replace(" ","")
        word.rstrip()
        if(len(word) < 20):
            hold_wk.append(word)
  
    counter=0
    final_team=[]
    
    for i in range(4):
        final_team.append(final_batsmen_ranklist[i][0].rstrip())
    for member in final_batsmen_ranklist:
        word=member[0].replace("\n","")
        word=word.replace("\\","")
        word=word.replace(" ","")
        word=word.replace("}","")
        if(word in hold_ar):
            final_team.append(member[0])
            counter=counter+1
            if(counter==2):
                break
            
    for member in final_batsmen_ranklist:
        word=member[0].replace("\n","")
        word=word.replace("\\","")
        word=word.replace(" ","")
        word=word.replace("}","")
        if(word in hold_wk and member[0].rstrip() not in final_team):
            final_team.append(member[0].rstrip())
            break
        
    for i in range(4):
        final_team.append(final_bowlers_ranklist[i][0].rstrip())
            
    with open('FinalTeam.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["2019 IPL TEAM"])
        for member in final_team:
            writer.writerow([member])
        
main()        
        
            
