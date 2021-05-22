import random as r

def numPlayers(pre_set):
    if pre_set==0:
        numPlay=int(input('How many players?'))
    else:
        numPlay=pre_set
    players=[]
    for x in range(numPlay):
        tempPlayer=input('Player ' + str(x+1) + ' name: ')
        players.append(tempPlayer)
    return players

def initTeams(numPlay,counter,pre_set_team):
    #randomize team
    if pre_set_team==0:
        if counter==0:
            print('You have ' +str(numPlay) + ' players.\n')
            numTeams=int(input('How many teams? '))
        else:
            numTeams=counter
    else:
        numTeams=pre_set_team

    team_list=[[] for x in range(numTeams)]

    return team_list

def setTeams(t,players):
    sizeRand=len(players)
    usedPlayers=[]

    while len(players)>0:
        
        for x in range(len(t)):
            selection=r.randrange(0,sizeRand)
            #ensures the selection will be a non previously selected player
            while players[selection] in usedPlayers:
                selection=r.randrange(0,sizeRand)
                
            t[x].append(players[selection])
            
            usedPlayers.append(players[selection])
            players.remove(players[selection])
            
            if len(players)<1:
                break
            else:
                sizeRand-=1
    return t,usedPlayers
            
def printTeams(team_print):
    for x in team_print:
        print('Team ' + str(team_print.index(x)+1) + ': ' + str(x))

def main(num_players=0,teams=0):
    players=numPlayers(num_players)
    repeat=0
    while True:
        team_blank=initTeams(len(players),repeat,teams)
        finalTeamSet,players=setTeams(team_blank,players)
        printTeams(finalTeamSet)
        
        redo=input('\nReshuffle teams? (Enter)\nIf you want to exit type something')
        if redo!='':
            break
        else:
            repeat=len(team_blank)

    return finalTeamSet[0]+finalTeamSet[1]

if __name__=='__main__':
    main()
