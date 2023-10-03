# API de prédiction de match de football

Cette API est basée sur la loi de Poisson pour prédire les probabilités d'un match de football. 

## Endpoints

### GET /probability/

Prédit la probabilité d'un certain résultat de match basé sur les identifiants de pari et de résultat fournis.

#### Paramètres :

- `bet_id`: Type de pari.
  1. Résultat du match (Domicile gagne, Match nul, Exterieur gagne).
  2. Double Chance.
  3. Nombre total de buts.
  4. Les deux équipes marqueront-elles ?
  5. Nombre de buts de l’équipe à domicile.
  6. Nombre de buts de l’équipe à l’extérieur.
  
- `outcome_id`: Identifiant du résultat.
  - Pour `bet_id = 1`: 1 = Domicile gagne, 2 = Match nul, 3 = Exterieur gagne.
  - Pour `bet_id = 2`: 1 = Domicile ou Nul, 2 = Exterieur ou Nul, 3 = Domicile ou Exterieur.
  - Pour `bet_id = 3, 5, 6`: 1 = Nombre de buts supérieur à specifiant, 2 = Nombre de buts inférieur à specifiant.
  - Pour `bet_id = 4`: 1 = Oui, 2 = Non.
  
- `specifiant`: Valeur spécifique (utilisé avec bet_id = 3, 5, 6). Par exemple, si vous pariez que le nombre total de buts sera supérieur à 3, alors specifiant serait 3.

#### Réponse :
Retourne la probabilité sous forme d'un dictionnaire :

```json
{
"probability": 0.56
}
```

## Exemple d'utilisation : 

Pour prédire la probabilité que Marseille gagne :
```bash
GET /probability/?bet_id=1&outcome_id=1
```
Pour prédire la probabilité que le nombre total de buts soit supérieur à 3 :
```bash
GET /probability/?bet_id=3&outcome_id=1&specifiant=3
```

## Test et Documentation

Pour tester l'API et visualiser la documentation, vous pouvez utiliser Swagger :

1. Assurez-vous que le serveur est en cours d'exécution.
2. Ouvrez votre navigateur et accédez à [Swagger UI](http://127.0.0.1:8000/docs#/default/get_probability_probability__get).


## Mise en place

1. Clonez ce dépôt.
2. Installez les dépendances nécessaires.
3. Exécutez le fichier principal pour démarrer le serveur.
