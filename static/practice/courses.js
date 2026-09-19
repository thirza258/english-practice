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

(() => {
  "use strict";

  const transcript = document.getElementById("listening-text");
  if (!transcript || !("speechSynthesis" in window) || !("SpeechSynthesisUtterance" in window)) return;
  const synth = window.speechSynthesis;
  const controls = document.getElementById("listening-controls");
  const play = document.getElementById("listen-play");
  const stop = document.getElementById("listen-stop");
  const speed = document.getElementById("listen-speed");
  const status = document.getElementById("listening-status");
  const text = JSON.parse(transcript.textContent);
  let activeUtterance = null;
  let voice = null;
  controls.hidden = false;

  function updateVoices() {
    const voices = synth.getVoices();
    voice = voices.find((item) => /^en[-_]GB/i.test(item.lang))
      || voices.find((item) => /^en([-_]|$)/i.test(item.lang));
    if (activeUtterance) return;
    play.disabled = !voice;
    status.textContent = voice
      ? "Ready. Listen before opening the transcript."
      : "No English playback voice is available. You can ask a partner to read the transcript aloud, or use the official audio samples below.";
  }

  function finish(message) {
    activeUtterance = null;
    play.disabled = !voice;
    stop.disabled = true;
    speed.disabled = false;
    play.textContent = "Play practice audio";
    status.textContent = message;
  }

  synth.addEventListener("voiceschanged", updateVoices);
  updateVoices();
  play.addEventListener("click", () => {
    if (!voice) return;
    synth.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    activeUtterance = utterance;
    utterance.voice = voice;
    utterance.lang = voice.lang;
    utterance.rate = Number(speed.value);
    play.disabled = true;
    stop.disabled = false;
    speed.disabled = true;
    play.textContent = "Playing…";
    status.textContent = "Listening in progress. Take notes as you listen.";
    utterance.onend = () => {
      if (activeUtterance === utterance) finish("Audio finished. Answer the questions, then use the transcript to review.");
    };
    utterance.onerror = () => {
      if (activeUtterance === utterance) finish("Playback is unavailable. Try again, ask a partner to read the transcript, or use the official audio samples.");
    };
    try {
      synth.speak(utterance);
    } catch (_) {
      finish("Playback is unavailable. Use the transcript with a partner or try the official audio samples.");
    }
  });
  stop.addEventListener("click", () => {
    finish("Audio stopped. Select play to listen from the beginning.");
    synth.cancel();
  });
  window.addEventListener("pagehide", () => {
    activeUtterance = null;
    synth.cancel();
  });
  window.addEventListener("pageshow", () => {
    if (!activeUtterance) finish("Ready. Listen before opening the transcript.");
    updateVoices();
  });
})();

(() => {
  "use strict";

  const timer = document.getElementById("speaking-timer");
  if (!timer) return;
  const display = document.getElementById("timer-display");
  const phase = document.getElementById("timer-phase");
  const start = document.getElementById("timer-start");
  const reset = document.getElementById("timer-reset");
  const status = document.getElementById("timer-status");
  const initialHelp = status.textContent;
  const preparation = Number(timer.dataset.preparation);
  const stages = [
    ...(preparation ? [{ label: "Prepare with keywords", ms: preparation * 1000 }] : []),
    { label: "Speak aloud", ms: Number(timer.dataset.seconds) * 1000 },
  ];
  let stage = 0;
  let remaining = stages[0].ms;
  let deadline = 0;
  let interval = null;
  let state = "ready";
  timer.hidden = false;

  function draw() {
    const seconds = Math.max(0, Math.ceil(remaining / 1000));
    display.textContent = `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
  }

  function tick() {
    // A deadline keeps the countdown accurate when a background tab throttles callbacks.
    remaining = deadline - Date.now();
    while (remaining <= 0 && state === "running") {
      stage += 1;
      if (stage === stages.length) {
        clearInterval(interval);
        interval = null;
        remaining = 0;
        state = "done";
        phase.textContent = "Practice finished";
        status.textContent = "Time is up. Review your speaking with the checklist and save your reflection below.";
        start.textContent = "Practise again";
      } else {
        deadline += stages[stage].ms;
        remaining = deadline - Date.now();
        phase.textContent = stages[stage].label;
        status.textContent = "Preparation is over. Start speaking aloud now.";
      }
    }
    draw();
  }

  start.addEventListener("click", () => {
    if (state === "running") {
      tick();
      if (state === "done") return;
      clearInterval(interval);
      interval = null;
      state = "paused";
      start.textContent = "Resume";
      phase.textContent = `${stages[stage].label} · paused`;
      status.textContent = "Timer paused. Resume when you are ready.";
      return;
    }
    if (state === "done") {
      stage = 0;
      remaining = stages[0].ms;
    }
    state = "running";
    deadline = Date.now() + remaining;
    phase.textContent = stages[stage].label;
    status.textContent = stage === 0 && preparation ? "Use this time to make brief keyword notes." : "Speak aloud and develop your answer.";
    start.textContent = "Pause";
    interval = setInterval(tick, 200);
    tick();
  });
  reset.addEventListener("click", () => {
    clearInterval(interval);
    interval = null;
    stage = 0;
    remaining = stages[0].ms;
    state = "ready";
    phase.textContent = "Ready to practise";
    start.textContent = "Start practice timer";
    status.textContent = initialHelp;
    draw();
  });
  window.addEventListener("pagehide", () => {
    if (state === "running") start.click();
  });
  draw();
})();
