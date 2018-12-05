from __future__ import print_function
import time
import od_python
from od_python.rest import ApiException
from pprint import pprint
import json
import os 
def getMatchesByPlayer(account_id,printToFile = True):
    # create an instance of the API class
    api_instance = od_python.PlayersApi()
    # account_id = 87278757 # int | Steam32 account ID
    # limit = 56 # int | Number of matches to limit to (optional)
    # offset = 56 # int | Number of matches to offset start by (optional)
    # win = 56 # int | Whether the player won (optional)
    # patch = 56 # int | Patch ID (optional)
    game_mode = 2 # int | Game Mode ID (optional)
    lobby_type = 1 # int | Lobby type ID (optional)
    # region = 56 # int | Region ID (optional)
    # date = 56 # int | Days previous (optional)
    # lane_role = 56 # int | Lane Role ID (optional)
    # hero_id = 56 # int | Hero ID (optional)
    # is_radiant = 56 # int | Whether the player was radiant (optional)
    # included_account_id = 56 # int | Account IDs in the match (array) (optional)
    # excluded_account_id = 56 # int | Account IDs not in the match (array) (optional)
    # with_hero_id = 56 # int | Hero IDs on the player's team (array) (optional)
    # against_hero_id = 56 # int | Hero IDs against the player's team (array) (optional)
    # significant = 56 # int | Whether the match was significant for aggregation purposes (optional)
    # having = 56 # int | The minimum number of games played, for filtering hero stats (optional)
    # sort = 'sort_example' # str | The field to return matches sorted by in descending order (optional)
    # project = 'project_example' # str | Fields to project (array) (optional)

    try: 
        # GET /players/{account_id}/matches
        api_response = api_instance.players_account_id_matches_get(account_id, game_mode=game_mode, lobby_type=lobby_type)
        matches = {}
        for match in api_response:
            mat = match.to_dict()
            matches[mat['match_id']] = mat
        if printToFile:
            with open('playerMatches/player_'+str(account_id)+'.json', 'w') as outfile:
                json.dump(matches, outfile, indent = 4, sort_keys = False)
        return matches

    except ApiException as e:
        print("Exception when calling PlayersApi->players_account_id_matches_get: %s\n" % e)

def getMatchesByID(match_id,account_id = None,printToFile = True):

    # create an instance of the API class
    api_instance = od_python.MatchesApi()
    # match_id = 4247243752 # int | 

    try: 
        # GET /matches/{match_id}
        api_response = api_instance.matches_match_id_get(match_id)
        match = api_response.to_dict()
        if printToFile:
            if account_id:
                if not os.path.exists('matches/'+str(account_id)+'/'):
                    os.makedirs('matches/'+str(account_id)+'/')
                with open('matches/'+str(account_id)+'/'+str(match_id)+'.json', 'w') as outfile:
                    json.dump(match, outfile, indent = 4, sort_keys = False)
        return match
    except ApiException as e:
        print("Exception when calling MatchesApi->matches_match_id_get: %s\n" % e)

def loadMatches(filename):
    with open(filename) as json_data:
        d = json.load(json_data)
    return d
if __name__ == '__main__':
    matches = loadMatches('playerMatches/87278757.json')
    matchs_ids = matches.keys()
    for i,match_id in enumerate(matchs_ids):
        if i!=0 and (i%60 == 0):
            print('curent game: ',i)
            time.sleep(60)
        getMatchesByID(match_id,87278757)
    # getMatchesByPlayer(87278757)
    
