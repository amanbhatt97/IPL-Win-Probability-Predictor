# Importing libraries
import streamlit as st
import pickle
import pandas as pd

# all team names
teams = ['Sunrisers Hyderabad',
         'Mumbai Indians',
         'Royal Challengers Bangalore',
         'Kolkata Knight Riders',
         'Kings XI Punjab',
         'Chennai Super Kings',
         'Rajasthan Royals',
         'Delhi Capitals']

# all cities names
cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
           'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
           'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
           'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
           'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
           'Sharjah', 'Mohali', 'Bengaluru']

# loading pickle file in right binary mode
pipe = pickle.load(open('pipe.pkl','rb'))

# Display Options

# display title
st.title('IPL Win Predictor')

# display 2 columns for team names
col1, col2 = st.columns(2)

# display team names in dropdown
with col1:
    batting_team = st.selectbox('Select the batting team',sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team',sorted(teams))

# display city names in dropdown
selected_city = st.selectbox('Select host city',sorted(cities))

# to input target score
target = st.number_input('Target', step = 1)

# display 3 columns for 'Score', 'Overs Completed', 'Wickets Out'
col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input('Score', step = 1)
with col4:
    overs = st.number_input('Overs completed', step = 1)
with col5:
    wickets = st.number_input('Wickets out', step = 1)

# make a button for 'Predict Probability'
if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    crr = score/overs
    rrr = (runs_left * 6)/balls_left

    input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],
                             'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],
                             'wickets_remain':[wickets_left],'target':[target],'crr':[crr],'rrr':[rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + " - " + str(round(win*100)) + "%")
    st.header(bowling_team + " - " + str(round(loss*100)) + "%")