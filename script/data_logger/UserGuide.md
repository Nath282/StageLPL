Description
===


Ce script a été conçu pour permettre la visualisation en continu des températures du four (et à terme des bobines) de l'expérience Sodium de l'équipe BEC du Laboratoire de Physique des Lasers (Université Sorbonne Paris Nord). Les températures sont mesurées à l'aide de thermocouples et récuperées grâce à un data logger PicoTech TC-08. L'architecture du projet est :

Driver python -> InfluxDB database -> grafana pdc agent -> grafana Cloud

Le driver python permet d'interagir avec le data logger et de récuperer les données de températures puis les exporter vers InfluxDB. Il repose sur le driver PicoSDK fourni par PicoTech sur leur site ainsi que sur la librairie influxdb3-python qui permet de communiquer avec InfluxDB. Le programme python est composé de deux fichiers : TCO8_driver.py qui est une réecriture du driver natif PicoSDK afin de faciliter son utilisation et main.py qui permet de recuperer et exporter les données. Ces fichiers sont executés dans un environnement virtuel dédié. Ces données sont ensuite envoyés dans un base de données InfluxDB (très efficace en terme de stockage pour des données temporelles) et sont conservés localement. L'agent pdc (Private Datasource Connection) de grafana permet à grafana Cloud de lire les données de la base et de les afficher, ce qui permet à quiconque de connecté sur le cloud de voir en direct l'évolution des températures. 


Utilisation en pratique
===

Le programme a été conçu pour qu'il puisse tourner en continu sans intervention pendant de grandes périodes de temps, notamment grâce à un fichier batch qui permet au programme de redemarrer au démarrage de l'ordinateur (fonctionne seulement sur Windows). L'agent grafana et InfluxDB qui ne necessite aucune maintenance sont exécutés dans des terminaux dédiées en tant que sub-process (et ne peuvent donc pas être gérés manuellement). Au contraire le script Python est exécuté dans le terminal où est exécuté le fichier batch ce qui permet une gestion manuelle. Le programme peut être arrêté en tapant Ctrl C puis executé de nouveau, ce qui est utile en cas de deboggage ou pour modifier des paramètres. Les logs du script Python sont consignés dans un fichier dédié temp.acquisition.log

Il suffit alors de se connecter à grafana Cloud et d'aller voir le dashboard correspondant.

Les paramètres importants du script (modifiables dans main.py) sont : 
- ENABLED_CHANNELS : liste indiquant quelles channels du data logger sont utilisés
- THERMOCOUPLE_TYPES : dictionnaire indiquant le type des thermocouples associées à chaque channel
- WAITING_TIME : intervalle de temps entre deux mesures en secondes
- LOG_LEVEL : niveau d'information affiché dans les logs, en cas de deboggage utiliser logging.DEBUG au lieu de logging.INFO

N.B. : Pour des raisons qui me sont obscures, la première mesure de température pour chaque channel après execution du script échoue systématiquement. 

Affichage des données avec grafana
===


Pour comprendre comment afficher les données avec grafana, il faut d'abord comprendre comment elles sont stockées avec InfluxDB. Les données exportés vers influx sont stockées dans des base de données, defini au demarrage. Au sein d'une base de données, les données vont être caractérisés par : 

- une table

- des champs (dans notre cas la température)

- des tags (dans notre cas le channel et le label associé)

- un timestamp (dans notre cas l'instant de la prise de mesure)

Une mesure de temperature va donc être écrit de la forme suivante sous Python :  

        Point("temperatures").tag("channel",chan).tag("label",label[chan]).field("temp",temp).time(datetime.now(timezone.utc))

où temperatures est le nom de la table et datetime.now(timezone.utc) permet d'enregistrer la date exacte de la mesure avec le bon fuseau horaire. 

L'affichage dans grafana se fait dans un dashboard. Creez un nouveau dashboard, add new elements, pannel et selectionner Time Series dans l'onglet All visualisations sur la droite de l'ecran comme type de graphe. Si lors de la connection à votre datasource vous l'avez selectionné comme Make default, elle devrait déjà être renseigné, sinon selectionnez la bonne datasource influxdb. Il ne vous reste plus qu'à selectionner les données que vous voulez afficher sous la forme d'une requête SQL. Grafana se charge d'afficher les bonnes données, la requête sert principalement pour faire de la selection. Par exemple :

        SELECT temp, time, channel from temperatures 
        WHERE channel >= 1 and channel <= 8

Cliquez sur Run query et vous devrez voir des valeurs s'afficher. Pour distinguer les données selon leur channel, il faut ajouter une transformation Partition by values. En selectionnant channel comme field, les données seront alors distingués selon leur channel !

Pour plus d'informations, regardez la documentation de Grafana.


Démarrage manuel
===

En cas d'erreur dans la chaine, le programme peut être relancé en executant de nouveau le fichier batch (il s'occupe de tuer influxdb et grafana pdc s'ils sont actifs). 

Pour un demarrage manuel complet, vous devez : 
- ouvrir un premier terminal et executer la commande suivante pour démarrer influxDB : 

        influxdb3 serve --node-id node0

- ouvrir un deuxième terminal et executer la commande suivante pour démarrer l'agent pdc de grafana :

        ./pdc -token GCLOUD_PDC_SIGNING_TOKEN \
        -cluster prod-eu-west-2 \
        -gcloud-hosted-grafana-id 1703718

- ouvrir un troisième terminal et lancer le script : 

        python main.py

Le prpgramme est alors lancé et il n'y a plus qu'à se connecter à grafana Cloud pour aller voir le dashboard. 

Installation complète 
===

Les étapes ci-dessus requiert d'avoir déjà installé et configurer l'agent pdc de grafana, InfluxDB et l'environnement virtuel du fichier python. Si ce n'est pas le cas, suivez les étapes suivantes : 

Installation de InfluxDB3 Core
---

Allez à l'adresse https://docs.influxdata.com/influxdb3/core/install/#download-and-install-the-latest-build-artifacts et telecharger le binary windows. 

Vous pouvez ensuite verifier l'installation en tapant dans un terminal : 

        influxdb3 --version

Il devrait afficher cela :

Si ce n'est pas le cas, allez voir la documentation sur leur site https://docs.influxdata.com/influxdb3/core/. Il faut ensuite creer le token admin qui permettra de se connecter à la base de données. Pour cela il faut commencer par lancer influxdb. Pour cela tapez : 

        influxdb3 serve --node-id node0

puis dans un autre terminal : 

        influxdb3 create token --admin

Influxdb vous affichera votre token, conservez le et copier collez le dans dans la variable TOKEN de main.py (n'oubliez pas d'ajouter des guillemets pour qu'il soit compris comme une chaine de caractère). 

Faites attention à bien noter ce token parce qu'il ne pourra pas être afficher de nouveau, et sans lui vous ne pourrez plus jamais acceder aux données enregistré sous le node0. De la même façon, vous ne pourrez pas acceder aux données stockés dans un autre node avec ce token. En effet les token crées sont associés à des nodes. Les nodes sont les differents dossiers dans lesquels sont stockées les données par InfluxDB et le node utilisé doit être déclaré au lancement de InfluxDB (c'est à ça que sert le tag --node-id lors de la commande influxdb3 serve).

Il faut ensuite créer la database où vont être stocké les données. Pour cela, tappez : 

        influxdb3 create database --token ADMIN_TOKEN DATABASE_NAME

où ADMIN_TOKEN devra être remplacé par le token que vous venez de generer et DATABASE_NAME par le nom de votre database (par exemple temperature_db). Attention, le nom de votre database ne doit contenir que des lettres (a-z,A-Z), des chiffres (0-9) et _ ou -. De plus, même si ce n'est pas indiqué dans la documentation, j'ai obtenu des erreurs lorsque le nom de ma database commençait par une majuscule.

Vous pouvez maintenant utiliser InfluxDB !

Installation de l'agent grafana PDC et connexion à grafana Cloud
---

Allez à l'adresse https://github.com/grafana/pdc-agent/releases/tag/v0.0.61 et telechargez le binary de l'agent correspondant à votre architecture. 

Connectez vous sur votre compte Grafana Cloud et allez dans l'onglet Connections puis cliquez sur Private Data Source Connect. Cliquez sur Add private agent puis Configuration Details. Choisissez binary comme méthode d'installation puis suivez les instructions. À la fin, si Test Agent Connection affiche 1 agent connected, cliquez sur Create a New datasource. Vous pourrez alors selectionner InfluxDB comme type de datasource. Checkez le port sur lequel écoute InfluxDB en tappant dans un terminal : 

        lsof -i -n | grep influxdb

Si le port est bien 8181 entrez dans le champ URL sur le site : 

        http://localhost:8181/

(sinon remplacez 8181 par le numero du port d'écoute de InfluxDB). Selectionnez Influxdb Enterprise 3.x en tant que produit et SQL as query language (vous pouvez selectionner le langage natif de influx InfluxQL si vous êtes familier avec mais ce n'est pas mon cas). 

Vous pouvez alors remplir les database settings en entrant DATABASE_NAME et ADMIN_TOKEN dans les champs correspondants.

Dans l'onglet Private Data Source Connect, selectionnez l'agent que vous venez de lancer. 

Vous pouvez alors enregistrer votre datasource en cliquant sur Save & Test. Si vous recevez un message de succès, vous avez bien connecté votre datasource et vous pouvez allez visualiser les données dans un dashboard ! Pensez à cliquer sur Make Default si ce projet est votre utilisation principale de Grafana Cloud.

Si vous obtenez un message d'erreur parlant de TLS handshake, verifiez dans l'onglet URL et Authentification que tous les paramètres de Auth and TLS/SSL Settings sont désactivés et dans l'onglet Database settings, cochez l'option Insecure connection dans les Advanced Database Settings. Si ça ne marche toujours pas, consultez la documentation.


Configuration du programme Python 
---
Si vous ne l'avez pas dejà, telecharger topus les fichiers du dossier data_logger présent dans mon repository github https://github.com/Nath282/StageLPL/tree/master/script/data_logger. Ouvrez un terminal et déplacez vous dans le directory correspondant au dossier ou vous avez telecharger les fichiers en tapand la commande suivante :

        cd C:/Users/path/to/data_logger

Puis creez l'environnement python virtuel en tapant : 

        python -m venv env

puis : 

        env\Scripts\activate.bat 
    
pour activer l'environnement. Vous pouvez ensuite telecharger toutes les librairies necessaires au script en tapant : 

        pip install -r requirements.txt

N'oubliez pas de modifier le shebang du script main.py (la toute première ligne du script) en indiquant le chemin vers votre environnement virtuel : 

        #!C:/Users/path/to/data_logger/env/bin/python3

Cela permettra de toujours executer le script main.py dans l'environnement virtuel env et de ne pas avoir à l'activer à chaque fois. 

Le programme est alors prêt à l'emploi !





