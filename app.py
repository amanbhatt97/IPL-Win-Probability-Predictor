#----- dependencies -----#
import streamlit as st
import pickle, joblib
import pandas as pd
import os, sys


# sys.path.append('..')
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 

# get the parent directory path
parent_directory = os.getcwd()

# paths
model_path = os.path.join(parent_directory, 'model') 


#----- all team names -----#
teams = ['Sunrisers Hyderabad',
         'Mumbai Indians',
         'Royal Challengers Bangalore',
         'Kolkata Knight Riders',
         'Kings XI Punjab',
         'Chennai Super Kings',
         'Rajasthan Royals',
         'Delhi Capitals']


#----- all cities names -----#
cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
           'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
           'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
           'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
           'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
           'Sharjah', 'Mohali', 'Bengaluru']


# loading pickle file in right binary mode
pipe = joblib.load(os.path.join(model_path, 'pipe.pkl'))
# print(os.path.join(model_path, 'pipe.pkl'))

#----- front-end -----#

# side bar
st.sidebar.info("Welcome to the IPL Win Probability Predictor dashboard!")

# Define page layout
col1, col2 = st.columns([1, 4])
# display title
with col2:
    st.title('IPL Win Predictor')
    st.markdown("---")

    # display 2 columns for team names
    col1, col2 = st.columns(2)

    # display team names in dropdown
    with col1:
        batting_team = st.selectbox('Select the batting team',sorted(teams))
        # Generate the list of available bowling teams
        available_bowling_teams = [team for team in sorted(teams) if team != batting_team]
        
    with col2:
        bowling_team = st.selectbox('Select the bowling team',sorted(available_bowling_teams))


    # display city names in dropdown
    selected_city = st.selectbox('Select host city',sorted(cities))

    # to input target score
    target = st.number_input('Target', step = 1, min_value=1, max_value=300)

    # display 3 columns for 'Score', 'Overs Completed', 'Wickets Out'
    col3,col4,col5 = st.columns(3)

    with col3:
        score = st.number_input('Current Score', step = 1, min_value=1, max_value=300)
    with col4:
        overs = st.number_input('Overs completed', step = 1, min_value=1, max_value=19)
    with col5:
        wickets = st.number_input('Wickets out', step = 1, min_value=0, max_value=9)


    # #----- make a button for 'Predict Probability' ------#
    # if st.button('Predict Probability'):
            
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

    st.markdown("---")
    st.header('Winning Probability') 
    st.info(batting_team + " - " + str(round(win*100)) + "%")
    st.info(bowling_team + " - " + str(round(loss*100)) + "%")



# Define usage instructions as a string
usage_instructions = """
**Usage Instructions**

**Note**: This predictor assumes that one of the team has already finished batting.
1. Select the batting team for which you want to calculate winning probability.
2. Select the bowling team and host city.
3. Type the target set for the batting team.
4. Type the current score, overs completed and number of wickets fallen.
5. Click on **Predict Probaility** button.

"""

with st.sidebar:
    st.markdown("---")
    st.markdown(usage_instructions)
    st.markdown("---")

with st.container():
    st.markdown("---")
    st.subheader("About the Dashboard")
    st.markdown("This dashboard predicts the winning probabilty of chasing team at any point of the match.")
    st.markdown("You can chose the batting and bowling team, host city, target, current score etc.")
    st.markdown("See Usage Instructions for elaborate instructions.") 
    st.markdown("---")
    st.subheader("Contact Information")
    st.markdown("For more information, please contact at:")
    st.markdown("Mail: [amanbhatt.1997.ab@gmail.com](mailto:support@example.com)")
    st.markdown("Portfolio: https://amanbhatt97.github.io/portfolio/")
    st.markdown("Linkedin: https://www.linkedin.com/in/amanbhatt1997/")
    st.markdown("Github: https://github.com/amanbhatt97")
    st.markdown("---")