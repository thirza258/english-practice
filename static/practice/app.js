(() => {
  const config = window.APP_CONFIG || {};
  const apiRoot = config.apiRoot || "/api/tests/";

  function readJsonScript(id) {
    const node = document.getElementById(id);
    if (!node) {
      return null;
    }
    try {
      return JSON.parse(node.textContent || "null");
    } catch {
      return null;
    }
  }

  const initialState = readJsonScript("initial-state-data");
  const initialResults = readJsonScript("initial-results-data");

  const els = {
    testScreen: document.getElementById("testScreen"),
    resultsScreen: document.getElementById("resultsScreen"),
    retryTestButton: document.getElementById("retryTestButton"),
    submitAnswerButton: document.getElementById("submitAnswerButton"),
    nextQuestionButton: document.getElementById("nextQuestionButton"),
    questionCounter: document.getElementById("questionCounter"),
    scoreCounter: document.getElementById("scoreCounter"),
    progressLabel: document.getElementById("progressLabel"),
    progressBar: document.getElementById("progressBar"),
    modePill: document.getElementById("modePill"),
    levelPill: document.getElementById("levelPill"),
    testPageTitle: document.getElementById("testPageTitle"),
    testPageSubtitle: document.getElementById("testPageSubtitle"),
    sideCardEyebrow: document.getElementById("sideCardEyebrow"),
    sideCardList: document.getElementById("sideCardList"),
    questionPanel: document.getElementById("questionPanel"),
    feedbackPanel: document.getElementById("feedbackPanel"),
    resultsSummary: document.getElementById("resultsSummary"),
    topicSummary: document.getElementById("topicSummary"),
    questionReview: document.getElementById("questionReview"),
    loadingOverlay: document.getElementById("loadingOverlay"),
    loadingMessage: document.getElementById("loadingMessage"),
    errorBanner: document.getElementById("errorBanner"),
  };

  const state = {
    mode: config.requestedMode || "sentence",
    level: config.requestedLevel || "all",
    testId: null,
    score: 0,
    totalQuestions: 10,
    totalParagraphs: 3,
    currentQuestion: null,
    pendingQuestion: null,
    feedback: null,
    results: null,
    selectedAnswer: null,
    selectedAnswers: {}, // for paragraph mode: { "1": "A", "2": "C", ... }
    activeBlankId: 1,
    essay: "", // for writing mode
    totalTasks: 1,
    busy: false,
  };

  function levelDisplayName(level) {
    switch ((level || "").toLowerCase()) {
      case "beginner":
        return "Beginner (A1-A2)";
      case "intermediate":
        return "Intermediate (B1-B2)";
      case "advanced":
        return "Advanced (C1-C2)";
      case "ielts_8_9":
      case "ielts":
        return "IELTS Band 8.0 – 9.0";
      case "all":
      default:
        return "All Levels (A1-C2 & IELTS)";
    }
  }

  function modeDisplayName(mode) {
    if (mode === "paragraph") {
      return "Paragraph Builder";
    }
    if (mode === "writing") {
      return "IELTS Writing";
    }
    return "Sentence Diagnostic";
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function setScreen(screenMode) {
    els.testScreen.classList.toggle("screen-active", screenMode === "question" || screenMode === "feedback");
    els.resultsScreen.classList.toggle("screen-active", screenMode === "results");
    els.testScreen.classList.toggle("hidden", screenMode === "results");
    els.resultsScreen.classList.toggle("hidden", screenMode !== "results");
  }

  function setLoading(active, message = "Preparing your diagnostic...") {
    state.busy = active;
    els.loadingMessage.textContent = message;
    els.loadingOverlay.classList.toggle("hidden", !active);

    let canSubmit = false;
    if (state.mode === "writing") {
      canSubmit = countWords(state.essay) >= MIN_SUBMIT_WORDS;
    } else if (state.mode === "paragraph" && state.currentQuestion?.blanks) {
      canSubmit = state.currentQuestion.blanks.every((b) => state.selectedAnswers[b.blank_id]);
    } else {
      canSubmit = Boolean(state.selectedAnswer);
    }

    els.submitAnswerButton.disabled = active || !canSubmit;
    els.nextQuestionButton.disabled = active;
    els.retryTestButton.disabled = active;
  }

  function showError(message) {
    els.errorBanner.textContent = message;
    els.errorBanner.classList.remove("hidden");
    window.clearTimeout(showError.timeoutId);
    showError.timeoutId = window.setTimeout(() => {
      els.errorBanner.classList.add("hidden");
    }, 4200);
  }

  function hideError() {
    els.errorBanner.classList.add("hidden");
  }

  async function requestJson(url, options = {}) {
    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        ...(options.headers || {}),
      },
      ...options,
    });

    let data = null;
    try {
      data = await response.json();
    } catch {
      data = null;
    }

    if (!response.ok || (data && data.ok === false)) {
      const message = data?.error || `Request failed with status ${response.status}.`;
      throw new Error(message);
    }

    return data;
  }

  function progressPercent(current, total) {
    if (!total) {
      return 0;
    }
    return Math.max(0, Math.min(100, Math.round((current / total) * 100)));
  }

  function renderHeader() {
    if (els.modePill) {
      els.modePill.textContent = `Mode: ${modeDisplayName(state.mode)}`;
    }
    if (els.levelPill) {
      els.levelPill.textContent = `Level: ${levelDisplayName(state.level)}`;
    }

    if (state.mode === "writing") {
      if (els.testPageTitle) {
        els.testPageTitle.textContent = "IELTS Writing Practice";
      }
      if (els.testPageSubtitle) {
        els.testPageSubtitle.textContent =
          "Write your response, then receive band scores for vocabulary range, structure, cohesion, and accuracy.";
      }
      if (els.sideCardEyebrow) {
        els.sideCardEyebrow.textContent = "How Writing Practice Works";
      }
      if (els.sideCardList) {
        els.sideCardList.innerHTML = `
          <li>Plan a paragraph for each part of the question before you start writing.</li>
          <li>Open every paragraph with a topic sentence, then develop it with a reason or example.</li>
          <li>Vary your vocabulary and mix simple, compound, and complex sentences.</li>
          <li>Your draft is saved in this browser until you submit it.</li>
        `;
      }
    } else if (state.mode === "paragraph") {
      if (els.testPageTitle) {
        els.testPageTitle.textContent = "Paragraph Cloze Practice";
      }
      if (els.testPageSubtitle) {
        els.testPageSubtitle.textContent = "Fill in each blank to build a cohesive paragraph. Rules and topics appear after submission.";
      }
      if (els.sideCardEyebrow) {
        els.sideCardEyebrow.textContent = "Paragraph Building Tips";
      }
      if (els.sideCardList) {
        els.sideCardList.innerHTML = `
          <li>Read the entire passage before choosing options to understand the flow.</li>
          <li>Click any blank in the paragraph or its tab below to select answers.</li>
          <li>Look for transitions, pronoun antecedents, and clause relationships.</li>
          <li>Submit when all blanks are filled to reveal paragraph cohesion insights.</li>
        `;
      }
    } else {
      if (els.testPageTitle) {
        els.testPageTitle.textContent = "Sentence Diagnostic";
      }
      if (els.testPageSubtitle) {
        els.testPageSubtitle.textContent = "Answer carefully. The topic and grammar rules appear only after submission.";
      }
      if (els.sideCardEyebrow) {
        els.sideCardEyebrow.textContent = "How Sentence Practice Works";
      }
      if (els.sideCardList) {
        els.sideCardList.innerHTML = `
          <li>Read the sentence and choose the best completion.</li>
          <li>The grammar topic appears only after you submit.</li>
          <li>Review the rule, explanation, and sentence rewrite after each answer.</li>
          <li>At the end, review topic accuracy and weak areas.</li>
        `;
      }
    }

    if (!state.currentQuestion) {
      return;
    }

    if (state.mode === "writing") {
      const currentTask = state.currentQuestion.task_number || 1;
      const totalTasks = state.totalTasks || 1;
      const progress = progressPercent(currentTask - 1, totalTasks);

      els.questionCounter.textContent = `Writing task ${currentTask} of ${totalTasks}`;
      els.scoreCounter.textContent = state.currentQuestion.title || "IELTS Writing";
      els.progressLabel.textContent = `${progress}%`;
      els.progressBar.style.width = `${progress}%`;
      return;
    }

    const isParagraph = state.mode === "paragraph";
    if (isParagraph) {
      const currentP = state.currentQuestion.paragraph_number || 1;
      const totalP = state.totalParagraphs || 3;
      const blanksCount = state.currentQuestion.blanks ? state.currentQuestion.blanks.length : 3;

      els.questionCounter.textContent = `Paragraph ${currentP} of ${totalP} (${blanksCount} Blanks)`;
      els.scoreCounter.textContent = `Score: ${state.score} / ${state.totalQuestions} Blanks`;
      const progress = progressPercent(currentP - 1, totalP);
      els.progressLabel.textContent = `${progress}%`;
      els.progressBar.style.width = `${progress}%`;
    } else {
      const currentQ = state.currentQuestion.question_number || 1;
      const totalQ = state.totalQuestions || 10;

      els.questionCounter.textContent = `Question ${currentQ} of ${totalQ}`;
      els.scoreCounter.textContent = `Score: ${state.score} / ${totalQ}`;
      const progress = progressPercent(currentQ - 1, totalQ);
      els.progressLabel.textContent = `${progress}%`;
      els.progressBar.style.width = `${progress}%`;
    }
  }

  // ---------------------------------------------------------------------------
  // SENTENCE MODE QUESTION RENDERING
  // ---------------------------------------------------------------------------
  function renderSentenceQuestion() {
    els.submitAnswerButton.textContent = "Submit Answer";
    els.submitAnswerButton.disabled = !state.selectedAnswer || state.busy;

    const optionsHtml = state.currentQuestion.options
      .map((option) => {
        const isSelected = state.selectedAnswer === option.label;
        const className = `option-button ${isSelected ? "is-selected" : ""}`;
        return `
          <button
            type="button"
            class="${className}"
            data-action="choose-sentence-answer"
            data-letter="${escapeHtml(option.label)}"
            aria-pressed="${isSelected ? "true" : "false"}"
          >
            <span class="option-letter">${escapeHtml(option.label)}</span>
            <span class="option-text">${escapeHtml(option.text)}</span>
          </button>
        `;
      })
      .join("");

    els.questionPanel.innerHTML = `
      <div class="prompt-card">
        <h3>${escapeHtml(state.currentQuestion.question)}</h3>
        <p class="hidden-topic-note">The grammar topic and rule are hidden until you submit your answer.</p>
        <div class="option-list">
          ${optionsHtml}
        </div>
      </div>
    `;
  }

  // ---------------------------------------------------------------------------
  // PARAGRAPH MODE QUESTION RENDERING
  // ---------------------------------------------------------------------------
  function renderParagraphQuestion() {
    els.submitAnswerButton.textContent = "Submit Paragraph";
    const blanks = state.currentQuestion.blanks || [];
    const allFilled = blanks.length > 0 && blanks.every((b) => state.selectedAnswers[b.blank_id]);
    els.submitAnswerButton.disabled = !allFilled || state.busy;

    // Replace [1], [2], [3] in paragraph text with interactive blank pills
    let paragraphHtml = escapeHtml(state.currentQuestion.text_with_blanks);
    blanks.forEach((b) => {
      const selectedLetter = state.selectedAnswers[b.blank_id];
      const selectedOption = selectedLetter ? b.options.find((o) => o.label === selectedLetter) : null;
      const displayText = selectedOption ? `${selectedLetter}. ${selectedOption.text}` : `[ Blank ${b.blank_id} ]`;
      const isFilled = Boolean(selectedLetter);
      const isActive = b.blank_id === state.activeBlankId;

      const blankPill = `
        <span
          class="paragraph-blank-pill ${isFilled ? "is-filled" : "is-empty"} ${isActive ? "is-active" : ""}"
          data-action="select-blank-tab"
          data-blank-id="${b.blank_id}"
          role="button"
          tabindex="0"
          title="Click to select answer for Blank ${b.blank_id}"
        >${escapeHtml(displayText)}</span>
      `;
      paragraphHtml = paragraphHtml.replace(`[${b.blank_id}]`, blankPill);
    });

    // Blank tabs
    const blankTabsHtml = blanks
      .map((b) => {
        const selectedLetter = state.selectedAnswers[b.blank_id];
        const isActive = b.blank_id === state.activeBlankId;
        const isFilled = Boolean(selectedLetter);
        return `
          <button
            type="button"
            class="blank-nav-tab ${isActive ? "is-active" : ""} ${isFilled ? "is-filled" : ""}"
            data-action="select-blank-tab"
            data-blank-id="${b.blank_id}"
          >
            <span class="tab-number">${b.blank_id}</span>
            <span class="tab-title">Blank ${b.blank_id}</span>
            ${selectedLetter ? `<span class="tab-selection">(${escapeHtml(selectedLetter)})</span>` : ""}
          </button>
        `;
      })
      .join("");

    // Active blank choices
    const activeBlank = blanks.find((b) => b.blank_id === state.activeBlankId) || blanks[0];
    const currentSelectedLetter = activeBlank ? state.selectedAnswers[activeBlank.blank_id] : null;

    let activeBlankOptionsHtml = "";
    if (activeBlank) {
      activeBlankOptionsHtml = activeBlank.options
        .map((option) => {
          const isSelected = currentSelectedLetter === option.label;
          const className = `option-button ${isSelected ? "is-selected" : ""}`;
          return `
            <button
              type="button"
              class="${className}"
              data-action="choose-paragraph-blank-answer"
              data-blank-id="${activeBlank.blank_id}"
              data-letter="${escapeHtml(option.label)}"
              aria-pressed="${isSelected ? "true" : "false"}"
            >
              <span class="option-letter">${escapeHtml(option.label)}</span>
              <span class="option-text">${escapeHtml(option.text)}</span>
            </button>
          `;
        })
        .join("");
    }

    els.questionPanel.innerHTML = `
      <div class="paragraph-exercise-card">
        <div class="paragraph-card-head">
          <span class="badge paragraph-badge">Paragraph Builder</span>
          <h3 class="paragraph-title">${escapeHtml(state.currentQuestion.title || "Paragraph Cloze Passage")}</h3>
        </div>

        <div class="paragraph-passage-box">
          <p class="paragraph-passage-text">${paragraphHtml}</p>
        </div>

        <div class="blanks-picker-container">
          <div class="blank-nav-tabs">
            ${blankTabsHtml}
          </div>

          <div class="active-blank-box">
            <div class="active-blank-head">
              <span class="eyebrow">Options for Blank [ ${activeBlank ? activeBlank.blank_id : 1} ]</span>
              <span class="active-blank-status">${currentSelectedLetter ? `Selected: Choice ${currentSelectedLetter}` : "Select the best option:"}</span>
            </div>
            <div class="option-list">
              ${activeBlankOptionsHtml}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  // ---------------------------------------------------------------------------
  // WRITING MODE RENDERING
  // ---------------------------------------------------------------------------
  const MIN_SUBMIT_WORDS = 25;
  const WORD_PATTERN = /[A-Za-z][A-Za-z'’-]*/g;

  function countWords(text) {
    return (String(text || "").match(WORD_PATTERN) || []).length;
  }

  function countSentences(text) {
    const trimmed = String(text || "").trim();
    if (!trimmed) {
      return 0;
    }
    return trimmed.split(/[.!?]+(?:\s|$)/).filter((part) => part.trim()).length;
  }

  function countParagraphs(text) {
    const trimmed = String(text || "").trim();
    if (!trimmed) {
      return 0;
    }
    return trimmed.split(/\n\s*\n+/).filter((part) => part.trim()).length;
  }

  function taskTypeLabel(taskType) {
    switch (taskType) {
      case "opinion":
        return "Opinion essay";
      case "discussion":
        return "Discussion essay";
      case "advantages_disadvantages":
        return "Advantages & disadvantages";
      case "problem_solution":
        return "Problem & solution";
      case "descriptive":
        return "Descriptive writing";
      case "narrative":
        return "Narrative writing";
      default:
        return "Writing task";
    }
  }

  // Drafts survive an accidental reload; storage may be unavailable, so every
  // access is guarded.
  function draftKey() {
    return `english-practice:draft:${state.testId || "new"}:${state.currentQuestion?.id || "w1"}`;
  }

  function loadDraft() {
    try {
      return window.localStorage.getItem(draftKey()) || "";
    } catch {
      return "";
    }
  }

  function saveDraft(text) {
    try {
      window.localStorage.setItem(draftKey(), text);
    } catch {
      /* storage unavailable */
    }
  }

  function clearDraft() {
    try {
      window.localStorage.removeItem(draftKey());
    } catch {
      /* storage unavailable */
    }
  }

  function renderWritingTask() {
    const task = state.currentQuestion;
    els.submitAnswerButton.textContent = "Submit for IELTS review";

    if (!state.essay) {
      state.essay = loadDraft();
    }

    const guidanceHtml = (task.guidance || []).map((tip) => `<li>${escapeHtml(tip)}</li>`).join("");

    els.questionPanel.innerHTML = `
      <div class="writing-task-card">
        <div class="writing-task-head">
          <span class="badge writing-badge">IELTS Writing</span>
          <span class="chip topic">${escapeHtml(taskTypeLabel(task.task_type))}</span>
          <span class="chip level">${escapeHtml(levelDisplayName(task.level))}</span>
        </div>
        <h3 class="writing-title">${escapeHtml(task.title)}</h3>
        <p class="writing-prompt">${escapeHtml(task.prompt)}</p>
        <div class="writing-guidance">
          <p class="eyebrow">How to approach it</p>
          <ul>${guidanceHtml}</ul>
        </div>
        <p class="writing-requirements">
          Minimum <strong>${escapeHtml(task.min_words)} words</strong> &middot;
          suggested time <strong>${escapeHtml(task.suggested_minutes)} minutes</strong>
        </p>
      </div>

      <div class="writing-composer">
        <label class="eyebrow" for="essayInput">Your response</label>
        <textarea
          id="essayInput"
          class="essay-input"
          rows="16"
          spellcheck="true"
          placeholder="Plan for a minute, then write your response here. Leave a blank line between paragraphs."
        >${escapeHtml(state.essay)}</textarea>
        <div class="essay-stats" id="essayStats"></div>
        <div class="progress-track writing-progress" aria-hidden="true">
          <div id="essayProgressBar" class="progress-bar" style="width: 0%"></div>
        </div>
        <p class="writing-note">
          Length, vocabulary range, sentence structure, and cohesion are measured on the server with
          NLTK and spaCy. Only your finished response and a one-line statistics summary are sent for
          band scoring, which keeps the review cheap.
        </p>
      </div>
    `;

    updateEssayStats();
  }

  function updateEssayStats() {
    const task = state.currentQuestion;
    const statsNode = document.getElementById("essayStats");
    const barNode = document.getElementById("essayProgressBar");
    if (!task || !statsNode) {
      return;
    }

    const words = countWords(state.essay);
    const minWords = Number(task.min_words) || 250;
    const reached = words >= minWords;
    const remaining = Math.max(0, minWords - words);

    statsNode.innerHTML = `
      <span class="stat-chip ${reached ? "is-reached" : ""}">${words} / ${minWords} words</span>
      <span class="stat-chip">${countSentences(state.essay)} sentences</span>
      <span class="stat-chip">${countParagraphs(state.essay)} paragraphs</span>
      ${
        reached
          ? `<span class="stat-chip is-reached">Length requirement met</span>`
          : `<span class="stat-chip is-pending">${remaining} more words needed</span>`
      }
    `;

    if (barNode) {
      barNode.style.width = `${Math.min(100, Math.round((words / minWords) * 100))}%`;
    }

    els.submitAnswerButton.disabled = state.busy || words < MIN_SUBMIT_WORDS;
  }

  function band(value) {
    return Number(value || 0).toFixed(1);
  }

  function percent(value) {
    return `${Math.round((Number(value) || 0) * 100)}%`;
  }

  function listSection(title, items, className) {
    if (!items || !items.length) {
      return "";
    }
    const rows = items.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
    return `
      <div class="report-block ${className}">
        <p class="eyebrow">${escapeHtml(title)}</p>
        <ul class="report-list">${rows}</ul>
      </div>
    `;
  }

  function writingReportHtml(report) {
    const metrics = report.metrics || {};
    const byExaminer = report.assessed_by === "examiner";

    const criteriaHtml = (report.criteria || [])
      .map(
        (criterion) => `
          <article class="criterion-card">
            <div class="criterion-head">
              <span class="criterion-label">${escapeHtml(criterion.label)}</span>
              <span class="criterion-band">${band(criterion.band)}</span>
            </div>
            <p class="criterion-comment">${escapeHtml(criterion.comment)}</p>
            <p class="criterion-measured">Measured estimate ${band(criterion.measured_band)}</p>
          </article>
        `,
      )
      .join("");

    const notesHtml = (report.notes || []).length
      ? `<div class="report-notes">${(report.notes || [])
          .map((note) => `<p>${escapeHtml(note)}</p>`)
          .join("")}</div>`
      : "";

    const correctionsHtml = (report.corrections || []).length
      ? `
        <div class="report-block">
          <p class="eyebrow">Corrections</p>
          <div class="corrections-grid">
            ${(report.corrections || [])
              .map(
                (fix) => `
                  <div class="correction-card">
                    <p class="correction-original">${escapeHtml(fix.original)}</p>
                    <p class="correction-fixed">${escapeHtml(fix.corrected)}</p>
                    ${fix.why ? `<p class="correction-why">${escapeHtml(fix.why)}</p>` : ""}
                  </div>
                `,
              )
              .join("")}
          </div>
        </div>
      `
      : "";

    const upgradesHtml = (report.vocabulary_upgrades || []).length
      ? `
        <div class="report-block">
          <p class="eyebrow">Wider vocabulary</p>
          <table class="upgrade-table">
            <thead>
              <tr><th>You wrote</th><th>Stronger alternatives</th><th>Source</th></tr>
            </thead>
            <tbody>
              ${(report.vocabulary_upgrades || [])
                .map(
                  (item) => `
                    <tr>
                      <td>${escapeHtml(item.basic)}${
                        item.count ? ` <span class="upgrade-count">&times;${escapeHtml(item.count)}</span>` : ""
                      }</td>
                      <td>${escapeHtml(item.stronger)}</td>
                      <td><span class="chip ${item.source === "examiner" ? "topic" : "level"}">${escapeHtml(
                        item.source === "examiner" ? "examiner" : "measured",
                      )}</span></td>
                    </tr>
                  `,
                )
                .join("")}
            </tbody>
          </table>
        </div>
      `
      : "";

    const metricChips = [
      ["Words", metrics.word_count],
      ["Sentences", metrics.sentence_count],
      ["Paragraphs", metrics.paragraph_count],
      ["Different words", metrics.unique_words],
      ["Beyond core vocabulary", percent(metrics.beyond_core_ratio)],
      ["Academic words", (metrics.academic_words_used || []).length],
      ["Complex sentences", percent(metrics.complex_sentence_ratio)],
      ["Average sentence", `${metrics.average_sentence_length || 0} words`],
      ["Length variation", metrics.sentence_length_sd],
      ["Passive forms", metrics.passive_count],
    ]
      .map(
        ([label, value]) => `
          <div class="metric-chip">
            <span>${escapeHtml(label)}</span>
            <strong>${escapeHtml(value === undefined || value === null ? "0" : value)}</strong>
          </div>
        `,
      )
      .join("");

    const linkerGroups = Object.entries(metrics.linkers_by_group || {});
    const linkersHtml = linkerGroups.length
      ? `<ul class="report-list">${linkerGroups
          .map(
            ([group, phrases]) =>
              `<li><strong>${escapeHtml(group)}:</strong> ${escapeHtml((phrases || []).join(", "))}</li>`,
          )
          .join("")}</ul>`
      : `<p class="report-empty">No cohesive devices were detected. Linking words such as however,
         therefore, and for instance guide the reader between ideas.</p>`;

    const academicHtml = (metrics.academic_words_used || []).length
      ? `<div class="word-chip-row">${(metrics.academic_words_used || [])
          .map((word) => `<span class="word-chip">${escapeHtml(word)}</span>`)
          .join("")}</div>`
      : `<p class="report-empty">No academic vocabulary was detected in this response.</p>`;

    const repeatedHtml = (metrics.overused_words || []).length
      ? `<div class="word-chip-row">${(metrics.overused_words || [])
          .map(
            (item) =>
              `<span class="word-chip is-warning">${escapeHtml(item.word)} &times;${escapeHtml(item.count)}</span>`,
          )
          .join("")}</div>`
      : `<p class="report-empty">No word is over-repeated.</p>`;

    const mechanicsHtml = (metrics.mechanics_issues || []).length
      ? `<ul class="report-list">${(metrics.mechanics_issues || [])
          .map((issue) => `<li>${escapeHtml(issue)}</li>`)
          .join("")}</ul>`
      : `<p class="report-empty">Punctuation, spacing, and capitalisation are clean.</p>`;

    const revealed = report.revealed || {};
    const revealedVocab = (revealed.useful_vocabulary || []).length
      ? `<div class="word-chip-row">${(revealed.useful_vocabulary || [])
          .map((word) => `<span class="word-chip is-target">${escapeHtml(word)}</span>`)
          .join("")}</div>`
      : "";

    const usage = report.usage || {};
    const usageLine =
      byExaminer && usage.total_tokens
        ? `<span class="report-meta-item">${escapeHtml(usage.total_tokens)} tokens used</span>`
        : "";

    return `
      <div class="writing-report">
        <div class="band-hero">
          <div class="band-hero-score">
            <span class="band-value">${band(report.overall_band)}</span>
            <span class="band-scale">/ 9.0</span>
          </div>
          <div class="band-hero-copy">
            <p class="eyebrow">Estimated IELTS band</p>
            <h3>${escapeHtml(report.title || "Writing report")}</h3>
            <div class="report-meta">
              <span class="report-meta-item">${escapeHtml(
                byExaminer ? "Examiner review + local analysis" : "Local analysis only",
              )}</span>
              <span class="report-meta-item">${escapeHtml(metrics.analyzer || "regex")}</span>
              ${usageLine}
            </div>
          </div>
        </div>

        ${notesHtml}

        <div class="criteria-grid">${criteriaHtml}</div>

        <div class="report-columns">
          ${listSection("What works", report.strengths, "is-positive")}
          ${listSection("What to improve", report.improvements, "is-negative")}
        </div>

        ${listSection("Also measured", report.measured_observations, "is-neutral")}
        ${correctionsHtml}
        ${upgradesHtml}

        <div class="report-block">
          <p class="eyebrow">Measured analysis</p>
          <div class="metric-grid">${metricChips}</div>
          <div class="report-subblock">
            <p class="report-subtitle">Cohesive devices used</p>
            ${linkersHtml}
          </div>
          <div class="report-subblock">
            <p class="report-subtitle">Academic vocabulary detected</p>
            ${academicHtml}
          </div>
          <div class="report-subblock">
            <p class="report-subtitle">Repetition</p>
            ${repeatedHtml}
          </div>
          <div class="report-subblock">
            <p class="report-subtitle">Mechanics</p>
            ${mechanicsHtml}
          </div>
        </div>

        ${
          revealed.model_outline
            ? `
          <div class="report-block is-revealed">
            <p class="eyebrow">Suggested paragraph plan</p>
            <p>${escapeHtml(revealed.model_outline)}</p>
            ${revealedVocab ? `<p class="report-subtitle">Target vocabulary for this task</p>${revealedVocab}` : ""}
          </div>
        `
            : ""
        }

        <div class="report-block">
          <p class="eyebrow">Your response</p>
          <div class="submitted-essay">${escapeHtml(report.essay || "")}</div>
        </div>
      </div>
    `;
  }

  function renderWritingFeedback() {
    els.feedbackPanel.innerHTML = writingReportHtml(state.feedback);
  }

  function renderWritingResults() {
    const results = state.results;
    const currentLevel = results.level || state.level;

    document.querySelectorAll(".mode-tab-btn").forEach((btn) => {
      btn.classList.toggle("is-active", btn.dataset.mode === "writing");
    });
    document.querySelectorAll(".level-tab-btn").forEach((btn) => {
      btn.classList.toggle("is-active", btn.dataset.level === currentLevel);
    });

    els.resultsSummary.innerHTML = [
      ["Mode", modeDisplayName("writing")],
      ["Level", levelDisplayName(currentLevel)],
      ["Overall band", band(results.overall_band)],
      ["Tasks completed", `${results.total_tasks || 1}`],
    ]
      .map(
        ([label, value]) => `
          <div class="summary-card">
            <span>${escapeHtml(label)}</span>
            <strong>${escapeHtml(value)}</strong>
          </div>
        `,
      )
      .join("");

    els.topicSummary.innerHTML = `
      <table>
        <thead>
          <tr><th>Assessment criterion</th><th>Band</th></tr>
        </thead>
        <tbody>
          ${(results.criteria_summary || [])
            .map(
              (criterion) =>
                `<tr><td>${escapeHtml(criterion.label)}</td><td>${band(criterion.band)}</td></tr>`,
            )
            .join("")}
        </tbody>
      </table>
    `;

    els.questionReview.innerHTML = (results.tasks || [])
      .map(
        (report) => `<article class="review-card writing-review-card">${writingReportHtml(report)}</article>`,
      )
      .join("");

    setScreen("results");
    setLoading(false);
  }

  function renderQuestion() {
    if (!state.currentQuestion) {
      return;
    }

    els.feedbackPanel.classList.add("hidden");
    els.feedbackPanel.innerHTML = "";
    els.nextQuestionButton.classList.add("hidden");
    els.submitAnswerButton.classList.remove("hidden");

    renderHeader();
    setScreen("question");

    if (state.mode === "writing") {
      renderWritingTask();
    } else if (state.mode === "paragraph") {
      renderParagraphQuestion();
    } else {
      renderSentenceQuestion();
    }
  }

  // ---------------------------------------------------------------------------
  // FEEDBACK RENDERING
  // ---------------------------------------------------------------------------
  function renderSentenceFeedback() {
    const feedback = state.feedback;
    const isCorrect = Boolean(feedback.is_correct);
    const headlineClass = isCorrect ? "is-correct" : "is-wrong";
    const itemLevel = feedback.level || state.level;
    const reasonRight = feedback.reason_right || (isCorrect ? feedback.explanation : "-");
    const reasonWrong = feedback.reason_wrong || (!isCorrect ? (feedback.selected_answer_explanation || (feedback.rule ? `${(feedback.selected_answer || "").split(". ")[1] || feedback.selected_answer} does not fit because ${feedback.rule[0].toLowerCase() + feedback.rule.slice(1)}` : "-")) : "-");

    els.feedbackPanel.innerHTML = `
      <div class="chip-row">
        <span class="chip topic">Topic: ${escapeHtml(feedback.grammar_topic)}</span>
        <span class="chip level">Level: ${escapeHtml(levelDisplayName(itemLevel))}</span>
        <span class="chip ${isCorrect ? "correct" : "wrong"}">${escapeHtml(feedback.headline)}</span>
      </div>
      <p class="feedback-headline ${headlineClass}">${escapeHtml(feedback.headline)}</p>
      <div class="feedback-grid">
        <p class="feedback-line"><strong>Correct answer:</strong> ${escapeHtml(feedback.correct_answer)}</p>
        <p class="feedback-line"><strong>Your answer:</strong> ${escapeHtml(feedback.selected_answer)}</p>
        <p class="feedback-line"><strong>Grammar rule:</strong> ${escapeHtml(feedback.rule)}</p>
        <p class="feedback-line"><strong>Reason you were right:</strong> ${escapeHtml(reasonRight)}</p>
        <p class="feedback-line"><strong>Reason you were wrong:</strong> ${escapeHtml(reasonWrong)}</p>
        <p class="feedback-line"><strong>Sentence:</strong> ${escapeHtml(feedback.sentence_explanation)}</p>
      </div>
    `;
  }

  function renderParagraphFeedback() {
    const feedback = state.feedback;
    const allCorrect = feedback.all_correct;
    const headlineClass = allCorrect ? "is-correct" : "is-partial";
    const itemLevel = feedback.level || state.level;

    const blanksReviewHtml = (feedback.blanks_feedback || [])
      .map((b) => {
        const isCorr = Boolean(b.is_correct);
        const reasonRight = b.reason_right || (isCorr ? b.explanation : "-");
        const reasonWrong = b.reason_wrong || (!isCorr ? (b.rule ? `${(b.selected_answer || "").split(". ")[1] || b.selected_answer} does not fit because ${b.rule[0].toLowerCase() + b.rule.slice(1)}` : "-") : "-");

        return `
          <div class="blank-feedback-card ${isCorr ? "is-correct-border" : "is-wrong-border"}">
            <div class="blank-feedback-head">
              <span class="blank-badge">Blank [ ${b.blank_id} ]</span>
              <span class="badge ${isCorr ? "status-positive" : "status-negative"}">${isCorr ? "Correct" : "Incorrect"}</span>
              <span class="chip topic">${escapeHtml(b.grammar_topic)}</span>
            </div>
            <div class="feedback-grid">
              <p class="feedback-line"><strong>Correct answer:</strong> ${escapeHtml(b.correct_answer)}</p>
              <p class="feedback-line"><strong>Your answer:</strong> ${escapeHtml(b.selected_answer)}</p>
              <p class="feedback-line"><strong>Rule:</strong> ${escapeHtml(b.rule)}</p>
              <p class="feedback-line"><strong>Reason you were right:</strong> ${escapeHtml(reasonRight)}</p>
              <p class="feedback-line"><strong>Reason you were wrong:</strong> ${escapeHtml(reasonWrong)}</p>
            </div>
          </div>
        `;
      })
      .join("");

    els.feedbackPanel.innerHTML = `
      <div class="chip-row">
        <span class="chip topic">Paragraph: ${escapeHtml(feedback.title || "Passage")}</span>
        <span class="chip level">Level: ${escapeHtml(levelDisplayName(itemLevel))}</span>
        <span class="chip ${allCorrect ? "correct" : "wrong"}">${feedback.score_this_paragraph} / ${feedback.total_blanks_this_paragraph} Blanks Correct</span>
      </div>
      <p class="feedback-headline ${headlineClass}">${escapeHtml(feedback.headline)}</p>

      <div class="full-text-review-card">
        <p class="eyebrow">Completed Paragraph</p>
        <p class="completed-paragraph-text">${escapeHtml(feedback.full_text)}</p>
      </div>

      ${feedback.paragraph_explanation ? `
        <div class="cohesion-insight-card">
          <p class="eyebrow">Paragraph Cohesion & Building Insight</p>
          <p>${escapeHtml(feedback.paragraph_explanation)}</p>
        </div>
      ` : ""}

      <div class="blanks-breakdown-section">
        <p class="eyebrow">Blank-by-Blank Review</p>
        <div class="blanks-review-grid">
          ${blanksReviewHtml}
        </div>
      </div>
    `;
  }

  function renderFeedback() {
    if (!state.feedback || !state.currentQuestion) {
      return;
    }

    if (state.mode === "writing") {
      renderWritingFeedback();
    } else if (state.mode === "paragraph") {
      renderParagraphFeedback();
    } else {
      renderSentenceFeedback();
    }

    els.feedbackPanel.classList.remove("hidden");
    els.nextQuestionButton.classList.remove("hidden");
    els.submitAnswerButton.classList.add("hidden");

    renderHeader();
    setScreen("feedback");
  }

  // ---------------------------------------------------------------------------
  // RESULTS RENDERING
  // ---------------------------------------------------------------------------
  function renderResults() {
    const results = state.results;
    if (!results) {
      return;
    }

    if ((results.mode || results.test_type || state.mode) === "writing") {
      renderWritingResults();
      return;
    }

    const currentMode = results.mode || results.test_type || state.mode;
    const currentLevel = results.level || state.level;

    // Highlight active filter buttons in control panel
    document.querySelectorAll(".mode-tab-btn").forEach((btn) => {
      btn.classList.toggle("is-active", btn.dataset.mode === currentMode);
    });
    document.querySelectorAll(".level-tab-btn").forEach((btn) => {
      btn.classList.toggle("is-active", btn.dataset.level === currentLevel);
    });

    const isParagraph = currentMode === "paragraph";
    const summaryCards = [
      ["Mode", modeDisplayName(currentMode)],
      ["Level", levelDisplayName(currentLevel)],
      [isParagraph ? "Blanks Correct" : "Score", `${results.correct_answers} / ${results.total_questions}`],
      ["Accuracy", `${results.percentage}%`],
      ["Correct", `${results.correct_answers}`],
      ["Incorrect", `${results.incorrect_answers}`],
    ]
      .map(
        ([label, value]) => `
          <div class="summary-card">
            <span>${escapeHtml(label)}</span>
            <strong>${escapeHtml(value)}</strong>
          </div>
        `,
      )
      .join("");

    const topicRows = (results.topic_summary || [])
      .map(
        (entry) => `
          <tr>
            <td>${escapeHtml(entry.topic)}</td>
            <td>${escapeHtml(entry.asked)}</td>
            <td>${escapeHtml(entry.correct)}</td>
            <td>${escapeHtml(entry.incorrect)}</td>
            <td>${escapeHtml(entry.accuracy)}%</td>
          </tr>
        `,
      )
      .join("");

    let reviewCardsHtml = "";
    if (isParagraph && results.paragraphs) {
      reviewCardsHtml = results.paragraphs
        .map((p) => {
          const blanksReview = (p.blanks || [])
            .map((b) => {
              const isCorr = Boolean(b.is_correct);
              const selected = b.selected_answer || "No answer";
              const reasonRight = b.reason_right || (isCorr ? b.explanation : "-");
              const reasonWrong = b.reason_wrong || (!isCorr ? (b.rule ? `${(selected || "").split(". ")[1] || selected} does not fit because ${b.rule[0].toLowerCase() + b.rule.slice(1)}` : "-") : "-");

              return `
                <div class="review-blank-row ${isCorr ? "is-corr" : "is-incorr"}">
                  <div class="review-blank-head">
                    <strong>Blank [ ${b.blank_id} ]:</strong>
                    <span class="badge ${isCorr ? "status-positive" : "status-negative"}">${isCorr ? "Correct" : "Incorrect"}</span>
                    <span class="chip topic">${escapeHtml(b.grammar_topic)}</span>
                  </div>
                  <div class="review-blank-meta">
                    <span><strong>Your answer:</strong> ${escapeHtml(selected)}</span>
                    <span><strong>Correct:</strong> ${escapeHtml(b.correct_answer)}</span>
                  </div>
                  <p class="review-blank-rule"><strong>Rule:</strong> ${escapeHtml(b.rule)}</p>
                  <p class="review-blank-why"><strong>Reason you were right:</strong> ${escapeHtml(reasonRight)}</p>
                  <p class="review-blank-why"><strong>Reason you were wrong:</strong> ${escapeHtml(reasonWrong)}</p>
                </div>
              `;
            })
            .join("");

          return `
            <article class="review-card paragraph-review-card">
              <div class="review-head">
                <div>
                  <p class="eyebrow">Paragraph ${escapeHtml(p.paragraph_number)}: ${escapeHtml(p.title)}</p>
                  <h3>${escapeHtml(p.title)}</h3>
                </div>
                <span class="chip level">Level: ${escapeHtml(levelDisplayName(p.level))}</span>
              </div>
              <div class="review-passage-box">
                <p>${escapeHtml(p.full_text)}</p>
              </div>
              ${p.paragraph_explanation ? `
                <div class="cohesion-insight-card">
                  <p class="eyebrow">Paragraph Cohesion Insight</p>
                  <p>${escapeHtml(p.paragraph_explanation)}</p>
                </div>
              ` : ""}
              <div class="review-blanks-container">
                ${blanksReview}
              </div>
            </article>
          `;
        })
        .join("");
    } else if (results.questions) {
      reviewCardsHtml = results.questions
        .map((question) => {
          const isCorr = Boolean(question.is_correct);
          const statusClass = isCorr ? "status-positive" : "status-negative";
          const statusText = isCorr ? "Correct" : "Incorrect";
          const selected = question.selected_answer || "No answer recorded";
          const qLevel = question.level ? levelDisplayName(question.level) : levelDisplayName(currentLevel);
          const reasonRight = question.reason_right || (isCorr ? question.explanation : "-");
          const reasonWrong = question.reason_wrong || (!isCorr ? (question.rule ? `${(selected || "").split(". ")[1] || selected} does not fit because ${question.rule[0].toLowerCase() + question.rule.slice(1)}` : "-") : "-");

          return `
            <article class="review-card">
              <div class="review-head">
                <div>
                  <p class="eyebrow">Question ${escapeHtml(question.question_number)}</p>
                  <h3>${escapeHtml(question.question)}</h3>
                </div>
                <span class="badge ${statusClass}">${escapeHtml(statusText)}</span>
              </div>
              <p class="question-text">${escapeHtml(question.question)}</p>
              <div class="review-meta">
                <span class="chip topic">Topic: ${escapeHtml(question.grammar_topic)}</span>
                <span class="chip level">Level: ${escapeHtml(qLevel)}</span>
                <span class="chip correct">Correct: ${escapeHtml(question.correct_answer)}</span>
                <span class="chip ${isCorr ? "correct" : "wrong"}">Your answer: ${escapeHtml(selected)}</span>
              </div>
              <ul class="review-list">
                <li><strong>Rule:</strong> <span>${escapeHtml(question.rule)}</span></li>
                <li><strong>Reason you were right:</strong> <span>${escapeHtml(reasonRight)}</span></li>
                <li><strong>Reason you were wrong:</strong> <span>${escapeHtml(reasonWrong)}</span></li>
                <li><strong>Sentence:</strong> <span>${escapeHtml(question.sentence_explanation)}</span></li>
              </ul>
            </article>
          `;
        })
        .join("");
    }

    els.resultsSummary.innerHTML = summaryCards;
    els.topicSummary.innerHTML = `
      <table>
        <thead>
          <tr>
            <th>Topic</th>
            <th>Asked</th>
            <th>Correct</th>
            <th>Incorrect</th>
            <th>Accuracy</th>
          </tr>
        </thead>
        <tbody>
          ${topicRows}
        </tbody>
      </table>
    `;
    els.questionReview.innerHTML = reviewCardsHtml;
    setScreen("results");
    setLoading(false);
  }

  function hydrateState(serverState, serverResults = null) {
    state.testId = serverState.id;
    state.mode = serverState.test_type || serverState.mode || config.requestedMode || "sentence";
    state.level = serverState.level || config.requestedLevel || "all";
    state.score = serverState.score || 0;
    state.totalQuestions = serverState.total_questions || 10;
    state.totalParagraphs = serverState.total_paragraphs || 3;
    state.totalTasks = serverState.total_tasks || 1;
    state.essay = "";
    state.pendingQuestion = null;
    state.feedback = null;
    state.results = null;
    state.selectedAnswer = null;
    state.selectedAnswers = {};
    state.activeBlankId = 1;

    if (serverState.completed) {
      state.results = serverResults || null;
      if (!state.results) {
        return false;
      }
      renderResults();
      return true;
    }

    const currentIndex = Number(serverState.current_index || 0);
    state.currentQuestion = serverState.questions?.[currentIndex] || null;
    if (!state.currentQuestion) {
      return false;
    }

    renderQuestion();
    setLoading(false);
    return true;
  }

  async function startTest(targetLevel = null, targetMode = null) {
    hideError();
    const lvl = targetLevel || state.level || config.requestedLevel || "all";
    const md = targetMode || state.mode || config.requestedMode || "sentence";

    state.level = lvl;
    state.mode = md;
    state.selectedAnswers = {};
    state.activeBlankId = 1;

    setLoading(true, `Generating ${levelDisplayName(lvl)} ${modeDisplayName(md)}...`);

    try {
      const data = await requestJson(config.startUrl, {
        method: "POST",
        body: JSON.stringify({ level: lvl, mode: md }),
      });

      state.testId = data.test_id;
      state.mode = data.test_type || data.mode || md;
      state.level = data.level || lvl;
      state.score = data.score || 0;
      state.totalQuestions = data.total_questions || 10;
      state.totalParagraphs = data.total_items || data.total_paragraphs || 3;
      state.totalTasks = data.total_items || data.total_tasks || 1;
      state.essay = "";
      state.currentQuestion = data.question;
      state.pendingQuestion = null;
      state.feedback = null;
      state.results = null;
      state.selectedAnswer = null;
      state.selectedAnswers = {};
      state.activeBlankId = 1;

      renderQuestion();
    } catch (error) {
      showError(error.message);
    } finally {
      setLoading(false);
    }
  }

  function initialize() {
    setLoading(true, "Preparing your diagnostic...");

    if (initialState && hydrateState(initialState, initialResults)) {
      return;
    }

    startTest();
  }

  async function retryTest(targetLevel = null, targetMode = null) {
    hideError();
    const lvl = targetLevel || state.level || "all";
    const md = targetMode || state.mode || "sentence";

    state.level = lvl;
    state.mode = md;
    state.selectedAnswers = {};
    state.activeBlankId = 1;

    setLoading(true, `Creating fresh ${levelDisplayName(lvl)} ${modeDisplayName(md)}...`);
    try {
      const targetUrl = state.testId ? `${apiRoot}${state.testId}/retry/` : config.startUrl;
      const data = await requestJson(targetUrl, {
        method: "POST",
        body: JSON.stringify({ level: lvl, mode: md }),
      });

      state.testId = data.test_id;
      state.mode = data.test_type || data.mode || md;
      state.level = data.level || lvl;
      state.score = data.score || 0;
      state.totalQuestions = data.total_questions || 10;
      state.totalParagraphs = data.total_items || data.total_paragraphs || 3;
      state.totalTasks = data.total_items || data.total_tasks || 1;
      state.essay = "";
      state.currentQuestion = data.question;
      state.pendingQuestion = null;
      state.feedback = null;
      state.results = null;
      state.selectedAnswer = null;
      state.selectedAnswers = {};
      state.activeBlankId = 1;

      renderQuestion();
    } catch (error) {
      showError(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function submitAnswer() {
    if (state.busy) {
      return;
    }

    const isWriting = state.mode === "writing";
    const isParagraph = state.mode === "paragraph";
    let bodyPayload = {};

    if (isWriting) {
      if (countWords(state.essay) < MIN_SUBMIT_WORDS) {
        showError(`Write at least ${MIN_SUBMIT_WORDS} words before submitting.`);
        return;
      }
      bodyPayload = { essay: state.essay };
    } else if (isParagraph) {
      const blanks = state.currentQuestion?.blanks || [];
      const allFilled = blanks.length > 0 && blanks.every((b) => state.selectedAnswers[b.blank_id]);
      if (!allFilled) {
        showError("Please select an answer for all blanks in the paragraph.");
        return;
      }
      bodyPayload = { answers: state.selectedAnswers };
    } else {
      if (!state.selectedAnswer) {
        showError("Choose an answer before submitting.");
        return;
      }
      bodyPayload = { selected_answer: state.selectedAnswer };
    }

    hideError();
    setLoading(
      true,
      isWriting
        ? "Analysing your writing and scoring it against the IELTS descriptors..."
        : "Checking your answer...",
    );
    try {
      const data = await requestJson(`${apiRoot}${state.testId}/answer/`, {
        method: "POST",
        body: JSON.stringify(bodyPayload),
      });

      state.score = data.score;
      state.feedback = data.feedback;
      state.pendingQuestion = data.next_question;

      if (isWriting) {
        clearDraft();
        state.essay = "";
      }

      if (data.completed && data.results) {
        state.results = data.results;
        renderResults();
        return;
      }

      renderFeedback();
    } catch (error) {
      showError(error.message);
    } finally {
      setLoading(false);
    }
  }

  function nextQuestion() {
    if (!state.pendingQuestion) {
      return;
    }

    state.currentQuestion = state.pendingQuestion;
    state.pendingQuestion = null;
    state.feedback = null;
    state.essay = "";
    state.selectedAnswer = null;
    state.selectedAnswers = {};
    state.activeBlankId = 1;
    renderQuestion();
  }

  document.addEventListener("input", (event) => {
    if (!event.target || event.target.id !== "essayInput") {
      return;
    }
    state.essay = event.target.value;
    saveDraft(state.essay);
    updateEssayStats();
  });

  document.addEventListener("click", (event) => {
    const target = event.target.closest("[data-action]");
    if (!target) {
      return;
    }

    const action = target.dataset.action;
    if (action === "retry-test") {
      retryTest();
      return;
    }
    if (action === "retry-level") {
      const lvl = target.dataset.level;
      retryTest(lvl, state.mode);
      return;
    }
    if (action === "retry-mode") {
      const md = target.dataset.mode;
      retryTest(state.level, md);
      return;
    }
    if (action === "submit-answer") {
      submitAnswer();
      return;
    }
    if (action === "next-question") {
      nextQuestion();
      return;
    }
    if (action === "choose-sentence-answer") {
      if (state.busy || state.mode !== "sentence") {
        return;
      }
      state.selectedAnswer = target.dataset.letter;
      els.submitAnswerButton.disabled = false;
      renderSentenceQuestion();
      return;
    }
    if (action === "select-blank-tab") {
      if (state.busy || state.mode !== "paragraph") {
        return;
      }
      const bId = Number(target.dataset.blankId);
      if (bId) {
        state.activeBlankId = bId;
        renderParagraphQuestion();
      }
      return;
    }
    if (action === "choose-paragraph-blank-answer") {
      if (state.busy || state.mode !== "paragraph") {
        return;
      }
      const bId = Number(target.dataset.blankId);
      const letter = target.dataset.letter;
      if (bId && letter) {
        state.selectedAnswers[bId] = letter;

        // Find next unfilled blank if any
        const blanks = state.currentQuestion?.blanks || [];
        const nextUnfilled = blanks.find((b) => !state.selectedAnswers[b.blank_id]);
        if (nextUnfilled) {
          state.activeBlankId = nextUnfilled.blank_id;
        }

        renderParagraphQuestion();
      }
      return;
    }
  });

  initialize();
})();
