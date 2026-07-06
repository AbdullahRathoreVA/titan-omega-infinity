"use client";

import { useCallback, useEffect, useState } from "react";
import { api, getToken, setToken, verifyToken } from "@/lib/api";
import { Login } from "./Login";
import { CommandCenter } from "./CommandCenter";

// Decides whether to show the login screen or the dashboard. When the core does
// not require auth (local dev / auth disabled), it goes straight to the
// dashboard. When auth IS required, we VERIFY the stored token actually works
// before trusting it — otherwise a stale token (e.g. after changing the
// username/password) would silently trap the dashboard in 401/demo mode.
export function AuthGate() {
  const [state, setState] = useState<"loading" | "login" | "ready">("loading");
  const [demo, setDemo] = useState(true);
  const [guest, setGuest] = useState(false);

  const probe = useCallback(async () => {
    const status = await api.authStatus();
    setDemo(status.demo);

    // Guest tour: no login wall — straight into the universe, read-only.
    // The flag is set on window BEFORE render so the boot scene greets the
    // visitor instead of the founder.
    if (status.guest && !getToken()) {
      (window as unknown as { __TITAN_GUEST?: boolean }).__TITAN_GUEST = true;
      setGuest(true);
      setState("ready");
      return;
    }

    if (!status.required) {
      setState("ready");
      return;
    }

    const token = getToken();
    if (!token) {
      setState("login");
      return;
    }

    // Verify the stored token really works; if it's stale, force a fresh login.
    const ok = await verifyToken();
    if (ok) {
      setState("ready");
    } else {
      setToken(null);
      setState("login");
    }
  }, []);

  useEffect(() => {
    void probe();
  }, [probe]);

  if (state === "loading") {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <span className="animate-pulseGlow font-mono text-sm text-hud-cyan">
          Booting Titan Omega…
        </span>
      </main>
    );
  }
  if (state === "login") {
    return <Login demo={demo} onSuccess={() => setState("ready")} />;
  }
  return (
    <>
      {guest && (
        <div className="fixed right-3 top-3 z-[999] rounded border border-hud-cyan/40 bg-black/70 px-3 py-1 font-mono text-[11px] tracking-wide text-hud-cyan">
          GUEST TOUR · read-only · sample data
        </div>
      )}
      <CommandCenter />
    </>
  );
}
