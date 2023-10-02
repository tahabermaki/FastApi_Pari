from fastapi import FastAPI, HTTPException
from typing import Optional
from math import exp, factorial

app = FastAPI()

LAMBDA_MARSEILLE =  0.968
LAMBDA_PSG = 1.78

def poisson_probability(lam: float, k: int) -> float:
    return (lam**k * exp(-lam)) / factorial(k)

total_goals_max = 10
@app.get("/probability/")

def get_probability(bet_id: int, outcome_id: int, specifiant: Optional[float] = None):
    
    if bet_id == 1:  # Résultat
        total_goals_max = 10
        if outcome_id == 1:  # Domicile gagne (ici, Marseille)
            prob_marseille_win = sum(
                poisson_probability(LAMBDA_MARSEILLE, i) * poisson_probability(LAMBDA_PSG, j)
                for i in range(total_goals_max)
                for j in range(i)
            )
            return {"probability": prob_marseille_win}
        
        elif outcome_id == 2:  # Match Nul
            prob_draw = sum(
                poisson_probability(LAMBDA_MARSEILLE, i) * poisson_probability(LAMBDA_PSG, i)
                for i in range(total_goals_max)
            )
            return {"probability": prob_draw}
        
        elif outcome_id == 3:  # Exterieur gagne (ici, PSG)
            prob_psg_win = sum(
                poisson_probability(LAMBDA_MARSEILLE, i) * poisson_probability(LAMBDA_PSG, j)
                for i in range(total_goals_max)
                for j in range(i+1, total_goals_max)
            )
            return {"probability": prob_psg_win}

    elif bet_id == 2:  # Double Chance
        total_goals_max = 10
        if outcome_id == 1:  # Domicile ou Nul
            prob_marseille_or_draw = sum(
                poisson_probability(LAMBDA_MARSEILLE, i) * poisson_probability(LAMBDA_PSG, j)
                for i in range(total_goals_max)
                for j in range(i+1)
            )
            return {"probability": prob_marseille_or_draw}
        
        elif outcome_id == 2:  # Exterieur ou Nul
            prob_psg_or_draw = sum(
                poisson_probability(LAMBDA_MARSEILLE, i) * poisson_probability(LAMBDA_PSG, j)
                for i in range(total_goals_max)
                for j in range(i, total_goals_max)
            )
            return {"probability": prob_psg_or_draw}
        
        elif outcome_id == 3:  # Domicile ou Exterieur
            prob_marseille_or_psg = 1 - sum(
                poisson_probability(LAMBDA_MARSEILLE, i) * poisson_probability(LAMBDA_PSG, i)
                for i in range(total_goals_max)
            )
            return {"probability": prob_marseille_or_psg}
            
    elif bet_id == 3:  # Nombre de buts
        total_prob = 0
        
        if outcome_id == 1:  # supérieur à specifiant
            # On calcule la probabilité que le total des buts soit supérieur à specifiant.
            for i in range(int(specifiant) + 1, 10):
                for j in range(10):
                    total_prob += poisson_probability(LAMBDA_MARSEILLE, i) * poisson_probability(LAMBDA_PSG, j)
            return {"probability": total_prob}
        
        elif outcome_id == 2:  # inférieur à specifiant
            # On calcule la probabilité que le total des buts soit inférieur à specifiant.
            for i in range(int(specifiant)):
                for j in range(int(specifiant)):
                    total_prob += poisson_probability(LAMBDA_MARSEILLE, i) * poisson_probability(LAMBDA_PSG, j)
            return {"probability": total_prob}

    elif bet_id == 4:  # Les deux équipes marquent
        if outcome_id == 1:  # oui
            prob_both_teams_score = sum(
                poisson_probability(LAMBDA_MARSEILLE, i) * poisson_probability(LAMBDA_PSG, j)
                for i in range(1, 10)
                for j in range(1, 10)
            )
            return {"probability": prob_both_teams_score}
        
        elif outcome_id == 2:  # non
            prob_both_teams_not_score = sum(
                poisson_probability(LAMBDA_MARSEILLE, 0) * poisson_probability(LAMBDA_PSG, j) +
                poisson_probability(LAMBDA_MARSEILLE, i) * poisson_probability(LAMBDA_PSG, 0) 
                for i in range(1, 10)
                for j in range(1, 10)
            ) + poisson_probability(LAMBDA_MARSEILLE, 0) * poisson_probability(LAMBDA_PSG, 0)
            
            return {"probability": prob_both_teams_not_score}


    elif bet_id == 5:  # Nombre de buts de l’équipe à domicile
        total_prob = 0
        
        if outcome_id == 1:  # supérieur à specifiant
            for i in range(int(specifiant) + 1, 10):
                total_prob += poisson_probability(LAMBDA_MARSEILLE, i)
            return {"probability": total_prob}
        
        elif outcome_id == 2:  # inférieur à specifiant
            for i in range(int(specifiant)):
                total_prob += poisson_probability(LAMBDA_MARSEILLE, i)
            return {"probability": total_prob}

    elif bet_id == 6:  # Nombre de buts de l’équipe à l’exterieur
        total_prob = 0
        
        if outcome_id == 1:  # supérieur à specifiant
            for i in range(int(specifiant) + 1, 10):
                total_prob += poisson_probability(LAMBDA_PSG, i)
            return {"probability": total_prob}
        
        elif outcome_id == 2:  # inférieur à specifiant
            for i in range(int(specifiant)):
                total_prob += poisson_probability(LAMBDA_PSG, i)
            return {"probability": total_prob}
        
    else:
        raise HTTPException(status_code=400, detail="Invalid bet_id, outcome_id or specifiant")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
