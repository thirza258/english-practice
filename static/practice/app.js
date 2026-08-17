(() => {
  const config = window.APP_CONFIG || {};
  const apiRoot = config.apiRoot || "/api/tests/";
  const totalQuestions = Number(config.totalQuestions || 10);

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
    mode: "idle",
    testId: null,
    score: 0,
    currentQuestion: null,
    pendingQuestion: null,
    feedback: null,
    results: null,
    selectedAnswer: null,
    busy: false,
  };

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function setMode(mode) {
    state.mode = mode;
    els.testScreen.classList.toggle("screen-active", mode === "question" || mode === "feedback");
    els.resultsScreen.classList.toggle("screen-active", mode === "results");
    els.testScreen.classList.toggle("hidden", mode === "results");
    els.resultsScreen.classList.toggle("hidden", mode !== "results");
  }

  function setLoading(active, message = "Preparing your diagnostic...") {
    state.busy = active;
    els.loadingMessage.textContent = message;
    els.loadingOverlay.classList.toggle("hidden", !active);
    els.submitAnswerButton.disabled = active || !state.selectedAnswer || state.mode !== "question";
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

  function optionButtons(question, interactive = true) {
    return question.options
      .map((option) => {
        const isSelected = state.selectedAnswer === option.label;
        let className = "option-button";
        if (!interactive && question.is_correct !== null) {
          if (option.label === question.correct_answer?.[0]) {
            className += " is-correct";
          }
          if (option.label === question.selected_answer?.[0] && !question.is_correct) {
            className += " is-wrong";
          }
        } else if (isSelected) {
          className += " is-selected";
        }

        return `
          <button
            type="button"
            class="${className}"
            data-action="choose-answer"
            data-letter="${escapeHtml(option.label)}"
            ${interactive ? "" : "disabled"}
            aria-pressed="${isSelected ? "true" : "false"}"
          >
            <span class="option-letter">${escapeHtml(option.label)}</span>
            <span class="option-text">${escapeHtml(option.text)}</span>
          </button>
        `;
      })
      .join("");
  }

  function renderHeader() {
    if (!state.currentQuestion) {
      return;
    }
    els.questionCounter.textContent = `Question ${state.currentQuestion.question_number} of ${totalQuestions}`;
    els.scoreCounter.textContent = `Score ${state.score} / ${totalQuestions}`;
    const progress = progressPercent(state.currentQuestion.question_number - 1, totalQuestions);
    els.progressLabel.textContent = `${progress}%`;
    els.progressBar.style.width = `${progress}%`;
  }

  function renderQuestion() {
    if (!state.currentQuestion) {
      return;
    }

    els.feedbackPanel.classList.add("hidden");
    els.feedbackPanel.innerHTML = "";
    els.nextQuestionButton.classList.add("hidden");
    els.submitAnswerButton.classList.remove("hidden");
    els.submitAnswerButton.disabled = !state.selectedAnswer || state.busy;

    renderHeader();
    setMode("question");

    els.questionPanel.innerHTML = `
      <div class="prompt-card">
        <h3>${escapeHtml(state.currentQuestion.question)}</h3>
        <p class="hidden-topic-note">The grammar topic is hidden until you submit your answer.</p>
        <div class="option-list">
          ${optionButtons(state.currentQuestion, true)}
        </div>
      </div>
    `;
  }

  function renderFeedback() {
    if (!state.feedback || !state.currentQuestion) {
      return;
    }

    const feedback = state.feedback;
    const isCorrect = feedback.is_correct;
    const headlineClass = isCorrect ? "is-correct" : "is-wrong";
    els.feedbackPanel.innerHTML = `
      <div class="chip-row">
        <span class="chip topic">Topic: ${escapeHtml(feedback.grammar_topic)}</span>
        <span class="chip ${isCorrect ? "correct" : "wrong"}">${escapeHtml(feedback.headline)}</span>
      </div>
      <p class="feedback-headline ${headlineClass}">${escapeHtml(feedback.headline)}</p>
      <div class="feedback-grid">
        <p class="feedback-line"><strong>Correct answer:</strong> ${escapeHtml(feedback.correct_answer)}</p>
        <p class="feedback-line"><strong>Your answer:</strong> ${escapeHtml(feedback.selected_answer)}</p>
        <p class="feedback-line"><strong>Grammar rule:</strong> ${escapeHtml(feedback.rule)}</p>
        <p class="feedback-line"><strong>Why the correct answer is right:</strong> ${escapeHtml(feedback.explanation)}</p>
        <p class="feedback-line"><strong>Why your selection is wrong:</strong> ${escapeHtml(feedback.selected_answer_explanation)}</p>
        <p class="feedback-line"><strong>Sentence:</strong> ${escapeHtml(feedback.sentence_explanation)}</p>
      </div>
    `;
    els.feedbackPanel.classList.remove("hidden");
    els.nextQuestionButton.classList.toggle("hidden", !state.pendingQuestion);
    els.submitAnswerButton.classList.add("hidden");
    renderHeader();
    setMode("feedback");
  }

  function renderResults() {
    const results = state.results;
    if (!results) {
      return;
    }

    const summaryCards = [
      ["Score", `${results.correct_answers} / ${results.total_questions}`],
      ["Percentage", `${results.percentage}%`],
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

    const topicRows = results.topic_summary
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

    const reviewCards = results.questions
      .map((question) => {
        const statusClass = question.is_correct ? "status-positive" : "status-negative";
        const statusText = question.is_correct ? "Correct" : "Incorrect";
        const selected = question.selected_answer || "No answer recorded";
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
              <span class="chip correct">Correct: ${escapeHtml(question.correct_answer)}</span>
              <span class="chip ${question.is_correct ? "correct" : "wrong"}">Your answer: ${escapeHtml(selected)}</span>
            </div>
            <ul class="review-list">
              <li><strong>Rule:</strong> <span>${escapeHtml(question.rule)}</span></li>
              <li><strong>Why it is correct:</strong> <span>${escapeHtml(question.explanation)}</span></li>
              <li><strong>Sentence:</strong> <span>${escapeHtml(question.sentence_explanation)}</span></li>
            </ul>
          </article>
        `;
      })
      .join("");

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
    els.questionReview.innerHTML = reviewCards;
    setMode("results");
    setLoading(false);
  }

  function hydrateState(serverState, serverResults = null) {
    state.testId = serverState.id;
    state.score = serverState.score || 0;
    state.pendingQuestion = null;
    state.feedback = null;
    state.results = null;
    state.selectedAnswer = null;

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

  async function startTest() {
    hideError();
    setLoading(true, "Generating a new diagnostic...");

    try {
      const data = await requestJson(config.startUrl, {
        method: "POST",
        body: JSON.stringify({}),
      });

      state.testId = data.test_id;
      state.score = data.score || 0;
      state.currentQuestion = data.question;
      state.pendingQuestion = null;
      state.feedback = null;
      state.results = null;
      state.selectedAnswer = null;
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

  async function retryTest() {
    hideError();
    if (!state.testId) {
      return startTest();
    }

    setLoading(true, "Creating a fresh diagnostic...");
    try {
      const data = await requestJson(`${apiRoot}${state.testId}/retry/`, {
        method: "POST",
        body: JSON.stringify({}),
      });

      state.testId = data.test_id;
      state.score = data.score || 0;
      state.currentQuestion = data.question;
      state.pendingQuestion = null;
      state.feedback = null;
      state.results = null;
      state.selectedAnswer = null;
      renderQuestion();
    } catch (error) {
      showError(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function submitAnswer() {
    if (state.busy || state.mode !== "question") {
      return;
    }
    if (!state.selectedAnswer) {
      showError("Choose an answer before submitting.");
      return;
    }

    hideError();
    setLoading(true, "Checking your answer...");
    try {
      const data = await requestJson(`${apiRoot}${state.testId}/answer/`, {
        method: "POST",
        body: JSON.stringify({ selected_answer: state.selectedAnswer }),
      });

      state.score = data.score;
      state.feedback = data.feedback;
      state.pendingQuestion = data.next_question;

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
    state.selectedAnswer = null;
    renderQuestion();
  }

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
    if (action === "submit-answer") {
      submitAnswer();
      return;
    }
    if (action === "next-question") {
      nextQuestion();
      return;
    }
    if (action === "choose-answer") {
      if (state.busy || state.mode !== "question") {
        return;
      }
      state.selectedAnswer = target.dataset.letter;
      els.submitAnswerButton.disabled = false;
      renderQuestion();
    }
  });

  initialize();
})();
