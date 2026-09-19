"""Original IELTS Academic preparation, from foundations to a Band 8 target.

Short drills teach individual skills; course completion is not a band assessment.
Format and assessment references were checked against IELTS.org in September 2026.
"""

from .course_types import Activity, Assignment, Course, Example, Lesson, Question, Section


IELTS_RESOURCES = (
    ("IELTS: Academic sample tests and listening audio", "https://ielts.org/take-a-test/preparation-resources/sample-test-questions/academic-test"),
    ("IELTS: Academic Reading format", "https://ielts.org/take-a-test/test-types/ielts-academic-test/ielts-academic-format-reading"),
    ("IELTS: Academic Writing format", "https://ielts.org/take-a-test/test-types/ielts-academic-test/ielts-academic-format-writing"),
    ("IELTS: Speaking format and assessment", "https://ielts.org/take-a-test/test-types/ielts-academic-test/ielts-academic-format-speaking"),
    ("IELTS: How band scores work", "https://ielts.org/take-a-test/your-results/ielts-scoring-in-detail"),
)


BEGINNER_COURSE = Course(
    slug="ielts-beginner",
    title="IELTS foundations",
    category="IELTS Academic",
    level="Beginner",
    practice_level="beginner",
    description="Start your IELTS journey with everyday English, manageable practice, and a study habit across listening, reading, speaking, and writing.",
    outcomes=(
        "Build a realistic weekly routine for all four skills.",
        "Listen for details, find evidence in a passage, and speak about familiar topics.",
        "Describe simple data and develop your first opinion paragraph.",
    ),
    project="A personal study plan, listening and reading notes, a spoken introduction, a data description, and an opinion paragraph.",
    resources=IELTS_RESOURCES,
    lessons=(
        Lesson(
            slug="build-your-study-habit", title="Build your IELTS study habit", minutes=12, skill="Study plan",
            goal="Understand the four skills and make a weekly plan you can actually follow.",
            sections=(
                Section("Know your destination", "IELTS tests listening, reading, writing, and speaking. These courses focus on Academic Reading and Writing; General Training uses different reading and writing tasks. Listening and Speaking are shared. A beginner should first build useful everyday English, then add exam timing as understanding improves."),
                Section("Small sessions with a purpose", "Try twenty minutes on five days: listen on Monday, read on Tuesday, speak on Wednesday, write on Thursday, and review on Friday. Keep an error log with the original mistake, a correction, and a new example. Course XP measures practice completed; it does not measure an IELTS band or promise a test result."),
            ),
            example=Example("I will learn every English word this weekend.", "On Monday I will listen to a short conversation, note three details, and check them against the transcript.", "The second goal names a task and a way to check it. It is small enough to repeat next week."),
            questions=(
                Question("Which plan covers all four IELTS skills?", ("Read a word list every day.", "Listen, read, speak, and write on separate days, then review mistakes.", "Only practise the skill you already enjoy."), 1, "A balanced routine gives each skill attention and makes room for review."),
                Question("What does finishing a course tell you?", ("Your official score is now Band 8.", "You no longer need speaking practice.", "You have completed the course activities and should check your skills with further practice."), 2, "Completion records practice. IELTS band scores require assessment of performance."),
            ),
            assignment=Assignment(
                "Write a five-day study plan. Give each day a skill, a small activity, and a way to review it. Name one difficulty you want to work on first.", 40,
                ("All four skills appear in my plan.", "Each activity has a realistic time and a review step.", "I have named one current difficulty."),
                "I can study for twenty minutes after dinner. On Monday I will listen and check three details. On Tuesday I will read a short article. On Wednesday I will describe my home aloud. On Thursday I will write a paragraph. On Friday I will correct my mistakes. Hearing numbers is my first priority.",
                label="Your study plan",
            ),
        ),
        Lesson(
            slug="listening-for-details", title="Listening: catch the important details", minutes=15, skill="Listening",
            goal="Pick out a time and a location, including a correction in a short announcement.",
            sections=(
                Section("Predict what you need", "Read the questions before you listen. A question about when needs a time or date; a question about where needs a place. You do not need to understand every word to find those details. Listen to the complete phrase so you do not confuse thirteen with thirty."),
                Section("Wait for the final information", "Speakers sometimes correct themselves. Words such as actually, sorry, and instead can introduce a change. Write the final confirmed detail. Try the training audio once before replaying it and opening the transcript to check what you missed."),
            ),
            example=Example("The trip is on Tuesday. Sorry, I mean Thursday. → Tuesday", "The trip is on Tuesday. Sorry, I mean Thursday. → Thursday", "The correction replaces the first day. A familiar word can be a distractor."),
            activity=Activity("listening", "A welcome session at the library", "Welcome to the town library. Our new student welcome session is on Saturday. It was planned for nine thirty, but the librarian will be in a meeting then, so we will begin at ten fifteen instead. Please come to the garden room on the ground floor. The computer room upstairs is being repaired. Bring a notebook and a pen. You do not need to bring your own books. The session is free, and it will finish before lunch."),
            questions=(
                Question("At what time will the welcome session begin?", ("9:30", "10:15", "12:00"), 1, "The announcement replaces nine thirty with ten fifteen because the librarian has a meeting."),
                Question("Where should students go?", ("The garden room", "The computer room", "The upstairs meeting room"), 0, "Students are asked to come to the garden room on the ground floor. The computer room is being repaired."),
            ),
            assignment=Assignment(
                "After listening, write the confirmed time, place, and one thing to bring in complete sentences. Explain which earlier detail could have confused you.", 30,
                ("I used the corrected time.", "I checked the place against the transcript after listening.", "I identified a distractor."),
                "The welcome session begins at ten fifteen in the garden room on the ground floor. I should bring a notebook and a pen. Nine thirty could confuse me because it is mentioned first, but the speaker changes that time.",
                label="Your listening notes",
            ),
        ),
        Lesson(
            slug="reading-for-evidence", title="Reading: find the evidence", minutes=15, skill="Reading",
            goal="Read for the main idea and distinguish a contradiction from missing information.",
            sections=(
                Section("Read with two purposes", "First skim a passage to understand its subject. Then scan for a detail named in a question. Read the sentence around that detail carefully. Similar meanings may use different words: free can mean costs nothing, and residents can mean people who live nearby."),
                Section("True, False, or Not Given", "True agrees with the passage. False contradicts it. Not Given means the passage does not settle the statement. Use the text as evidence, even if you know something else about the subject. A missing opening date does not prove that a proposed date is wrong."),
            ),
            example=Example("Passage: The café opens at eight. Statement: It opens at nine. → Not Given", "Passage: The café opens at eight. Statement: It opens at nine. → False", "An explicit different time is a contradiction. Not Given is used when there is not enough information."),
            activity=Activity("reading", "The neighbourhood garden", "A neighbourhood garden opens to visitors every Saturday morning. Local volunteers grow vegetables there and teach visitors how to look after small plants. Entry costs nothing, but visitors must bring their own containers if they want to take a plant home. A nearby school sends a group of pupils once a month. The volunteers hope to add a sheltered seating area next year. They have not yet decided how to pay for it."),
            questions=(
                Question("Visitors must pay to enter the garden.", ("True", "False", "Not Given"), 1, "Entry costs nothing, so the claim that visitors must pay is contradicted."),
                Question("The garden first opened in 2019.", ("True", "False", "Not Given"), 2, "The passage does not say when the garden first opened."),
            ),
            assignment=Assignment(
                "Summarise who uses the garden and what visitors can do there. Explain why one statement in the quiz is False and the other is Not Given.", 40,
                ("My summary uses only information in the passage.", "I have evidence for the contradiction.", "I have not invented an opening date."),
                "Local volunteers, visitors, and pupils use the garden. People can learn to look after plants without paying an entry fee. The payment statement is false because entry costs nothing. The date statement is not given because the passage never says when the garden opened.",
                label="Your reading notes",
            ),
        ),
        Lesson(
            slug="speaking-about-yourself", title="Speaking: answer, explain, and give an example", minutes=15, skill="Speaking",
            goal="Give a natural answer about your daily life and practise saying it aloud.",
            sections=(
                Section("Start with a direct answer", "In Speaking Part 1, familiar subjects include work, study, home, and interests. Answer the question first, then add a reason or a specific example. Two or three connected sentences can tell the listener much more than a single word."),
                Section("Make yourself easy to follow", "Speak at a comfortable pace. Stress important words and pause between ideas. You do not need a different accent to be clear. Use the timer for a short practice answer, then repeat with different wording rather than memorising a script."),
            ),
            example=Example("Do you enjoy cooking? Yes. Good.", "Yes, I enjoy cooking because it helps me relax. On Sundays I usually make vegetable soup with my sister.", "A direct answer, a reason, and a personal detail make the response easier to follow."),
            activity=Activity("speaking", "Your first speaking turn", "What do you enjoy doing in your free time? Say what it is, why you enjoy it, and when you last did it. Speak for about 45 seconds, then try again without reading a script. This is a short foundation drill, not a full Speaking test.", seconds=45, preparation_seconds=15),
            questions=(
                Question("Which answer develops 'Do you like your hometown?'", ("Yes.", "Yes, especially its parks. I walk there with my family at weekends.", "Hometown, hometown, hometown."), 1, "The second answer gives a clear response and a relevant personal example."),
                Question("What should you prioritise when practising pronunciation?", ("Speaking as fast as possible", "Copying an accent perfectly", "Making your words and ideas easy to understand"), 2, "Clear sounds, useful stress, and sensible pauses help the listener understand you."),
            ),
            assignment=Assignment(
                "After speaking aloud, note your main answer and one example you used. Name one word to pronounce more clearly or one place where you could pause.", 30,
                ("I answered aloud before writing these notes.", "I gave a reason or a personal example.", "I tried the answer again using my improvement."),
                "I talked about walking by the river because it helps me relax. My example was a walk with my brother last Sunday. I want to pronounce river more clearly and pause before explaining why I enjoy the activity.",
                label="Your speaking reflection",
            ),
        ),
        Lesson(
            slug="writing-describe-data", title="Writing Task 1: describe a simple change", minutes=20, skill="Writing",
            goal="Write accurate comparisons and a short overview using a small table.",
            sections=(
                Section("Describe what the data shows", "Academic Task 1 asks you to report visual information such as charts, tables, processes, or maps. Begin by identifying the subject and time period. Then give an overview of the main features and support it with selected details. Avoid inventing reasons for a change."),
                Section("Build towards the full task", "Use rose from X to Y, fell by X, and remained unchanged carefully. From and to name the start and end; by names the difference. This first drill asks for sixty words. A full Academic Task 1 requires at least 150 words, with about twenty minutes recommended."),
            ),
            example=Example("Bus journeys rose by 120 to 80.", "Bus journeys rose from 80 to 120, an increase of 40.", "The starting figure is 80 and the ending figure is 120. The increase is their difference."),
            activity=Activity("reading", "Practice data: journeys to a college", "Number of daily journeys in a small college survey:\nBus: 80 in 2020; 120 in 2025.\nBicycle: 40 in 2020; 90 in 2025.\nCar: 150 in 2020; 110 in 2025.\nThese are counts of journeys, not percentages. The data is invented for this exercise."),
            questions=(
                Question("Which sentence is an accurate overview?", ("Every mode became more popular.", "Bus and bicycle journeys rose, while car journeys fell.", "Car journeys disappeared completely."), 1, "Both bus and bicycle counts increased, while the car count fell from 150 to 110."),
                Question("How much did bicycle journeys increase?", ("By 50", "By 90", "By 40 percent"), 0, "The count rose from 40 to 90: 90 minus 40 is 50 journeys."),
            ),
            assignment=Assignment(
                "Write a short report about the table. Introduce the survey, give an overview, and compare at least two figures. This is a shortened foundation drill.", 60,
                ("I included an overview of the main changes.", "My numbers, units, and time periods are correct.", "I did not invent causes for the trends."),
                "The table compares daily journeys to a college by three forms of transport in 2020 and 2025. Overall, bus and bicycle journeys increased, while car journeys decreased. Bus journeys rose from 80 to 120. Bicycle journeys grew by 50, from 40 to 90. By contrast, car journeys fell from 150 to 110. Cars had the highest count at the start, but buses led in 2025. Bicycles remained the least common mode in both years.",
            ),
        ),
        Lesson(
            slug="writing-your-first-argument", title="Writing Task 2: build an opinion paragraph", minutes=20, skill="Writing",
            goal="State an opinion and develop it with a reason and a relevant example.",
            sections=(
                Section("Answer the actual question", "When a prompt asks whether you agree, make your position clear. Choose a reason you can explain. Ask how or why it supports your opinion, then give a plausible example. You can use your own experience; you do not need invented statistics or expert quotations."),
                Section("Connect the ideas", "Use because to give a reason and for example to introduce an illustration. Read your paragraph aloud to check that each sentence adds something. This eighty-word drill builds towards Task 2; a full task requires at least 250 words, with about forty minutes recommended."),
            ),
            example=Example("Libraries are good. Libraries are important. Libraries are very good.", "Libraries should stay open in the evening because many people work during the day. For example, an evening study room lets a shop assistant learn after a shift.", "The example explains how evening opening helps a particular person, instead of repeating the opinion."),
            questions=(
                Question("Which point supports evening library opening?", ("Some people need a quiet place to study after work.", "Libraries have existed for a long time.", "Many buildings have windows."), 0, "Access after working hours directly explains why evening opening would help."),
                Question("What should follow a main reason?", ("The same reason copied twice", "An explanation of how it works and a relevant example", "A statistic you invented"), 1, "Development connects the reason to the opinion and helps the reader understand its significance."),
            ),
            assignment=Assignment(
                "Do you agree that local libraries should open in the evening? Write an opinion paragraph with a reason, an explanation, and an example. This is a shortened foundation drill.", 80,
                ("My opinion answers the question.", "I explained my reason rather than repeating it.", "My example is relevant and my sentences connect."),
                "I agree that local libraries should open in the evening because many people cannot visit during the working day. An evening opening gives them a quiet place to read or study when their jobs are finished. For example, a shop assistant could use the library to prepare for an English test after work. This would be especially helpful if the assistant shares a small home with a large family. The library would make learning easier for people who have little time or space of their own.",
            ),
        ),
    ),
)


INTERMEDIATE_COURSE = Course(
    slug="ielts-intermediate", title="IELTS skill builder", category="IELTS Academic", level="Intermediate",
    practice_level="intermediate",
    description="Turn a foundation in English into confident IELTS practice. Follow arguments, recognise paraphrases, develop a long speaking turn, and write complete reports and essays.",
    outcomes=(
        "Use an error log to choose the practice that helps you most.",
        "Handle listening distractors, reading paraphrases, and a two-minute talk.",
        "Write a 150-word Academic Task 1 report and a 250-word Task 2 essay.",
    ),
    project="An evidence-based study plan and a portfolio of all four skills, including a full report and essay.",
    resources=IELTS_RESOURCES,
    lessons=(
        Lesson(
            slug="turn-mistakes-into-a-plan", title="Turn mistakes into a study plan", minutes=12, skill="Study plan",
            goal="Use the cause of a mistake to choose a useful next exercise.",
            sections=(
                Section("Diagnose before adding more tests", "For every missed answer, find the exact evidence and label the cause: unknown language, a distractor, an unsupported inference, a word-limit mistake, or lost time. In writing, check whether a paragraph answers the prompt before polishing vocabulary. For speaking, listen to a recording you make yourself or ask a partner which point was unclear."),
                Section("Practise, review, repeat", "Choose one weakness for a short focused session. Then try a different example without notes. Revisit it a few days later. Keep some weekly practice in every skill, with extra time for the weakest. When completing full writing tasks, budget about twenty minutes for Task 1 and forty for Task 2 within the sixty-minute Writing test."),
            ),
            example=Example("I got the listening answer wrong, so I need fifty more questions.", "I selected the first date before the speaker corrected it. I will practise three correction phrases, then try an unfamiliar announcement.", "The plan targets the cause of the error and tests whether the skill transfers to new material."),
            questions=(
                Question("You chose an answer because it repeated a word from the audio. What should you review?", ("Only the spelling of that word", "Whether the speaker confirmed or rejected the idea around that word", "How to guess more quickly"), 1, "A repeated word may be a distractor. Review the surrounding meaning and the final decision."),
                Question("Which is the strongest evidence of improvement?", ("Remembering the answer to an old question", "Buying another notebook", "Applying the same strategy successfully to an unfamiliar example"), 2, "A fresh example tests the underlying skill rather than recall of a previous answer."),
            ),
            assignment=Assignment(
                "Choose a recent or likely difficulty. Write a one-week plan with a focused exercise, a later review, a fresh example, and practice for your other three skills.", 50,
                ("I named a cause rather than only a low score.", "I included review and an unfamiliar task.", "All four skills have time in my week."),
                "My main difficulty is confusing missing information with a contradiction. On Monday I will underline evidence in a short passage. On Wednesday I will explain my wrong answers, and on Friday I will try a new passage. I will also listen on Tuesday, practise a long speaking turn on Thursday, and write and revise an essay at the weekend.",
                label="Your study plan",
            ),
        ),
        Lesson(
            slug="listening-follow-decisions", title="Listening: follow a changing decision", minutes=18, skill="Listening",
            goal="Recognise rejected suggestions and identify a speaker's final recommendation.",
            sections=(
                Section("Follow the direction of the conversation", "In a discussion, several options can be mentioned before a decision is made. Listen for turns such as initially, the trouble is, on balance, and we have agreed. Keep a possible answer in mind until the speaker confirms it."),
                Section("Match meaning, not just words", "A question may say accessible while a speaker says easy to reach by bus. Read the choices first and predict possible paraphrases. After answering, use the transcript to explain why each rejected choice is wrong. Then listen once more without looking."),
            ),
            example=Example("We could print a survey, but postage would be expensive. Let's use an online form. → printed survey", "We could print a survey, but postage would be expensive. Let's use an online form. → online form", "The first idea is rejected because of its cost. The final sentence confirms the method."),
            activity=Activity("listening", "A student project update", "Here is an update on our student research project. We originally intended to compare three city museums. After our tutor pointed out that travel would take too much time, we narrowed the project to the university museum. We considered interviewing the director, but she is away until next month. Instead, we will ask visitors to complete a short questionnaire after their visit. The museum can give us attendance figures as well, although these will only provide background information. Our main question is whether visitors find the displays easy to understand. We are not trying to measure how much historical knowledge they remember. The tutor has approved the new plan and asked us to test our questions with five volunteers first."),
            questions=(
                Question("What will be the main source of the students' research data?", ("An interview with the director", "Visitors' questionnaire responses", "Attendance figures from three museums"), 1, "The director is away. Visitors will complete the questionnaire; attendance figures are only background."),
                Question("What are the students primarily investigating?", ("The clarity of the displays", "How many dates visitors remember", "The cost of travelling to museums"), 0, "The speaker asks whether displays are easy to understand: this is a paraphrase of their clarity."),
            ),
            assignment=Assignment(
                "Summarise the final project and explain two rejected ideas. Include one paraphrase linking a quiz question to the recording.", 45,
                ("I identified the final research method.", "I explained why earlier ideas were dropped.", "I matched a meaning expressed in different words."),
                "The students will use visitor questionnaires at the university museum to investigate how clear its displays are. They dropped the three-museum comparison because travel would take too long, and the director cannot be interviewed because she is away. The phrase easy to understand expresses the same idea as clarity in the question.",
                label="Your listening notes",
            ),
        ),
        Lesson(
            slug="reading-paraphrases-and-headings", title="Reading: follow paraphrases and main ideas", minutes=20, skill="Reading",
            goal="Identify a paragraph's purpose and check the strength of a claim.",
            sections=(
                Section("Choose the heading for the whole paragraph", "A heading should capture the main idea, not a memorable example. After reading a paragraph, write a five-word summary before looking at headings. Notice whether the paragraph explains a problem, describes a method, contrasts views, or reports a result."),
                Section("Check the scope of the claim", "Words such as all, some, only, and may change meaning. Some people improved does not establish that everyone improved. In True/False/Not Given questions, use False only when the text contradicts the claim. Do not supply missing comparisons from your own knowledge."),
            ),
            example=Example("A paragraph describes staff learning new software, adjusting schedules, and sharing desks. Heading: The cost of one computer.", "Heading: How staff adapted to a new workplace.", "The wider heading includes all the paragraph's changes; the narrow one invents a focus on price."),
            activity=Activity("reading", "Testing a different working week", "A. A small design company tested a four-day working week for three months without reducing pay. Managers shortened routine meetings and set aside quiet periods for complex work. The aim was to preserve output while reducing unnecessary interruptions.\n\nB. At the end of the trial, completed projects remained at roughly the same level. Most staff reported feeling less tired, although two employees said that longer daily schedules made childcare more difficult. Managers therefore decided to offer several scheduling options instead of one timetable for everyone.\n\nC. The company has not published a calculation of its electricity savings. Its director also cautioned that a design office may be able to change schedules more easily than a business that must serve customers throughout the week. A longer trial is planned before any permanent policy is introduced."),
            questions=(
                Question("Which heading best fits paragraph B?", ("Staff reactions lead to a more flexible approach", "The history of electricity prices", "Why all employees rejected the trial"), 0, "Paragraph B reports mixed experiences and the resulting decision to offer scheduling options."),
                Question("The company saved more electricity than nearby businesses during the trial.", ("True", "False", "Not Given"), 2, "No electricity calculation or comparison with neighbouring businesses is provided."),
            ),
            assignment=Assignment(
                "Give each paragraph a short heading. Explain the evidence for your heading for B and why the electricity comparison cannot be confirmed.", 50,
                ("Each heading covers the paragraph's main purpose.", "I distinguished most staff from every employee.", "I avoided inventing a comparison."),
                "My headings are Trial design for A, Mixed experiences and flexible schedules for B, and Limits and next steps for C. Paragraph B links staff reactions to a decision about timetables. Most staff felt less tired, but two faced childcare problems. The electricity comparison is not given because the company has published no calculation and the passage gives no figures for other businesses.",
                label="Your reading notes",
            ),
        ),
        Lesson(
            slug="speaking-the-long-turn", title="Speaking Part 2: develop a long turn", minutes=18, skill="Speaking",
            goal="Use brief notes to organise a one-to-two-minute talk about an experience.",
            sections=(
                Section("Plan with keywords", "For the Part 2 long turn, you have one minute to prepare and speak for up to two minutes. Use the cue card to make a few keywords: who, where, what happened, and why it mattered. Full written sentences can tempt you to read rather than speak."),
                Section("Develop an experience", "Move from background to a specific event and then a reflection. When you run short, explain a detail or compare your feelings before and after. Natural transitions such as at first, a few days later, and looking back can help the listener follow your experience."),
            ),
            example=Example("I learned cooking. It was nice. It was very nice.", "At first I could only make rice. My cousin showed me how to prepare soup, and after a few tries I cooked dinner for my family. That small success made me less nervous about trying new recipes.", "The speaker develops a sequence and explains its significance instead of repeating an adjective."),
            activity=Activity("speaking", "Describe a useful skill you learned", "Describe a useful skill you learned. Say what the skill is, when and how you learned it, who helped you, and explain why it is useful to you. Prepare with keywords for one minute, then speak for one to two minutes.", seconds=120, preparation_seconds=60),
            questions=(
                Question("Which preparation notes are most useful for a spontaneous talk?", ("A complete essay to read word for word", "A list of unrelated advanced words", "Cooking — cousin — first soup — family dinner — confidence"), 2, "A short sequence of relevant keywords supports a connected answer without scripting every sentence."),
                Question("You have described the event but still have time. What can you add?", ("An explanation of why it mattered and how your feelings changed", "The same opening repeated", "An unrelated memorised introduction"), 0, "A reflection develops the topic and gives the listener a reason to care about the experience."),
            ),
            assignment=Assignment(
                "After your spoken turn, save the keywords you used and reflect on your organisation. Name one moment that needed a clearer explanation and practise that part again.", 40,
                ("I used the preparation time for keywords.", "I spoke aloud and developed the experience.", "I reviewed one specific improvement."),
                "My keywords were cycling, uncle, quiet street, first independent ride, and confidence. I moved from learning the basics to using the skill to visit friends. The middle needed a clearer example, so I repeated that part and explained how my uncle helped me balance without holding the bicycle.",
                label="Your speaking reflection",
            ),
        ),
        Lesson(
            slug="writing-task-one-report", title="Writing Task 1: group and compare data", minutes=25, skill="Writing",
            goal="Write a complete report with an overview and meaningful comparisons.",
            sections=(
                Section("Select the important features", "Begin with the subject, measure, and years. Identify the largest change, the highest or lowest category, and any reversal. An overview pulls those patterns together. Organise the detail paragraphs around comparisons instead of describing every figure in isolation."),
                Section("Keep the report factual", "Use past forms for completed past periods and preserve the units. An increase from twenty percent to thirty percent is ten percentage points; it is not a ten percent relative increase. Task 1 reports the supplied information, so avoid giving your own opinion or an unsupported cause."),
            ),
            example=Example("There were 30, then 20. Another number was 20 and then 35.", "Car travel fell from 30% to 20%, while cycling rose from 20% to 35% and became the leading mode.", "The comparison names the categories, keeps the units, and highlights a change in rank."),
            activity=Activity("reading", "Practice table: commuting to a campus", "Share of journeys to a campus, by main mode:\nCar: 30% in 2015; 20% in 2025.\nBus: 40% in 2015; 30% in 2025.\nBicycle: 20% in 2015; 35% in 2025.\nWalking: 10% in 2015; 15% in 2025.\nEach year's shares sum to 100%. These figures are invented for practice."),
            questions=(
                Question("Which overview best captures the main patterns?", ("Cars were the leading mode in both years.", "Cycling became the leading mode as car and bus shares fell; walking also rose.", "Every category increased by the same amount."), 1, "Cycling rose to 35%, above every other category. Cars and buses lost share while walking gained."),
                Question("How should the change in cycling's share be expressed?", ("An increase of 15 percentage points", "An increase of 15 journeys", "A fall of 20 percent"), 0, "35% minus 20% equals 15 percentage points. The table gives shares, not journey counts."),
            ),
            assignment=Assignment(
                "Summarise the table in at least 150 words. Select the main features and make relevant comparisons. Try drafting in twenty minutes, then review.", 150,
                ("My overview identifies the main shifts and leading mode.", "I grouped details and supported them with accurate figures.", "I used percentages and percentage points correctly."),
                "The table compares the proportions of journeys to a campus made by car, bus, bicycle and on foot in 2015 and 2025. Overall, the shares of car and bus travel declined, while cycling and walking became more common. Cycling replaced the bus as the most widely used mode by the end of the period.\n\nIn 2015, buses accounted for the largest share of journeys, at 40%, followed by cars at 30%. By 2025, both figures had fallen by ten percentage points, to 30% and 20% respectively. Together, these two modes represented half of all journeys in the later year, compared with 70% at the beginning.\n\nThe pattern for the remaining modes was different. Cycling increased from 20% to 35%, a gain of fifteen percentage points and the largest change in the table. Walking also rose, although more modestly, from 10% to 15%. Despite this growth, walking remained the least common way of reaching the campus in both years. The gap between cycling and walking therefore widened over the period.",
            ),
        ),
        Lesson(
            slug="writing-task-two-essay", title="Writing Task 2: develop a complete essay", minutes=45, skill="Writing",
            goal="Discuss two views, maintain your own position, and support it with developed reasons.",
            sections=(
                Section("Map every part of the prompt", "A discuss-both-views question with your opinion needs all three elements. Plan a reason for each view and decide where you stand. Your position should be clear in the introduction and consistent with the conclusion. You may prefer one view while recognising a useful point in the other."),
                Section("Give each paragraph a job", "Start a body paragraph with its main claim. Explain the mechanism, illustrate it, and relate it to the question. Use examples that a reader can understand without specialist knowledge. Leave a few minutes to check that you answered every instruction and corrected frequent grammar errors."),
            ),
            example=Example("Sports are good. Art is also good. Both are important things.", "Supporters of sports lessons emphasise health: regular activity helps pupils build habits that may continue outside school. A class that introduces several activities also lets children find one they enjoy.", "The developed version explains a benefit and gives a mechanism instead of making repeated broad claims."),
            questions=(
                Question("What does 'Discuss both views and give your own opinion' require?", ("Only the view you agree with", "Both views and a clear personal position", "A list of vocabulary about the topic"), 1, "The task contains three requirements. Covering only one view leaves part of the task unanswered."),
                Question("Which revision most improves a thin body paragraph?", ("Explain why the reason matters and add a relevant example", "Replace every common word with a rare word", "Add however to each sentence"), 0, "Development helps the reader follow the argument. Vocabulary and linking words should fit the meaning naturally."),
            ),
            assignment=Assignment(
                "Some people think schools should give more time to sport, while others think art and music deserve more time. Discuss both views and give your own opinion. Write at least 250 words, aiming for forty minutes.", 250,
                ("I discussed both views and made my opinion clear.", "Each body paragraph explains a reason with support.", "My conclusion follows the argument and my language is natural."),
                "Schools have limited time, and deciding how much to devote to sport, art and music can be difficult. Some people favour more physical activity, while others would protect creative subjects. Although sport makes an important contribution to health, I believe schools should maintain a balance so that children can develop different interests and abilities.\n\nThose who support more sport point to the value of regular exercise. Many pupils spend long periods sitting in classrooms and may continue sitting when they return home. A sports lesson gives every child a chance to move, including children whose families cannot afford a club. Team activities can also teach cooperation, because players need to communicate and support one another to achieve a shared goal. These are practical benefits that extend beyond the school field.\n\nArt and music offer a different but equally valuable form of development. They allow children to communicate ideas that they may find difficult to express in ordinary conversation. For example, a pupil who rarely speaks in class might gain confidence by helping to create a group performance. Creative lessons also encourage sustained attention: improving a drawing or learning a piece of music requires repeated attempts and careful observation. Removing this time could reduce opportunities for pupils whose strengths are less visible in academic or sporting tasks.\n\nIn my view, schools should provide regular access to both areas rather than expand one by sharply reducing the other. They can then offer optional clubs for children who want additional practice. A balanced timetable recognises that health, creativity and confidence all contribute to a useful education, and that different pupils discover their abilities through different activities.",
            ),
        ),
    ),
)


BAND8_COURSE = Course(
    slug="ielts-band-8", title="IELTS Band 8 preparation", category="IELTS Academic", level="Advanced · Target Band 8",
    practice_level="ielts_8_9",
    description="Work towards Band 8 with precise comprehension, nuanced arguments, flexible speaking, and deliberate revision. Build consistency across all four skills.",
    outcomes=(
        "Plan around skill-specific evidence and official assessment criteria.",
        "Follow qualified claims and speak with depth, clarity, and flexibility.",
        "Select key data, develop a nuanced essay, and revise recurring errors.",
    ),
    project="A targeted improvement plan, evidence-led listening and reading reviews, a spoken discussion, a report, and a revised essay.",
    resources=IELTS_RESOURCES,
    lessons=(
        Lesson(
            slug="plan-for-band-eight", title="Build a plan for a Band 8 target", minutes=15, skill="Study plan",
            goal="Separate a target score from evidence of readiness and choose your next priorities.",
            sections=(
                Section("Assess each skill separately", "A strong overall result can hide a weaker individual skill. Check whether your own goal calls for an overall band or a minimum in each section. Use fresh official sample tasks to review comprehension, and compare writing and speaking with the published criteria. These short lessons are focused drills, not full mock tests or official assessments."),
                Section("Aim for control, not decoration", "For a high-band target, develop ideas fully, organise them naturally, and choose precise language. In speaking, work on sustained coherence, flexible expression, grammatical control, and intelligibility. Review recurring errors until you can avoid them in unfamiliar tasks. Rare words and long sentences help only when they express the intended meaning accurately."),
            ),
            example=Example("My vocabulary is advanced, so every essay must be Band 8.", "My examples are relevant, but I leave one part of the prompt underdeveloped. I will plan all instructions before drafting and ask for feedback on my weakest paragraph.", "The second judgement identifies a specific limitation that vocabulary alone cannot resolve."),
            questions=(
                Question("Which is the best reason to change your preparation plan?", ("You found a list of very unusual words.", "Fresh tasks repeatedly reveal weak paragraph development and missed qualifications.", "You have completed the same familiar test several times."), 1, "Repeated problems on unfamiliar work reveal skills to improve, rather than an answer pattern to memorise."),
                Question("Does completing this course certify a Band 8 score?", ("Yes, XP converts directly to an IELTS band.", "Yes, if every quiz answer is correct.", "No. It records practice; readiness needs broader assessment."), 2, "Short quizzes and self-reviewed assignments do not assess the full range of IELTS performance."),
            ),
            assignment=Assignment(
                "Write an improvement plan for a Band 8 target. State your current evidence for each skill, two priorities, and how you will check progress with unfamiliar work and feedback. If you have no baseline yet, say how you will establish one.", 60,
                ("I distinguished a target from a measured result.", "My priorities come from evidence or a plan to collect it.", "I included unfamiliar tasks and feedback for productive skills."),
                "I have not yet established a reliable baseline, so I will begin with official sample tasks and ask for feedback on one essay and a recorded speaking response. My likely priorities are developing counterarguments and recognising qualified claims. I will check these against the results before deciding. Each week I will use unfamiliar listening and reading material, revise one written response, and repeat a speaking topic with a different example. I will track individual skills rather than assume an overall target describes them all.",
                label="Your Band 8 preparation plan",
            ),
        ),
        Lesson(
            slug="listening-qualified-claims", title="Listening: hear the limits of a claim", minutes=20, skill="Listening",
            goal="Distinguish a promising result from a proven cause and follow an academic qualification.",
            sections=(
                Section("Listen beyond the headline", "An academic speaker may present a positive finding and then restrict its interpretation. Listen for although, only in, may reflect, and cannot yet conclude. A result can be real within one study while still being uncertain in other settings."),
                Section("Separate result, explanation, and recommendation", "Keep three short notes: what was observed, what might explain it, and what should happen next. A tempting answer often upgrades an association into a cause or turns a cautious proposal into a firm recommendation. Check the strength of the speaker's language before deciding."),
            ),
            example=Example("Participants who used the app read more, although they volunteered for the trial. → The app makes everyone read more.", "The trial found higher reading among users, but volunteer selection limits a causal conclusion.", "The observation is narrower than the claim that the app caused improvement for everyone."),
            activity=Activity("listening", "A lecture on urban cooling research", "Today we will look at a pilot study of shaded bus stops. Researchers measured afternoon temperatures at twelve stops with newly installed trees and twelve stops without them. The shaded stops were cooler on average, and passengers reported greater comfort. This is encouraging, but it is not enough to show that planting trees will have the same effect everywhere. The shaded stops also had lighter paving, which may have contributed to the difference. In addition, the measurements covered just two weeks during a relatively mild summer. The team does not recommend abandoning tree planting; it recommends separating the effects of shade and surface materials in the next study. Researchers plan to compare otherwise similar stops over several seasons and to record the cost of maintaining the trees. A decision about expanding the programme should take both comfort and maintenance into account, rather than temperature measurements alone."),
            questions=(
                Question("Why is the lecturer cautious about attributing all the cooling to trees?", ("Passengers disliked every shaded stop.", "No temperature measurements were taken.", "The shaded stops also had different paving."), 2, "Lighter paving could contribute to cooling, so the pilot does not isolate the effect of trees."),
                Question("Which next step does the lecturer support?", ("A comparison across seasons that separates shade from surface effects", "Immediate expansion based only on temperature", "Abandoning tree planting entirely"), 0, "The proposed study compares otherwise similar stops across seasons and includes maintenance costs."),
            ),
            assignment=Assignment(
                "Summarise the observation, two limits on its interpretation, and the proposed next study. Explain how one incorrect answer overstates the lecture.", 55,
                ("I separated the observed result from a causal claim.", "I included the paving difference and short observation period.", "I preserved the speaker's cautious recommendation."),
                "Shaded stops were cooler and passengers reported greater comfort. However, lighter paving could partly explain the cooling, and measurements covered only two weeks in a mild summer. The next study should compare similar stops across seasons and examine maintenance costs. Immediate expansion based only on temperature would overstate the lecture, which calls for stronger evidence and a broader decision.",
                label="Your listening analysis",
            ),
        ),
        Lesson(
            slug="reading-evaluate-an-argument", title="Reading: evaluate an argument precisely", minutes=22, skill="Reading",
            goal="Track a writer's position and distinguish qualified agreement from a universal claim.",
            sections=(
                Section("Track who holds each view", "A passage can describe an advocate's argument before the writer challenges it. Mark the source of a view: supporters, critics, or the writer. For Yes/No/Not Given questions, decide whether the statement matches the writer's claim, contradicts it, or is not established."),
                Section("Preserve qualifications", "Compare every part of a claim: who, what, when, and under which conditions. A proposal that may work with safeguards is not an endorsement without conditions. Outside knowledge, however reasonable, cannot replace the writer's evidence. Read the surrounding argument when a single sentence seems ambiguous."),
            ),
            example=Example("The writer says digital access can help when training is available. → Digital access always solves exclusion.", "The writer supports digital access conditionally and treats training as part of the solution.", "The qualification controls the claim. Removing it produces a stronger position than the writer expresses."),
            activity=Activity("reading", "When a public service goes digital", "Supporters of moving public services online often emphasise convenience. A resident can renew a permit without taking time away from work, while staff can spend less time entering routine information. These advantages are substantial, and there is little reason to preserve a slow process simply because it is familiar.\n\nHowever, convenience for one group does not establish accessibility for everyone. Some residents share devices, have unreliable connections, or need assistance interpreting a form. A well-designed website may remove several barriers while leaving others untouched. Counting completed online applications therefore tells us relatively little about people who abandoned the process before submitting anything.\n\nThe strongest case for digital provision is consequently a conditional one. Authorities should simplify common transactions online while preserving a workable assisted route. This need not mean keeping every existing office unchanged. Shared support desks, telephone assistance, or scheduled local visits may serve residents more effectively, depending on local circumstances.\n\nEvaluation should examine both successful use and exclusion. Researchers could ask who needs repeated help, whether errors are resolved, and how much time different groups spend completing the same task. Without such evidence, claims that a service has become universally accessible confuse a convenient channel with a complete solution. Digital provision deserves expansion when these practical conditions are addressed; its value is weakened by treating it as sufficient on its own."),
            questions=(
                Question("The writer believes an online service alone is sufficient for every resident.", ("Yes", "No", "Not Given"), 1, "The writer explicitly argues for an assisted route and rejects the idea that digital provision is sufficient by itself."),
                Question("The writer says telephone assistance costs less than every kind of support desk.", ("Yes", "No", "Not Given"), 2, "The passage lists possible assistance channels but never ranks their costs."),
            ),
            assignment=Assignment(
                "Summarise the writer's position, identify its condition, and explain the evidence behind both quiz answers. Suggest one piece of information that would be needed to settle the cost comparison.", 65,
                ("I represented the writer's own position accurately.", "I retained the need for an assisted route.", "I separated a contradiction from an absent cost comparison."),
                "The writer supports expanding digital services when authorities also address exclusion and provide practical assistance. Online convenience alone is not sufficient, so the universal claim contradicts the argument. The claim about telephone costs is not given because no comparative costs appear. To settle it, we would need comparable figures for telephone support and each kind of support desk, including the resources required to handle similar requests. The writer's proposal is conditional support for digital provision, rather than an unconditional endorsement.",
                label="Your reading analysis",
            ),
        ),
        Lesson(
            slug="speaking-explain-and-qualify", title="Speaking Part 3: explain and qualify a view", minutes=20, skill="Speaking",
            goal="Develop an abstract answer with a mechanism, a counterpoint, and a clear conclusion.",
            sections=(
                Section("Move from personal experience to wider ideas", "Part 3 explores broader issues linked to a topic. Start with a direct view, explain why it might hold, and illustrate it. You can distinguish groups or circumstances: a change may help commuters but create difficulties for people with limited internet access."),
                Section("Be flexible without losing direction", "Use a qualification when it improves accuracy, not as a memorised phrase. If you cannot recall a word, explain the idea in simpler terms. Keep a natural pace, stress key contrasts, and avoid restarting every sentence to correct a minor slip. Record yourself separately if you want to review pronunciation."),
            ),
            example=Example("Technology is always beneficial because technology is very beneficial for everybody.", "Technology can make public services easier to reach, particularly for people who work long hours. However, an online system still needs an assisted route for residents who cannot use it independently.", "The answer explains who benefits and introduces a relevant limit without abandoning its main point."),
            activity=Activity("speaking", "Discuss access to public services", "Should public services move entirely online? Explain a benefit, consider a group that could be disadvantaged, and propose a practical balance. Then answer a follow-up aloud: How could a local authority tell whether its new system is successful? Use two minutes for the main discussion drill. Real Part 3 is an interactive discussion; this is individual rehearsal.", seconds=120),
            questions=(
                Question("Which qualification strengthens an argument for online services?", ("They can help, provided that people who need assistance can still obtain it.", "Every technological change is perfect.", "There are advantages and disadvantages, and that is everything."), 0, "The condition is specific and directly addresses an access problem."),
                Question("What is a useful response when a precise word will not come to mind?", ("Stop the answer entirely.", "Explain the idea clearly using other words.", "Repeat an unrelated difficult word."), 1, "Paraphrasing keeps communication moving and demonstrates flexible use of language."),
            ),
            assignment=Assignment(
                "After answering the main question and follow-up aloud, record your argument in notes. Identify a useful qualification, a successful paraphrase, and one aspect of delivery to practise again.", 50,
                ("I answered both questions aloud.", "My examples and qualifications supported my position.", "I reviewed clarity, pace, and one specific improvement."),
                "I supported expanding online services while keeping help available. My qualification concerned residents who share devices or cannot understand a form independently. I paraphrased accessibility as being able to complete a task without unnecessary barriers. For the follow-up, I suggested tracking failed applications as well as successful ones. I need to pause before my counterpoint so that the contrast is easier to follow.",
                label="Your speaking reflection",
            ),
        ),
        Lesson(
            slug="writing-task-one-precision", title="Writing Task 1: select, compare, and stay precise", minutes=25, skill="Writing",
            goal="Write a selective overview and support it without inventing patterns between data points.",
            sections=(
                Section("Select a useful organising principle", "High-quality reporting makes the most important features easy to see. Group categories by a shared pattern or a useful contrast, then support the overview with enough evidence. Do not let a long list of figures obscure the larger changes."),
                Section("Respect what the data cannot show", "Two observations show a change between points, not a steady change throughout the period. Avoid steadily unless intermediate observations support it. Keep the measure clear and distinguish a change in percentage points from a proportional change. Check that every comparison uses compatible units and periods."),
            ),
            example=Example("The share rose steadily every year from 20% to 35%, according to two observations ten years apart.", "The share rose from 20% to 35% between the two recorded years.", "Two endpoints do not establish what happened in every intervening year."),
            activity=Activity("reading", "Practice table: electricity sources", "Share of electricity generated in three regions:\nNorth — renewable: 20% in 2010, 55% in 2025; other sources: 80%, 45%.\nCentral — renewable: 35% in 2010, 50% in 2025; other sources: 65%, 50%.\nSouth — renewable: 10% in 2010, 40% in 2025; other sources: 90%, 60%.\nOnly these two years were measured. The table does not show total electricity output or individual fuels. The figures are invented for practice."),
            questions=(
                Question("Which overview is fully supported?", ("Every region increased total electricity production.", "Renewable shares rose everywhere; North overtook Central, while South remained lowest.", "Renewable generation rose steadily every year."), 1, "The shares and rankings are supported. Total output and changes between the two years are not reported."),
                Question("Which region had the largest increase in renewable share?", ("North, at 35 percentage points", "Central, at 50 percentage points", "South, at 40 percentage points"), 0, "North rose from 20% to 55%, a 35-point increase, compared with 15 in Central and 30 in South."),
            ),
            assignment=Assignment(
                "Summarise the table in at least 150 words, selecting the main features and making comparisons. Aim for twenty minutes, then check every claim against the data.", 150,
                ("My overview covers common growth and the change in ranking.", "I selected figures to support meaningful comparisons.", "I avoided claims about total output, individual fuels, or steady annual growth."),
                "The table compares the shares of electricity generated from renewable and other sources in three regions in 2010 and 2025. Overall, renewables gained share in every region. North overtook Central to record the largest renewable proportion in the later year, while South retained the smallest share despite substantial growth.\n\nIn 2010, Central led with 35% of its electricity coming from renewable sources, compared with 20% in North and 10% in South. By 2025, North's figure had reached 55%, an increase of 35 percentage points and the largest gain recorded. Central's share rose more modestly, by fifteen points, to exactly half of its electricity generation.\n\nSouth also experienced a sizeable shift, with its renewable share increasing by thirty percentage points to 40%. Other sources nevertheless remained dominant there, accounting for the remaining 60% in 2025. In contrast, these sources had become the smaller component in North, at 45%, while Central's electricity was divided equally between the two categories. The figures describe the composition of generation rather than the total amount produced.",
            ),
        ),
        Lesson(
            slug="writing-task-two-nuance", title="Writing Task 2: develop a nuanced position", minutes=45, skill="Writing",
            goal="Build a clear argument, address a counterargument, and revise for precision and control.",
            sections=(
                Section("Decide exactly how far you agree", "A to-what-extent prompt allows full or partial agreement. Define the scope of your position, then make each paragraph advance it. A counterargument is useful when you explain how it changes or limits your conclusion; merely mentioning the opposite view adds little depth."),
                Section("Revise meaning before decoration", "First check whether the response addresses the whole prompt and develops its main ideas. Then check paragraph progression, reference words, and vocabulary precision. Finally inspect recurring grammar problems, including articles, agreement, and sentence boundaries. Complex structures should carry a useful relationship, not exist only to appear advanced."),
            ),
            example=Example("Public transport should be free because free things are good. Cars are bad. This proves it.", "Free fares can remove a cost barrier, but their effect depends on service quality. A commuter is unlikely to leave a car at home if the alternative bus runs only once an hour.", "The argument explains a mechanism and its limit, creating a reasoned basis for a qualified position."),
            questions=(
                Question("Which thesis answers 'To what extent do you agree?' with a clear qualification?", ("There are many opinions in modern society.", "I support targeted fare reductions, but reliable services should take priority over making every journey free.", "Transport is an increasingly contemporary phenomenon."), 1, "The thesis states a policy preference and the condition that limits support for free travel."),
                Question("Which revision should come first?", ("Insert a rare synonym in every sentence.", "Make every sentence longer.", "Check that each paragraph develops an idea relevant to the prompt."), 2, "Relevance and development are the foundation. Word choice and grammar then make that argument precise."),
            ),
            assignment=Assignment(
                "Governments should make all public transport free to reduce the use of private cars. To what extent do you agree or disagree? Write at least 250 words in about forty minutes, then revise one paragraph for development and precision.", 250,
                ("My position states how far I agree and remains consistent.", "I developed mechanisms, examples, and a relevant counterargument.", "I revised one paragraph and checked recurring language errors."),
                "Making public transport free is often proposed as a way to persuade drivers to leave their cars at home. Although removing fares would benefit some passengers, I only partly agree with this policy. Reliable services and targeted financial support are likely to be more useful priorities than free travel for everyone.\n\nThe strongest argument for eliminating fares is that price can prevent people from using an otherwise suitable service. A worker who makes several journeys each day may find the combined cost difficult to manage, especially when changing between operators. Free travel would remove this obstacle and could also simplify boarding. For people on low incomes, the benefit would extend beyond commuting by making education and essential appointments easier to reach. These gains should not be dismissed simply because some current passengers would have paid anyway.\n\nHowever, cost is only one reason why people drive. A parent who must reach a workplace after taking a child to school may need connections that the existing network does not provide. Even a free bus will be unattractive if it is infrequent or routinely delayed. If replacing fare income leaves less money for vehicles, maintenance or additional routes, the policy could weaken the very service it is intended to promote. Its success therefore depends on secure funding and an understanding of local travel needs.\n\nI would favour affordable fares, with free or heavily discounted travel for groups who need it most, alongside investment in frequency and useful connections. Where a government can fund both excellent services and universal free travel, the broader policy may be reasonable. In many places, though, making public transport a practical alternative should come before removing its price entirely. This approach addresses both the financial and everyday barriers that influence whether people continue to rely on private cars.",
            ),
        ),
    ),
)


IELTS_COURSES = (BEGINNER_COURSE, INTERMEDIATE_COURSE, BAND8_COURSE)
