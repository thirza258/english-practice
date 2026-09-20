"""The four IELTS courses: how to perform well in each skill, then guided practice."""

from dataclasses import replace

from .course_types import Course, Section
from .ielts_courses import BEGINNER_COURSE, INTERMEDIATE_COURSE, BAND8_COURSE, IELTS_RESOURCES
from .ielts_techniques import (
    LISTENING_START, LISTENING_MAPS, LISTENING_BAND8,
    READING_START, READING_COMPLETION, READING_BAND8,
    SPEAKING_START, SPEAKING_DELIVERY, SPEAKING_BAND8,
)


LEVELS = (("Beginner", "beginner"), ("Intermediate", "intermediate"), ("Band 8 target", "ielts_8_9"))
LESSON_REDIRECTS = {}


def practice_lesson(source, slug, skill, level, title, technique, mistake):
    original = next(lesson for lesson in source.lessons if lesson.slug == slug)
    LESSON_REDIRECTS[(source.slug, slug)] = (f"ielts-{skill.lower()}", slug)
    return replace(original, title=title, level=level, technique=technique,
                   sections=(*original.sections, Section("Avoid this common mistake", mistake)))


SPEAKING_COURSE = Course(
    slug="ielts-speaking", title="How to ace IELTS Speaking", category="IELTS", skill="Speaking",
    level="Beginner → Intermediate → Band 8 target",
    description="Learn how to give developed answers, speak clearly, handle all three parts, and respond naturally to follow-up questions.",
    outcomes=("Develop Part 1 answers without memorising a script.", "Organise Part 2 and improve fluency, pronunciation, and paraphrasing.", "Explain and qualify Part 3 views with Band 8 control as your target."),
    project="A set of spoken answers across Parts 1, 2, and 3, with a review of fluency, vocabulary, grammar, and pronunciation.",
    resources=(IELTS_RESOURCES[3], IELTS_RESOURCES[4], IELTS_RESOURCES[0]),
    strategy=(
        Section("Answer the question first", "Give a direct response, then explain a reason or a specific example. Listen to the actual wording, especially when the examiner changes the question."),
        Section("Give your answer a direction", "For the long turn, use the preparation minute for a few keywords. Develop an experience in a sequence and explain why it mattered. For discussion questions, explain a mechanism and a relevant limit."),
        Section("Make understanding easy", "Pause between ideas, stress important contrasts, and describe a missing word another way. Practise grammar and pronunciation that make your own meaning clear."),
        Section("Review and repeat with a change", "Use the four speaking criteria to choose a specific improvement. Repeat with a new example and seek feedback on a recorded response where possible."),
    ),
    lessons=(
        SPEAKING_START,
        practice_lesson(BEGINNER_COURSE, "speaking-about-yourself", "Speaking", "Beginner", "Ace Part 1: answer, explain, and give an example", "Answer → reason → personal example → natural finish.", "A memorised speech can miss the question. Answer twice with different examples, and keep each answer relevant rather than extending it just to fill time."),
        practice_lesson(INTERMEDIATE_COURSE, "speaking-the-long-turn", "Speaking", "Intermediate", "Ace Part 2: plan and develop your long turn", "Use keyword notes → set the scene → develop an event → explain its significance.", "Writing full sentences during preparation can use up the minute and encourage reading. Choose a few keywords and expand them aloud. Develop a detail when you need more to say."),
        SPEAKING_DELIVERY,
        practice_lesson(BAND8_COURSE, "speaking-explain-and-qualify", "Speaking", "Band 8 target", "Ace Part 3: explain and qualify an argument", "State a view → show how it works → consider a limitation → reach a clear judgement.", "Adding 'on the other hand' without a real contrast does not develop your reasoning. Explain which people or circumstances change the answer and why."),
        SPEAKING_BAND8,
    ),
)

READING_COURSE = Course(
    slug="ielts-reading", title="How to ace IELTS Reading", category="IELTS Academic", skill="Reading",
    level="Beginner → Intermediate → Band 8 target",
    description="Learn how to locate evidence, recognise paraphrases, choose headings, handle True/False/Not Given, and protect accuracy under time pressure.",
    outcomes=("Find the relevant sentence and verify the full claim.", "Use distinct approaches for headings, matching information, and completion tasks.", "Handle qualified arguments and review errors to improve timed accuracy."),
    project="An evidence log covering common question types, plus a personal timing and recovery routine for Academic Reading.",
    resources=(IELTS_RESOURCES[1], IELTS_RESOURCES[0], IELTS_RESOURCES[4]),
    strategy=(
        Section("Identify the task", "Read the instructions and decide whether you need a main idea, a specific detail, words from the passage, or agreement with a claim. Check reuse rules and word limits."),
        Section("Locate, then verify", "Scan for an anchor or a paraphrase. Read the surrounding sentences closely before choosing. A repeated word locates possible evidence; it does not establish the answer."),
        Section("Check the whole claim", "Compare the people, time, quantity, and strength of each statement with the text. Distinguish a contradiction from information the passage does not supply."),
        Section("Manage time and learn from errors", "Move on when a question stops producing new evidence, then return. After practice, record the exact phrase or inference that caused each error and test the correction on a fresh passage."),
    ),
    lessons=(
        READING_START,
        practice_lesson(BEGINNER_COURSE, "reading-for-evidence", "Reading", "Beginner", "Ace True/False/Not Given with evidence", "Locate the claim → look for agreement or contradiction → choose Not Given only when unresolved.", "An unmentioned fact is not automatically false. Find a sentence that directly contradicts the statement before choosing False, and do not import facts from outside the passage."),
        practice_lesson(INTERMEDIATE_COURSE, "reading-paraphrases-and-headings", "Reading", "Intermediate", "Choose headings and recognise paraphrases", "Summarise the paragraph → compare heading meanings → reject a heading that covers only one detail.", "Do not choose a heading solely because it repeats a memorable noun. A correct heading covers the paragraph's main job, including any contrast or change of direction."),
        READING_COMPLETION,
        practice_lesson(BAND8_COURSE, "reading-evaluate-an-argument", "Reading", "Band 8 target", "Track the writer's position and qualified claims", "Identify whose view it is → preserve its conditions → check the exact statement.", "A view attributed to supporters is not automatically the writer's position. Watch the writer's response and retain conditions such as only if or provided that."),
        READING_BAND8,
    ),
)

WRITING_COURSE = Course(
    slug="ielts-writing", title="How to ace IELTS Writing", category="IELTS Academic", skill="Writing",
    level="Beginner → Intermediate → Band 8 target",
    description="Learn how to plan Task 1 reports and Task 2 essays, select key features, develop arguments, and revise against the writing criteria.",
    outcomes=("Build accurate Task 1 comparisons and a clear Task 2 position.", "Write complete reports and essays with organised, developed ideas.", "Refine precision, qualification, and grammatical control for a Band 8 target."),
    project="A Task 1 report and a Task 2 essay, revised for task coverage, organisation, vocabulary, and grammar.",
    resources=(IELTS_RESOURCES[2], ("IELTS: Writing assessment and band descriptors", "https://ielts.org/take-a-test/preparation-resources/writing-test-resources"), IELTS_RESOURCES[0]),
    strategy=(
        Section("Decode the task before drafting", "For Task 1, identify the subject, units, period, and main patterns. For Task 2, mark every instruction and decide exactly what position the essay will defend."),
        Section("Plan the reader's route", "Task 1 needs an overview and selected supporting comparisons. Task 2 needs a clear position and paragraphs that develop reasons rather than repeat an opinion."),
        Section("Make each detail do a job", "Support a reported trend with accurate figures. Support an argument by explaining how it works and giving a relevant example. Choose vocabulary for precision and use complex grammar where it expresses a useful relationship."),
        Section("Check in four passes", "Review task coverage first, then progression and connections, then word choice, and finally recurring grammar errors. For full practice, aim for about twenty minutes on Task 1 and forty on Task 2."),
    ),
    lessons=(
        practice_lesson(BEGINNER_COURSE, "writing-describe-data", "Writing", "Beginner", "Ace Task 1 foundations: overview and accurate comparisons", "Identify the data → state the main pattern → support it with selected figures.", "Listing every number without an overview leaves the main message unclear. First state what increased, decreased, or stood out; then select figures that support that picture."),
        practice_lesson(BEGINNER_COURSE, "writing-your-first-argument", "Writing", "Beginner", "Ace Task 2 foundations: turn an opinion into a reason", "Answer the prompt → choose a reason → explain how it works → illustrate it.", "Repeating that an idea is important does not explain it. Ask how or why your reason supports your position, and add a concrete example that answers that question."),
        practice_lesson(INTERMEDIATE_COURSE, "writing-task-one-report", "Writing", "Intermediate", "Plan and write a complete Task 1 report", "Introduce → give an overview → group comparisons → verify numbers and units.", "An increase from twenty percent to thirty percent is ten percentage points, not a ten percent relative increase. Preserve units and do not invent a cause for the pattern."),
        practice_lesson(INTERMEDIATE_COURSE, "writing-task-two-essay", "Writing", "Intermediate", "Plan and write a complete Task 2 essay", "Map every instruction → plan both views → maintain your position → develop each reason.", "A discuss-both-views prompt also needs your own opinion when requested. Do not let one well-developed side hide a missing second view or an unclear position."),
        practice_lesson(BAND8_COURSE, "writing-task-one-precision", "Writing", "Band 8 target", "Refine Task 1 for selection and precision", "Select the major features → compare accurately → remove unsupported interpretations.", "Two endpoints do not show that a change was steady. Check each adjective and comparison against the information actually supplied, including the limits of that information."),
        practice_lesson(BAND8_COURSE, "writing-task-two-nuance", "Writing", "Band 8 target", "Refine Task 2 for depth, nuance, and control", "Define the extent of agreement → explain mechanisms → address a counterargument → revise.", "An obscure synonym cannot repair a thin argument. Revise relevance and development before polishing vocabulary, and make any counterargument affect the reasoning."),
    ),
)

LISTENING_COURSE = Course(
    slug="ielts-listening", title="How to ace IELTS Listening", category="IELTS", skill="Listening",
    level="Beginner → Intermediate → Band 8 target",
    description="Learn how to predict answers, follow corrections and maps, reject distractors, and keep up with lectures without losing your place.",
    outcomes=("Prepare before the audio and catch confirmed details.", "Follow changing decisions, paraphrases, and directions on a map.", "Separate predictions from findings and review errors for one-play accuracy."),
    project="A listening error log covering details, decisions, directions, and lecture claims, with a recovery strategy for missed answers.",
    resources=(("IELTS: Listening format and question types", "https://ielts.org/take-a-test/test-types/ielts-academic-test/ielts-academic-format-listening"), IELTS_RESOURCES[0], IELTS_RESOURCES[4]),
    strategy=(
        Section("Read and predict", "Before each recording, identify the required information and possible paraphrases. For a completion gap, predict the type of word or number and note the permitted word count."),
        Section("Follow the final meaning", "Wait through corrections and rejected suggestions. On a map, follow movements and landmarks in sequence. In a lecture, distinguish background, prediction, result, and qualification."),
        Section("Recover immediately", "If a detail is missed, move to the next question and listen for a new anchor. Holding on to one lost answer can make you miss several more."),
        Section("Audit, then test the correction", "After one-play practice, use the transcript to identify the decisive phrase. Review distractors, spelling, plurals, and word limits. Try the same technique on unfamiliar audio."),
    ),
    lessons=(
        LISTENING_START,
        practice_lesson(BEGINNER_COURSE, "listening-for-details", "Listening", "Beginner", "Catch times, places, and corrected details", "Predict the detail → hear the first suggestion → wait for confirmation → note the final answer.", "The first time or place mentioned may be replaced. Keep listening for correction signals and use the confirmed detail, rather than the first familiar word."),
        practice_lesson(INTERMEDIATE_COURSE, "listening-follow-decisions", "Listening", "Intermediate", "Reject distractors and follow the final decision", "Read the choices → track rejected options → identify the final decision and its paraphrase.", "A repeated word can belong to an idea the speakers reject. In review, explain why each alternative is wrong as well as why the chosen answer is supported."),
        LISTENING_MAPS,
        practice_lesson(BAND8_COURSE, "listening-qualified-claims", "Listening", "Band 8 target", "Follow academic claims without overstating them", "Separate the result, possible explanation, limitation, and recommendation.", "A promising finding does not prove a universal cause. Preserve words such as may and only, and do not turn a suggested next study into a recommendation for immediate expansion."),
        LISTENING_BAND8,
    ),
)


IELTS_COURSES = (SPEAKING_COURSE, READING_COURSE, WRITING_COURSE, LISTENING_COURSE)
LESSON_ORIGINS = {destination: origin for origin, destination in LESSON_REDIRECTS.items()}
