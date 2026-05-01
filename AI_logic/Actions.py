def get_actions(state):
    actions = ['shoot_player','shoot_dealer']

    if state.turn == 'Player':
        items = state.player.items
    else:
        items = state.dealer.items

    if 'saw' in items:
        actions.append('use_saw')
    
    if 'magnifier' in items:
        actions.append('use_magifier')

    return actions


def is_terminal(state):
    if state.player.hp<=0:
        return True
    
    elif state.dealer.hp<=0:
        return True
    
    elif state.shell_index >= len(state.shells):
        return True
    
    return False

def apply_action(state,action):
    s = state.copy()
    shell = s.shells[s.shell_index]

    if action == 'shoot_dealer':
        s.shell_index += 1

        if shell=='Live':
            s.dealer.hp -= 1
            if s.turn=='Player':
                s.turn = 'Dealer'
            else:
                s.turn = 'Player'
        else:
            if s.turn=='Player':
                s.turn = 'Dealer'

    elif action == 'shoot_player':
        s.shell_index += 1

        if shell == 'Live':
            s.player.hp -= 1
            if s.turn=='Player':
                s.turn = 'Dealer'
            else:
                s.turn = 'Player'
        
        else:
            if s.turn == 'Dealer':
                s.turn = 'Player'
        
    return s

