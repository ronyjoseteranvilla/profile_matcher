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
Is in .json files