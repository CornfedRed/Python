import streamlit as st
import plotly.graph_objects as go
import calendar
from datetime import datetime
import random
from random import randrange
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd






# ------------------------------- mySQL Server ------------------------------
db = mysql.connector.connect(
    host="gt7champ.cqlgkgr3sepu.us-west-2.rds.amazonaws.com",
    user="admin",
    password= st.secrets["dbPassword"],
    port="3306",
    database="GT7"
)




# ------------------------------- Settings ------------------------------

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """

st.markdown(hide_st_style, unsafe_allow_html=True)


# ------------------------------ Functions -----------------------------

cursor = db.cursor()







#------------------------------ Sidebar Menu -----------------------------

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Race", "Standings", "Configuration"],
        icons=["caret-right-square-fill", "card-list", "gear"],
        default_index=1, #Starting Menu Item,
        #### Menu Settings ####
        styles={
            "container": {"padding": "0!important", "background-color": "#B0B0B0"},
            "icon": {"color": "white", "font-size": "25px"}, 
            "nav-link": {
                "font-size": "25px", 
                "text-align": "left", 
                "margin":"0px", 
                "--hover-color": "#eee"
            },
            "nav-link-selected": {"background-color": "red"},
        },
    )







########################################################################
# ------------------------------- Race -------------------------------
if selected == "Race" :


    cursor.execute("SELECT champName from championship")
    allchampionships = cursor.fetchall()
    championship = [item[0] for item in allchampionships]

  
    cursor.execute("SELECT * from Tracks")
    tracks = cursor.fetchall()
            
    cursor.execute("Select racerName from racersGT")  
    allracers = cursor.fetchall()
    racerNames = [item[0] for item in allracers] 

    cursor.execute("Select powerType from powerTrain")
    powerTrains = cursor.fetchall()
    powertrainName = [item[0] for item in powerTrains]
    

    generateRace = st.button("Generate Race")

        
    st.subheader("Select desired settings")


    slider_range = st.slider("Select Minimum and Maximum PP", value=[400,1100])
    minPP = slider_range[0]
    maxPP = slider_range[1]
    racepp = random.randint(minPP,maxPP)

    selected_championship = st.selectbox("Select Championship:", championship)
        

    st.write("---")     
    st.title(f"Race")
    st.write("---") 

    global race
    global racetype

    race = random.choice(tracks)        
    racetype = random.choice(powertrainName)
    racerNames.sort()

    st.subheader("Track")
                
    st.write("Race Track:  ", race[1])
    st.write("Race Length:  ", race[3])
    st.write("Race Weather:  ", race[4])
    st.write("Race Surface:  ", race[6])
    st.subheader("Performance Points")
    st.write("Race PP: ", racepp)
    st.subheader("Vehicle")
    if race[3] == "Dirt" :
        st.write("Vehicle Type: 4WD")
    else :
            st.write("Vehicle Type: ", racetype)
  

            
                
                
    st.write("---") 
    st.header(f"Race Results")
    st.write("---") 
    st.write(race[1])                
    firstplace = st.radio("First Place", racerNames, horizontal=True, index=0)
    secondplace = st.radio("Second Place", racerNames, horizontal=True, index=0)
    pole = st.radio("Pole Position", racerNames, horizontal=True, index=0)
    fastestlap = st.radio("Fastest Lap", racerNames, horizontal=True, index=0)


    saveRace = st.button("Save Race Results")           

    if saveRace:
                
        cursor.execute("INSERT INTO completedRaces (championship, raceTrack, firstPlace, secondPlace, Pole, fastestLap) VALUES(%s,%s,%s,%s,%s,%s)", (selected_championship,race[0],firstplace,secondplace,pole,fastestlap))
        db.commit()
        st.success("Race Results Saved!")  
                
        

    




    
    
    
    
    
    
###########################################################################
# ------------------------------- Standings -------------------------------
if selected == "Standings" :
    cursor.execute("SELECT champName from championship")
    allchampionships = cursor.fetchall()
    championship = [item[0] for item in allchampionships]
    
    st.title(f"Standings")
    selectedchamp = st.selectbox("Championship", championship)
    
    cursor.execute("Select champFirst from championship WHERE champName=%s", [selectedchamp])
    temp = cursor.fetchall()
    firstPlace1 = temp[0][0]
    cursor.execute("Select champSecond from championship WHERE champName=%s", [selectedchamp])
    temp = cursor.fetchall()
    secondPlace1 = temp[0][0]
    cursor.execute("Select champFastest from championship WHERE champName=%s", [selectedchamp])
    temp = cursor.fetchall()
    Fastest1 = temp[0][0]
    cursor.execute("Select champPole from championship WHERE champName=%s", [selectedchamp])
    temp = cursor.fetchall()
    Pole1 = temp[0][0]



    cursor.execute("SELECT * from completedRaces WHERE championship=%s", [selectedchamp])
    completedRaces = cursor.fetchall()

    #cursor.execute("SELECT racerName from championshipRacers WHERE champName=%s", [selectedchamp])
    #standingsDict = pd.DataFrame(cursor.fetchall())
    
    cursor.execute("SELECT * from completedRaces WHERE championship=%s", [selectedchamp])
    standingsDict = pd.DataFrame(cursor.fetchall())
    



      
    #standingsDict.to_dict()




   
    st.write(firstPlace1, " ", secondPlace1, " ", Fastest1, " ", Pole1)
    st.write(standingsDict)









    
    
    
    
    
    
    
    
    
    
    

########################################################################
# ------------------------------- Config -------------------------------
if selected == "Configuration" :

    selectedconfig = option_menu(
        
        menu_title=None,
        options=["Add Racer", "Add Track", "Add Vehicle Type", "Add Championship"],
        icons=["person", "arrow-clockwise", "minecart", "trophy"],
        default_index=0, #Starting Menu Item
        orientation="horizontal",
        #### Menu Settings ####
        styles={
            "container": {"padding": "0!important", "background-color": "#B0B0B0"},
            "icon": {"color": "white", "font-size": "30px"}, 
            "nav-link": {
                "font-size": "12px", 
                "text-align": "center", 
                "margin":"0px", 
                "--hover-color": "#eee"
            },
            "nav-link-selected": {"background-color": "red"},
        },
    )
    
   

# ------------------------------- Add Racer-------------------------------
    
    if selectedconfig == "Add Racer" :

        st.header(f"Add Racer")
        with st.form("Racer Form", clear_on_submit=True):
            displayname = st.text_input("Display Name:")
            racernumber = st.number_input ("Number:", min_value=1, max_value=999, format="%i")
            submitted = st.form_submit_button("Save Data")
            if submitted:                               
                cursor.execute("INSERT INTO racersGT (racerName, racerNumber) VALUES (%s,%s)", (displayname,racernumber))
                db.commit()
              
                st.write(f"Display Name: {displayname}")
                st.write(f"Number: {racernumber}")
                st.success("Racer Added!")




# ------------------------------- Add Track-------------------------------
    
    if selectedconfig == "Add Track" :
        
        st.header("Add Track")
        with st.form("Track Form"):
            trackName = st.text_input("Track Name")
            countryName = st.text_input("Country")
            totalLength =st.text_input("Length")
            weatherAvail = st.radio("Weather Type", ('Wet and Dry', 'Dry Only'), horizontal=True, index=0)
            timeAvail = st.radio("Driveable at night?", ('Yes', 'Twilight Only', 'No'), horizontal=True, index=0)
            typeTrack = st.radio("Surface Type", ('Asphalt', 'Asphalt - Rally', 'Asphalt - Roval', 'Asphalt - Street', 'Dirt', 'Concrete'), horizontal=True, index=0)
            reverseLayout = st.radio("Reverse Available", ('Yes', 'No'), horizontal=True, index=0)
            submitted = st.form_submit_button("Save Track")

            if submitted:
                cursor.execute("INSERT INTO Tracks (Track, Country, Length, Weather, Drivable, Type, Reverse) VALUES (%s, %s, %s, %s, %s, %s, %s)", (trackName, countryName, totalLength, weatherAvail, timeAvail,typeTrack,reverseLayout))
                db.commit()
                st.success("Power Train Added!")


        
 

# ------------------------------- Add Type-------------------------------
    
    if selectedconfig == "Add Vehicle Type" :
    
        st.header(f"Add Drivetrain")
        with st.form('Power Trains'):
            ptName = st.text_input("PowerTrain")
            submitted = st.form_submit_button("Save Power Train")

            if submitted:
                cursor.execute("INSERT INTO powerTrain (powerType) VALUES (%s)", (ptName))
                db.commit()
                st.success("Power Train Added!")


   
# ------------------------------- Add Championship-------------------------------
    
    if selectedconfig == "Add Championship" :

        st.header(f"Add Championship")
        with st.form("Championship Form", clear_on_submit=True):
            cname = st.text_input("Championship Name:")
            firstp = st.number_input("First Place Points:", min_value=1, max_value=999, format="%i")
            secondp = st.number_input("Second Place Points:", min_value=1 ,max_value=999, format="%i")
            thirdp = st.number_input("Third Place Points:",  min_value=0 , max_value=999, format="%i")
            fastest = st.number_input("Fastest Lap Points:", min_value=1 , max_value=999, format="%i")  
            pole = st.number_input("Pole Position Points:", min_value=1 , max_value=999, format="%i")              
            submitted = st.form_submit_button("Save Data")

            
            if submitted:
                cursor.execute("INSERT INTO championship (champName, champFirst, champSecond, champThird, champFastest, champPole) VALUES (%s,%s,%s,%s,%s,%s)", (cname,firstp,secondp,thirdp,fastest,pole))
                db.commit() 
                st.success("Championship Added!")
