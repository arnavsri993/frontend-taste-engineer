(() => {
  "use strict";

  const OFFICIAL_SOURCE = "https://www.rockstargames.com/VI/";
  const STORAGE_KEY = "leonida-heat-ledger-dispatch";
  const dispatchCopy = {
    daylight: {
      caption: "Daylight dispatch: hot concrete, mangrove water, and a causeway running straight toward Vice City.",
      status: "Daylight dispatch selected.",
      folio: "L-06 / VIEW A",
      themeColor: "#ffc145",
    },
    midnight: {
      caption: "Midnight dispatch: cobalt water, lit windows, and the same road carrying a different kind of evidence.",
      status: "Midnight dispatch selected.",
      folio: "L-06 / VIEW B",
      themeColor: "#0b1525",
    },
  };

  const root = document.documentElement;
  const themeColor = document.querySelector('meta[name="theme-color"]');
  const menuButton = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector("[data-menu]");
  const menuLabel = menuButton?.querySelector(".menu-toggle-label");
  const dispatchButtons = Array.from(document.querySelectorAll("[data-dispatch-button]"));
  const dispatchCaption = document.querySelector("#dispatch-caption");
  const dispatchStatus = document.querySelector("#dispatch-status");
  const boardFolio = document.querySelector(".board-folio");
  const copyButton = document.querySelector("[data-copy-source]");
  const copyStatus = document.querySelector("#copy-status");
  const sourceUrl = document.querySelector("#source-url");
  const offlineNotice = document.querySelector("#offline-notice");
  const navLinks = Array.from(document.querySelectorAll("[data-nav-link]"));
  const observedSections = navLinks
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);

  root.classList.add("js");

  function readPreference() {
    try {
      const value = window.localStorage.getItem(STORAGE_KEY);
      return value in dispatchCopy ? value : "daylight";
    } catch (_error) {
      return "daylight";
    }
  }

  function savePreference(value) {
    try {
      window.localStorage.setItem(STORAGE_KEY, value);
    } catch (_error) {
      // The visual switch remains functional when storage is unavailable.
    }
  }

  function setDispatch(nextMode, { announce = true, persist = true } = {}) {
    const mode = nextMode in dispatchCopy ? nextMode : "daylight";
    const copy = dispatchCopy[mode];

    root.dataset.dispatch = mode;
    dispatchButtons.forEach((button) => {
      const selected = button.dataset.dispatchButton === mode;
      button.setAttribute("aria-pressed", String(selected));
    });

    if (dispatchCaption) dispatchCaption.textContent = copy.caption;
    if (boardFolio) boardFolio.textContent = copy.folio;
    if (themeColor) themeColor.setAttribute("content", copy.themeColor);
    if (dispatchStatus && announce) dispatchStatus.textContent = copy.status;
    if (persist) savePreference(mode);
  }

  function closeMenu({ restoreFocus = false } = {}) {
    if (!menuButton || !menu) return;
    menuButton.setAttribute("aria-expanded", "false");
    menu.dataset.open = "false";
    if (menuLabel) menuLabel.textContent = "Menu";
    if (restoreFocus) menuButton.focus();
  }

  function openMenu() {
    if (!menuButton || !menu) return;
    menuButton.setAttribute("aria-expanded", "true");
    menu.dataset.open = "true";
    if (menuLabel) menuLabel.textContent = "Close";
    const firstLink = menu.querySelector("a");
    firstLink?.focus();
  }

  function toggleMenu() {
    if (!menuButton) return;
    const isOpen = menuButton.getAttribute("aria-expanded") === "true";
    if (isOpen) closeMenu({ restoreFocus: true });
    else openMenu();
  }

  function updateNetworkStatus() {
    if (!offlineNotice) return;
    offlineNotice.hidden = navigator.onLine;
  }

  function selectSourceAddress() {
    if (!sourceUrl) return;
    const range = document.createRange();
    const selection = window.getSelection();
    range.selectNodeContents(sourceUrl);
    selection?.removeAllRanges();
    selection?.addRange(range);
    sourceUrl.focus();
  }

  function rejectAfter(delay) {
    return new Promise((_, reject) => {
      window.setTimeout(() => reject(new Error("Clipboard request timed out")), delay);
    });
  }

  async function copyOfficialSource() {
    if (!copyButton || !copyStatus) return;

    copyButton.dataset.copyState = "copying";
    copyButton.disabled = true;
    copyButton.textContent = "Copying…";
    copyStatus.textContent = "";
    delete copyStatus.dataset.state;

    try {
      if (!navigator.clipboard?.writeText) throw new Error("Clipboard API unavailable");
      await Promise.race([
        navigator.clipboard.writeText(OFFICIAL_SOURCE),
        rejectAfter(900),
      ]);
      copyStatus.dataset.state = "success";
      copyStatus.textContent = "Official Rockstar address copied.";
      copyButton.textContent = "Source copied";
      copyButton.dataset.copyState = "success";
    } catch (_error) {
      copyStatus.dataset.state = "error";
      copyStatus.textContent = "Copy is unavailable here. The official address is selected below.";
      copyButton.textContent = "Select source link";
      copyButton.dataset.copyState = "error";
      selectSourceAddress();
    } finally {
      copyButton.disabled = false;
    }
  }

  function updateActiveNavigation(sectionId) {
    navLinks.forEach((link) => {
      if (link.getAttribute("href") === `#${sectionId}`) {
        link.setAttribute("aria-current", "location");
      } else {
        link.removeAttribute("aria-current");
      }
    });
  }

  menuButton?.addEventListener("click", toggleMenu);

  menu?.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeMenu();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menuButton?.getAttribute("aria-expanded") === "true") {
      closeMenu({ restoreFocus: true });
    }
  });

  window.addEventListener("resize", () => {
    if (window.matchMedia("(min-width: 901px)").matches) closeMenu();
  });

  dispatchButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
      setDispatch(button.dataset.dispatchButton);
    });

    button.addEventListener("keydown", (event) => {
      if (!["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(event.key)) return;
      event.preventDefault();
      const direction = ["ArrowRight", "ArrowDown"].includes(event.key) ? 1 : -1;
      const nextIndex = (index + direction + dispatchButtons.length) % dispatchButtons.length;
      dispatchButtons[nextIndex].focus();
      setDispatch(dispatchButtons[nextIndex].dataset.dispatchButton);
    });
  });

  copyButton?.addEventListener("click", copyOfficialSource);
  sourceUrl?.addEventListener("click", selectSourceAddress);

  window.addEventListener("online", updateNetworkStatus);
  window.addEventListener("offline", updateNetworkStatus);

  if ("IntersectionObserver" in window && observedSections.length) {
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visible?.target.id) updateActiveNavigation(visible.target.id);
      },
      { rootMargin: "-28% 0px -58%", threshold: [0, 0.15, 0.45] },
    );
    observedSections.forEach((section) => observer.observe(section));
  }

  setDispatch(readPreference(), { announce: false, persist: false });
  updateNetworkStatus();

  window.requestAnimationFrame(() => {
    window.requestAnimationFrame(() => root.classList.add("js-ready"));
  });
})();
