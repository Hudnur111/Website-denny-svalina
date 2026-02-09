// ===== HAUPT-SCRIPT: Navigation, Animationen, Theme-Handling =====
(function () {
  const tabs = Array.from(document.querySelectorAll(".tab"));
  const sections = Array.from(document.querySelectorAll(".section"));

  // ===== TAB-NAVIGATION: Sektion-Wechsel =====
  // Wechselt aktiven Tab und zeigt entsprechenden Section-Inhalt an
  function setActive(id) {
    sections.forEach((s) => s.classList.toggle("active", s.id === id));
    tabs.forEach((b) => b.setAttribute("aria-selected", String(b.dataset.tab === id)));

    // Wenn Skills-Sektion: Meter animieren
    if (id === "skills") {
      document.querySelectorAll(".meter").forEach((m) => {
        const fill = Number(m.getAttribute("data-fill") || 0);
        const span = m.querySelector("span");
        if (span) span.style.width = fill + "%";
      });
    }
  }

  // Event-Listener: Klick auf Tab triggert Content-Wechsel
  tabs.forEach((btn) => btn.addEventListener("click", () => setActive(btn.dataset.tab)));

  // ===== FOOTER-JAHR: Automatisch aktualisieren =====
  const yearElement = document.getElementById("year");
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
  }

  // ===== KONTAKT-FORMULAR: Mailto-Integration =====
  const form = document.getElementById("contactForm");
  const note = document.getElementById("formNote");

  if (form) {
    form.addEventListener("submit", (e) => {
      // Standard-Form-Verhalten verhindern, eigene E-Mail-Aktion durchführen
      e.preventDefault();
      const name = document.getElementById("name").value.trim();
      const email = document.getElementById("email").value.trim();
      const msg = document.getElementById("msg").value.trim();

      // Mailto-URL zusammenstellen mit Nutzerdaten
      const subject = encodeURIComponent("Kontakt über Portfolio-Website");
      const body = encodeURIComponent(
        "Name: " + (name || "-") + "\n" + "E-Mail: " + (email || "-") + "\n\n" + "Nachricht:\n" + (msg || "-")
      );

      // Feedback: Mailto-Client öffnen oder Fehlermeldung
      if (note) {
        note.style.display = "block";
        note.textContent = "Entwurf erstellt. Wenn sich kein Mailprogramm öffnet, ist Mailto im Browser blockiert.";
      }
      window.location.href = "mailto:dennysvalina@gmail.com?subject=" + subject + "&body=" + body;
    });
  }

  // Standard-Tab beim Laden: "Über mich"
  setActive("ueber");

  // ===== SCROLL-REVEAL ANIMATIONEN: IntersectionObserver =====
  // Prüfe, ob Nutzer Bewegungsanimationen reduziert haben möchte (Accessibility)
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Alle Elemente sammeln, die animiert werden sollen
  const toObserve = Array.from(
    document.querySelectorAll(
      ".card, .item, .skill, .meter, .headline, .lead, .pillrow, .tags, .cta"
    )
  );

  // Alle Elemente initial mit 'animate'-Klasse versehen (versteckt/transparent)
  toObserve.forEach((el) => el.classList.add("animate"));

  if (prefersReduced) {
    // Für Nutzer mit Bewegungsempfindlichkeit: Alles direkt sichtbar machen
    toObserve.forEach((el) => el.classList.add("in-view"));
    // Skill-Meter sofort zum finalen Wert
    document.querySelectorAll(".meter").forEach((m) => {
      const span = m.querySelector("span");
      const fill = Number(m.getAttribute("data-fill") || 0);
      if (span) span.style.width = fill + "%";
    });
  } else {
    // ===== IntersectionObserver: Elegante Scroll-Reveal Animationen =====
    const obs = new IntersectionObserver((entries, o) => {
      // Callback: Wenn Element in Sichtbereich kommt, Animation anstoßen
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const el = entry.target;
          // Aktiviert CSS-Transition/Animation für dieses Element
          el.classList.add("in-view");

          // Spezialfall: Skill-Meter mit Ladebalken animieren
          if (el.classList.contains("meter")) {
            const span = el.querySelector("span");
            const fill = Number(el.getAttribute("data-fill") || 0);
            if (span) span.style.width = fill + "%";
          } else {
            // Verzögerter Eintritt für Kinder-Elemente (visueller Staggering-Effekt)
            Array.from(el.children).forEach((c, i) => {
              c.style.transitionDelay = i * 40 + "ms";
            });
          }
          // Element aus Beobachtung entfernen (Performance-Optimierung)
          o.unobserve(el);
        }
      });
    }, {
      threshold: 0.12,
    });

    // Observer zu allen animierbaren Elementen starten
    toObserve.forEach((el) => obs.observe(el));
  }

  // ===== THEME HANDLING: Light / Dark Mode System =====
  const toggle = document.getElementById("themeToggle");
  const systemDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)");

  // Wendet Theme an: setzt data-theme Attribut und updatet Toggle-Icon
  function applyTheme(theme) {
    // Theme-Logik: Explizit Dark/Light oder System-Einstellung folgen
    if (theme === "dark") document.documentElement.setAttribute("data-theme", "dark");
    else if (theme === "light") document.documentElement.removeAttribute("data-theme");
    else {
      /* system preference */
      if (systemDark && systemDark.matches) document.documentElement.setAttribute("data-theme", "dark");
      else document.documentElement.removeAttribute("data-theme");
    }
    // Update UI: Toggle-Button Icon wechseln
    const isDark = document.documentElement.getAttribute("data-theme") === "dark";
    if (toggle) {
      toggle.setAttribute("aria-pressed", String(isDark));
      // Icon: 🌙 für Light-Mode, ☀️ für Dark-Mode
      toggle.textContent = isDark ? "☀️" : "🌙";
    }
  }

  // ===== THEME-PERSISTENZ: localStorage + System-Prefs =====
  // Beim Laden: Gespeicherte Einstellung oder System-Preferenz nutzen
  const stored = localStorage.getItem("theme");
  applyTheme(stored || "system");

  // ===== TOGGLE-BUTTON: Theme umschalten (Dark <-> Light) =====
  if (toggle) {
    toggle.addEventListener("click", () => {
      // Aktuellen Mode ermitteln und alternieren
      const cur = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
      const next = cur === "dark" ? "light" : "dark";
      // Neue Wahl speichern und sofort anwenden
      localStorage.setItem("theme", next);
      applyTheme(next);
    });
  }

  // ===== SYSTEMPREFERENZ-BEOBACHTER: OS-Theme ändert sich =====
  // Wenn Nutzer System-Theme ändert und wir im 'system'-Modus sind: Follow-up
  if (systemDark && systemDark.addEventListener) {
    systemDark.addEventListener("change", () => {
      const stored = localStorage.getItem("theme");
      // Nur folgen wenn User nicht manuell gewählt hat
      if (!stored || stored === "system") applyTheme("system");
    });
  }
})();
// ===== Ende: Haupt-Script =====
