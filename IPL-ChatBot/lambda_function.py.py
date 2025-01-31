#Prithiv IPL ChatBot lambda Function Code

import json
import boto3
import csv
from io import StringIO
from datetime import datetime

# Initialize the S3 client
s3 = boto3.client('s3')

# S3 bucket and file details (replace with your S3 bucket and file names)
S3_BUCKET = 'prithiv-aws'
S3_KEY = 'ipl_2019_dataset.csv'

# Function to read the IPL data from S3
def get_ipl_data():
    try:
        response = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
        csv_data = response['Body'].read().decode('utf-8')
        csv_reader = csv.DictReader(StringIO(csv_data))
        return list(csv_reader)  # Return a list of dictionaries representing each row
    except Exception as e:
        print(f"Error reading data from S3: {e}")
        return []

# Helper functions to build responses
def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }

def close(session_attributes, fulfillment_state, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }

def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }

# Helper function to find the match details based on teams and match date
def find_match(ipl_data, teamOne, teamTwo, match_date):
    # Convert the match_date (from Lex) from YYYY-MM-DD to DD/MM/YY format
    match_date = datetime.strptime(match_date, '%Y-%m-%d').strftime('%d/%m/%y')
    
    for match in ipl_data:
        if (match['team1'] == teamOne and match['team2'] == teamTwo) or (match['team1'] == teamTwo and match['team2'] == teamOne):
            if match['date'] == match_date:
                return match
    return None

# Intent Handlers
def handle_toss_details(intent_request, ipl_data):
    slots = intent_request['currentIntent']['slots']
    session_attributes = intent_request['sessionAttributes']

    # Check if slots are missing
    if slots['teamOne'] is None:
        return elicit_slot(session_attributes, 'TossDetailsIntent', slots, 'teamOne', 'Which is the first team?')
    if slots['teamTwo'] is None:
        return elicit_slot(session_attributes, 'TossDetailsIntent', slots, 'teamTwo', 'Which is the second team?')
    if slots['date'] is None:
        return elicit_slot(session_attributes, 'TossDetailsIntent', slots, 'date', 'On what date was the match played?')

    team1 = slots['teamOne']
    team2 = slots['teamTwo']
    match_date = slots['date']

    match = find_match(ipl_data, team1, team2, match_date)

    if match:
        toss_winner = match['toss_winner']
        toss_decision = match['toss_decision']
        message = f"The toss was won by {toss_winner}, and they chose to {toss_decision}."
    else:
        message = f"Sorry, I couldn't find a match between {team1} and {team2} on {match_date}."

    return close(intent_request['sessionAttributes'], 'Fulfilled', message)

def handle_player_of_match(intent_request, ipl_data):
    slots = intent_request['currentIntent']['slots']
    session_attributes = intent_request['sessionAttributes']

    # Check if slots are missing
    if slots['teamOne'] is None:
        return elicit_slot(session_attributes, 'PlayerOfTheMatchIntent', slots, 'teamOne', 'Which is the first team?')
    if slots['teamTwo'] is None:
        return elicit_slot(session_attributes, 'PlayerOfTheMatchIntent', slots, 'teamTwo', 'Which is the second team?')
    if slots['date'] is None:
        return elicit_slot(session_attributes, 'PlayerOfTheMatchIntent', slots, 'date', 'On what date was the match played?')

    team1 = slots['teamOne']
    team2 = slots['teamTwo']
    match_date = slots['date']

    match = find_match(ipl_data, team1, team2, match_date)

    if match:
        player_of_match = match['player_of_match']
        message = f"The player of the match was {player_of_match}."
    else:
        message = f"Sorry, I couldn't find a match between {team1} and {team2} on {match_date}."

    return close(intent_request['sessionAttributes'], 'Fulfilled', message)

def handle_venue_details(intent_request, ipl_data):
    slots = intent_request['currentIntent']['slots']
    session_attributes = intent_request['sessionAttributes']

    # Check if slots are missing
    if slots['teamOne'] is None:
        return elicit_slot(session_attributes, 'VenueDetailsIntent', slots, 'teamOne', 'Which is the first team?')
    if slots['teamTwo'] is None:
        return elicit_slot(session_attributes, 'VenueDetailsIntent', slots, 'teamTwo', 'Which is the second team?')
    if slots['date'] is None:
        return elicit_slot(session_attributes, 'VenueDetailsIntent', slots, 'date', 'On what date was the match played?')

    team1 = slots['teamOne']
    team2 = slots['teamTwo']
    match_date = slots['date']

    match = find_match(ipl_data, team1, team2, match_date)

    if match:
        venue = match['venue']
        message = f"The match was played at {venue}."
    else:
        message = f"Sorry, I couldn't find a match between {team1} and {team2} on {match_date}."

    return close(intent_request['sessionAttributes'], 'Fulfilled', message)

def handle_match_results(intent_request, ipl_data):
    slots = intent_request['currentIntent']['slots']
    session_attributes = intent_request['sessionAttributes']

    # Check if slots are missing
    if slots['teamOne'] is None:
        return elicit_slot(session_attributes, 'MatchDetailsIntent', slots, 'teamOne', 'Which is the first team?')
    if slots['teamTwo'] is None:
        return elicit_slot(session_attributes, 'MatchDetailsIntent', slots, 'teamTwo', 'Which is the second team?')
    if slots['date'] is None:
        return elicit_slot(session_attributes, 'MatchDetailsIntent', slots, 'date', 'On what date was the match played?')

    team1 = slots['teamOne']
    team2 = slots['teamTwo']
    match_date = slots['date']

    match = find_match(ipl_data, team1, team2, match_date)

    if match:
        winner = match['winner']
        win_by_runs = match['win_by_runs']
        win_by_wickets = match['win_by_wickets']

        if int(win_by_runs) > 0:
            message = f"The match was won by {winner} by {win_by_runs} runs."
        elif int(win_by_wickets) > 0:
            message = f"The match was won by {winner} by {win_by_wickets} wickets."
        else:
            message = f"The match was won by {winner}."

    else:
        message = f"Sorry, I couldn't find a match between {team1} and {team2} on {match_date}."

    return close(intent_request['sessionAttributes'], 'Fulfilled', message)

# Dispatch function to route to the right intent handler
def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']
    
    # Load the IPL data from S3
    ipl_data = get_ipl_data()

    # Dispatch to intent handlers
    if intent_name == 'TossDetailsIntent':
        return handle_toss_details(intent_request, ipl_data)
    elif intent_name == 'PlayerOfTheMatchIntent':
        return handle_player_of_match(intent_request, ipl_data)
    elif intent_name == 'VenueDetailsIntent':
        return handle_venue_details(intent_request, ipl_data)
    elif intent_name == 'MatchDetailsIntent':
        return handle_match_results(intent_request, ipl_data)
    else:
        raise Exception(f"Intent with name {intent_name} not supported")

# Main handler
def lambda_handler(event, context):
    return dispatch(event)