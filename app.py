from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def get_hackathon_participants():
    api_key = '066b23ac7287f5acc661b39edbf3a3710eecf1afa1ffbbea17'
    hackathon_id = 'hackfest-2023'

    # Get current page number from request args
    page_number = int(request.args.get('page_number', '1'))
    action = request.args.get('action')
    if action == 'Next Page':
        page_number += 1
    elif action == 'Previous Page':
        page_number -= 1

    # Initialize variables for pagination
    skip = 0
    limit = 20

    # Send GET request to /hackathons/{hackathon_id}/participants
    while True:
        response = requests.get(
            f'https://cache.showwcase.com/hackathons/{hackathon_id}/participants',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': api_key
            },
            params={
                'skip': page_number*limit,
                'limit': limit
            })

        # Check if the HTTP request was successful
        if response.status_code == 200:
            data = response.json()
            
            usernames = [participant['displayName'] for participant in data]
            resumes = [participant['resumeUrl'] for participant in data]
            headlines=[participant['headline'] for participant in data]
            # Create list of participant dicts with usernames and resumes
            participants = [{'username': username, 'resumeUrl': resume,'headline':headline} for username, resume, headline in zip(usernames, resumes, headlines)]
    
            # Return an HTML template with the list of hackathon participants
            return render_template('participants.html', participants=participants, page_number=page_number)
        
        elif response.status_code == 404:
            return f'Error: Hackathon not found'
        
        else:
            return f'Error: {response.status_code} - {response.text}'
        
        
