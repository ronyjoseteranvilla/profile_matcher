# profile_matcher
Simple Micro service for a user profile matcher

### Task Description

Hi, you are tasked by the business analyst of your team with creating a simple service that will serve as a very simple user profile matcher.

**The profile matcher service will have to do the following:**
-	Based on the unique client id it should extract the current player profile from the database of your choice 
-	Based on the current running campaigns, it should update the current player profile (mock an api service that will return the list of current running campaigns) 

**The flow should be this:**
The client will call the profile matcher API here: GET /get_client_config/{player_id}
The service will get the full profile from the database and then match the current profile of the player with the current campaign settings and will determine if the current player profile matches any of the campaign conditions (matchers)
If the requirements are met, then the current player profile will be updated (add the campaign name to the profile – active campaign) and returned to the user.

**Data:**
Is in .json files inside `src/web/database/data/`


### Installation Process
- Copy variables from  `.vscode/.env_example` into `.vscode/.env`
- Install python env: `python -m venv .venv`
- Activate environment: `source .venv/Scripts/activate`
- Install packages: `pip install -r requirements.txt`
- Install Database Container: `docker compose --env-file .vscode/.env up -d profile_match_database`
    - **Optional:** at this point you can run the whole application (real+test database and api) by not specifying a service name on the `docker compose` command. Ex: `docker compose --env-file .vscode/.env up -d`
- Run migration: `alembic upgrade head` This will create the `player_profiles` and  `current_campaigns`
- Run APP: 
    - With VsCode Debug Launcher
        - Create a file `.vscode/launch.json`
        - Copy the content of `.vscode/launch.example.json` into new file
        - Now on VsCode debugger you can Run `Run Player Profile API`
    - With Docker
        - Run the command `docker compose --env-file .vscode/.env up -d profile_matcher_api`

### Testing
- Run Test Database Instance: `docker compose --env-file .vscode/.env up -d profile_matcher_test_database`

This will create a new Container for the test databases, that will expose the port `5433` vs the production Database Container that is with port `5432`.

- Run tests from VsCode Test Explorer