# TP-Online-diary

Contexte du projet

Vous travaillez pour une ESN. Un client vous demande de développer pour lui une application web.

Votre client est un coach de vie, il aide les personnes a se sentir bien dans leur quotidien. Pour suivre le moral de ses clients en deux séances de coaching, il leur demande d'écrire tous les jours un petit texte.

Il y a quelque temps, un influenceur a conseillé ce coach à sa communauté, il est depuis totalement débordé et a eu l'idée d'un outil numérique pour automatiser son suivi. (ppff les coachs...)

Vous devez donc construire et publier:

    une base de données pour stocker les informations de votre coach
    une API REST avec fastAPI (ou autre) pour pouvoir intéagir avec cette base de données
    une application web avec streamlit (ou autre) utilisée comme interface grafique.

Ce qu'un client (du coach) doit pouvoir faire:

    ajouter un texte à la date du jour
    modifier un texte à la date du jour
    lire son texte à la date du jour ou à n'importe quelle date

Ce que le coach doit pouvoir faire:

    ajouter/supprimer/renommer un client.
    ajouter/supprimer/modifier certaines informations sur le client.
    obtenir la liste de tous ses clients et les informations stockées sur lui.
    pour un certain client à une certaine date obtenir le texte d'une client, son sentiment majoritaire, sa roue des émotions (% de chaque sentiment)
    Pour un certain client, un certain jour, une certaine semaine, un certain mois ou une certaine année: récupérer la roue des sentiments moyenne sur la période
    Pour un certain jour, une certaine semaine, un certain mois, une certaine année: récupérer la roue des sentiments moyennes de l'ensemble de ses clients sur la période.

Conseil: utiliser les bases de données exploitées lors de la recherche de sentiments pour simuler des contenus passés.

​

Bonus:

Sur votre outil de visualisation préféré, réaliser un tableau de bord pour le coach qui requétera l'API

​