import json
import os
import sys


def readHeroes(community=False):
    if community:
        with open('gameConstants/heroes_community.json') as input_file:
            heroes = json.load(input_file)
        return heroes
    else:
        with open('gameConstants/heroes.json') as input_file:
            heroes = json.load(input_file)
        return heroes

def simpleRep(game):
    skip_bans = False
    bans_exist = False
    # print(game.keys())
    picks_bans = game['picks_bans']
    players = game['players']

    #getting the list of banned herores

    max_ban = -sys.maxsize - 1
    banned_heroes = []
    if picks_bans is None:
        skip_bans = True
    else:
        bans_exist = True
        for pick_ban in picks_bans:
            if not pick_ban['is_pick']:
                banned_heroes.append(pick_ban['hero_id'])
        if len(banned_heroes) > max_ban:
            max_ban =len(banned_heroes)
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
    x = ally_team + enemy_team
    if not skip_bans:
        x +=  banned_heroes

    return x,[y],bans_exist,max_ban

def rolesRep(game):
    radiant = []
    dire = []
    player_team = None
    heroes = readHeroes(community=True)
    community_roles = ['Offlane', 'Support', 'Roaming Support', 'Safelane Carry', 'Mid']
    valve_roles = ['Nuker', 'Support', 'Disabler', 'Pusher', 'Initiator', 'Durable', 'Carry', 'Jungler', 'Escape']
    players = game['players']
    for player in players:
        ally_community_roles = [0,0,0,0,0]
        enemy_community_roles = [0,0,0,0,0]
        player_community_roles = [0,0,0,0,0]

        ally_valve_roles = [0,0,0,0,0,0,0,0,0]
        enemy_valve_roles = [0,0,0,0,0,0,0,0,0]
        player_valve_roles = [0,0,0,0,0,0,0,0,0]

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

    if account_team:
        ally_team = radiant
        enemy_team = dire
    else :
        ally_team = dire
        enemy_team = radiant

    ally_team.sort()
    enemy_team.sort()

    hero_valve_roles = heroes[str(hero_id)]['roles']
    hero_community_roles = heroes[str(hero_id)]['community_roles']

    for role in hero_community_roles:
        player_community_roles[(community_roles.index(role))] += 1
        player_community_roles[(community_roles.index(role))] += 1

    for role in hero_valve_roles:
        player_valve_roles[(valve_roles.index(role))] += 1
        player_valve_roles[(valve_roles.index(role))] += 1

    for hero in ally_team:
        hero_valve_roles = heroes[str(hero)]['roles']
        hero_community_roles = heroes[str(hero)]['community_roles']

        for role in hero_community_roles:
            ally_community_roles[(community_roles.index(role))] += 1
            enemy_community_roles[(community_roles.index(role))] += 1

        for role in hero_valve_roles:
            ally_valve_roles[(valve_roles.index(role))] += 1
            enemy_valve_roles[(valve_roles.index(role))] += 1

    x = ally_community_roles + enemy_community_roles + ally_valve_roles + enemy_valve_roles
    y = player_community_roles + player_valve_roles

    return x,y


def parseDataByPlayer(account_id,game_mode = None,simple_rep=True,roles_rep = False,write_to_file = True):
    community_roles = ['Offlane', 'Support', 'Roaming Support', 'Safelane Carry', 'Mid']
    valve_roles = ['Nuker', 'Support', 'Disabler', 'Pusher', 'Initiator', 'Durable', 'Carry', 'Jungler', 'Escape']
    my_path = 'matches/'+str(account_id)+'_'+str(game_mode)+'/'
    Y = []
    X = []
    bans_exist = False
    max_ban = 0
    if not os.path.exists(my_path):
        print('No data availabe under the matches dir for this player')
    if not os.path.isdir(my_path):
        print('No data availabe under the matches dir for this player')
    games_files = [my_path+f for f in os.listdir(my_path) if os.path.isfile(os.path.join(my_path,f))]
    if len(games_files) <= 0:
        print('No data availabe under the matches dir for this player')

    for game_file in games_files:
        with open(game_file) as input_file:
            game = json.load(input_file)
        version = game['version']
        match_id = game['match_id']
        start_time = game['start_time']
        x = [match_id,version,start_time]
        y = []
        if simple_rep:
            simple_x,simple_y,ban_e,num_ban = simpleRep(game)
            if ban_e:
                bans_exist = ban_e
            if num_ban > max_ban:
                max_ban = num_ban
            x += simple_x
            y += simple_y

        if roles_rep:
            roles_x,roles_y = rolesRep(game)
            x+= roles_x
            y += roles_y 

        X.append(x)
        Y.append(y)

    if write_to_file:
        filename_x = str(account_id) + '_'+str(game_mode)
        filename_y = str(account_id) + '_'+str(game_mode)
        if simple_rep:
            filename_x += '_simpleRep'
            filename_y += '_simpleRep'
        if roles_rep:
            filename_x += '_rolesRep'
            filename_y += '_rolesRep'

        filename_x += '_all_X.csv'
        filename_y += '_all_Y.csv'

        f = open(filename_x,'w')
        line = 'match_id,version,start_time,'
        if simple_rep:
            for i in range(4):
                line += 'ally_hero'+str(i+1)+','

            for i in range(5):
                line += 'enemy_team'+str(i+1)+','

            if bans_exist :
                for i in range(max_ban):
                    line += 'banned_hero'+str(i+1)+','
        if roles_rep:
            for role in community_roles:
                line += 'ally_num_of_'+role+','
            for role in community_roles:
                line += 'enemy_num_of_'+role+','
            for role in valve_roles:
                line += 'ally_num_of_'+role+','
            for role in valve_roles:
                line += 'enemy_num_of_'+role+','

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
        line = ''
        if simple_rep:
            line += 'hero_picked,'
        if roles_rep:
            for role in community_roles:
                line += 'player_num_of_'+role+','
            for role in valve_roles:
                line += 'player_num_of_'+role+','

        line = line[:-1]
        line += '\n'
        f.write(line)
        for y in Y:
            line = ''
            for el in y:
                line += str(el) +','
            line +=  '\n'
            f.write(line) 
            f.close()

def parseDataToSequences(account_id,game_mode,trunc=True,write_to_file = True):
    my_path = 'matches/'+str(account_id)+'_'+str(game_mode)+'/'
    if not os.path.exists(my_path):
        print('No data availabe under the matches dir for this player')
    if not os.path.isdir(my_path):
        print('No data availabe under the matches dir for this player')
    games_files = [my_path+f for f in os.listdir(my_path) if os.path.isfile(os.path.join(my_path,f))]
    if len(games_files) <= 0:
        print('No data availabe under the matches dir for this player')

    X = []
    Y = []
    for game_file in games_files:
        with open(game_file) as input_file:
            game = json.load(input_file)
        version = game['version']
        match_id = game['match_id']
        start_time = game['start_time']
        x = [match_id,version,start_time]
        picks_bans = game['picks_bans']
        players = game['players']
        seq_raw = []
        if picks_bans is not None:
            for pick_ban in picks_bans:
                seq_raw.append((pick_ban['is_pick'],pick_ban['hero_id'],pick_ban['team'],pick_ban['order']))
        else:
            continue
        player_team = -1
        player_pick = -1
        for player in players:
            if player['account_id'] == account_id:
                for se in seq_raw:
                    if se[1] == player['hero_id']:
                        player_team = se[2]
                        player_pick = se[1]

        seq_raw.sort(key=lambda tup: tup[3])
        seq = ''
        for el in seq_raw:
            if el[0] == False:
                seq+= 'BAN,'
            else:
                seq+= 'PICK,'

            if el[2] == player_team:
                seq+= 'ALLY_TEAM,'
            else:
                seq+= 'ENEMY_TEAM,'

            seq += str(el[1])+ ','
            if el[1] == player_pick:
                if trunc:
                    break
        seq = seq[:-1]
        x.append(seq)
        X.append(x)
        Y.append(player_pick)
        

    if write_to_file:
        filename_x = str(account_id) + '_'+str(game_mode)
        filename_y = str(account_id) + '_'+str(game_mode)
        if trunc:
            filename_x+'_trunc'
            filename_x+'_trunc'
            
        filename_x += '_seqsX.csv'
        filename_y += '_seqsY.csv'
        
        f = open(filename_x,'w')
        line = 'match_id,version,start_time,seqs\n'
        f.write(line)
        line = ''
        for x in X:
            for el in x:
                line += str(el)+','
            line = line[:-1]
            line += '\n'
            f.write(line)

        f.close()
        f = open(filename_y,'w')

        line = 'hero_picked\n'
        f.write(line)
        line = ''
        for y in Y:
            line += str(y) + '\n'
            f.write(line)

        f.close()
def parseRoles():
    heroes = readHeroes()
    f = open('gameConstants/community_roles.txt')
    lines = f.readlines()
    filename = 'gameConstants/heroes_community.json'
    for line in lines:
        components = line.split('|')
        name = components[0].strip()
        roles_str = components[1].replace('\n','').strip()
        roles = roles_str.split(',')
        for i,role in enumerate(roles):
            roles[i] = role.strip()
        for hero in heroes:
            for valve_roles in heroes[hero]['roles']:
                s.add(valve_roles)
            if heroes[hero]['localized_name'] == name:
                heroes[hero]['community_roles'] = roles

    with open(filename,'w') as outfile:
        json.dump(heroes, outfile, indent = 4, sort_keys = False)
    return heroes


if __name__ == '__main__':
    account_id = 82262664
    game_mode = 2
    # parseDataByPlayer(account_id,game_mode,True,False,False)
    parseDataToSequences(account_id,game_mode)
    # parseRoles()
