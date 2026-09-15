(() => {
  "use strict";

  const form = document.getElementById("lesson-form");
  if (!form) return;

  const draft = form.elements.namedItem("draft");
  const reviewed = form.elements.namedItem("reviewed");
  const counter = document.getElementById("draft-count");
  const status = document.getElementById("draft-status");
  const edits = document.getElementById("practice-edits");
  const key = form.dataset.draftKey;
  const minimum = Number(form.dataset.minWords);
  const submittedDraft = draft.value;
  let storageAvailable = true;

  function updateCount() {
    const count = (draft.value.match(/[A-Za-z][A-Za-z'’\-]*/g) || []).length;
    counter.textContent = `${count} / ${minimum} words minimum`;
    counter.classList.toggle("writing-minimum-met", count >= minimum);
  }

  function saveDraft() {
    try {
      localStorage.setItem(key, draft.value);
      storageAvailable = true;
    } catch (_) {
      storageAvailable = false;
    }
    status.textContent = storageAvailable
      ? "Draft saved on this device. Submit to update your progress."
      : "Draft autosave is unavailable. Submit to save your work.";
  }

  try {
    const localDraft = localStorage.getItem(key);
    if (localDraft !== null && localDraft.trim() !== submittedDraft.trim()) {
      draft.value = localDraft.slice(0, draft.maxLength);
      reviewed.checked = false;
      status.textContent = "Your unsubmitted draft was restored from this device.";
      edits.hidden = false;
    } else if (localDraft !== null) {
      localStorage.removeItem(key);
    }
  } catch (_) {
    storageAvailable = false;
    status.textContent = "Draft autosave is unavailable. Submit to save your work.";
  }

  draft.addEventListener("input", () => {
    reviewed.checked = false;
    updateCount();
    saveDraft();
  });
  form.addEventListener("input", () => { edits.hidden = false; });
  form.addEventListener("submit", saveDraft);
  window.addEventListener("beforeunload", (event) => {
    if (!storageAvailable && draft.value !== submittedDraft) {
      event.preventDefault();
      event.returnValue = "";
    }
  });
  // A deliberate submission saves through Django even when local storage is blocked.
  form.addEventListener("submit", () => { storageAvailable = true; });
  updateCount();

  if (location.hash === "#lesson-feedback") {
    document.getElementById("lesson-feedback")?.focus();
  }
})();
