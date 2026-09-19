"""Original, self-contained lessons. Stable slugs are used for saved progress."""

from __future__ import annotations

from .course_types import Assignment, Course, Example, Lesson, Question, Section
from .ielts_courses import IELTS_COURSES


PARTICIPLES_COURSE = Course(
    slug="participles",
    title="English participles",
    category="Grammar",
    level="Beginner to advanced",
    description="Use forms such as running and written to build verb phrases, describe people and things, and connect ideas clearly.",
    outcomes=(
        "Recognise present and past participles, including irregular forms.",
        "Use participles in continuous, perfect, and passive constructions.",
        "Write precise descriptions and participle clauses with clear subjects.",
    ),
    project="A short scene using participles in verb phrases, descriptions, and a clearly connected clause.",
    resources=(
        ("Cambridge: Verb forms", "https://dictionary.cambridge.org/uk/grammar/british-grammar/verb"),
        ("Cambridge: Verbs — basic forms", "https://dictionary.cambridge.org/uk/grammar/british-grammar/verbs-basic-forms"),
        ("British Council: Adjectives ending in -ed and -ing", "https://learnenglish.britishcouncil.org/free-resources/grammar/a1-a2/adjectives-ending-ed-ing"),
        ("British Council: Participle clauses", "https://learnenglish.britishcouncil.org/free-resources/grammar/c1/participle-clauses"),
    ),
    lessons=(
        Lesson(
            slug="present-and-past-participles",
            title="Meet present and past participles",
            minutes=10,
            goal="Recognise participle forms such as running, played, and written.",
            sections=(
                Section("Two forms to recognise", "A participle is a verb form used in a larger verb phrase or a description. The present participle ends in -ing: running, writing, playing. Regular past participles end in -ed, as in played. Irregular ones include written, taken, and seen. Learn irregular verbs as a set: write, wrote, written."),
                Section("A form is not a tense", "The names 'present participle' and 'past participle' do not tell you the time by themselves. In 'Noor was running', running is a present participle, but was places the action in the past. Compare 'I wrote a note yesterday' with 'I have written a note': wrote is a simple past form; written is a past participle."),
                Section("Notice the job of an -ing form", "The same -ing form can have different jobs. In 'Noor is running', it helps form a continuous verb phrase. In 'Running keeps Noor fit', it names an activity and works as the subject; traditional grammar calls this use a gerund. Read the whole sentence before deciding what the form does."),
            ),
            example=Example(
                "Noor is run around the park. She has wrote a note about her route.",
                "Noor is running around the park. She has written a note about her route.",
                "After is, running forms the continuous verb phrase. After has, use the past participle written, rather than the simple past form wrote.",
            ),
            questions=(
                Question("Which word is the present participle in 'Noor was running along the path'?", (
                    "was",
                    "running",
                    "path",
                ), 1, "Running is the -ing participle. Was is the helper verb that places the continuous action in the past."),
                Question("Which form is the past participle of 'write'?", (
                    "wrote",
                    "writing",
                    "written",
                ), 2, "The forms are write, wrote, written. Use written after have or has when forming a perfect construction."),
            ),
            assignment=Assignment(
                "Write two or three sentences about preparing for an activity. Use one continuous phrase such as 'am practising' and one perfect phrase such as 'have written'. Check the participle in each phrase.",
                20,
                ("My -ing participle follows a suitable form of be.", "My perfect phrase uses have or has plus a past participle.", "I checked any irregular past participles."),
                "I am practising a short talk for our reading group. I have written three notes to help me remember the main points, and my friend is checking them.",
            ),
        ),
        Lesson(
            slug="participles-in-verb-phrases",
            title="Build continuous, perfect, and passive forms",
            minutes=12,
            goal="Choose the participle that fits the verb phrase and the meaning.",
            sections=(
                Section("Continuous: be plus -ing", "Use a form of be with a present participle to present an action as in progress: 'Noor is writing' or 'Noor was writing'. The helper verb carries tense and agreement. In an ordinary complete sentence, 'Noor writing a note' needs a helper such as is or was."),
                Section("Perfect: have plus a past participle", "Use have, has, or had with a past participle to look back from a reference time. 'Noor has written the note' presents the completed note as relevant now. 'Noor had written the note before the call' places the writing before another past event. Written stays the same; the helper changes."),
                Section("Passive: be plus a past participle", "A passive construction presents the subject as receiving an action: 'The note was written by Noor.' Compare 'Noor was writing the note', where Noor was doing the writing. A past participle is not automatically passive: in 'Noor has written the note', Noor is still the writer."),
            ),
            example=Example(
                "At six, Noor was written the instructions. By seven, she had wrote them. The instructions were print by her brother.",
                "At six, Noor was writing the instructions. By seven, she had written them. The instructions were printed by her brother.",
                "Was writing shows an action in progress, had written looks back at its completion, and were printed describes an action performed on the instructions.",
            ),
            questions=(
                Question("Choose the correct form: 'By the time we arrived, Noor had ___ the instructions.'", (
                    "wrote",
                    "writing",
                    "written",
                ), 2, "Had needs the past participle written. Wrote is the simple past form, and writing belongs to a different construction."),
                Question("Which sentence presents the report as receiving the action?", (
                    "The report was checked by two editors.",
                    "Two editors were checking the report.",
                    "Two editors have checked the report.",
                ), 0, "Was checked is passive: the report receives the checking. In the other sentences, the editors are the subjects carrying out the action."),
            ),
            assignment=Assignment(
                "Write three connected sentences about preparing something: show an action in progress, an action completed before another past event, and something receiving an action. Use 'was/were + -ing', 'had + past participle', and a passive phrase.",
                25,
                ("My continuous phrase uses an -ing participle.", "Had is followed by the past participle, not the simple past form.", "The subject of my passive phrase receives the action."),
                "I was arranging the chairs while Noor welcomed our guests. She had written the programme before the doors opened. The printed copies were placed on each seat by my brother.",
            ),
        ),
        Lesson(
            slug="participles-as-adjectives",
            title="Describe people and things with participles",
            minutes=10,
            goal="Use participles as adjectives and distinguish meanings such as interested and interesting.",
            sections=(
                Section("Give a noun a useful description", "Participles can work as adjectives: a smiling child, a damaged box, a written invitation. A description can also follow the noun, as in 'the guests waiting outside' or 'the invitation written by Noor'. Keep the description close to the noun it belongs to."),
                Section("Distinguish a feeling from its cause", "With pairs such as interested/interesting and excited/exciting, the -ed adjective describes the feeling and the -ing adjective describes what causes it. 'I was interested in the talk' describes my response. 'The speaker was interesting' describes the speaker's effect on listeners. People can cause feelings too, so -ing adjectives can describe people."),
                Section("Use meaning, not only the ending", "The feeling/cause pattern applies to those adjective pairs, not to every participle. A broken window has no emotion. A running engine describes an activity; a repaired engine describes the result of a repair. Ask what you want the reader to understand about the noun."),
            ),
            example=Example(
                "I enjoyed the talk, but I described my reaction by saying, 'I was very interesting.'",
                "I was very interested in the talk. The speaker gave an interesting explanation of the photographs displayed behind her.",
                "Interested describes the listener's reaction; interesting describes the explanation's effect. Displayed tells us which photographs the writer means.",
            ),
            questions=(
                Question("Choose the adjective that describes Noor's reaction: 'The unexpected ending made Noor feel ___.'", (
                    "surprising",
                    "surprised",
                    "surprise",
                ), 1, "Surprised describes Noor's feeling. The ending was surprising because it caused that reaction."),
                Question("What does 'an inspiring teacher' mean?", (
                    "A teacher who makes other people feel inspired.",
                    "A teacher who must be feeling inspired.",
                    "An incorrect phrase because -ing adjectives cannot describe people.",
                ), 0, "Inspiring describes the effect the teacher has on others. An -ing adjective can describe a person who causes a feeling."),
            ),
            assignment=Assignment(
                "Describe a class, event, or visit. Use a feeling/cause pair such as interested/interesting, and add a participle description of a thing, such as 'a written note' or 'the pictures displayed near the door'.",
                25,
                ("My feeling adjective describes the person experiencing the feeling.", "My -ing adjective identifies what causes the feeling.", "My other participle description belongs clearly to its noun."),
                "I was interested in the artist's explanation of her work. Her interesting stories helped me understand the paintings displayed near the entrance. I kept the written guide so I could read more at home.",
            ),
        ),
        Lesson(
            slug="participle-clauses-and-clear-subjects",
            title="Connect ideas with a clear subject",
            minutes=15,
            goal="Write present, past, and perfect participle clauses without confusing who does the action.",
            sections=(
                Section("Connect related ideas", "An introductory participle clause can add a related action or description: 'Carrying a box, Noor opened the door with her elbow.' The -ing clause describes Noor's action. A past participle clause often has passive meaning: 'Written in large letters, the sign was easy to read.' The sign received the writing."),
                Section("Make the subject fit", "For the introductory clauses practised here, the understood subject must match the subject of the main clause. In 'Walking into the hall, the paintings caught my attention', the wording makes the paintings seem to be walking. Name the walker immediately after the comma, or write a full clause that names both subjects."),
                Section("Show an earlier action", "Having plus a past participle marks an action completed before the main one: 'Having checked the tickets, Noor opened the doors.' Use it when that sequence matters. If the order, reason, or subject is unclear, use a full clause with after, because, or while. Do not compress a sentence at the cost of its meaning."),
            ),
            example=Example(
                "Walking into the hall, the paintings caught my attention.",
                "Walking into the hall, I noticed the paintings.",
                "I is now the subject of both walking and noticed. Another clear option is 'As I walked into the hall, the paintings caught my attention.' That version gives each clause its own subject.",
            ),
            questions=(
                Question("Which sentence makes the subject of the introductory clause clear?", (
                    "Carrying a heavy bag, the door was difficult to open.",
                    "Carrying a heavy bag, Noor pushed the door with her shoulder.",
                    "Carrying a heavy bag, the rain began to fall.",
                ), 1, "Noor is the person carrying the bag and pushing the door. The other sentences attach carrying to subjects that cannot carry that bag."),
                Question("What does 'Having written the note, Noor left it on the desk' tell us?", (
                    "Noor wrote the note after leaving it on the desk.",
                    "Someone else wrote the note while Noor waited.",
                    "Noor finished writing the note before leaving it on the desk.",
                ), 2, "Having written is a perfect participle clause. It places Noor's completed writing before her action in the main clause."),
            ),
            assignment=Assignment(
                "Write a short scene about preparing for a visit or event. Include a continuous or perfect verb phrase, a participle used as a description, and an introductory participle clause. Check which subject each clause describes.",
                40,
                ("I used a correct participle in my verb phrase.", "My description clearly belongs to a person or thing.", "My introductory participle clause and main clause share the intended subject.", "The sequence of events is clear."),
                "Having written the welcome note, Noor placed it beside the door. Her brother was arranging the chairs while she checked the table. The flowers delivered that morning stood in a blue vase. Smiling at the first visitor, Noor stepped forward to offer a seat.",
            ),
        ),
    ),
)


WRITING_COURSE = Course(
    slug="better-writing",
    title="Write better English",
    category="Writing",
    level="Beginner to intermediate",
    description="Turn your ideas into clear sentences, connected paragraphs, and a polished short piece.",
    outcomes=(
        "Choose a purpose and write for a particular reader.",
        "Use precise words and develop ideas with useful detail.",
        "Connect paragraphs and revise your own writing.",
    ),
    project="A short recommendation for improving a familiar place, revised for clarity and flow.",
    resources=(
        ("Purdue OWL: Concision", "https://owl.purdue.edu/owl/general_writing/academic_writing/conciseness/index.html"),
        ("Purdue OWL: On paragraphs", "https://owl.purdue.edu/owl/general_writing/academic_writing/paragraphs_and_paragraphing/index.html"),
    ),
    lessons=(
        Lesson(
            slug="purpose-and-clear-sentences",
            title="Start with a purpose and a clear sentence",
            minutes=10,
            goal="Tell your reader what matters, using a specific subject and a useful verb.",
            sections=(
                Section("Choose your reader", "Before drafting, finish this sentence: I want this reader to understand or do ___. A message to a friend and a request to a manager need different details. For this course, imagine asking the person who runs a library, school, or workplace to make one practical improvement."),
                Section("Put the action where readers can find it", "Name who does what: 'The library closes at six.' A direct verb often makes an action easier to see than a phrase such as 'makes a decision about'. Active voice is useful when the actor matters; passive voice is useful when the action or affected person deserves attention."),
                Section("Be precise without changing the meaning", "Replace empty phrases with information the reader can use. 'Soon' may need a date; 'better facilities' may need an example. A shorter sentence is only an improvement if it keeps the necessary meaning. Do not invent details just to sound specific."),
            ),
            example=Example(
                "I am writing this message in order to say that the room has some problems that need attention.",
                "Please repair the two broken lights in the reading room before Friday's evening class.",
                "The revision gives the reader an action, a location, and a deadline. These details are part of this imagined situation; in your own writing, use details you know.",
            ),
            questions=(
                Question("Which request gives a caretaker the clearest action?", (
                    "Something should be done about the place.",
                    "Please replace the broken lock on the study-room door.",
                    "There are a variety of important issues to consider.",
                ), 1, "Replacing a named lock is a specific action. The other requests leave the reader guessing what needs attention."),
                Question("Which revision keeps the meaning of 'The team made a decision to postpone the meeting'?", (
                    "The team cancelled every meeting.",
                    "The meeting was unnecessary.",
                    "The team decided to postpone the meeting.",
                ), 2, "'Decided' expresses the same action more directly. Cancelling changes the outcome, and calling the meeting unnecessary adds a new opinion."),
            ),
            assignment=Assignment(
                "Choose a familiar place and one improvement it needs. Write a short request to the person responsible. Name the improvement and explain who would benefit. Keep this idea for the next lessons.",
                30,
                ("I know who my reader is.", "My request names one practical change.", "My verbs and details make the meaning clear."),
                "Please keep the school library open until seven on Wednesdays. Students who attend afternoon clubs currently have little time to borrow books. One later evening would let us choose reading material without missing our activities.",
            ),
        ),
        Lesson(
            slug="develop-a-paragraph",
            title="Build a paragraph that develops an idea",
            minutes=12,
            goal="Support one main point with a reason, an example, and an explanation.",
            sections=(
                Section("Give the paragraph a job", "A paragraph should help the reader follow one main point. For a recommendation, a useful opening states a benefit. Each following sentence should develop that benefit rather than start an unrelated topic."),
                Section("Move from a claim to support", "Try this scaffold: point, reason, example, explanation. Explain why the example supports your point. This is a drafting aid, not a required sentence count. A short message may need less support than an essay."),
                Section("Use honest examples", "An observation from your experience can make an idea concrete. Label imagined situations as possibilities. Avoid making up statistics or claiming that a personal example proves something is true for everyone."),
            ),
            example=Example(
                "The waiting area needs benches. Benches are good. There are buses outside. It would be better.",
                "Adding benches would make the waiting area more comfortable. People sometimes wait through several bus arrivals before their route appears. A parent carrying a child, for example, could sit while watching for the bus. A few seats would make that wait easier.",
                "Every sentence develops the benefit of seating. The example helps explain the benefit instead of simply repeating that benches are good.",
            ),
            questions=(
                Question("Your paragraph argues for a quiet study area. Which detail best supports it?", (
                    "The building was painted blue last year.",
                    "The cafeteria sells several kinds of fruit.",
                    "Students currently share a table beside a noisy reception desk.",
                ), 2, "The noisy desk explains why a quieter space would help. Paint and fruit do not develop this particular point."),
                Question("After giving an example, what should you check?", (
                    "Whether you have explained how the example supports your point.",
                    "Whether you can add a statistic even without a source.",
                    "Whether every sentence uses a different topic.",
                ), 0, "Connect the example to your claim. Support should be relevant and honest, and the paragraph should keep a clear focus."),
            ),
            assignment=Assignment(
                "Develop the recommendation from lesson 1 into one paragraph. State a benefit, explain why it matters, and give a specific example. You can copy your saved response from the previous lesson.",
                50,
                ("The paragraph has one main point.", "My example is relevant and honestly described.", "I explain how the example supports my recommendation."),
                "A later library closing time would help students who stay for clubs. Our activities finish at five thirty, just before the library closes. After a long rehearsal, for example, a student may have only a few minutes to choose a book. Keeping the library open until seven on Wednesdays would give these students time to browse and ask for advice.",
            ),
        ),
        Lesson(
            slug="connect-your-ideas",
            title="Connect ideas and vary your sentences",
            minutes=12,
            goal="Make the relationship between sentences easy to follow.",
            sections=(
                Section("Choose the relationship first", "Ask whether the next idea adds information, contrasts with it, explains a cause, or shows a result. Then choose a connector if one is needed: 'also', 'however', 'because', or 'therefore'. A connector cannot repair a connection that does not make sense."),
                Section("Carry familiar information forward", "A phrase such as 'this extra hour' can refer back to a later closing time. Give pronouns a clear noun to refer to. Repeating a key term is often clearer than replacing it with a distant synonym."),
                Section("Use sentence length deliberately", "Join closely related ideas when the connection helps: 'Because the room is small, we can try four desks first.' Keep a short sentence for a key point. When joining two complete sentences with 'however', use a full stop or a semicolon before it, not just a comma."),
            ),
            example=Example(
                "The new timetable would help students. However, students could borrow books after clubs. It costs money, it needs planning.",
                "The new timetable would help students borrow books after clubs. This extra hour would give them time to browse. However, staffing would cost money, so the school could begin with a four-week trial.",
                "'This extra hour' carries the idea forward. 'However' introduces a real drawback, and 'so' connects that drawback to a practical response.",
            ),
            questions=(
                Question("Choose the best connector: 'The room is small. ___, it can hold only six desks.'", (
                    "As a result",
                    "In contrast",
                    "For example",
                ), 0, "The desk limit is a result of the room's size. It is not a contrast or an example of another room."),
                Question("Which version correctly links two complete sentences?", (
                    "The plan is useful, however, it is expensive.",
                    "The plan is useful. However, it is expensive.",
                    "The plan is useful however it is expensive.",
                ), 1, "A full stop separates the two complete sentences. 'However' alone cannot join them with a comma."),
            ),
            assignment=Assignment(
                "Write two connected paragraphs about your recommendation: one about the benefit, one about a possible difficulty and a practical response. Use a clear reference such as 'this change' and a connector that matches the meaning.",
                50,
                ("Each paragraph has a distinct job.", "My connectors express the actual relationship.", "My pronouns and phrases such as 'this change' have clear references."),
                "Keeping the library open later on Wednesdays would give students time to borrow books after clubs. This extra hour would be especially useful during busy project weeks.\n\nHowever, the school would need to arrange staff cover. A four-week trial could show how many students use the service before the school commits to a permanent change. Staff could then adjust the timetable using that information.",
            ),
        ),
        Lesson(
            slug="revise-and-finish",
            title="Revise and finish your writing",
            minutes=15,
            goal="Turn your draft into a focused recommendation through separate revision passes.",
            sections=(
                Section("Read first for the message", "Imagine receiving your draft without knowing the background. Can you identify the request and the reason for it? Move important context earlier, remove unrelated details, and explain gaps in the argument before polishing individual words."),
                Section("Read again for language", "Read aloud to find sentences that are hard to follow. Check verb tense, subject–verb agreement, articles, pronoun references, and punctuation. Replace vague language, but keep words you understand and can use naturally."),
                Section("Finish with a useful next step", "For this recommendation, close with an action the reader can consider. Avoid introducing an unrelated new argument in the ending. Keep your original draft nearby so you can see which changes improved meaning and which only changed the sound."),
            ),
            example=Example(
                "In conclusion, there are many advantages and disadvantages regarding this matter. Everyone knows that action must happen.",
                "Could we try the later closing time for four Wednesdays and record how many students use it? This would give the school a basis for deciding whether to continue.",
                "The ending offers a manageable next step and explains its purpose. It avoids claiming agreement from everyone.",
            ),
            questions=(
                Question("Your draft uses correct grammar but never explains the benefit of your request. What should you revise first?", (
                    "Replace everyday words with longer words.",
                    "Add more punctuation.",
                    "Explain why the requested change would help the reader or community.",
                ), 2, "Fixing the missing reason improves the message. More elaborate vocabulary cannot replace a clear explanation."),
                Question("Which ending best fits a proposal to add bicycle parking?", (
                    "Could we test one rack near the entrance and review its use after a month?",
                    "In conclusion, transport is a topic with many topics.",
                    "The cafeteria should also change its menu.",
                ), 0, "The trial is a concrete next step connected to the proposal. The other endings are vague or introduce a different issue."),
            ),
            assignment=Assignment(
                "Combine and revise your earlier drafts into a complete recommendation. Include the request, a developed benefit, a possible difficulty, and a practical next step. Read it once for meaning and once for language before saving.",
                80,
                ("My reader can identify the request immediately.", "I develop a benefit and address a realistic difficulty.", "My ending gives a next step.", "I checked grammar, punctuation, and unnecessary repetition."),
                "Please consider keeping the school library open until seven on Wednesdays. Students who attend clubs would then have time to borrow books and ask for help after their activities.\n\nAt present, a rehearsal can finish only a few minutes before closing. A later evening would make the library easier to use during project weeks, when students need several sources.\n\nStaff cover would need planning. Could we begin with a four-week trial and record attendance? These records would help the school decide whether the extra hour is useful enough to continue.",
            ),
        ),
    ),
)


STORY_COURSE = Course(
    slug="storytelling",
    title="Tell a better story",
    category="Storytelling",
    level="Intermediate and above",
    description="Create a character readers care about, build a meaningful conflict, and shape a satisfying short story.",
    outcomes=(
        "Give a character a goal, an obstacle, and something to lose.",
        "Build scenes through choices, consequences, detail, and dialogue.",
        "Keep a consistent viewpoint and revise a complete short story.",
    ),
    project="An original short story in which a difficult choice changes the outcome.",
    resources=(
        ("Purdue OWL: Writing compelling characters", "https://owl.purdue.edu/owl/subject_specific_writing/creative_writing/writers/fiction-basics/writing_compelling_characters.html"),
        ("Purdue OWL: Building and revealing characters", "https://owl.purdue.edu/owl/subject_specific_writing/creative_writing/writers/fiction-basics/building_and_revealing_characters.html"),
    ),
    lessons=(
        Lesson(
            slug="character-goal-and-stakes",
            title="Give your character a reason to act",
            minutes=10,
            goal="Build a story idea around a character who wants something and faces a meaningful obstacle.",
            sections=(
                Section("Start with a concrete want", "A wish such as 'be happy' is difficult to turn into a scene. A goal such as 'return a borrowed bicycle before its owner leaves' gives your character an action. Ask why this matters to this particular person."),
                Section("Add an obstacle and stakes", "An obstacle blocks the goal. Stakes explain what could be lost. A damaged bicycle is an obstacle; losing a friend's trust is a stake. Small, personal consequences can carry a story just as well as a large disaster."),
                Section("Leave room for a choice", "A useful story premise creates competing needs. Your character might want to hide a mistake and also keep a friendship. When both are difficult to achieve, the character must make a revealing choice."),
            ),
            example=Example(
                "Mira was a girl who lived in a town. One day something interesting happened.",
                "Mira had twenty minutes to return her friend's bicycle. Its front wheel was bent, and her friend was waiting to ride it to an interview.",
                "The opening gives Mira a goal, a deadline, an obstacle, and a reason the damage matters. It invites a decision about what she will do next.",
            ),
            questions=(
                Question("Which premise gives a character the clearest goal and obstacle?", (
                    "A man thought about life in a beautiful place.",
                    "A baker must deliver a wedding cake, but the only bridge is closed.",
                    "There were many people in a city.",
                ), 1, "The delivery is a concrete goal and the closed bridge blocks it. The other premises do not yet create a clear action."),
                Question("In Mira's story, which detail describes a stake?", (
                    "The bicycle has two wheels.",
                    "The town has several streets.",
                    "Her friend may miss an interview and stop trusting her.",
                ), 2, "Missing the interview and losing trust are consequences of failure. Stakes help the reader understand why the goal matters."),
            ),
            assignment=Assignment(
                "Invent a character with a specific goal, an obstacle, and something personal to lose. Write a short premise ending with a difficult choice. Use this character throughout the course.",
                30,
                ("My character wants something concrete.", "An obstacle makes the goal difficult.", "The reader can understand what the character might lose."),
                "Rafi wants to return his sister's camera before her graduation ceremony. He discovers that the lens is cracked. With no money for a repair, he must choose between hiding the damage and admitting that he borrowed it without asking.",
            ),
        ),
        Lesson(
            slug="plot-through-consequences",
            title="Build a plot from choices and consequences",
            minutes=12,
            goal="Connect events so each attempt changes what happens next.",
            sections=(
                Section("Turn a list into a chain", "A list of events tells us what happened next. A plot also gives us reasons: because a repair shop is closed, Mira asks a neighbour; because the neighbour needs the truth, she must explain the damage. Let one event create the next problem or opportunity."),
                Section("Try a simple shape", "For this short story, use five beats: a goal, a disruption, an attempt that complicates matters, a decisive choice, and a consequence. You can change the structure later. This scaffold helps you finish a first draft without adding too many side events."),
                Section("Prepare the turning point", "The decisive moment should grow from earlier information. If a neighbour can help, establish that neighbour before the ending. A surprise can work when readers can look back and see why it was possible."),
            ),
            example=Example(
                "Mira saw the damage. Then it rained. Then she met a neighbour. Then the bicycle was fixed.",
                "Mira tried to straighten the wheel, but the brake jammed. Because riding was now impossible, she asked her neighbour for a lift. He agreed only after she called her friend and explained why they needed his car.",
                "Mira's attempt creates a new problem, which leads to a choice. The neighbour helps, but Mira still has to take responsibility.",
            ),
            questions=(
                Question("Which event best follows from a character missing the last bus?", (
                    "She calls the friend she has been avoiding to ask for a lift.",
                    "A paragraph lists unrelated facts about the moon.",
                    "The story starts describing an unrelated holiday.",
                ), 0, "The missed bus creates a need, and asking the avoided friend adds a meaningful choice. The other events do not follow from the problem."),
                Question("A stranger solves every problem in the final line. What revision would give the protagonist more agency?", (
                    "Add more adjectives to describe the stranger.",
                    "Make the outcome depend on a difficult choice the protagonist makes.",
                    "Remove the protagonist from the final scene.",
                ), 1, "Agency means the character's actions affect the outcome. A meaningful decision connects the ending to the character's journey."),
            ),
            assignment=Assignment(
                "Outline your story in five beats: goal, disruption, attempt, decisive choice, and consequence. Use 'because', 'but', or 'so' to explain how at least two events connect.",
                50,
                ("Events connect through causes and consequences.", "An attempt makes the situation change.", "My character's choice affects the ending."),
                "Rafi needs to return the camera before the ceremony. He finds a cracked lens, so he visits a repair stall. The seller cannot fix it in time, but offers a rental camera. Because Rafi cannot pay the deposit, he must call his sister and admit what happened. She brings her card, and he agrees to repay the rental cost with his weekend earnings.",
            ),
        ),
        Lesson(
            slug="scenes-detail-and-dialogue",
            title="Bring a scene to life",
            minutes=15,
            goal="Use selected details, action, and dialogue while keeping one viewpoint.",
            sections=(
                Section("Show the moments that matter", "At a turning point, let the reader notice an action or a sensory detail: a finger hovering over the call button, or rain tapping a bent wheel. Choose details that reveal the situation or emotion. You do not need to describe every sight and sound."),
                Section("Let dialogue do work", "Give each speaker a reason to speak: asking, avoiding, admitting, or persuading. A gesture can suggest what a speaker leaves unsaid. Start a new paragraph when the speaker changes. In a simple dialogue tag, write: 'I broke it,' she said. For a separate action, write: 'I broke it.' She lowered her head."),
                Section("Choose whose experience we follow", "First person uses 'I'. Third-person limited follows one character using 'he', 'she', or 'they'. In a scene limited to Mira, describe what she can observe or infer; do not suddenly state another person's private thoughts as fact. Use summary to move quickly between important scenes."),
            ),
            example=Example(
                "Mira was very nervous. Her friend was secretly furious. They had a conversation about the bicycle.",
                "Mira pressed the phone against her damp sleeve. 'The wheel is bent,' she said. At the other end, a door clicked shut. 'Can I still get to the interview?' her friend asked. Mira looked at her neighbour's car. 'Yes. I can get you there.'",
                "Actions and sounds carry the tension. We stay with what Mira can perceive, and the dialogue changes her next action rather than repeating background information.",
            ),
            questions=(
                Question("Which sentence stays within a viewpoint limited to Mira?", (
                    "Her friend secretly decided never to trust anyone again.",
                    "Across town, a stranger dreamed about a train.",
                    "Her friend's voice sounded tighter than usual to Mira.",
                ), 2, "Mira can hear a voice and interpret it. The other options reveal private experiences she cannot access in this viewpoint."),
                Question("Which revision shows nervousness through a concrete action?", (
                    "He folded the receipt until it was too small to read.",
                    "He was nervous in a very nervous way.",
                    "Nervousness was something that he felt.",
                ), 0, "Folding the receipt gives the reader an observable detail. The other versions simply repeat the emotion label."),
            ),
            assignment=Assignment(
                "Write the decisive scene from your outline. Include a specific sensory detail, two spoken lines, and an action that reveals emotion. Stay with one character's viewpoint and separate speakers into paragraphs.",
                60,
                ("My details reveal something useful about the moment.", "The dialogue changes the situation or reveals a motive.", "I keep a consistent viewpoint.", "Each new speaker starts a new paragraph."),
                "Rafi rubbed the cracked edge of the lens cap. The repair stall smelled of hot dust.\n\n'I borrowed your camera,' he told his sister on the phone. 'The lens is broken.'\n\nFor a moment, he heard only traffic. 'Are you still coming to the ceremony?' she asked.\n\nHe looked at the rental camera on the counter. 'Yes. And I have a plan, if you can meet me here.'",
            ),
        ),
        Lesson(
            slug="ending-and-revision",
            title="Write an ending that earns its place",
            minutes=20,
            goal="Finish a complete story and revise it for change, consistency, and rhythm.",
            sections=(
                Section("Answer the story's central question", "The ending can show success, failure, or a mixed result. Let the reader understand what happened to the main goal and what the decisive choice cost. A relationship may change even when the practical problem is solved."),
                Section("Show a small sign of change", "You do not have to explain a moral. A final action can suggest a new attitude: a character who borrowed without asking now waits for permission. An image or object from the opening can return with a changed meaning."),
                Section("Revise in three passes", "First check the chain of events: does the ending grow from the character's decisions? Next check viewpoint and tense. If you tell the main events in the past, keep that timeline consistent and signal deliberate shifts. Finally, read aloud and cut repetition while preserving details that carry emotion."),
            ),
            example=Example(
                "Everything was perfect after that. Mira learned that honesty is always the best policy. The end.",
                "Her friend reached the interview on time, but the bicycle still needed a new wheel. That evening, Mira left her first repair payment on the kitchen table. Beside it lay a note: 'May I borrow your pump on Saturday?'",
                "The practical outcome has a cost, and the final request suggests changed behaviour. The ending lets an action carry the meaning.",
            ),
            questions=(
                Question("Which ending best completes a story about a character learning to ask for help?", (
                    "A new villain arrives with no earlier connection to the story.",
                    "The character calls a friend before attempting the next difficult task.",
                    "The narrator lists every street in the town.",
                ), 1, "The final action reflects a change connected to the story's conflict. It gives the reader evidence of growth."),
                Question("Which revision pass should come before polishing individual adjectives?", (
                    "Make every sentence the same length.",
                    "Add a surprising event to every paragraph.",
                    "Check that the character's decisions lead plausibly to the ending.",
                ), 2, "A coherent chain of events gives the story its foundation. Word-level polish comes after the larger story works."),
            ),
            assignment=Assignment(
                "Use your premise, outline, and scene to write a complete short story. Include an opening goal, an obstacle, a difficult choice, and an ending that shows a consequence or change. Give it a title and revise your tense and viewpoint.",
                120,
                ("The opening gives the reader a reason to care.", "My character's choice affects the outcome.", "The ending answers the main story question.", "My viewpoint, tense, and dialogue punctuation are consistent."),
                "The Borrowed Camera\n\nRafi found the crack in the lens an hour before his sister's graduation. He had borrowed her camera without asking. Now its photographs carried a pale line across the middle.\n\nAt the repair stall, the seller shook his head. A repair would take days. A rental sat beside the register, but Rafi could not afford the deposit. He unfolded his empty wallet once more, then called his sister.\n\n'I broke your camera,' he said. The words came out quieter than the traffic.\n\n'Bring yourself to the ceremony,' she replied. 'We'll work out the photographs.'\n\nHe explained the rental. She met him at the stall, and he promised to repay the cost. At the ceremony, he held the replacement carefully. When she asked him to take a picture, he waited for her nod before lifting it.",
            ),
        ),
    ),
)


COURSES = (PARTICIPLES_COURSE, WRITING_COURSE, STORY_COURSE, *IELTS_COURSES)
