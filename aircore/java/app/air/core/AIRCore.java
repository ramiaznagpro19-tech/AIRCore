/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

package app.air.core;

import android.content.Context;
import androidx.annotation.NonNull;
import org.mozilla.geckoview.BuildConfig;
import org.mozilla.geckoview.GeckoRuntime;
import org.mozilla.geckoview.GeckoRuntimeSettings;

/** Point d'entree du moteur AIRCore (base sur GeckoView, sans telemetrie). */
public final class AIRCore {
  /** Nom du moteur. */
  public static final String NAME = "AIRCore";

  /** Version d'AIRCore. */
  public static final String VERSION = "@AIRCORE_VERSION@";

  /** Jeton ajoute au User-Agent. */
  public static final String USER_AGENT_TOKEN = NAME + "/" + VERSION;

  private static GeckoRuntime sRuntime;

  private AIRCore() {}

  /** Version de Gecko sur laquelle repose AIRCore. */
  public static @NonNull String geckoVersion() {
    return BuildConfig.MOZ_APP_VERSION;
  }

  /** Reglages par defaut d'AIRCore : pas de debogage distant, pas de console, pas de rapport. */
  public static @NonNull GeckoRuntimeSettings.Builder defaultSettings() {
    return new GeckoRuntimeSettings.Builder()
        .remoteDebuggingEnabled(false)
        .consoleOutput(false)
        .aboutConfigEnabled(false);
  }

  /** Renvoie le moteur unique de l'appli, cree au premier appel. */
  public static synchronized @NonNull GeckoRuntime runtime(final @NonNull Context context) {
    if (sRuntime == null) {
      sRuntime = GeckoRuntime.create(context.getApplicationContext(), defaultSettings().build());
    }
    return sRuntime;
  }
}
