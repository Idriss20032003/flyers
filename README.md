# CW02

## Cas d'usage

Le projet se nomme Flyers. Flyers est un réseau social qui permet de créer et de rejoindre des événements tout en collaborant ou échangeant avec les autres utilisateurs. Les événements peuvent être financés à l'aide d'une billeterie.

## Config branch

Avant d'utiliser le site, il faut entrer quelques lignes de code dans le terminal:

cd <chemin_vers_projet>/cw02
python -m venv env
source env/Scripts/activate
cd Flyers/
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

A partir d'ici, les modules nécessaires ont été installés, la base de données a été créée et le serveur est ouvert en local
On peut maintenant accéder au site en entrant l'URL http://127.0.0.1:8000/ dans un navigateur de recherche

## Création superuser

Pour avoir accès à la partie admin du site, il faut entrer dans le terminal bash :

python manage.py createsuperuser

Il faudra alors entrer le nom d'utilisateur et un mot de passe

## Description MVP

Le projet ce décompose en trois fonctionnalités : Authentication, Flow et Chat

- Authentication : partie du code centrée sur l'authentification des utilisateurs c'est à dire la connexion et l'inscription de nouveaux utilisateurs.

    MVP : connexion, inscription, déconnexion

    Améliorations réalisées au cours de la semaine:
    - utilisation d'une classe User implémentée par Django puis création d'une classe utilisateur plus détaillée permettant l'édition de profil
    - consultation du profil personnel et du profil d'autres utilisateurs
    - demande de l'autorisation de faire financer ses événements à un superuser et liaison d'un profil à un compte bancaire à travers l'API de Stripe

- Chat : partie du code centrée sur la messagerie instantanée du site

    MVP : implémentation d'un échange de données entre utilisateurs de façon instantanée via des protocoles websocket à l'aide du framework Django channels

    Améliorations réalisées au cours de la semaine:
    - création d'une messagerie instantanée pour créer des groupes de discussion pour chaque événement lors de son ajout
    - création d'une roadmap pour chaque événement

- Flow : partie du code centrée, dans un premier temps, sur le fil d'actualités du site 
    
    MVP : création d'événement en précisant certains champs (titre, description, ...), affichage des événements, recherche d'événements via leurs titres

    Améliorations réalisées au cours de la semaine:
    - ajout de nouveaux champs pour la création d'événement (type d'événement, possibilité de financement, ...)
    - ajout de nouveaux champs de recherche (type d'événement, tag, date)
    - ajout de certains détails dans l'affichage des événements et ajout d'un bouton like

## Améliorations non terminées

- Envoi de médias (photo, vidéo, ...) dans les messageries instantanées
- Montrer qui est en train d'écrire
- Montrer les utilisateurs connectés 

## Fonctionalités non complétées/ Améliorations possibles

- API vers google calendar et mettre les événements dans un agenda
- Possibilité de crowdfunding
- Recherche d'utilisateur
- Organisation des conversations (du plus au moins récent)
- Notifications 
- Mise en évidence des conversations où des message non lus ont été envoyés
- Ajout de sondages
- Recherche en fonction du lieu
- Demande d'amis, suivi d'utilisateurs
