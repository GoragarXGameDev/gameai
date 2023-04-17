def get_onlineevolution_conf(game: str, budget: int) -> dict:
    if game == 'Asmacag':
        if budget == 0.5:
            return {
                "population_size": 150,
                "mutation_rate": 0.4,
                "survival_rate": 0.5
            }
        elif budget == 1:
            return {
                "population_size": 150,
                "mutation_rate": 0.2,
                "survival_rate": 0.8
            }
        elif budget == 3:
            return {
                "population_size": 200,
                "mutation_rate": 0.3,
                "survival_rate": 0.5
            }
        elif budget == 5:
            return {
                "population_size": 250,
                "mutation_rate": 0.5,
                "survival_rate": 0.5
            }
    elif game == 'TankWar':
        pass
    elif game == 'HeroAcademy':
        pass

def get_onlineevolution_random_conf(game: str, budget: int) -> dict:
    if game == 'Asmacag':
        if budget == 0.5:
            return {
                "population_size": 150,
                "mutation_rate": 0.4,
                "survival_rate": 0.5,
                "random_new_valid_action": True
            }
        elif budget == 1:
            return {
                "population_size": 150,
                "mutation_rate": 0.2,
                "survival_rate": 0.8,
                "random_new_valid_action": True
            }
        elif budget == 3:
            return {
                "population_size": 200,
                "mutation_rate": 0.3,
                "survival_rate": 0.5,
                "random_new_valid_action": True
            }
        elif budget == 5:
            return {
                "population_size": 250,
                "mutation_rate": 0.5,
                "survival_rate": 0.5,
                "random_new_valid_action": True
            }
    elif game == 'TankWar':
        pass
    elif game == 'HeroAcademy':
        pass