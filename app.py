import os
import requests
from flask import Flask, request
from github import Github, GithubIntegration
import json


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
    #print(f"==>> payload: {payload}")



    owner = payload['repository']['owner']['login']
    repo_name = payload['repository']['name']

    pretty_json = json.dumps(payload, indent=4)

    print(f"payload: {pretty_json}")


    # Get a git connection as our bot
    # Here is where we are getting the permission to talk as our bot and not
    # as a Python webservice
    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_installation(owner, repo_name).id
        ).token
    )
    repo = git_connection.get_repo(f"{owner}/{repo_name}")

    print(type(repo))


    local_dir = "./code_paste/"



    repo_contents = repo.get_contents(".git")
    print(f"==>> type(repo_contents): {type(repo_contents)}")
    print(f"==>> repo_contents: {repo_contents}")



    # issue = repo.get_issue(number=payload['pull_request']['number'])




    #print("\n\n\n\n\n MADE IT TO END \n\n\n\n")



    return "ok"


if __name__ == "__main__":
    app.run(debug=True, port=5000)