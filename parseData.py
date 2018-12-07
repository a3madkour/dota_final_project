import json
import os 

def readHeroes():
    with open('gameConstants/heroes.json') as input_file:
        heroes = json.load(input_file)    
    return heroes

def parseDataOfPlayer(account_id,game_mode = None,write_to_file = True):
    heroes = readHeroes()    
    my_path = 'matches/'+str(account_id)+'_'+str(game_mode)+'/'
    Y = []
    X = []
    bans_exist = False
    if not os.path.exists(my_path):
        print('No data availabe under the matches dir for this player')
    if not os.path.isdir(my_path):
        print('No data availabe under the matches dir for this player')
    games_files = [my_path+f for f in os.listdir(my_path) if os.path.isfile(os.path.join(my_path,f))]
    if len(games_files) <= 0:
        print('No data availabe under the matches dir for this player')
    for game_file in games_files:
        skip_bans = False
        with open(game_file) as input_file:
            game = json.load(input_file)    
        # print(game.keys())
        picks_bans = game['picks_bans']
        players = game['players']
        version = game['version']
        match_id = game['match_id']
        start_time = game['start_time']

        #getting the list of banned herores

        banned_heroes = []  
        if picks_bans is None:
            skip_bans = True
        else:
            bans_exist = True
            for pick_ban in picks_bans:
                if not pick_ban['is_pick']:
                    banned_heroes.append(pick_ban['hero_id'])
        #getting the hero picks by teams and the player we are looking at 
        radiant = []
        dire = []
        player_team = None
        y = -1
        for player in players:
            keys = list(player.keys())
            keys.sort()
            hero_id = player['hero_id']
            player_account_id = player['account_id']
            is_radiant = player['is_radiant']
            if account_id == player_account_id:
                y = hero_id
                account_team = is_radiant
            else:
                if is_radiant:
                    radiant.append(hero_id)
                else:
                    dire.append(hero_id)
        Y.append(y)

        if account_team:
            ally_team = radiant
            enemy_team = dire
        else :
            ally_team = dire
            enemy_team = radiant


        #append the match_id,version ally_team,enemy_team,banned heroes,verison of the game
        ally_team.sort()
        enemy_team.sort()
        banned_heroes.sort()
        x = [match_id,version,start_time] + ally_team + enemy_team  
        if not skip_bans:
            x +=  banned_heroes 
        X.append(x)

    if write_to_file:  
        filename = str(account_id) + '_'+str(game_mode)+'_all_X.csv'
        filename_y = str(account_id) + '_'+str(game_mode)+'_all_Y.csv'
        f = open(filename,'w')
        line = 'match_id,version,start_time,'
        for i in range(4):
            line += 'ally_hero'+str(i+1)+','

        for i in range(5):
            line += 'enemy_team'+str(i+1)+','

        if bans_exist :
            for i in range(12):
                line += 'banned_hero'+str(i+1)+','
        line = line[:-1]
        line += '\n'
        f.write(line)
        for x in X:
            line = ''
            for el in x:
                line += str(el)+','
            line += '\n'
            f.write(line)
        f.close()

        f = open(filename_y,'w')
        f.write('hero_picked\n')
        for y in Y:
            line = str(y) + '\n'
            f.write(line)

        f.close()
    

def parseRoles():
    heroes = readHeroes()
    f = open('gameConstants/community_roles.txt')
    lines = f.readlines()
    for line in lines:
        components = line.split('-')
        name = components[0].strip()
        roles = components[1].replace('\n','').strip()
        print(name)
        print(roles)


if __name__ == '__main__':
    account_id = 224051329
    game_mode = 22
    # parseDataOfPlayer(account_id,game_mode)
    parseRoles()
