 PRÉSENTATION GLOBALE

Notre système reproduit un hôpital moderne en architecture microservices :

 HÔPITAL DIGITAL - VISION D'ENSEMBLE

                         ┌─────────────────┐
                         │     🌐 CLIENT   │
                         │  Navigateur /   │
                         │  Applications   │
                         └─────────────────┘
                                   │
                                   ▼
                         ┌─────────────────┐
                         │   🚪 API GATEWAY│
                         │     Port 8080   │
                         └─────────────────┘
                                   │
          ┌─────────────┬─────────────┬─────────────┬─────────────┐
          ▼             ▼             ▼             ▼             ▼
    ┌─────────┐   ┌────────────┐  ┌────────────┐  ┌─────────┐  ┌─────────────┐
    │ 🔐 AUTH │   │ 🏥 MEDICAL │  │ 👥 USERS   │  │ 📄 OCR  │  │  ML / AI    │
    │ Port 8001│   │ Port 8003 │  │ Port 8006  │  │ Port8005│  │ Port 8004   │
    └─────────┘   └────────────┘  └────────────┘  └─────────┘  └─────────────┘
          │             │             │             │             │
          │             │             │             │             │
          ▼             ▼             ▼             ▼             ▼
    ┌─────────┐   ┌────────────┐  ┌────────────┐  ┌─────────┐  ┌─────────────┐
    │ auth_db │   │ medical_db │  │ users_db   │  │ ocr_db  │  │ ml_db       │
    │ Port5432│   │ Port5433   │  │ Port5434   │  │ Port5435│  │ Port5436    │
    └─────────┘   └────────────┘  └────────────┘  └─────────┘  └─────────────┘
                                      │
                                      ▼
                                ┌─────────────┐
                                │Blockchain / │
                                │ ledger_db   │
                                │ Port5437    │
            

---

### **Page 1 : Page de Titre**

# Documentation Technique Complète

## Librairies Partagées (`shared_libs`) pour l'Architecture Microservices du Système Hospitalier

---

### **Page 2 : Table des Matières**

1.  **Introduction à l'Architecture `shared_libs`**
    *   Philosophie et Objectifs
    *   Diagramme d'Interaction des Composants

2.  **Le Cœur de la Sécurité : `shared_libs/security`**
    *   **Classe `JWTHandler` : Le Bureau des Badges d'Accès**
        *   Rôle et Concept des JWT
        *   Analyse des Méthodes (`create_access_token`, `verify_token`, `get_current_user`)
    *   **Classe `PasswordHasher` : Le Coffre-Fort des Mots de Passe**
        *   Principe du Hashage Sécurisé
        *   Analyse des Méthodes (`hash_password`, `verify_password`)
    *   **Classe `AuthMiddleware` : L'Agent de Sécurité à l'Entrée**
        *   Le Rôle d'un Middleware
        *   Fonctionnement Détaillé du `__call__`
        *   Analyse des Méthodes (`_is_public_route`, `require_role`)
    *   **Classe `ServiceAuthenticator` : Le Courrier Interne Sécurisé**
        *   Sécurisation de la Communication Inter-Services
        *   Analyse des Méthodes (`verify_service_api_key`, `make_authenticated_request`)
    *   **Classe `SecurityConfig` : Le Directeur de la Sécurité**
        *   Rôle d'Orchestrateur
        *   Analyse des Méthodes (`setup_security`, `get_auth_dependency`, `get_role_dependency`)

3.  **La Boîte à Outils Universelle : `shared_libs/utils`**
    *   **Classe `APIResponse` : Le Langage Commun**
        *   Importance de la Standardisation
        *   Exemples de Réponses (Succès, Erreur, Pagination)
    *   **Classe `DataValidator` : Le Contrôleur Qualité**
        *   Validation et Nettoyage des Données
    *   **Classe `StructuredLogger` : Le Journal de Bord Intelligent**
        *   Bénéfices du Logging Structuré
    *   **Classe `ErrorHandler` : Le Service des Urgences Logiciel**
        *   Gestion Globale des Exceptions
    *   **Classe `ConfigManager` : Le Centre de Configuration**
        *   Centralisation des Paramètres

4.  **La Fondation des Données : `shared_libs/database`**
    *   **Classe `BaseModel` : Le Plan de Construction**
        *   Rôle et Avantages

5.  **Synthèse et Flux de Vie d'une Requête**
    *   Schéma récapitulatif

---

### **Page 3 : Introduction à l'Architecture `shared_libs`**

#### Philosophie et Objectifs

La bibliothèque `shared_libs` est le fondement de notre architecture microservices. Elle a été conçue selon les principes **DRY (Don't Repeat Yourself)** et de **séparation des préoccupations**.

**Objectifs Clés :**
1.  **Cohérence :** Tous les services partagent la même logique pour la sécurité, le logging, la gestion des erreurs et le formatage des réponses.
2.  **Sécurité Centralisée :** Les mécanismes de sécurité sont définis une seule fois et appliqués uniformément, réduisant la surface d'attaque.
3.  **Productivité Accélérée :** Les développeurs peuvent se concentrer sur la logique métier spécifique à leur service sans réinventer la roue pour les fonctionnalités transverses.
4.  **Maintenabilité :** Une mise à jour de sécurité ou d'un utilitaire dans `shared_libs` se propage à tous les services.

#### Diagramme d'Interaction des Composants

Ce diagramme montre comment les principaux composants interagissent lors d'une requête API.

```mermaid
graph TD
    A[Requête HTTP Entrante] --> B(AuthMiddleware);
    B -- Route Publique? --> C{Décision};
    C -- Oui --> D[Contrôleur de la Route];
    C -- Non --> E(JWTHandler);
    E -- Valide le Token --> F{Token Valide?};
    F -- Oui --> D;
    F -- Non --> G[Erreur 401 Unauthorized];
    
    D -- Accès aux Données --> H(BaseModel);
    D -- Logique Métier --> I(DataValidator);
    D -- Enregistre une Action --> J(StructuredLogger);
    D -- Erreur Inattendue --> K(ErrorHandler);
    D -- Renvoie une Réponse --> L(APIResponse);
    
    subgraph "shared_libs"
        B; E; H; I; J; K; L;
    end
```

---

### **Page 4 : Le Cœur de la Sécurité - `JWTHandler`**

#### Classe `JWTHandler` : Le Bureau des Badges d'Accès

**Rôle :** Gérer l'intégralité du cycle de vie des JSON Web Tokens (JWT). C'est le composant qui crée les "badges d'accès" sécurisés pour les utilisateurs et qui vérifie l'authenticité de ces badges à chaque fois qu'ils sont présentés.

**Concept Clé :** L'authentification par JWT est **stateless**. Le serveur n'a pas besoin de stocker d'informations sur la session de l'utilisateur. Toutes les données nécessaires (ID, rôle, date d'expiration) sont contenues dans le token lui-même, de manière sécurisée et infalsifiable grâce à la signature.

#### Analyse Détaillée des Méthodes

`__init__(self)`
*   **But :** Initialise le gestionnaire avec les paramètres de sécurité essentiels.
*   **Fonctionnement :** Il charge la clé secrète, l'algorithme et les durées de vie des tokens depuis les variables d'environnement (`.env`). Si aucune clé secrète n'est fournie, il en génère une de manière sécurisée pour éviter les configurations par défaut dangereuses.

`create_access_token(self, data: Dict) -> str`
*   **But :** Créer un badge d'accès (token) à courte durée de vie.
*   **Fonctionnement :**
    1.  Prend en entrée un dictionnaire contenant les informations de l'utilisateur (`user_id`, `email`, `role`).
    2.  Ajoute des "claims" (informations) standards :
        *   `exp` (expiration) : Calcule la date et l'heure d'expiration (ex: dans 30 minutes).
        *   `iat` (issued at) : Enregistre l'heure de création.
    3.  Utilise la bibliothèque `jose.jwt` pour encoder ces données avec la clé secrète et l'algorithme (HS256). Le résultat est une chaîne de caractères `HEADER.PAYLOAD.SIGNATURE`.

`verify_token(self, token: str) -> Dict`
*   **But :** Valider un token.
*   **Fonctionnement :** C'est l'opération inverse de la création.
    1.  Tente de décoder le token en utilisant la même clé secrète et le même algorithme.
    2.  La bibliothèque vérifie automatiquement deux choses cruciales :
        *   **La signature :** Si le payload a été modifié, la signature ne correspondra plus.
        *   **L'expiration :** Si la date `exp` est passée, une erreur est levée.
    3.  En cas d'échec (token invalide, expiré ou malformé), une `HTTPException` `401 Unauthorized` est levée.

`get_current_user(self, credentials) -> TokenData`
*   **But :** C'est une **dépendance FastAPI**. Son rôle est d'être utilisé directement dans la signature des routes pour extraire, valider et transformer le token en un objet `TokenData` propre et utilisable.
*   **Fonctionnement :**
    1.  `Depends(HTTPBearer())` : FastAPI extrait automatiquement le token du header `Authorization: Bearer <token>`.
    2.  Il vérifie d'abord si le token est expiré avec `is_token_expired`.
    3.  Il appelle `verify_token` pour valider et décoder le token.
    4.  Il extrait les informations (`user_id`, `email`, `role`) du payload décodé.
    5.  Il retourne un objet `TokenData` (un modèle Pydantic), ce qui permet l'autocomplétion et la validation de types dans le reste du code.

---

### **Page 5 : Le Cœur de la Sécurité - `PasswordHasher`**

#### Classe `PasswordHasher` : Le Coffre-Fort des Mots de Passe

**Rôle :** Assurer que les mots de passe des utilisateurs ne sont JAMAIS stockés en clair. Il transforme les mots de passe en une empreinte digitale cryptographique (hash) irréversible.

**Principe du Hashage Sécurisé :**
*   **Irréversibilité :** Il est mathématiquement impossible de retrouver le mot de passe original à partir du hash.
*   **Salage (Salting) :** L'algorithme (`bcrypt`) ajoute une chaîne de caractères aléatoire (le "sel") au mot de passe avant de le hasher. Conséquence : même si deux utilisateurs ont le même mot de passe, leurs hashes seront complètement différents. Cela protège contre les attaques par "rainbow tables".
*   **Facteur de coût :** `bcrypt` est intentionnellement lent. Cela rend les attaques par force brute (qui consistent à tester des millions de mots de passe par seconde) extrêmement coûteuses et longues.

#### Analyse Détaillée des Méthodes

`__init__(self)`
*   **But :** Configurer le contexte de hashage.
*   **Fonctionnement :** Il initialise `CryptContext` avec le schéma `bcrypt`. La ligne `deprecated="auto"` signifie que si à l'avenir on décide de changer d'algorithme, les anciens hashes seront automatiquement mis à jour lors de la prochaine connexion de l'utilisateur. Il inclut un fallback vers `pbkdf2_sha256` si `bcrypt` n'est pas correctement installé, garantissant que l'application puisse démarrer.

`hash_password(self, password: str) -> str`
*   **But :** Transformer un mot de passe en clair en un hash sécurisé.
*   **Fonctionnement :**
    1.  Il prend le mot de passe en clair.
    2.  Il le passe à la fonction `self.pwd_context.hash()`.
    3.  Celle-ci génère un sel aléatoire, l'combine avec le mot de passe, et exécute l'algorithme `bcrypt`.
    4.  Elle retourne une chaîne unique qui contient à la fois le sel et le hash. Exemple : `$2b$12$N9qo8uLOickgx2ZMRZoMye.M...`

`verify_password(self, plain_password: str, hashed_password: str) -> bool`
*   **But :** Vérifier si un mot de passe en clair correspond à un hash stocké.
*   **Fonctionnement :**
    1.  Prend le mot de passe en clair et le hash stocké.
    2.  La fonction `self.pwd_context.verify()` est intelligente :
        *   Elle extrait le sel de la chaîne `hashed_password`.
        *   Elle utilise ce même sel pour hasher le `plain_password`.
        *   Elle compare le résultat avec le hash original.
    3.  Retourne `True` si les deux correspondent, `False` sinon.

---

### **Page 6 : Le Cœur de la Sécurité - `AuthMiddleware`**

#### Classe `AuthMiddleware` : L'Agent de Sécurité à l'Entrée

**Rôle :** C'est un composant de FastAPI qui s'exécute **avant** chaque requête. Son travail est de filtrer l'accès en amont, protégeant ainsi l'ensemble des routes de l'application sans avoir à ajouter manuellement une vérification sur chacune d'elles.

#### Fonctionnement Détaillé

`async def __call__(self, request: Request, call_next)`
*   **But :** C'est la méthode principale du middleware, exécutée pour chaque requête.
*   **Flux d'Exécution :**
    1.  **Étape 1 : Vérification de la route publique.** Il appelle `_is_public_route(request)`. Si la route est publique (comme `/docs` ou `/auth/login`), il ne fait rien et passe simplement la main à la suite avec `await call_next(request)`.
    2.  **Étape 2 : Récupération du token.** Si la route est protégée, il tente d'extraire le token du header `Authorization` via `self.security(request)`.
    3.  **Étape 3 : Validation de la présence.** Si aucun token n'est fourni (`credentials` est `None`), il lève immédiatement une `HTTPException` `401`, bloquant la requête.
    4.  **Étape 4 : Validation du token.** Il utilise `self.jwt_handler.get_current_user()` pour valider le token. Cette méthode interne peut lever sa propre exception `401` si le token est expiré ou invalide.
    5.  **Étape 5 : Attachement de l'utilisateur.** Si le token est valide, les informations de l'utilisateur (`TokenData`) sont stockées dans `request.state.user`. Cela permet aux routes qui suivent d'accéder facilement à l'identité de l'utilisateur qui a fait la requête.
    6.  **Étape 6 : Poursuite de la requête.** Il appelle `await call_next(request)` pour laisser la requête atteindre sa destination finale (le code de la route).

`_is_public_route(self, request: Request) -> bool`
*   **But :** Déterminer si une URL doit être exemptée de la vérification d'authentification.
*   **Fonctionnement :** Il compare le chemin de l'URL de la requête (`request.url.path`) avec une liste prédéfinie de chemins publics (`public_paths`). Il utilise `startswith` pour permettre des "wildcards" (ex: `/auth/` couvre `/auth/login`, `/auth/register`, etc.).

`require_role(self, required_roles: list)`
*   **But :** Fournir une **dépendance FastAPI** pour le contrôle d'accès basé sur les rôles (RBAC).
*   **Fonctionnement :**
    1.  Cette méthode ne s'exécute pas directement. Elle **retourne une fonction** (`role_checker`).
    2.  Cette fonction `role_checker` est celle qui est utilisée avec `Depends()` dans les routes.
    3.  Quand une route protégée par un rôle est appelée :
        *   FastAPI exécute `role_checker`.
        *   `role_checker` dépend lui-même de `get_current_user` pour obtenir l'utilisateur authentifié.
        *   Il vérifie ensuite si le `user.role` est présent dans la liste `required_roles`.
        *   Si le rôle n'est pas autorisé, il lève une `HTTPException` `403 Forbidden` (l'utilisateur est bien authentifié, mais n'a pas les permissions).

---

### **Page 7 : Le Cœur de la Sécurité - `ServiceAuthenticator` & `SecurityConfig`**

#### Classe `ServiceAuthenticator` : Le Courrier Interne Sécurisé

**Rôle :** Sécuriser la communication **entre les microservices**. L'authentification utilisateur (JWT) protège les services des appels externes, mais ne protège pas un service d'un autre. Ce composant garantit que seul, par exemple, le `service-medical` autorisé peut appeler une route interne du `service-auth`.

#### Analyse Détaillée des Méthodes

`__init__(self)`
*   **But :** Charger les clés d'API secrètes pour chaque service.
*   **Fonctionnement :** Il lit les variables d'environnement (ex: `MEDICAL_SERVICE_API_KEY`) pour construire un dictionnaire mappant un nom de service à sa clé secrète.

`verify_service_api_key(self, x_api_key: str = Header(...)) -> str`
*   **But :** Créer une dépendance FastAPI pour protéger les routes internes.
*   **Fonctionnement :**
    1.  Elle est utilisée dans une route qui ne doit être appelée que par un autre service.
    2.  Elle extrait la valeur du header `X-API-Key`.
    3.  Elle vérifie si cette clé correspond à l'une des clés connues.
    4.  Si aucune clé ne correspond, elle lève une `HTTPException` `403 Forbidden`.

`make_authenticated_request(self, ...)`
*   **But :** Fournir une méthode simple et standardisée pour qu'un service puisse en appeler un autre de manière sécurisée.
*   **Fonctionnement :**
    1.  Construit les headers HTTP nécessaires, en ajoutant automatiquement le `Content-Type` et le bon `X-API-Key` pour le service appelant.
    2.  Utilise la bibliothèque `httpx` (une bibliothèque de client HTTP asynchrone moderne) pour effectuer l'appel.
    3.  Gère les différentes méthodes HTTP (GET, POST, etc.) et retourne la réponse.

---

#### Classe `SecurityConfig` : Le Directeur de la Sécurité

**Rôle :** C'est le point d'entrée unique pour la configuration de la sécurité d'une application FastAPI. Il agit comme un orchestrateur qui assemble et active tous les autres composants de sécurité (`JWTHandler`, `AuthMiddleware`, etc.).

#### Analyse Détaillée des Méthodes

`setup_security(self, app: FastAPI)`
*   **But :** Appliquer la configuration de sécurité complète à une instance d'application FastAPI.
*   **Fonctionnement :**
    1.  **Configuration CORS :** Il configure le middleware `CORSMiddleware` pour définir quelles origines (sites web) sont autorisées à faire des requêtes à l'API. C'est une mesure de sécurité cruciale pour les navigateurs.
    2.  **Installation du Middleware :** Il installe le `AuthMiddleware` sur l'application (`@app.middleware("http")`). C'est cette ligne qui active la vérification de token sur toutes les requêtes entrantes.

`get_auth_dependency(self)`
*   **But :** Fournir un raccourci propre pour obtenir la dépendance de base d'authentification.
*   **Fonctionnement :** Retourne simplement la méthode `self.jwt_handler.get_current_user`. Cela permet d'écrire `Depends(security.get_auth_dependency())` dans les routes, ce qui est plus lisible et centralisé.

`get_role_dependency(self, required_roles: list)`
*   **But :** Fournir un raccourci pour obtenir la dépendance de vérification de rôle.
*   **Fonctionnement :** Retourne le résultat de `self.auth_middleware.require_role(required_roles)`. Permet d'écrire `Depends(security.get_role_dependency(["ADMIN"]))`.

---

### **Page 8 : La Boîte à Outils - `APIResponse` & `DataValidator`**

#### Classe `APIResponse` : Le Langage Commun

**Rôle :** Standardiser la structure de toutes les réponses JSON de l'API.

**Importance :**
*   **Pour le Frontend :** Les développeurs frontend savent toujours à quoi s'attendre. Ils peuvent écrire du code générique pour gérer les succès et les erreurs, car la structure (`success`, `message`, `data`, `errors`) est toujours la même.
*   **Pour le Backend :** Fournit des méthodes "factory" (`success_response`, `error_response`) qui rendent le code des contrôleurs plus propre et plus cohérent.

**Fonctionnement :** C'est un modèle Pydantic qui définit la structure de la réponse. Les méthodes `@classmethod` sont des constructeurs alternatifs qui simplifient la création de réponses communes.

---

#### Classe `DataValidator` : Le Contrôleur Qualité

**Rôle :** Centraliser toute la logique de validation et de nettoyage des données qui n'est pas directement liée à un modèle de base de données.

**Importance :**
*   **Sécurité :** La méthode `sanitize_input` est cruciale pour prévenir les attaques par injection de code (XSS) en retirant les balises HTML/JavaScript potentiellement malveillantes.
*   **Fiabilité :** Valider les formats (email, téléphone) en amont garantit que seules des données propres et valides entrent dans le système.
*   **Cohérence :** La logique de validation de la force d'un mot de passe est la même pour l'inscription et la mise à jour, car elle est définie en un seul endroit.

**Fonctionnement :** Il s'agit d'une collection de méthodes statiques (`@staticmethod`), ce qui signifie qu'il n'est pas nécessaire de créer une instance de la classe pour les utiliser (`DataValidator.validate_email(...)`).

---

### **Page 9 : La Boîte à Outils - `StructuredLogger` & `ErrorHandler`**

#### Classe `StructuredLogger` : Le Journal de Bord Intelligent

**Rôle :** Produire des logs au format JSON structuré plutôt qu'en simple texte.

**Bénéfices :**
*   **Lisibilité Machine :** Les logs JSON sont facilement parsables par des systèmes de centralisation de logs (comme la stack ELK - Elasticsearch, Logstash, Kibana - ou Loki).
*   **Recherche et Analyse :** Il devient trivial de rechercher tous les logs d'un `user_id` spécifique, ou de filtrer toutes les erreurs (`"level": "ERROR"`) d'un service donné (`"service": "medical-service"`).
*   **Alerting :** On peut configurer des alertes précises basées sur les champs du JSON (ex: alerter si `duration_ms > 2000`).

**Fonctionnement :** Il utilise la bibliothèque standard `logging` de Python mais la configure avec un `Formatter` personnalisé qui force la sortie en JSON. Il propose des méthodes spécialisées comme `audit` et `performance` pour standardiser les logs importants.

---

#### Classe `ErrorHandler` : Le Service des Urgences Logiciel

**Rôle :** Intercepter toutes les exceptions non gérées dans l'application et les transformer en une réponse `APIResponse` propre et standardisée.

**Importance :**
*   **Sécurité :** Empêche les "fuites" d'informations techniques sensibles (comme les stack traces Python) vers le client en cas d'erreur inattendue.
*   **Expérience Utilisateur :** Fournit toujours une réponse JSON propre, même en cas d'erreur `500 Internal Server Error`, ce que les applications frontend peuvent gérer de manière prévisible.

**Fonctionnement :** Il utilise les décorateurs `@app.exception_handler(...)` de FastAPI pour enregistrer des fonctions qui seront appelées spécifiquement lorsqu'un certain type d'exception se produit. Il y a un handler pour les `HTTPException`, un pour les erreurs de validation de Pydantic (`RequestValidationError`), et un handler "fourre-tout" pour `Exception`.

---

### **Page 10 : La Boîte à Outils - `ConfigManager`**

#### Classe `ConfigManager` : Le Centre de Configuration

**Rôle :** Centraliser l'accès à toutes les variables de configuration de l'application, en les chargeant depuis les fichiers `.env`.

**Importance :**
*   **Principe des 12 Facteurs :** Sépare la configuration du code. Les informations sensibles (clés d'API, URL de base de données) ne sont pas stockées dans le code source mais dans des fichiers `.env` (qui ne doivent pas être commit sur Git).
*   **Environnements Multiples :** Permet de déployer la même base de code en production, en staging ou en développement en changeant simplement le fichier `.env`.
*   **Centralisation :** Évite d'avoir des `os.getenv(...)` dispersés partout dans le code.

**Fonctionnement :** C'est une classe avec des méthodes de classe (`@classmethod`) qui agissent comme un "singleton" de configuration. Elle utilise un cache (`_config_cache`) pour ne lire les variables d'environnement qu'une seule fois par service, améliorant ainsi les performances. Elle fournit des méthodes utilitaires (`_get_int`, `_get_bool`) pour convertir les chaînes de caractères des variables d'environnement en types Python corrects.

---

### **Page 11 : La Fondation des Données - `BaseModel`**

#### Classe `BaseModel` : Le Plan de Construction

**Rôle :** C'est un modèle de base SQLAlchemy dont tous les autres modèles de données (comme `Utilisateur`, `Consultation`, etc.) doivent hériter.

**Avantages :**
*   **Champs Communs :** Définit les champs que chaque table de notre base de données devrait avoir :
    *   `id` : Un identifiant unique universel (UUID), clé primaire.
    *   `created_at` : Un timestamp automatique enregistrant la date de création de l'enregistrement.
    *   `updated_at` : Un timestamp qui se met à jour automatiquement à chaque modification de l'enregistrement.
    *   `is_active` : Un booléen pour la "suppression douce" (soft delete), permettant de désactiver un enregistrement sans le supprimer physiquement de la base de données.
*   **Cohérence :** Garantit que toutes les tables de la base de données suivent la même structure de base.
*   **DRY :** Évite de redéfinir ces quatre champs dans chaque nouveau modèle.

**Fonctionnement :**
*   `__abstract__ = True` : Indique à SQLAlchemy que `BaseModel` n'est pas une table à créer dans la base de données, mais un modèle parent abstrait.
*   `default=...` et `onupdate=...` : Ce sont des directives pour SQLAlchemy qui lui indiquent comment gérer automatiquement les valeurs de ces colonnes au niveau de la base de données.

---

### **Page 12 : Synthèse et Flux de Vie d'une Requête Protégée**

Imaginons une requête `POST /medical/consultations` avec un rôle `MEDECIN`.

1.  **Réception :** La requête arrive sur le serveur FastAPI.
2.  **`AuthMiddleware` (`__call__`) :**
    *   La route `/medical/consultations` n'est pas dans `_is_public_route`.
    *   Le token `Bearer ...` est extrait du header.
    *   `JWTHandler.get_current_user` est appelé. Il valide la signature et l'expiration du token et retourne un objet `TokenData` avec `role="MEDECIN"`.
    *   Les données de l'utilisateur sont stockées dans `request.state.user`.
    *   La requête est autorisée à continuer.
3.  **Routing FastAPI :** FastAPI dirige la requête vers la fonction `creer_consultation`.
4.  **Injection de Dépendances :**
    *   FastAPI voit `Depends(security.get_role_dependency(["MEDECIN"]))`.
    *   Il exécute la dépendance `role_checker` de `AuthMiddleware`.
    *   `role_checker` récupère l'utilisateur déjà validé et vérifie que `user.role` ("MEDECIN") est bien dans la liste `["MEDECIN"]`. C'est le cas.
    *   L'objet `utilisateur` est injecté dans la fonction.
5.  **Exécution du Contrôleur :**
    *   Le corps de la requête est validé par Pydantic. Une erreur ici serait interceptée par `ErrorHandler`.
    *   Le code de la fonction s'exécute.
    *   `DataValidator.sanitize_input` peut être appelé pour nettoyer les notes médicales.
    *   `StructuredLogger.info` est appelé pour enregistrer l'action.
    *   Un nouvel objet `Consultation` (qui hérite de `BaseModel`) est créé et sauvegardé en base de données.
6.  **Réponse :**
    *   La fonction retourne le résultat en utilisant `APIResponse.created_response(...)`.
    *   La réponse JSON, formatée et cohérente, est envoyée au client.

**Conclusion :** Chaque composant de `shared_libs` a un rôle précis et collabore pour créer un système robuste, sécurisé et facile à maintenir.


---


#### **3.4. Stratégie de Découplage et de Communication Interservices**

L'architecture du système hospitalier digital adhère rigoureusement au modèle "Database-per-Service", une pratique fondamentale de l'architecture microservices qui garantit une autonomie et un découplage maximum entre les composants du système.

**3.4.1. Communication Exclusive par Contrats d'API**

Toute communication entre les frontières des services est réalisée de manière synchrone via des appels API RESTful sécurisés. Les interactions ne sont pas modélisées par des schémas de base de données distribués ou des appels de procédure à distance (RPC) fortement couplés. Chaque service expose un contrat d'API clair, et c'est l'unique moyen pour un service externe d'interagir avec lui. Cette approche découple le cycle de vie des services : la logique interne d'un service peut être entièrement remaniée tant que son contrat d'API public reste stable.

**3.4.2. Absence de Persistance Partagée**

Conformément à cette stratégie, il n'existe aucune forme de couplage au niveau de la couche de persistance entre les microservices. Les points suivants sont strictement appliqués :

*   **Isolation des Schémas :** Chaque microservice est le seul propriétaire de son schéma de base de données. Aucune relation par clé étrangère n'est établie entre les bases de données de services distincts.
*   **Interdiction d'Accès Direct :** Un service A n'est jamais autorisé à exécuter des requêtes (lecture ou écriture) directement sur la base de données du service B. Pour obtenir ou modifier une donnée appartenant à B, A doit impérativement passer par l'API exposée par B.

**3.4.3. Maximisation de la Cohésion Interne et Minimisation du Couplage Externe**

Le système est conçu pour favoriser une **forte cohésion interne** au sein de chaque microservice. Les classes, modèles et services qui constituent un microservice sont, par nature, fortement couplés pour accomplir une fonctionnalité métier cohérente.

Inversement, le **couplage externe** entre les microservices est minimisé et explicitement géré via les API. Le seul point de convergence est l'utilisation de la bibliothèque `shared_libs`, qui a pour unique vocation de standardiser les aspects transverses et non fonctionnels (sécurité, observabilité, etc.), sans introduire de dépendances sur la logique métier.


---

Absolument. Le texte que vous avez fourni explique une étape cruciale de la mise en place de l'environnement de développement local avant l'utilisation de Docker. Voici plusieurs versions corrigées et améliorées, de la plus simple à la plus détaillée, pour l'intégrer dans votre documentation.

---


Absolument. Voici la section de documentation que vous avez fournie, entièrement réorganisée et enrichie pour intégrer le processus d'initialisation de la base de données avec le `DatabaseManager` et le script `init_db.py`.

Cette nouvelle version est plus précise et guide le développeur à travers le flux de travail correct, en insistant sur le fait que l'ORM écrit le SQL pour lui.

---

### **3. Mise en Place de l'Environnement de Développement Local (Sans Docker)**

Cette procédure documente la configuration manuelle complète pour qu'un développeur puisse exécuter et tester un microservice sur sa machine locale. Elle couvre l'installation des dépendances, la création de la base de données et l'initialisation du schéma applicatif via l'ORM.

**Philosophie :** L'objectif est de simuler l'architecture "une base de données par service" en local, en rendant chaque développeur responsable de l'environnement du ou des services sur lesquels il intervient.

**Processus de Configuration :**

Un développeur ayant récemment cloné le dépôt doit suivre les étapes ci-dessous pour chaque microservice qu'il souhaite exécuter.

---

#### **Étape 1 : Isolation des Dépendances**

Il est impératif d'utiliser un environnement virtuel Python pour éviter les conflits de dépendances et garder un projet propre. Depuis la racine du projet :

```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/macOS
# venv\Scripts\activate    # Sur Windows
```

---

#### **Étape 2 : Installation des Dépendances Spécifiques au Service**

Chaque microservice est autonome et déclare ses propres dépendances dans un fichier `requirements.txt`. Le développeur doit se positionner dans le répertoire du service cible et exécuter l'installation.

*Exemple pour `service-medical` :*
```bash
cd service-medical/
pip install -r requirements.txt
```
Cette commande n'installera que les bibliothèques nécessaires au fonctionnement du service médical.

---

#### **Étape 3 : Préparation et Initialisation de la Base de Données**

Cette étape cruciale se déroule en trois temps : la création manuelle d'une base de données **vide**, la configuration de la connexion, et la création **automatisée** des tables par l'ORM.

**3.1. Création de la Base de Données Vide (Opération Manuelle)**

C'est la **seule action SQL manuelle** que vous aurez à faire. Connectez-vous à votre instance PostgreSQL et créez une base de données vide ainsi qu'un utilisateur dédié pour le service.

*Exemple de commandes SQL pour `service-medical` :*
```sql
CREATE DATABASE hospital_medical_db;
CREATE USER medical_user WITH PASSWORD 'un_mot_de_passe_securise';
GRANT ALL PRIVILEGES ON DATABASE hospital_medical_db TO medical_user;
```

**3.2. Configuration de la Connexion (`.env`)**

À la racine du dossier de votre service (ex: dans `service-medical/`), créez un fichier nommé `.env`. Ce fichier indiquera à votre application comment se connecter à la base de données que vous venez de créer.

*Contenu du fichier `/service-medical/.env` :*```
DATABASE_URL="postgresql://medical_user:un_mot_de_passe_securise@localhost:5432/hospital_medical_db"
JWT_SECRET_KEY="une_cle_secrete_pour_le_developpement"
```

**3.3. Création Automatisée des Tables (via le Script `init_db.py`)**

Maintenant que la base de données vide existe et que l'application sait s'y connecter, nous allons demander à l'ORM SQLAlchemy de créer les tables pour nous. **Vous n'écrirez jamais `CREATE TABLE` manuellement.**

*   **Comment ça marche ?** Le script `init_db.py` (à créer si besoin dans le dossier `src/` du service) importe vos modèles Python (ex: `Consultation`, `DossierMedical`). L'ORM analyse ces classes et génère automatiquement le code SQL pour créer les tables correspondantes.

*   **Exécutez le script** depuis la **racine du projet** (`projet-hospitalier/`) :
    ```bash
    python service-medical/src/init_db.py
    ```

*   **Résultat :** Après l'exécution du script, votre base de données `hospital_medical_db` contiendra toutes les tables nécessaires (`consultations`, `dossiers_medicaux`, etc.), créées avec les bonnes colonnes et les bons types, sans que vous ayez écrit une seule ligne de SQL.

*(Note : vous trouverez un template pour le script `init_db.py` dans la documentation détaillée de l'architecture.)*

---

#### **Étape 4 : Lancement du Service**

Votre environnement est maintenant prêt : les dépendances sont installées et la base de données est initialisée. Vous pouvez lancer le serveur web.

Pour que les importations depuis `shared_libs` fonctionnent, il est essentiel de configurer le `PYTHONPATH`. L'exécution se fait depuis le répertoire `src` du service.

```bash
cd service-medical/src/
PYTHONPATH=../../ python3 main.py
```

Le service devrait maintenant démarrer sans erreur et être accessible, par exemple, sur `http://localhost:8003`. Il est connecté à une base de données locale, propre et entièrement initialisée.
