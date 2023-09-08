import os
import requests
from flask import Flask, request
from github import Github, GithubIntegration


app = Flask(__name__)
# MAKE SURE TO CHANGE TO YOUR APP NUMBER!!!!!
app_id = 387327
# Read the bot certificate
pem_key_path = "/Users/dariyankhan/open_sc_coin/test-gh-app-dk.2023-09-08.private-key.pem"
with open(
        os.path.normpath(os.path.expanduser("/Users/dariyankhan/open_sc_coin/test-gh-app-dk.2023-09-08.private-key.pem")),
        'r'
) as cert_file:
    app_key = cert_file.read()

# Create an GitHub integration instance
git_integration = GithubIntegration(
    app_id,
    app_key,
)


@app.route("/", methods=['POST'])
def bot():
    # Get the event payload
    payload = request.json
    print(f"==>> payload: {payload}")



    # Check if the event is a GitHub PR creation event
    if not all(k in payload.keys() for k in ['action', 'pull_request']) and \
            payload['action'] == 'opened':
        
        print("I am here!!!")
        return "ok"

    owner = payload['repository']['owner']['login']
    repo_name = payload['repository']['name']

    print("\n\n\n\n\n Yeah boiiiiiii \n\n\n\n")



    # Get a git connection as our bot
    # Here is where we are getting the permission to talk as our bot and not
    # as a Python webservice
    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_installation(owner, repo_name).id
        ).token
    )
    repo = git_connection.get_repo(f"{owner}/{repo_name}")

    issue = repo.get_issue(number=payload['pull_request']['number'])

    #Call meme-api to get a random meme
    response = requests.get(url='https://meme-api.herokuapp.com/gimme')
    if response.status_code != 200:
        # print("\n\n\n\n\n UNDER RESPONSE \n\n\n\n")
        return 'ok'

    #Get the best resolution meme
    #meme_url = response.json()['preview'][-1]
    #Create a comment with the random meme
    issue.create_comment(f"Hello world!!!!")

    print("\n\n\n\n\n MADE IT TO END \n\n\n\n")



    return "ok"


if __name__ == "__main__":
    app.run(debug=True, port=5000)