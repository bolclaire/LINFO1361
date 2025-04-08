
# fonction de filtre pour les actions
# au cas où le format n'est pas celui espéré
# désaccord : Ioannis dit inutile, Claire dit utile
# si récupéré -> ranger dans alphabeta.py
def filter(action : FenixAction, actions : list[FenixAction]) :
    for valid_action in actions :
        if (valid_action.start == action.start and valid_action.end == action.end) :
            return valid_action
    print(1)
    return random.choice(actions)