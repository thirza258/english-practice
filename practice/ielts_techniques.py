"""Original lessons that teach a repeatable approach before asking learners to practise."""

from .course_types import Activity, Assignment, Example, Lesson, Question, Section


SPEAKING_START = Lesson(
    slug="speaking-how-to-score-well", title="Understand what earns marks in Speaking", minutes=15,
    skill="Speaking", level="Beginner",
    technique="Answer directly → explain why → add a specific detail → finish naturally.",
    goal="Build a clear spoken answer and review it using the four speaking criteria.",
    sections=(
        Section("Know what the examiner listens for", "Speaking is assessed through fluency and coherence, vocabulary, grammar, and pronunciation. Start by making your meaning easy to follow. A short answer with a reason and a concrete detail gives you room to show these skills. A long list of impressive words does not help if it does not answer the question."),
        Section("Use a flexible answer shape", "For a familiar Part 1 question, give your answer immediately, explain a reason, and add an example when it is useful. For 'Do you like your neighbourhood?', you might name one feature, explain its value, and mention a recent experience. Treat this as a support for thinking, not a script that every answer must follow."),
        Section("Avoid the one-word answer and the memorised speech", "Practise the same question twice with different examples. This teaches flexible expression. If the question changes from what you enjoy to what you would improve, change the answer too. Review one delivery issue, such as a missing pause, and one language issue, such as an incorrect verb form."),
    ),
    example=Example("Do you enjoy studying English? Yes. English is a ubiquitous phenomenon in contemporary society.", "Yes, especially when I can use it in a conversation. Last week I explained a recipe to a visitor, and being understood made the practice feel worthwhile.", "The revised answer is relevant, developed, and personal. The listener can follow it without a memorised introduction."),
    activity=Activity("speaking", "Try the answer–reason–detail approach", "Do you prefer studying alone or with other people? Give a direct answer, explain a reason, and add an example from your experience. Speak for about forty-five seconds, then answer again with a different example.", seconds=45, preparation_seconds=15),
    questions=(
        Question("Which answer best develops 'Do you enjoy your neighbourhood?'", ("Yes, because I can walk to the park. I met a friend there yesterday.", "Yes. Yes. Yes.", "The neighbourhood is a multifaceted paradigm."), 0, "The first response answers the question and develops it through a reason and a specific detail."),
        Question("Which practice habit helps you respond naturally?", ("Memorise one speech for every question.", "Answer related questions using different examples and wording.", "Replace every common word with an unfamiliar one."), 1, "Variation helps you listen to the actual question and express your meaning flexibly."),
    ),
    assignment=Assignment("After both spoken attempts, note your answer, reason, and two different examples. Choose one change to improve clarity or accuracy on your next attempt.", 40,
        ("I spoke both answers aloud.", "I answered the question before developing it.", "I reviewed one specific improvement."),
        "I prefer studying with a partner because we can notice each other's mistakes. My first example was practising a conversation with my cousin. My second was checking an essay with a classmate. I will pause after my main answer and check the past tense when describing a finished experience.", label="Your speaking reflection"),
)

SPEAKING_DELIVERY = Lesson(
    slug="speaking-fluency-and-pronunciation", title="Sound clear and keep your answer moving", minutes=18,
    skill="Speaking", level="Intermediate",
    technique="Group words into ideas → stress key words → paraphrase a missing word → continue.",
    goal="Use thought groups, clear stress, and paraphrasing to improve fluency and intelligibility.",
    sections=(
        Section("Pause between ideas", "Read 'I prefer the morning / because it is quiet / and I can concentrate' aloud. The slashes mark possible pauses, not words to say. Keep words within each group connected and let the important meaning words carry stress. Practise first slowly, then at a comfortable conversational pace."),
        Section("Recover without starting again", "If you cannot recall a word, describe its function or give an example. A reusable bottle can become 'a bottle I refill instead of throwing away'. Briefly correct a slip if it changes your meaning, then continue. Constantly restarting an answer makes its structure harder to follow."),
        Section("Review the listener's effort", "If possible, record yourself separately or ask a partner to identify your main point. Check whether pauses separate ideas, important contrasts are audible, and sentence endings are clear. You do not need to imitate a particular accent. Work on one specific sound or stress pattern you found difficult, then repeat the answer."),
    ),
    example=Example("I prefer the morning because because because I prefer the morning it is quiet and quiet is good.", "I prefer the morning / because the house is quiet. / In the evening, by contrast, / I am usually too tired to concentrate.", "Thought groups and a clear contrast help the listener follow the answer. The slashes show practice pauses only."),
    activity=Activity("speaking", "Explain a preference clearly", "When is the best time of day for you to study, and why? Explain your preference and contrast it with another time. If a word is difficult to recall, describe the idea in other words. Repeat the answer with deliberate pauses between ideas.", seconds=60),
    questions=(
        Question("Where is a natural pause in 'I cycle to work because it saves money'?", ("I cycle to / work because it saves money", "I cycle to work / because it saves money", "I / cycle / to / work / because"), 1, "The second pause separates the main action from its reason while keeping meaningful phrases together."),
        Question("You forget the word 'thermometer'. What should you do?", ("Abandon the whole answer.", "Repeat an unrelated advanced word.", "Say 'the instrument used to measure temperature' and continue."), 2, "A clear description preserves the meaning and allows the answer to continue."),
    ),
    assignment=Assignment("After speaking, write one sentence with slashes showing useful pauses. Describe a paraphrase you used and the delivery change you will practise next.", 40,
        ("I spoke aloud at a comfortable pace.", "I used pauses between meaningful groups of words.", "I described an idea in other words when needed."),
        "I study before breakfast / because my home is quiet / and I feel rested. I described distractions as things that pull my attention away from the task. On my next attempt I will stress the contrast between morning and evening and avoid restarting when I make a small slip.", label="Your speaking reflection"),
)

SPEAKING_BAND8 = Lesson(
    slug="speaking-band-eight-control", title="Build Band 8 control across follow-up questions", minutes=20,
    skill="Speaking", level="Band 8 target",
    technique="State a view → explain the mechanism → qualify it → adapt to the follow-up.",
    goal="Give a developed discussion answer and adapt it when the examiner changes the angle.",
    sections=(
        Section("Develop your reasoning", "A strong discussion response shows how one idea leads to another. If you say that museums should be free, explain who benefits and how access changes. Then consider a relevant limitation, such as funding. Choose precise words you can use accurately, and check that any idiom fits the discussion naturally."),
        Section("Listen again when the question changes", "A follow-up about funding asks for a different relationship from a question about access. Briefly connect to your earlier answer, then address the new angle. Compare options or explain a consequence where appropriate. Do not repeat a prepared paragraph just because it contains vocabulary on the same topic."),
        Section("Use the criteria to choose a next step", "Review whether your reasoning was easy to follow, your vocabulary conveyed exact meanings, your grammar handled relationships accurately, and your pronunciation stayed clear. Ask a teacher or capable partner for feedback where possible. A short solo drill can reveal an improvement target; it cannot establish an official Speaking band."),
    ),
    example=Example("Should museums be free? Yes. How should they be funded? Yes, museums should be free because museums should be free.", "Entry could be free for local residents, with public funding covering essential costs. For additional exhibitions, modest charges might be reasonable, provided that visitors still have access to the main collection.", "The answer responds to funding and balances access with a practical limitation. It advances the discussion instead of repeating its first claim."),
    activity=Activity("speaking", "Adapt across two discussion questions", "First answer: Should museums offer free entry? Then answer: How could a museum fund its work while remaining accessible? Spend roughly a minute on each question. Explain a mechanism and a limitation, and make your second answer respond to the funding question.", seconds=120),
    questions=(
        Question("The examiner moves from the benefits of tourism to its costs. What should change?", ("Nothing: repeat the benefits paragraph.", "Address costs directly and explain a relevant trade-off.", "Ignore the new question and tell a memorised story."), 1, "A follow-up tests your response to its own meaning. A relevant connection is useful, but the answer needs a new focus."),
        Question("Which review note best supports further improvement?", ("I need more impressive words, whatever they mean.", "My response was long, so it must be Band 8.", "My funding example was relevant, but I need to explain why a charge would not exclude low-income visitors."), 2, "The note identifies a precise gap in development and a useful next practice step."),
    ),
    assignment=Assignment("Summarise how your second spoken answer addressed the changed question. Note one strength and one next step using the speaking criteria.", 50,
        ("I answered both questions aloud.", "I developed a mechanism and a relevant qualification.", "I used the criteria to identify a specific next step."),
        "My first answer focused on access for families, while my second considered public funding and charges for special exhibitions. I kept the distinction between the main collection and optional events clear. My next step is to explain how discounted tickets could help people with limited incomes, then check whether that additional detail fits naturally into my spoken answer.", label="Your speaking reflection"),
)

READING_START = Lesson(
    slug="reading-locate-before-answering", title="Find the answer without reading every word twice", minutes=15,
    skill="Reading", level="Beginner",
    technique="Read the instruction → predict a paraphrase → locate the passage → check the full sentence.",
    goal="Use a question to locate relevant information and verify its meaning in context.",
    sections=(
        Section("Know what you are looking for", "Identify the task type and underline the important meaning in the question. A name, date, or unusual object can be a useful anchor. Predict how the passage might express the idea differently: the price was reduced may become it became cheaper."),
        Section("Scan, then slow down", "Move quickly through the text to locate an anchor or its paraphrase. Once you find it, read the complete sentence and nearby sentences carefully. The first matching word is a location clue, not proof of an answer. A nearby contrast may reverse the apparent meaning."),
        Section("Keep outside knowledge out", "Base the answer on the supplied passage. Before choosing, point to the words that support it. If you cannot explain the connection, revisit the text. After checking, record the paraphrase you missed so you can recognise it in a new passage."),
    ),
    example=Example("Question: Why did the café extend its opening hours? Passage mentions prices. → Because meals became cheaper.", "Passage: Longer opening hours let evening workers eat after their shifts. → To serve people finishing work late.", "The answer matches the reason in the passage. A nearby mention of prices would not explain the hours."),
    activity=Activity("reading", "A changed timetable", "The town library began opening until eight in the evening after local workers said they could not arrive before its former closing time of five. The extended hours apply on Tuesdays and Thursdays. Saturday opening has not changed. The library also replaced its old booking form, but membership fees remain the same. Staff will review the timetable after three months."),
    questions=(
        Question("Why did the library introduce later opening?", ("To make visits possible for people finishing work late", "To increase membership fees", "To close on Saturdays"), 0, "The passage says workers could not arrive before five. Later opening addresses that access problem."),
        Question("Which phrase in the passage matches 'the previous closing hour'?", ("after three months", "former closing time", "extended hours"), 1, "Former means previous, and closing time expresses the idea of the closing hour."),
    ),
    assignment=Assignment("Identify the evidence for the first answer and explain the paraphrase in the second. Write a short sequence you will use on your next reading question.", 40,
        ("I found a sentence supporting my answer.", "I matched meaning rather than one repeated word.", "I recorded a method I can reuse."),
        "The evidence is that local workers could not arrive before five. This explains why the library opened later. Former closing time means the previous closing hour. Next time I will read the instruction, identify the key idea, locate a possible paraphrase, and check the full sentence before choosing an answer.", label="Your reading strategy notes"),
)

READING_COMPLETION = Lesson(
    slug="reading-completion-and-word-limits", title="Keep marks in completion and matching tasks", minutes=18,
    skill="Reading", level="Intermediate",
    technique="Identify the required information → locate evidence → fit the grammar → check the word limit.",
    goal="Choose a completion that follows the instructions and distinguish matching a detail from matching a heading.",
    sections=(
        Section("Let the gap guide you", "A gap after 'stored in' probably needs a place or container. Predict the grammatical role before locating the evidence. When instructions ask for words from the passage, use the relevant words from that passage and respect the maximum. An answer can express the right idea and still break the task's word limit."),
        Section("Match the thing the question asks for", "Matching headings asks for a paragraph's main idea; matching information may ask where a particular detail appears. In the latter task, a small example can be the decisive evidence. Read instructions about whether a paragraph letter or option can be reused, rather than assuming the rule is always the same."),
        Section("Make a final accuracy pass", "Read the completed sentence aloud in your head. Check that the selected words fit its grammar and meaning, and check spelling and number of words. Do not add an explanatory phrase simply to show you understood; extra words can make a valid answer invalid."),
    ),
    example=Example("Instruction: NO MORE THAN TWO WORDS. Passage: Samples were stored in sealed containers. Answer: in sealed containers", "Answer: sealed containers", "The question already supplies the preposition. Adding it both duplicates the grammar and exceeds the two-word limit."),
    activity=Activity("reading", "A seed-storage project", "A. Volunteers collected seeds from several gardens during September. Each packet was labelled with the plant name and collection date.\n\nB. The team placed the packets inside sealed containers to protect them from moisture. The containers were kept in a cool room at the community centre.\n\nC. In spring, pupils will plant a selection of the seeds and compare how many grow. The organisers will use those results to refine next year's collection process."),
    questions=(
        Question("Choose NO MORE THAN TWO WORDS from the passage: 'Packets were placed inside ___.'", ("inside sealed containers", "sealed containers", "the team placed"), 1, "Sealed containers is the exact two-word phrase needed after inside."),
        Question("Which paragraph describes a plan to evaluate the project's results?", ("A", "B", "C"), 2, "Paragraph C describes planting seeds, comparing growth, and using the results to improve the process."),
    ),
    assignment=Assignment("Explain why the longer completion loses the mark even though it contains the correct container. Then explain how you found the paragraph about evaluation.", 40,
        ("I followed the word limit and checked the completed sentence.", "I distinguished a detail-matching task from a heading task.", "I identified the actual evidence for evaluation."),
        "The longer answer adds inside, although the sentence already supplies it, and contains three words instead of the permitted two. Paragraph C describes comparing how many seeds grow and using the results to improve the next collection. I found the evaluation detail by matching its meaning rather than searching only for the word evaluation.", label="Your reading strategy notes"),
)

READING_BAND8 = Lesson(
    slug="reading-timing-and-trap-review", title="Protect your accuracy under time pressure", minutes=20,
    skill="Reading", level="Band 8 target",
    technique="Locate evidence → test every part of the claim → move on when stuck → return and check.",
    goal="Make accurate decisions about difficult claims and use a practical recovery routine during a timed test.",
    sections=(
        Section("Give difficult questions a limit", "Academic Reading gives sixty minutes for the whole test. A roughly twenty-minute budget per passage can be a starting practice plan, but adapt it to difficulty and your own results. When a question stops yielding new evidence, mark it to return to and move on. Leave time to check unanswered items and completion instructions."),
        Section("Check scope and comparison", "Before deciding that a claim matches, inspect words such as all, most, only, before, and more than. A study in two centres cannot automatically support a claim about every centre. A comparison also needs evidence for both sides. Treat an unmentioned explanation as missing information, not automatically as a contradiction."),
        Section("Review the decision that failed", "After a timed practice, record your chosen answer, the evidence, and the exact word or inference that led you astray. Separate language gaps from time-management problems. Rework the decision slowly, then apply the same check to a different passage. Simply repeating a familiar test can hide the original weakness."),
    ),
    example=Example("Text: The service improved in two pilot centres. Claim: It improved in every centre nationwide. → True", "The pilot result does not establish a nationwide result. Look for further evidence before choosing True, False, or Not Given.", "The claim changes the population being described. Limited evidence does not settle a broader claim by itself."),
    activity=Activity("reading", "A pilot with boundaries", "Two local centres introduced a shared appointment system. In both centres, average waiting times fell during the three-month trial. Neither centre changed its number of staff. The evaluation did not compare the centres with services outside the trial. Its authors recommended a wider study before claiming that the system would work equally well throughout the country."),
    questions=(
        Question("The trial centres employed more staff during the trial.", ("True", "False", "Not Given"), 1, "The passage explicitly says neither centre changed its number of staff, contradicting an increase."),
        Question("Waiting times at centres outside the trial also fell.", ("True", "False", "Not Given"), 2, "The evaluation gives no result for centres outside the trial. That absence is not a contradiction."),
    ),
    assignment=Assignment("Explain the distinction between the two answers. Then write your routine for a question that takes too long and one error-log entry you could reuse in a later test.", 50,
        ("I checked who and where each claim describes.", "I distinguished contradiction from missing evidence.", "I planned when to move on and how to review."),
        "The staffing claim is false because staff numbers did not change. The result outside the trial is not given because the passage reports only the pilot centres. When I cannot find new evidence, I will mark the question and return after answering others. My error log will remind me to check the population in a claim before extending a limited finding to other places.", label="Your timed-reading review"),
)

LISTENING_START = Lesson(
    slug="listening-predict-and-check", title="Prepare your ears before the recording starts", minutes=15,
    skill="Listening", level="Beginner",
    technique="Read ahead → predict the answer type → listen for the final detail → check spelling.",
    goal="Predict a number, name, or place and use corrections to identify the confirmed information.",
    sections=(
        Section("Use the question before the audio", "Read the available questions and identify what each needs: a price, a time, a person, or a location. Look at the words around a gap to predict its grammar. That preparation gives your attention a clear purpose when the recording begins."),
        Section("Wait for confirmation", "A speaker may mention an old price before giving a new one. Signals such as actually, instead, and sorry can change the answer. Keep listening until the detail is settled. In IELTS the recordings are played once; in these lessons, try once first and replay only for review."),
        Section("Do not lose the next answer", "If you miss a detail, move your attention to the next question instead of replaying the missed words in your head. Afterwards, compare your notes with the transcript. Check letters, plural endings, and any word limit when you practise completion tasks."),
    ),
    example=Example("It costs fifteen pounds, sorry, fifty pounds. → 15", "It costs fifteen pounds, sorry, fifty pounds. → 50", "The speaker's correction replaces the first amount. Predicting a price tells you which detail to focus on."),
    activity=Activity("listening", "Booking a weekend workshop", "Thank you for asking about the photography workshop. The old leaflet gives the price as thirty pounds, but that was last year's fee. This year the workshop costs forty pounds, including materials. We will meet in the studio beside the main entrance. The lecture hall is being used for a concert, so please do not wait there. You can bring a camera if you have one, but we also have a few available to borrow."),
    questions=(
        Question("What is this year's workshop fee?", ("30 pounds", "40 pounds", "50 pounds"), 1, "Thirty pounds was last year's price; the confirmed current fee is forty pounds."),
        Question("Where will participants meet?", ("The lecture hall", "Outside the concert entrance", "The studio beside the main entrance"), 2, "The studio is the meeting place. The lecture hall is a mentioned but unsuitable alternative."),
    ),
    assignment=Assignment("Explain what answer types you predicted, the confirmed details, and one distractor. Write what you will do if you miss an answer in a later recording.", 40,
        ("I read the questions before listening.", "I followed the correction to the final details.", "I have a recovery plan for a missed answer."),
        "I predicted a price and a place. The confirmed fee is forty pounds, and the meeting point is the studio beside the main entrance. Thirty pounds was an outdated price that could distract me. If I miss an answer, I will follow the next question instead of losing several details while worrying about the first.", label="Your listening strategy notes"),
)

LISTENING_MAPS = Lesson(
    slug="listening-follow-a-map", title="Follow directions and keep your position on a map", minutes=20,
    skill="Listening", level="Intermediate",
    technique="Find the starting point → orient the map → follow each movement → confirm the landmark.",
    goal="Track a route through a simple map and distinguish the correct landmark from a distractor.",
    sections=(
        Section("Orient before listening", "Locate the entrance, compass direction, and fixed labels. Imagine yourself at the starting point facing the stated direction. If the speaker turns, left and right refer to the traveller's new direction, not permanently to the left and right edges of the page."),
        Section("Follow relationships in order", "Track phrases such as opposite, beyond, on the corner, and just before. Keep following the route even when an answer seems obvious, because a later phrase can distinguish two similar locations. A building named in a route may simply be a landmark you pass."),
        Section("Review why a tempting location was wrong", "After checking, retrace the path while replaying the recording. Name the phrase that eliminated each distractor. Practise again on an unfamiliar map so that success depends on understanding directions rather than remembering a label."),
    ),
    example=Example("The speaker says 'walk past the café to the studio opposite the garden'. → Stop at the café.", "Continue beyond the café and identify the studio across from the garden.", "Past indicates movement beyond a landmark; opposite identifies the destination by its relationship to another place."),
    activity=Activity("listening", "Find two rooms on the campus map", "Begin at the south gate, facing north. Walk along the central path. At the first junction you will see the café on your left and the library on your right. Continue north without turning. The next pair of buildings is the studio on your left and the garden room on your right. Your photography session is in the building opposite the garden room. After the session, return towards the south gate. At the first junction you reach on the way back, turn east into the building where the books are kept. This is where you should return your visitor pass.", map_rows=(("Studio", "↑ North", "Garden room"), ("Café", "Central path", "Library"), ("", "South gate", ""))),
    questions=(
        Question("Where is the photography session?", ("The café", "The studio", "The garden room"), 1, "After passing the café and library, the studio is opposite the garden room."),
        Question("Where should visitors return their passes?", ("The library", "The south gate", "The studio"), 0, "On the return route, the first junction is beside the café and library. East leads to the library, described as the building with books."),
    ),
    assignment=Assignment("Trace the route from the gate to the session and then to the pass-return point. Explain how facing south on the return route changes which side is east.", 45,
        ("I used the map's north direction and starting gate.", "I treated passed buildings as landmarks rather than destinations.", "I retraced the return route with the changed direction."),
        "From the south gate I travel north past the café and library. The studio is on the west side, opposite the garden room. On the return route I face south, so east is now on my left. At the next junction I turn into the library to return the pass, using the reference to books to confirm the destination.", label="Your route review"),
)

LISTENING_BAND8 = Lesson(
    slug="listening-recover-and-audit", title="Stay with a lecture and stop losing easy marks", minutes=20,
    skill="Listening", level="Band 8 target",
    technique="Track the lecture structure → separate result from explanation → recover immediately → audit precision.",
    goal="Use signposting and an error audit to follow a lecture accurately on the first listen.",
    sections=(
        Section("Track the speaker's structure", "Listen for the move from background to method, result, limitation, and next step. Brief signposts such as to test this, we found, and however help you locate your place in a lecture. Note the relationship between ideas rather than attempting to transcribe every sentence."),
        Section("Keep the strength of the claim", "A recording may suggest a possible cause without proving it. It may also contrast an original prediction with an unexpected result. Do not replace may with definitely or some participants with everyone. The qualifying phrase can be as important as the central noun."),
        Section("Audit errors after one-play practice", "Classify a missed answer as a vocabulary gap, a distractor, a lost place, or an accuracy error such as spelling or an extra word. Find the decisive phrase in the transcript, then listen again to recognise it. Return to unfamiliar one-play material to see whether the correction carries over."),
    ),
    example=Example("We expected attendance to rise, but it remained unchanged. Satisfaction improved. → Attendance increased.", "Attendance stayed the same; satisfaction improved.", "The prediction is not the result. Following the contrast prevents a familiar phrase from becoming a false answer."),
    activity=Activity("listening", "Reviewing a reminder-system experiment", "The college tested an appointment reminder system in one department. Staff expected fewer missed appointments, but the overall number of missed appointments changed very little. What did change was the number of early cancellations. More students cancelled in advance, allowing staff to offer those places to other students. We should be cautious about assuming that reminders alone caused this change. During the trial, staff also introduced a simpler cancellation form. The next experiment will keep the form the same for everyone and compare groups receiving different kinds of reminders. For now, the practical benefit appears to be earlier notice, rather than a proven reduction in missed appointments."),
    questions=(
        Question("What practical improvement was observed?", ("Every student attended every appointment.", "Staff stopped accepting cancellations.", "More students cancelled early enough for places to be offered to others."), 2, "Early cancellations increased. The recording does not report a substantial fall in missed appointments."),
        Question("Why can the change not be confidently attributed to reminders alone?", ("The cancellation form also became easier to use.", "The college collected no information.", "All departments used exactly the same system."), 0, "The simplified form changed at the same time, so its effect needs to be separated from the reminders."),
    ),
    assignment=Assignment("Separate the prediction, observed result, and limitation. Identify a phrase that could have misled you and choose an error category and review step for it.", 50,
        ("I distinguished the prediction from the observed result.", "I retained the limitation on the causal explanation.", "I planned to test the improvement with unfamiliar audio."),
        "Staff predicted fewer missed appointments, but the observed improvement was earlier cancellation. The simpler form could have contributed, so reminders alone are not a proven cause. The phrase expected fewer missed appointments could mislead me if I missed the contrast that followed. I would classify this as a distractor error, replay the contrast, and test the strategy on an unfamiliar lecture.", label="Your listening accuracy review"),
)
