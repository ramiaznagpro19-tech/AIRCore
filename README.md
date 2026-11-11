# AIRCore

Moteur de rendu web pour Android du navigateur **AIR Navig**, basé sur **Gecko / GeckoView** (le moteur de Firefox), sans télémétrie.

## Ce que fait ce dépôt
À chaque compilation, GitHub Actions :
1. **récupère le code Gecko officiel** de Firefox, à la version figée dans `GECKO_VERSION` (actuellement Gecko 160.0.1, branche `release` de https://github.com/mozilla-firefox/firefox) ;
2. **applique les modifications AIRCore** (`aircore/patch.py`) ;
3. **compile** le moteur et produit **`AIRCore-….aar`** (Android arm64-v8a), publié dans « Releases ».

Le code de Gecko n'est pas copié dans ce dépôt : il pèse plusieurs Go (environ 350 000 fichiers), au-delà des limites d'envoi de GitHub. Seules les modifications AIRCore sont versionnées, comme le font IronFox ou Tor Browser.

## Modifications AIRCore
| Domaine | Modification | Fichier Gecko |
|---|---|---|
| Télémétrie | Télémétrie Gecko, pings, envoi Glean/FOG, DAP, mesure publicitaire (PPA) coupés | `mobile/android/app/geckoview-prefs.js` |
| Études | Normandy / Shield désactivés | idem |
| Plantages | L'envoi des rapports vers Mozilla (Socorro) est supprimé du code Java | `geckoview/CrashReporter.java` |
| Connexions de vérification | Portail captif, test de connectivité, détection MITM coupés ; Safe Browsing sans envoi de fichiers à Google | `geckoview-prefs.js` |
| User-Agent | `… Firefox/160.0 AIRCore/1.0` (le jeton Firefox reste pour la compatibilité des sites) | `GeckoViewSettings.sys.mjs` |
| Identifiants | Fichier `AIRCore-….aar` ; API `app.air.core.AIRCore` (les coordonnées Maven internes restent `org.mozilla.geckoview`, dont dépend le projet Gradle de Gecko) | `app/air/core/AIRCore.java` |

Pocket, Sync et les comptes Firefox ne font pas partie de GeckoView (ils sont dans l'appli Firefox, pas dans le moteur) : il n'y a rien à retirer.

## Compilation rapide
Pour rester autour de 20 minutes, AIRCore utilise le mode « artifact build » de Mozilla : **tout le Java, le JavaScript et les réglages sont recompilés depuis le code modifié**, et seul le moteur C++ précompilé (`libxul.so`) vient des serveurs de Mozilla, pour la même version. La télémétrie C++ qu'il contient est rendue inerte par les réglages ci-dessus.

## Utilisation dans une appli
```java
GeckoRuntime runtime = app.air.core.AIRCore.runtime(context);
GeckoSession session = new GeckoSession();
session.open(runtime);
geckoView.setSession(session);
session.loadUri("https://example.org");
```

## Mettre Gecko à jour
Modifier `GECKO_REF` / `GECKO_LABEL` dans `GECKO_VERSION` (commit de la branche `release`), puis envoyer : la compilation repart toute seule. Si un fichier de Mozilla a changé, `patch.py` s'arrête avec un message clair.

## Licence
Gecko et les modifications AIRCore sont sous licence **Mozilla Public License 2.0**. « Firefox » est une marque de Mozilla : AIRCore n'utilise pas ce nom ni son logo.
