// ===================== AIRCore : reglages ajoutes au moteur =====================
// Aucune telemetrie, aucun rapport de donnees, aucune etude, aucun rapport de plantage,
// aucune connexion de  verification  vers les serveurs de Mozilla.

// Telemetrie Gecko
pref("toolkit.telemetry.enabled", false);
pref("toolkit.telemetry.unified", false);
pref("toolkit.telemetry.archive.enabled", false);
pref("toolkit.telemetry.server", "data:,");
pref("toolkit.telemetry.geckoview.streaming", false);
pref("toolkit.telemetry.newProfilePing.enabled", false);
pref("toolkit.telemetry.shutdownPingSender.enabled", false);
pref("toolkit.telemetry.firstShutdownPing.enabled", false);
pref("toolkit.telemetry.updatePing.enabled", false);
pref("toolkit.telemetry.bhrPing.enabled", false);
pref("toolkit.telemetry.dap_enabled", false);
pref("toolkit.telemetry.user_characteristics_ping.opt-out", true);
pref("toolkit.telemetry.coverage.opt-out", true);
pref("toolkit.coverage.opt-out", true);
pref("toolkit.coverage.endpoint.base", "");
pref("dom.security.unexpected_system_load_telemetry_enabled", false);
pref("browser.ping-centre.telemetry", false);

// Envoi de donnees (Glean / FOG compris)
pref("datareporting.healthreport.uploadEnabled", false);
pref("datareporting.policy.dataSubmissionEnabled", false);
pref("datareporting.usage.uploadEnabled", false);

// Mesure publicitaire  respectueuse de la vie privee  (PPA)
pref("dom.private-attribution.submission.enabled", false);

// Etudes et experiences a distance
pref("app.normandy.enabled", false);
pref("app.normandy.api_url", "");
pref("app.shield.optoutstudies.enabled", false);

// Rapports de plantage
pref("breakpad.reportURL", "");
pref("browser.crashReports.unsubmittedCheck.enabled", false);
pref("browser.crashReports.unsubmittedCheck.autoSubmit2", false);

// Connexions de verification vers Mozilla
pref("network.captive-portal-service.enabled", false);
pref("network.connectivity-service.enabled", false);
pref("captivedetect.canonicalURL", "");
pref("security.certerrors.mitm.priming.enabled", false);

// Navigation securisee : protection gardee, mais aucun envoi d'empreinte de fichier a Google
pref("browser.safebrowsing.downloads.remote.enabled", false);

// Identite du moteur
pref("aircore.version", "1.0");
