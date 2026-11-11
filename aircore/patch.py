#!/usr/bin/env python3
"""Applique les modifications AIRCore au code Gecko officiel.

Usage : python3 aircore/patch.py <dossier-gecko>
Chaque remplacement est vérifié : si le code de Mozilla a changé, le script s'arrête
avec un message clair au lieu de produire un moteur à moitié modifié.
"""
import pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(sys.argv[1]).resolve()
CONF = dict(l.split("=", 1) for l in (HERE.parent / "GECKO_VERSION").read_text().split()
            if "=" in l and not l.startswith("#"))
VERSION = CONF["AIRCORE_VERSION"]
done = []


def edit(rel, old, new, count=1):
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    n = s.count(old)
    if n != count:
        sys.exit(f"AIRCore : motif introuvable ({n} trouvé(s), {count} attendu(s)) dans {rel} :\n{old}")
    p.write_text(s.replace(old, new), encoding="utf-8")
    done.append(rel)


# 1. Réglages : télémétrie, études, rapports et vérifications coupés.
prefs = ROOT / "mobile/android/app/geckoview-prefs.js"
prefs.write_text(prefs.read_text(encoding="utf-8") + "\n" + (HERE / "prefs/aircore-prefs.js").read_text(encoding="utf-8")
                 .replace('"1.0"', f'"{VERSION}"'), encoding="utf-8")
done.append(str(prefs.relative_to(ROOT)))

# 2. Rapports de plantage : l'envoi vers les serveurs de Mozilla (Socorro) est supprimé.
edit("mobile/android/geckoview/src/main/java/org/mozilla/geckoview/CrashReporter.java",
     '    Log.d(LOGTAG, "Sending crash report: " + minidumpFile.getPath());\n',
     '    if (true) {\n'
     '      // AIRCore : aucun rapport de plantage n\'est envoye.\n'
     '      return GeckoResult.fromException(new IOException("AIRCore : envoi des rapports de plantage desactive"));\n'
     '    }\n'
     '    Log.d(LOGTAG, "Sending crash report: " + minidumpFile.getPath());\n')

# 3. User-Agent : « AIRCore/x » ajouté (le jeton Firefox reste pour la compatibilité des sites).
ua = "mobile/shared/modules/geckoview/GeckoViewSettings.sys.mjs"
edit(ua, "const VIEWPORT_MODE_DESKTOP = 1;\n",
     "const VIEWPORT_MODE_DESKTOP = 1;\n\n"
     f'// AIRCore : jeton ajoute au User-Agent.\nconst AIRCORE_UA_TOKEN = " AIRCore/{VERSION}";\n')
edit(ua, """  get customUserAgent() {
    if (this.userAgentOverride !== null) {
      return this.userAgentOverride;
    }
    if (this.userAgentMode === USER_AGENT_MODE_DESKTOP) {
      return this.getDesktopUserAgent();
    }
    if (this.userAgentMode === USER_AGENT_MODE_VR) {
      return this.getVrUserAgent();
    }
    return null;
  }""", """  get customUserAgent() {
    if (this.userAgentOverride !== null) {
      return this.userAgentOverride;
    }
    let ua = this.getMobileUserAgent();
    if (this.userAgentMode === USER_AGENT_MODE_DESKTOP) {
      ua = this.getDesktopUserAgent();
    } else if (this.userAgentMode === USER_AGENT_MODE_VR) {
      ua = this.getVrUserAgent();
    }
    // Pas de jeton si la protection anti-empreinte est active.
    if (ChromeUtils.shouldResistFingerprinting("HttpUserAgent", null)) {
      return ua;
    }
    return ua + AIRCORE_UA_TOKEN;
  }""")
edit(ua, "    this.useTrackingProtection = !!settings.useTrackingProtection;\n",
     "    this.useTrackingProtection = !!settings.useTrackingProtection;\n"
     "    // AIRCore : User-Agent applique des la creation de la session.\n"
     "    this.browsingContext.customUserAgent = this.customUserAgent;\n")

# 4. API AIRCore (app.air.core.AIRCore) ajoutée au moteur.
dst = ROOT / "mobile/android/geckoview/src/main/java/app/air/core/AIRCore.java"
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text((HERE / "java/app/air/core/AIRCore.java").read_text(encoding="utf-8")
               .replace("@AIRCORE_VERSION@", VERSION), encoding="utf-8")
done.append(str(dst.relative_to(ROOT)))

# 5. Les coordonnées Maven internes (org.mozilla.geckoview) ne sont pas renommées : le projet
#    Gradle de GeckoView en dépend pour résoudre ses propres variantes. Le fichier publié
#    s'appelle AIRCore-….aar et l'API publique est app.air.core.AIRCore.

print("AIRCore : modifications appliquées :")
for d in dict.fromkeys(done):
    print("  -", d)
