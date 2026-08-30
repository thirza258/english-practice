from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class QuestionBlueprint:
    topic: str
    question: str
    correct_answer: str
    distractors: Sequence[str]
    rule: str
    explanation: str
    sentence_explanation: str
    secondary_topics: Sequence[str] = ()
    level: str = "intermediate"


@dataclass(frozen=True)
class BlankBlueprint:
    blank_id: int
    topic: str
    correct_answer: str
    distractors: Sequence[str]
    rule: str
    explanation: str
    secondary_topics: Sequence[str] = ()


@dataclass(frozen=True)
class ParagraphBlueprint:
    title: str
    text_with_blanks: str
    blanks: Sequence[BlankBlueprint]
    level: str
    full_text: str
    paragraph_explanation: str


QUESTION_BANK: list[QuestionBlueprint] = [
    # -------------------------------------------------------------------------
    # BEGINNER (A1 - A2)
    # -------------------------------------------------------------------------
    QuestionBlueprint(
        topic="Choosing the correct word to complete a simple sentence",
        question="They ___ ready for the meeting.",
        correct_answer="are",
        distractors=("is", "was", "be", "been"),
        rule="Use the plural form of the verb when the subject is plural.",
        explanation="They is a plural subject, so the sentence needs the plural verb are.",
        sentence_explanation="They are ready for the meeting.",
        level="beginner",
    ),
    QuestionBlueprint(
        topic="Personal pronouns",
        question="___ is reading a novel in the living room.",
        correct_answer="She",
        distractors=("Her", "Hers", "Herself", "Them"),
        rule="Use a subject pronoun as the subject of a sentence.",
        explanation="She is the subject pronoun needed to perform the action of reading.",
        sentence_explanation="She is reading a novel in the living room.",
        level="beginner",
    ),
    QuestionBlueprint(
        topic="Personal pronouns",
        question="Can you please give the notebook to ___?",
        correct_answer="me",
        distractors=("I", "my", "mine", "myself"),
        rule="Use an object pronoun after a preposition.",
        explanation="To is a preposition, so the object pronoun me must be used.",
        sentence_explanation="Can you please give the notebook to me?",
        level="beginner",
    ),
    QuestionBlueprint(
        topic="Subject-verb agreement",
        question="Every morning, my father ___ a cup of green tea.",
        correct_answer="drinks",
        distractors=("drink", "drinking", "drank", "is drink"),
        rule="A singular third-person subject takes a singular verb ending in -s in the simple present tense.",
        explanation="My father is a singular subject, so the verb drinks is required.",
        sentence_explanation="Every morning, my father drinks a cup of green tea.",
        level="beginner",
    ),
    QuestionBlueprint(
        topic="Subject-verb agreement",
        question="The puppies ___ playfully in the garden right now.",
        correct_answer="are playing",
        distractors=("is playing", "plays", "played", "playing"),
        rule="Use are with a plural subject in the present continuous tense.",
        explanation="The puppies is plural, so are playing is the correct present continuous form.",
        sentence_explanation="The puppies are playing playfully in the garden right now.",
        level="beginner",
    ),
    QuestionBlueprint(
        topic="Adjectives",
        question="She wore a ___ jacket to the party.",
        correct_answer="red",
        distractors=("redden", "redness", "redly", "redder"),
        rule="Adjectives modify nouns.",
        explanation="Red is the base adjective that describes the jacket.",
        sentence_explanation="She wore a red jacket to the party.",
        level="beginner",
    ),
    QuestionBlueprint(
        topic="Adverbs",
        question="He finished the easy assignment ___ before dinner.",
        correct_answer="quickly",
        distractors=("quick", "quicker", "quickest", "quickness"),
        rule="Adverbs describe how an action is performed.",
        explanation="Quickly tells how he finished the assignment.",
        sentence_explanation="He finished the easy assignment quickly before dinner.",
        level="beginner",
    ),
    QuestionBlueprint(
        topic="Degrees of comparison",
        question="This exercise is ___ than the previous one.",
        correct_answer="easier",
        distractors=("easy", "easiest", "more easy", "easily"),
        rule="Use the comparative form -er when comparing two things.",
        explanation="Easier is the comparative form of easy when comparing two exercises.",
        sentence_explanation="This exercise is easier than the previous one.",
        level="beginner",
    ),
    QuestionBlueprint(
        topic="Compound sentences",
        question="The sun was bright, ___ we wore our sunglasses.",
        correct_answer="so",
        distractors=("because", "although", "unless", "if"),
        rule="Use so to connect a cause to its result in a compound sentence.",
        explanation="So coordinates two independent clauses and introduces the result.",
        sentence_explanation="The sun was bright, so we wore our sunglasses.",
        level="beginner",
    ),
    QuestionBlueprint(
        topic="Prepositional idioms",
        question="The train departs ___ eight o'clock sharp.",
        correct_answer="at",
        distractors=("on", "in", "to", "for"),
        rule="Use at to specify exact times on the clock.",
        explanation="At is the standard preposition used with specific clock times.",
        sentence_explanation="The train departs at eight o'clock sharp.",
        level="beginner",
    ),
    QuestionBlueprint(
        topic="Choosing the correct word to complete a simple sentence",
        question="There ___ five apples in the fruit basket.",
        correct_answer="are",
        distractors=("is", "was", "be", "being"),
        rule="Use there are when introducing a plural noun phrase in the present tense.",
        explanation="Five apples is plural, requiring are after there.",
        sentence_explanation="There are five apples in the fruit basket.",
        level="beginner",
    ),
    QuestionBlueprint(
        topic="English usage",
        question="They do not ___ any help with the luggage.",
        correct_answer="need",
        distractors=("needs", "needed", "needing", "to need"),
        rule="After the auxiliary do/does/did not, use the base form of the main verb.",
        explanation="Need is the base verb form following do not.",
        sentence_explanation="They do not need any help with the luggage.",
        level="beginner",
    ),

    # -------------------------------------------------------------------------
    # INTERMEDIATE (B1 - B2)
    # -------------------------------------------------------------------------
    QuestionBlueprint(
        topic="Subject-verb agreement",
        question="The list of items ___ on the table.",
        correct_answer="is",
        distractors=("are", "were", "be", "have been"),
        rule="The main subject is list, which is singular.",
        explanation="The subject list is singular, so the verb must be is.",
        sentence_explanation="The list of items is on the table.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Personal pronouns",
        question="Between you and ___, the plan changed.",
        correct_answer="me",
        distractors=("I", "she", "they", "we"),
        rule="Use an object pronoun after a preposition.",
        explanation="Between is a preposition, so the pronoun after it should be me.",
        sentence_explanation="Between you and me, the plan changed.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Adverb phrases",
        question="She spoke ___ during the interview.",
        correct_answer="clearly",
        distractors=("clear", "quick", "bright", "softness"),
        rule="An adverb phrase or adverb form modifies the verb spoke.",
        explanation="Clearly is the adverb that describes how she spoke.",
        sentence_explanation="She spoke clearly during the interview.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Appositives",
        question="My brother, ___, will drive us home.",
        correct_answer="a skilled mechanic",
        distractors=("skillfully", "many cars", "to fix the car", "who fixes"),
        rule="An appositive renames the noun that comes before it.",
        explanation="A skilled mechanic is a noun phrase that renames my brother.",
        sentence_explanation="My brother, a skilled mechanic, will drive us home.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Noun phrases",
        question="The decision ___ surprised everyone.",
        correct_answer="to postpone the launch",
        distractors=("postponing launch", "postpone launch", "postponed launch", "postpone to the launch"),
        rule="A noun phrase can function as the subject or object of a sentence.",
        explanation="To postpone the launch is a noun phrase that completes the subject decision.",
        sentence_explanation="The decision to postpone the launch surprised everyone.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Compound sentences",
        question="The weather was cold, ___ we stayed inside.",
        correct_answer="so",
        distractors=("because", "although", "unless", "if"),
        rule="A compound sentence joins two independent clauses with a coordinating conjunction.",
        explanation="So joins two independent clauses and shows the result of the cold weather.",
        sentence_explanation="The weather was cold, so we stayed inside.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Complex sentences",
        question="We left early ___ the road was closing.",
        correct_answer="because",
        distractors=("and", "but", "or", "yet"),
        rule="A complex sentence uses a dependent clause to explain or modify the main clause.",
        explanation="Because introduces the dependent clause that explains why we left early.",
        sentence_explanation="We left early because the road was closing.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Adjective clauses",
        question="The teacher ___ helped me was very kind.",
        correct_answer="who",
        distractors=("where", "when", "what", "whose"),
        rule="An adjective clause describes a noun and often begins with a relative pronoun.",
        explanation="Who introduces the clause that describes the teacher.",
        sentence_explanation="The teacher who helped me was very kind.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Adverb clauses",
        question="We waited inside ___ the rain stopped.",
        correct_answer="until",
        distractors=("who", "that", "despite", "although"),
        rule="An adverb clause can show time, condition, reason, or contrast.",
        explanation="Until introduces a time clause showing when we waited inside.",
        sentence_explanation="We waited inside until the rain stopped.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Noun clauses",
        question="I don't know ___ she meant.",
        correct_answer="what",
        distractors=("where", "when", "whose", "how much"),
        rule="A noun clause can act as the object of a verb like know.",
        explanation="What she meant is the noun clause that works as the object of know.",
        sentence_explanation="I don't know what she meant.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Present participles",
        question="I saw the children ___ in the park.",
        correct_answer="playing",
        distractors=("played", "play", "to play", "plays"),
        rule="A present participle can describe an action in progress.",
        explanation="Playing shows the children were in the middle of the action.",
        sentence_explanation="I saw the children playing in the park.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Past participles",
        question="The letter was ___ yesterday.",
        correct_answer="sent",
        distractors=("sending", "send", "sends", "sender"),
        rule="Past participles often appear with forms of be in passive voice.",
        explanation="Sent is the past participle needed after was.",
        sentence_explanation="The letter was sent yesterday.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Gerunds",
        question="___ regularly helps improve stamina.",
        correct_answer="Running",
        distractors=("Run", "To run", "Ran", "Runs"),
        rule="A gerund is a verb form ending in -ing that functions as a noun.",
        explanation="Running works as the subject of the sentence.",
        sentence_explanation="Running regularly helps improve stamina.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Infinitives",
        question="He hopes ___ the exam.",
        correct_answer="to pass",
        distractors=("passing", "passed", "pass", "passes"),
        rule="An infinitive is to plus the base form of the verb.",
        explanation="To pass is the infinitive that follows hopes.",
        sentence_explanation="He hopes to pass the exam.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Degrees of comparison",
        question="This puzzle is ___ than the last one.",
        correct_answer="harder",
        distractors=("hard", "hardest", "hardly", "more hard"),
        rule="Use the comparative form when comparing two things.",
        explanation="Harder is the comparative form used to compare two puzzles.",
        sentence_explanation="This puzzle is harder than the last one.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Conditional clauses",
        question="If I ___ enough time, I would travel more.",
        correct_answer="had",
        distractors=("have", "will have", "having", "has"),
        rule="Use the past form in a hypothetical conditional if-clause.",
        explanation="Had is correct because the sentence describes an unreal present situation.",
        sentence_explanation="If I had enough time, I would travel more.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="English usage",
        question="She has a deep ___ for music.",
        correct_answer="appreciation",
        distractors=("appreciate", "appreciator", "appreciatively", "appreciable"),
        rule="Choose the word that fits the sentence meaning and part of speech.",
        explanation="Appreciation is the noun that fits after deep.",
        sentence_explanation="She has a deep appreciation for music.",
        level="intermediate",
    ),
    QuestionBlueprint(
        topic="Prepositional idioms",
        question="He is interested ___ science.",
        correct_answer="in",
        distractors=("on", "at", "with", "for"),
        rule="Many English expressions require a fixed preposition.",
        explanation="Interested in is the standard idiomatic combination.",
        sentence_explanation="He is interested in science.",
        level="intermediate",
    ),

    # -------------------------------------------------------------------------
    # ADVANCED (C1 - C2)
    # -------------------------------------------------------------------------
    QuestionBlueprint(
        topic="Subjunctive mood",
        question="The manager requested that he ___ early.",
        correct_answer="arrive",
        distractors=("arrives", "arrived", "arriving", "has arrived"),
        rule="In the subjunctive mood, base form verbs often follow demand or request verbs.",
        explanation="Arrive is the base form used after requested that.",
        sentence_explanation="The manager requested that he arrive early.",
        level="advanced",
    ),
    QuestionBlueprint(
        topic="Subjunctive mood",
        question="It is essential that every applicant ___ the guidelines thoroughly.",
        correct_answer="read",
        distractors=("reads", "is reading", "has read", "will read"),
        rule="Mandative subjunctive requires the uninflected base form of the verb in that-clauses after essential.",
        explanation="Read is the uninflected base verb form required in this subjunctive construction.",
        sentence_explanation="It is essential that every applicant read the guidelines thoroughly.",
        level="advanced",
    ),
    QuestionBlueprint(
        topic="Inverted subject and predicate",
        question="Under the bridge ___ a small boat.",
        correct_answer="was",
        distractors=("were", "are", "be", "been"),
        rule="Inversion can place the verb before the subject for emphasis or style.",
        explanation="Was agrees with the singular subject a small boat after the prepositional phrase.",
        sentence_explanation="Under the bridge was a small boat.",
        level="advanced",
    ),
    QuestionBlueprint(
        topic="Inverted subject and predicate",
        question="Rarely ___ such dedication in a young researcher.",
        correct_answer="have I seen",
        distractors=("I have seen", "I saw", "did I saw", "I had seen"),
        rule="Negative or restrictive adverbs placed at the start of a sentence trigger subject-auxiliary inversion.",
        explanation="Rarely at the beginning of a clause requires the inverted order have I seen.",
        sentence_explanation="Rarely have I seen such dedication in a young researcher.",
        level="advanced",
    ),
    QuestionBlueprint(
        topic="Causative constructions",
        question="She had her laptop ___ yesterday.",
        correct_answer="repaired",
        distractors=("repair", "repairing", "repairs", "to repair"),
        rule="Causative structures can show that someone arranged for an action to happen.",
        explanation="Repaired shows she arranged for someone else to fix the laptop.",
        sentence_explanation="She had her laptop repaired yesterday.",
        level="advanced",
    ),
    QuestionBlueprint(
        topic="Causative constructions",
        question="The supervisor got the team ___ their reports before noon.",
        correct_answer="to submit",
        distractors=("submit", "submitted", "submitting", "submission"),
        rule="The causative verb get takes an object followed by a to-infinitive.",
        explanation="To submit is the to-infinitive required after get + object.",
        sentence_explanation="The supervisor got the team to submit their reports before noon.",
        level="advanced",
    ),
    QuestionBlueprint(
        topic="Elliptical constructions",
        question="I can swim faster than he can ___.",
        correct_answer="swim",
        distractors=("swims", "swimming", "to swim", "swam"),
        rule="Elliptical constructions omit repeated words that are understood from context.",
        explanation="Swim is understood after can, so the sentence avoids repeating the verb phrase.",
        sentence_explanation="I can swim faster than he can swim.",
        level="advanced",
    ),
    QuestionBlueprint(
        topic="Elliptical constructions",
        question="Some engineers prefer working remotely; others, ___ in the office.",
        correct_answer="working",
        distractors=("works", "worked", "to work", "are work"),
        rule="Gapping in elliptical clauses maintains parallel participle structure while omitting the verb prefer.",
        explanation="Working parallels the gerund structure in the first clause.",
        sentence_explanation="Some engineers prefer working remotely; others, working in the office.",
        level="advanced",
    ),
    QuestionBlueprint(
        topic="Parallel structure",
        question="The plan was to write, to edit, and ___.",
        correct_answer="to publish",
        distractors=("publishing", "published", "publish", "publishes"),
        rule="Items in a series should share the same grammatical form.",
        explanation="To publish matches the other infinitive phrases in the series.",
        sentence_explanation="The plan was to write, to edit, and to publish.",
        level="advanced",
    ),
    QuestionBlueprint(
        topic="Parallel structure",
        question="The executive admired both her sharp intellect and ___ under pressure.",
        correct_answer="her composure",
        distractors=("she was composed", "composedly working", "how composed she was", "to be composed"),
        rule="Correlative conjunctions like both...and must connect grammatically parallel noun phrases.",
        explanation="Her composure is a noun phrase that parallels her sharp intellect.",
        sentence_explanation="The executive admired both her sharp intellect and her composure under pressure.",
        level="advanced",
    ),
    QuestionBlueprint(
        topic="Conditional clauses",
        question="Had we known about the storm, we ___ our trip.",
        correct_answer="would have cancelled",
        distractors=("will cancel", "had cancelled", "would cancel", "cancelled"),
        rule="Inverted third conditional clauses require would have + past participle in the main clause.",
        explanation="Would have cancelled expresses the unreal past result of the inverted condition.",
        sentence_explanation="Had we known about the storm, we would have cancelled our trip.",
        level="advanced",
    ),
    QuestionBlueprint(
        topic="English usage",
        question="The proposed hypothesis was found to be utterly devoid ___ empirical evidence.",
        correct_answer="of",
        distractors=("from", "with", "in", "by"),
        rule="The adjective devoid idiomatically takes the preposition of.",
        explanation="Devoid of is the correct fixed collocation meaning entirely lacking in something.",
        sentence_explanation="The proposed hypothesis was found to be utterly devoid of empirical evidence.",
        level="advanced",
    ),

    # -------------------------------------------------------------------------
    # IELTS BAND 8.0 - 9.0 (C2 / RARE VOCABULARY & LEXICAL MASTERY)
    # -------------------------------------------------------------------------
    QuestionBlueprint(
        topic="English usage",
        question="The author's arguments were so ___ that even her fiercest ideological opponents found them impossible to refute.",
        correct_answer="cogent",
        distractors=("specious", "bombastic", "pedantic", "inchoate"),
        rule="Use cogent to describe an argument or case that is clear, logical, and powerfully convincing.",
        explanation="Cogent is the precise academic adjective denoting an argument that is logically sound and unassailable.",
        sentence_explanation="The author's arguments were so cogent that even her fiercest ideological opponents found them impossible to refute.",
        level="ielts_8_9",
    ),
    QuestionBlueprint(
        topic="English usage",
        question="The spokesperson attempted to ___ the regulatory failure by burying the critical data in convoluted technical jargon.",
        correct_answer="obfuscate",
        distractors=("elucidate", "corroborate", "promulgate", "exonerate"),
        rule="Use obfuscate when an action deliberately makes something obscure, unclear, or difficult to understand.",
        explanation="Obfuscate accurately conveys intentionally concealing or confusing facts through convoluted language.",
        sentence_explanation="The spokesperson attempted to obfuscate the regulatory failure by burying the critical data in convoluted technical jargon.",
        level="ielts_8_9",
    ),
    QuestionBlueprint(
        topic="English usage",
        question="Despite initial public skepticism, the policy reform yielded remarkably ___ outcomes for urban biodiversity.",
        correct_answer="salutary",
        distractors=("pernicious", "insidious", "superfluous", "deleterious"),
        rule="Salutary describes an effect or influence that produces good results or beneficial consequences, especially after adversity.",
        explanation="Salutary indicates a genuinely beneficial impact, contrasting with the initial public skepticism.",
        sentence_explanation="Despite initial public skepticism, the policy reform yielded remarkably salutary outcomes for urban biodiversity.",
        level="ielts_8_9",
    ),
    QuestionBlueprint(
        topic="Inverted subject and predicate",
        question="Seldom ___ such a trenchant critique of economic orthodoxy been articulated with such mathematical rigor.",
        correct_answer="has",
        distractors=("is", "was", "having", "were"),
        rule="Negative adverbs like Seldom placed at the head of a sentence demand subject-auxiliary inversion in the present perfect.",
        explanation="Has is the inverted auxiliary agreeing with the singular subject 'such a trenchant critique'.",
        sentence_explanation="Seldom has such a trenchant critique of economic orthodoxy been articulated with such mathematical rigor.",
        level="ielts_8_9",
    ),
    QuestionBlueprint(
        topic="Subjunctive mood",
        question="The ethics committee recommended that the lead investigator ___ all financial ties to the pharmaceutical sponsor immediately.",
        correct_answer="sever",
        distractors=("severs", "severed", "is severing", "has severed"),
        rule="The mandative subjunctive following verbs of recommendation requires the uninflected base verb form.",
        explanation="Sever is the base verb form required in that-clauses after recommended that.",
        sentence_explanation="The ethics committee recommended that the lead investigator sever all financial ties to the pharmaceutical sponsor immediately.",
        level="ielts_8_9",
    ),
    QuestionBlueprint(
        topic="English usage",
        question="There is an irreconcilable ___ between the government's ostensible environmental pledges and its continued subsidies for fossil fuels.",
        correct_answer="dichotomy",
        distractors=("panacea", "plethora", "surfeit", "hiatus"),
        rule="A dichotomy refers to a division or contrast between two things that are represented as being entirely opposed or contradictory.",
        explanation="Dichotomy conveys the sharp, contradictory split between environmental pledges and fossil fuel subsidies.",
        sentence_explanation="There is an irreconcilable dichotomy between the government's ostensible environmental pledges and its continued subsidies for fossil fuels.",
        level="ielts_8_9",
    ),
    QuestionBlueprint(
        topic="English usage",
        question="The theoretical framework remained robust, ___ the slight anomalies observed during empirical trials.",
        correct_answer="notwithstanding",
        distractors=("whereas", "whereupon", "insofar", "henceforth"),
        rule="Notwithstanding functions as a formal preposition of concession meaning 'in spite of' or 'despite'.",
        explanation="Notwithstanding concedes the presence of slight anomalies while maintaining the overall robustness of the framework.",
        sentence_explanation="The theoretical framework remained robust, notwithstanding the slight anomalies observed during empirical trials.",
        level="ielts_8_9",
    ),
    QuestionBlueprint(
        topic="English usage",
        question="The diplomat's ___ silence during the heated deliberations was widely interpreted as implicit disapproval.",
        correct_answer="conspicuous",
        distractors=("ephemeral", "capricious", "tenuous", "supercilious"),
        rule="Conspicuous describes something clearly visible, striking, or attracting attention because of being unusual.",
        explanation="Conspicuous silence refers to an omission or silence that is noticeably prominent and meaningful.",
        sentence_explanation="The diplomat's conspicuous silence during the heated deliberations was widely interpreted as implicit disapproval.",
        level="ielts_8_9",
    ),
    QuestionBlueprint(
        topic="Parallel structure",
        question="The newly appointed dean sought not only to overhaul the outdated curriculum, but also ___ rigorous peer-review standards across all departments.",
        correct_answer="to institute",
        distractors=("instituting", "instituted", "institution of", "having instituted"),
        rule="Correlative structures with 'not only [infinitive]... but also [infinitive]' must maintain strict grammatical parallelism.",
        explanation="To institute maintains the parallel infinitive construction initiated by 'to overhaul'.",
        sentence_explanation="The newly appointed dean sought not only to overhaul the outdated curriculum, but also to institute rigorous peer-review standards across all departments.",
        level="ielts_8_9",
    ),
    QuestionBlueprint(
        topic="English usage",
        question="Through a series of ___ observations, the macroeconomist correctly anticipated the currency devaluation months before financial markets reacted.",
        correct_answer="perspicacious",
        distractors=("vacuous", "obtuse", "pusillanimous", "profligate"),
        rule="Perspicacious means possessing acute mental vision, keen discernment, and deep understanding of complex phenomena.",
        explanation="Perspicacious highlights sharp intellectual discernment and acute foresight in economic analysis.",
        sentence_explanation="Through a series of perspicacious observations, the macroeconomist correctly anticipated the currency devaluation months before financial markets reacted.",
        level="ielts_8_9",
    ),
    QuestionBlueprint(
        topic="Conditional clauses",
        question="___ the archival evidence not surfaced during the restoration, the historical manuscript would have remained attributed to an anonymous scribe.",
        correct_answer="Had",
        distractors=("If", "Should", "Were", "Would"),
        rule="Inverted third conditional clauses omit 'if' and front the auxiliary 'Had' with the subject.",
        explanation="Had introduces the counterfactual past conditional without requiring the conjunction 'if'.",
        sentence_explanation="Had the archival evidence not surfaced during the restoration, the historical manuscript would have remained attributed to an anonymous scribe.",
        level="ielts_8_9",
    ),
    QuestionBlueprint(
        topic="English usage",
        question="Such arbitrary administrative dictates are completely antithetical ___ the principles of scientific transparency.",
        correct_answer="to",
        distractors=("with", "from", "against", "for"),
        rule="The formal adjective antithetical idiomatically collocates with the preposition to (antithetical to).",
        explanation="Antithetical to is the established academic collocation meaning mutually incompatible or directly opposed.",
        sentence_explanation="Such arbitrary administrative dictates are completely antithetical to the principles of scientific transparency.",
        level="ielts_8_9",
    ),
    QuestionBlueprint(
        topic="English usage",
        question="The sudden resignation of the chief economist created an institutional ___ that paralyzed policy decisions for several quarters.",
        correct_answer="lacuna",
        distractors=("plethora", "panoply", "sycophant", "paradigm"),
        rule="A lacuna refers to an unfilled space, gap, or missing element in a structure, text, or institution.",
        explanation="Lacuna represents the critical vacuum or absence left by the departure of key leadership.",
        sentence_explanation="The sudden resignation of the chief economist created an institutional lacuna that paralyzed policy decisions for several quarters.",
        level="ielts_8_9",
    ),
    QuestionBlueprint(
        topic="English usage",
        question="Premature withdrawal of monetary stimulus threatens to ___ existing inflationary pressures across emerging markets.",
        correct_answer="exacerbate",
        distractors=("ameliorate", "palliate", "extenuate", "assuage"),
        rule="Exacerbate means to make a problem, bad situation, or negative feeling worse or more severe.",
        explanation="Exacerbate precisely conveys worsening or intensifying existing inflation.",
        sentence_explanation="Premature withdrawal of monetary stimulus threatens to exacerbate existing inflationary pressures across emerging markets.",
        level="ielts_8_9",
    ),
    QuestionBlueprint(
        topic="Inverted subject and predicate",
        question="Scarcely ___ the diplomatic envoy delivered her ultimatum when peace negotiations abruptly collapsed.",
        correct_answer="had",
        distractors=("has", "was", "did", "would"),
        rule="Restrictive fronting with Scarcely... when requires subject-auxiliary inversion in the past perfect.",
        explanation="Had is the inverted past auxiliary paired with the subsequent time clause 'when peace negotiations abruptly collapsed'.",
        sentence_explanation="Scarcely had the diplomatic envoy delivered her ultimatum when peace negotiations abruptly collapsed.",
        level="ielts_8_9",
    ),
]



PARAGRAPH_BANK: list[ParagraphBlueprint] = [
    # -------------------------------------------------------------------------
    # BEGINNER (A1 - A2) PARAGRAPHS
    # -------------------------------------------------------------------------
    ParagraphBlueprint(
        title="My Daily Routine",
        text_with_blanks=(
            "Every morning, Alex wakes up at seven o'clock. He prepares a quick breakfast [1] he needs energy for the day. "
            "After eating, he walks to the bus stop. The bus usually [2] on time. "
            "In the evening, he relaxes at home with his family, and [3] watch a movie together."
        ),
        blanks=(
            BlankBlueprint(
                blank_id=1,
                topic="Cause and effect conjunctions",
                correct_answer="because",
                distractors=("but", "so", "unless", "although"),
                rule="Use because to introduce the reason for an action.",
                explanation="Because introduces the reason why Alex eats breakfast (he needs energy).",
            ),
            BlankBlueprint(
                blank_id=2,
                topic="Subject-verb agreement in simple present",
                correct_answer="arrives",
                distractors=("arrive", "arriving", "arrived", "is arrive"),
                rule="A singular third-person subject takes a singular verb ending in -s in simple present.",
                explanation="The bus is singular third-person, requiring the singular verb arrives.",
            ),
            BlankBlueprint(
                blank_id=3,
                topic="Subject pronouns",
                correct_answer="they",
                distractors=("them", "their", "theirs", "themselves"),
                rule="Use the subject pronoun they to refer to multiple people as the subject.",
                explanation="They refers back to Alex and his family and acts as the subject for watch.",
            ),
        ),
        level="beginner",
        full_text=(
            "Every morning, Alex wakes up at seven o'clock. He prepares a quick breakfast because he needs energy for the day. "
            "After eating, he walks to the bus stop. The bus usually arrives on time. "
            "In the evening, he relaxes at home with his family, and they watch a movie together."
        ),
        paragraph_explanation=(
            "Paragraph Building: This paragraph organizes ideas chronologically using temporal transitions "
            "(Every morning -> After eating -> In the evening) and maintains pronoun clarity and present tense consistency."
        ),
    ),
    ParagraphBlueprint(
        title="A Weekend in the Park",
        text_with_blanks=(
            "Last Saturday, Maya visited the city park with her younger brother. The weather was sunny, [1] many people were enjoying the outdoors. "
            "They saw several children [2] near the fountain. "
            "Maya bought two ice creams, and her brother thanked [3] with a big smile."
        ),
        blanks=(
            BlankBlueprint(
                blank_id=1,
                topic="Coordinating conjunctions for results",
                correct_answer="so",
                distractors=("because", "although", "if", "while"),
                rule="Use so to connect a cause to its logical result in a compound sentence.",
                explanation="So links the pleasant sunny weather to the result of people enjoying the outdoors.",
            ),
            BlankBlueprint(
                blank_id=2,
                topic="Present participles after perception verbs",
                correct_answer="playing",
                distractors=("play", "played", "to play", "plays"),
                rule="Use the -ing participle after verbs of perception like see to describe an action in progress.",
                explanation="Playing shows the children were actively engaged in play when Maya saw them.",
            ),
            BlankBlueprint(
                blank_id=3,
                topic="Object pronouns",
                correct_answer="her",
                distractors=("she", "hers", "herself", "him"),
                rule="Use an object pronoun following a transitive verb.",
                explanation="Her is the object pronoun receiving the action of the verb thanked.",
            ),
        ),
        level="beginner",
        full_text=(
            "Last Saturday, Maya visited the city park with her younger brother. The weather was sunny, so many people were enjoying the outdoors. "
            "They saw several children playing near the fountain. Maya bought two ice creams, and her brother thanked her with a big smile."
        ),
        paragraph_explanation=(
            "Paragraph Building: Narrative paragraphs connect events smoothly by establishing setting, describing ongoing scenes, and concluding with character reactions."
        ),
    ),
    ParagraphBlueprint(
        title="Learning a Musical Instrument",
        text_with_blanks=(
            "Playing the guitar is both fun and rewarding. When Lucas first started, the chords were difficult [1] practice every day. "
            "However, he did not [2] up. "
            "Now, he plays [3] than he did last year, and his friends love listening to him."
        ),
        blanks=(
            BlankBlueprint(
                blank_id=1,
                topic="Infinitives with adjectives",
                correct_answer="to",
                distractors=("for", "in", "at", "with"),
                rule="Adjectives like difficult take a to-infinitive complement.",
                explanation="To completes the infinitive phrase 'to practice' after difficult.",
            ),
            BlankBlueprint(
                blank_id=2,
                topic="Base verb after auxiliary did not",
                correct_answer="give",
                distractors=("gives", "gave", "giving", "given"),
                rule="After the negative past auxiliary did not, use the uninflected base verb.",
                explanation="Give is the base verb needed in the phrasal verb give up.",
            ),
            BlankBlueprint(
                blank_id=3,
                topic="Irregular comparative adverbs",
                correct_answer="better",
                distractors=("good", "best", "well", "more well"),
                rule="The comparative adverb form of well is better.",
                explanation="Better compares his current guitar performance to his past skill level.",
            ),
        ),
        level="beginner",
        full_text=(
            "Playing the guitar is both fun and rewarding. When Lucas first started, the chords were difficult to practice every day. "
            "However, he did not give up. Now, he plays better than he did last year, and his friends love listening to him."
        ),
        paragraph_explanation=(
            "Paragraph Building: Using contrast transition words like 'However' helps illustrate a shift from initial challenge to eventual success."
        ),
    ),

    # -------------------------------------------------------------------------
    # INTERMEDIATE (B1 - B2) PARAGRAPHS
    # -------------------------------------------------------------------------
    ParagraphBlueprint(
        title="The Importance of Ocean Conservation",
        text_with_blanks=(
            "Oceans cover more than seventy percent of the Earth's surface and regulate global climate. [1], human activities have placed marine ecosystems under severe stress. "
            "Plastic pollution, [2] threatens thousands of species, continues to accumulate in ocean gyres. "
            "If communities [3] proactive measures to reduce waste now, future generations will inherit healthier marine habitats."
        ),
        blanks=(
            BlankBlueprint(
                blank_id=1,
                topic="Contrastive discourse transitions",
                correct_answer="However",
                distractors=("Therefore", "In addition", "For instance", "Similarly"),
                rule="Use However to signal a contrast between two distinct arguments or situations.",
                explanation="However transitions from the ocean's ecological value to the contrasting crisis of human pollution.",
            ),
            BlankBlueprint(
                blank_id=2,
                topic="Non-restrictive relative clauses",
                correct_answer="which",
                distractors=("who", "where", "what", "whose"),
                rule="Use which to introduce a non-defining relative clause providing extra details about a concept or object.",
                explanation="Which correctly refers to plastic pollution within comma boundaries.",
            ),
            BlankBlueprint(
                blank_id=3,
                topic="First conditional in future scenarios",
                correct_answer="take",
                distractors=("took", "will take", "had taken", "taking"),
                rule="In first conditional sentences, use simple present in the if-clause and will + verb in the main clause.",
                explanation="Take is simple present in the conditional clause that pairs with 'will inherit'.",
            ),
        ),
        level="intermediate",
        full_text=(
            "Oceans cover more than seventy percent of the Earth's surface and regulate global climate. However, human activities have placed marine ecosystems under severe stress. "
            "Plastic pollution, which threatens thousands of species, continues to accumulate in ocean gyres. If communities take proactive measures to reduce waste now, future generations will inherit healthier marine habitats."
        ),
        paragraph_explanation=(
            "Paragraph Building: Expository paragraphs build strength through a clear opening assertion, a transition to the counter-problem ('However'), non-defining supporting detail ('which...'), and an actionable conditional conclusion."
        ),
    ),
    ParagraphBlueprint(
        title="The Psychology of Habit Formation",
        text_with_blanks=(
            "Developing a new routine requires consistent repetition over several weeks. When an action is repeated in a specific environment, the brain creates neural pathways that make the behavior automatic. "
            "[1], trying to change multiple habits simultaneously often leads to burnout. "
            "Experts recommend [2] on one small change at a time. "
            "By [3] clear triggers, individuals can build sustainable routines that last."
        ),
        blanks=(
            BlankBlueprint(
                blank_id=1,
                topic="Adversative discourse connectors",
                correct_answer="Nonetheless",
                distractors=("Furthermore", "Consequently", "Specifically", "Namely"),
                rule="Use Nonetheless to introduce an important caveat or qualification to the preceding idea.",
                explanation="Nonetheless signals that despite the automatic nature of habits, attempting too many at once fails.",
            ),
            BlankBlueprint(
                blank_id=2,
                topic="Gerunds following recommendation verbs",
                correct_answer="focusing",
                distractors=("focus", "to focus", "focused", "focuses"),
                rule="The verb recommend directly takes a gerund (-ing form) when followed directly by an action.",
                explanation="Focusing is the gerund required after the verb recommend.",
            ),
            BlankBlueprint(
                blank_id=3,
                topic="Preposition followed by gerund",
                correct_answer="establishing",
                distractors=("establish", "established", "to establish", "establishment"),
                rule="Prepositions expressing method (such as by) take a gerund complement.",
                explanation="Establishing is the gerund indicating method following the preposition by.",
            ),
        ),
        level="intermediate",
        full_text=(
            "Developing a new routine requires consistent repetition over several weeks. When an action is repeated in a specific environment, the brain creates neural pathways that make the behavior automatic. "
            "Nonetheless, trying to change multiple habits simultaneously often leads to burnout. Experts recommend focusing on one small change at a time. "
            "By establishing clear triggers, individuals can build sustainable routines that last."
        ),
        paragraph_explanation=(
            "Paragraph Building: Effective explanatory paragraphs move from general theory to practical complication ('Nonetheless'), followed by expert guidance and methodology ('By establishing...')."
        ),
    ),
    ParagraphBlueprint(
        title="The Rise of Renewable Energy",
        text_with_blanks=(
            "Over the past decade, solar and wind power have transitioned from alternative experiments into primary energy sources. Technological advances have substantially lowered production costs, [1] clean energy more accessible worldwide. "
            "Many governments have invested heavily in infrastructure [2] meet ambitious climate targets. "
            "As energy storage systems continue to improve, reliance on fossil fuels [3] significantly over the coming decades."
        ),
        blanks=(
            BlankBlueprint(
                blank_id=1,
                topic="Participle clauses expressing result",
                correct_answer="making",
                distractors=("made", "makes", "to make", "make"),
                rule="A present participle (-ing) clause can express the natural outcome or result of the main clause action.",
                explanation="Making introduces the positive outcome resulting from lower production costs.",
            ),
            BlankBlueprint(
                blank_id=2,
                topic="Purpose expressions with infinitives",
                correct_answer="in order to",
                distractors=("so that", "due to", "in spite of", "because"),
                rule="Use in order to followed by a base verb to declare a direct objective or purpose.",
                explanation="In order to cleanly connects the government investment to the goal of meeting climate targets.",
            ),
            BlankBlueprint(
                blank_id=3,
                topic="Future predictions in complex sentences",
                correct_answer="will decrease",
                distractors=("decreased", "has decreased", "had decreased", "decreases"),
                rule="When a subordinate clause with As describes an ongoing process, the main forecast uses will + verb.",
                explanation="Will decrease expresses the expected future projection across coming decades.",
            ),
        ),
        level="intermediate",
        full_text=(
            "Over the past decade, solar and wind power have transitioned from alternative experiments into primary energy sources. Technological advances have substantially lowered production costs, making clean energy more accessible worldwide. "
            "Many governments have invested heavily in infrastructure in order to meet ambitious climate targets. As energy storage systems continue to improve, reliance on fossil fuels will decrease significantly over the coming decades."
        ),
        paragraph_explanation=(
            "Paragraph Building: Analytical paragraphs establish historical context, present causative evidence via participle clauses, state institutional purpose, and project future trends."
        ),
    ),

    # -------------------------------------------------------------------------
    # ADVANCED (C1 - C2) PARAGRAPHS
    # -------------------------------------------------------------------------
    ParagraphBlueprint(
        title="Artificial Intelligence and Governance",
        text_with_blanks=(
            "The rapid integration of autonomous algorithms into high-stakes decision making has sparked intense philosophical debate. [1] these systems offer unprecedented analytical speed, they frequently perpetuate systemic biases embedded within historical training datasets. "
            "It is therefore vital that regulatory bodies [2] transparent auditing standards for automated models. "
            "Only through rigorous oversight [3] public trust be preserved in an era of automated governance."
        ),
        blanks=(
            BlankBlueprint(
                blank_id=1,
                topic="Concessive subordinating conjunctions",
                correct_answer="While",
                distractors=("Because", "Since", "Unless", "Provided that"),
                rule="Use While or Although to introduce a dependent concession clause contrasting with the main clause.",
                explanation="While introduces the concession regarding computational speed while highlighting underlying dataset biases.",
            ),
            BlankBlueprint(
                blank_id=2,
                topic="Mandative subjunctive in that-clauses",
                correct_answer="establish",
                distractors=("establishes", "established", "will establish", "are establishing"),
                rule="Expressions of necessity or urgency (It is vital that...) require the uninflected base subjunctive form.",
                explanation="Establish is the required subjunctive base verb after 'It is vital that regulatory bodies...'.",
            ),
            BlankBlueprint(
                blank_id=3,
                topic="Restrictive inversion with Only",
                correct_answer="can",
                distractors=("could have", "is able to", "will be able", "ought"),
                rule="Sentences beginning with restrictive prepositional phrases like 'Only through...' trigger subject-auxiliary inversion.",
                explanation="Can acts as the inverted auxiliary verb preceding the subject 'public trust'.",
            ),
        ),
        level="advanced",
        full_text=(
            "The rapid integration of autonomous algorithms into high-stakes decision making has sparked intense philosophical debate. While these systems offer unprecedented analytical speed, they frequently perpetuate systemic biases embedded within historical training datasets. "
            "It is therefore vital that regulatory bodies establish transparent auditing standards for automated models. Only through rigorous oversight can public trust be preserved in an era of automated governance."
        ),
        paragraph_explanation=(
            "Paragraph Building: Academic prose achieves persuasive impact by balancing concessions ('While...'), mandating structural imperatives via subjunctive syntax, and culminating in emphatic inverted rhetoric ('Only through... can...')."
        ),
    ),
    ParagraphBlueprint(
        title="Architectural Design and Urban Well-being",
        text_with_blanks=(
            "Contemporary urban architecture is increasingly evaluated not merely by aesthetic elegance, but by [1] to foster communal well-being. Incorporating natural light and open green spaces has been proven to mitigate psychological fatigue among residents. "
            "Had urban planners recognized these benefits a century ago, modern metropolitan centers [2] far more livable today. "
            "[3] should city officials prioritize developer profits over the long-term mental health of citizens."
        ),
        blanks=(
            BlankBlueprint(
                blank_id=1,
                topic="Correlative conjunction parallelism",
                correct_answer="its capacity",
                distractors=("their capacity", "it is capable", "having capacity", "to be capable"),
                rule="Phrases connected by correlative conjunctions (not merely by... but by...) must maintain parallel prepositional structure.",
                explanation="Its capacity forms a parallel noun phrase governed by 'by', balancing 'by aesthetic elegance'.",
            ),
            BlankBlueprint(
                blank_id=2,
                topic="Mixed counterfactual conditionals",
                correct_answer="would be",
                distractors=("will be", "would have been", "had been", "are"),
                rule="When a past unreal condition ('Had planners recognized...') produces a present state ('today'), use would + base verb.",
                explanation="Would be accurately expresses the hypothetical present condition resulting from the past counterfactual.",
            ),
            BlankBlueprint(
                blank_id=3,
                topic="Negative fronting with inversion",
                correct_answer="Under no circumstances",
                distractors=("In some cases", "As a result", "For this reason", "In addition"),
                rule="Negative introductory adverbials trigger inverted auxiliary-subject word order (Under no circumstances should officials...).",
                explanation="Under no circumstances introduces the strong prohibition while triggering the inverted modal 'should city officials'.",
            ),
        ),
        level="advanced",
        full_text=(
            "Contemporary urban architecture is increasingly evaluated not merely by aesthetic elegance, but by its capacity to foster communal well-being. Incorporating natural light and open green spaces has been proven to mitigate psychological fatigue among residents. "
            "Had urban planners recognized these benefits a century ago, modern metropolitan centers would be far more livable today. Under no circumstances should city officials prioritize developer profits over the long-term mental health of citizens."
        ),
        paragraph_explanation=(
            "Paragraph Building: Sophisticated argumentation links aesthetic critique to civic duty using parallel correlative phrasing, counterfactual temporal reflection, and emphatic negative fronting."
        ),
    ),
    ParagraphBlueprint(
        title="Historical Linguistics and Language Evolution",
        text_with_blanks=(
            "Languages are dynamic systems that continually evolve in response to cultural contact, migration, and technological innovation. [1] the core syntactic structures of a language may appear stable over generations, subtle phonetic shifts relentlessly reshape pronunciation. "
            "Were researchers [2] ancient manuscripts without comparative phonological methods, many historical dialects would remain completely undecipherable. "
            "The study of etymology thus illuminates not only where words originate, but [3] societies transform over centuries."
        ),
        blanks=(
            BlankBlueprint(
                blank_id=1,
                topic="Concessive subordinating conjunctions",
                correct_answer="Even though",
                distractors=("Because", "Unless", "Provided that", "Inasmuch as"),
                rule="Use Even though to concede an apparent fact while emphasizing a contrasting reality in the independent clause.",
                explanation="Even though concedes surface structural stability while introducing the relentless reality of phonetic change.",
            ),
            BlankBlueprint(
                blank_id=2,
                topic="Inverted hypothetical conditional with Were",
                correct_answer="to examine",
                distractors=("examining", "examined", "examine", "had examined"),
                rule="Inverted second conditionals beginning with Were take a to-infinitive (Were + subject + to-verb).",
                explanation="To examine completes the inverted hypothetical conditional structure after 'Were researchers'.",
            ),
            BlankBlueprint(
                blank_id=3,
                topic="Parallel content clauses with correlative markers",
                correct_answer="how",
                distractors=("what", "which", "whom", "whose"),
                rule="Correlative structures (not only... but...) connecting noun clauses must maintain parallel interrogative syntax.",
                explanation="How forms a parallel indirect question clause matching 'where words originate'.",
            ),
        ),
        level="advanced",
        full_text=(
            "Languages are dynamic systems that continually evolve in response to cultural contact, migration, and technological innovation. Even though the core syntactic structures of a language may appear stable over generations, subtle phonetic shifts relentlessly reshape pronunciation. "
            "Were researchers to examine ancient manuscripts without comparative phonological methods, many historical dialects would remain completely undecipherable. "
            "The study of etymology thus illuminates not only where words originate, but how societies transform over centuries."
        ),
        paragraph_explanation=(
            "Paragraph Building: High-register expository writing balances scientific nuance with concessive framing, inverted hypothetical conditionals ('Were researchers to examine...'), and correlative syntactic parallelism."
        ),
    ),

    # -------------------------------------------------------------------------
    # IELTS BAND 8.0 - 9.0 (C2 / SCHOLARLY DISCOURSE & RARE VOCABULARY)
    # -------------------------------------------------------------------------
    ParagraphBlueprint(
        title="Epistemological Limits and Artificial Cognition",
        text_with_blanks=(
            "The philosophical premise that neural networks genuinely comprehend linguistic semantics remains highly contentious. "
            "[1] contemporary language models demonstrate astonishing fluency, many cognitive scientists contend that statistical mimicry is fundamentally distinct from intentional semantic grasp. "
            "It is therefore incumbent upon computational linguists that they [2] empirical paradigms capable of distinguishing syntactic fluency from true comprehension. "
            "Only by establishing such rigorous benchmarks [3] the cognitive frontier of artificial intelligence be definitively mapped."
        ),
        blanks=(
            BlankBlueprint(
                blank_id=1,
                topic="Concessive prepositional connectors",
                correct_answer="Notwithstanding the fact that",
                distractors=("Inasmuch as", "Because of", "On the premise that", "Henceforth"),
                rule="Notwithstanding the fact that introduces a formal concessive subordinate clause in scholarly prose.",
                explanation="Notwithstanding the fact that concedes the fluency of language models while introducing the counterargument regarding genuine understanding.",
            ),
            BlankBlueprint(
                blank_id=2,
                topic="Mandative subjunctive in that-clauses",
                correct_answer="devise",
                distractors=("devises", "devised", "are devising", "will devise"),
                rule="Expressions of necessity (It is incumbent upon X that they...) demand the uninflected base subjunctive verb form.",
                explanation="Devise is the required base subjunctive form following the expression of urgency.",
            ),
            BlankBlueprint(
                blank_id=3,
                topic="Inversion with restrictive fronting",
                correct_answer="can",
                distractors=("should have", "might be able", "would have", "is to"),
                rule="Sentences beginning with restrictive phrases like 'Only by...' trigger subject-auxiliary inversion in the main clause.",
                explanation="Can acts as the inverted auxiliary preceding the subject 'the cognitive frontier'.",
            ),
        ),
        level="ielts_8_9",
        full_text=(
            "The philosophical premise that neural networks genuinely comprehend linguistic semantics remains highly contentious. "
            "Notwithstanding the fact that contemporary language models demonstrate astonishing fluency, many cognitive scientists contend that statistical mimicry is fundamentally distinct from intentional semantic grasp. "
            "It is therefore incumbent upon computational linguists that they devise empirical paradigms capable of distinguishing syntactic fluency from true comprehension. "
            "Only by establishing such rigorous benchmarks can the cognitive frontier of artificial intelligence be definitively mapped."
        ),
        paragraph_explanation=(
            "Paragraph Building (IELTS Band 8-9): High-level academic discourse achieves cohesion through concessive clauses ('Notwithstanding the fact that...'), mandative subjunctive syntax, and culminative inversion ('Only by... can...')."
        ),
    ),
    ParagraphBlueprint(
        title="Historiography and Archival Hermeneutics",
        text_with_blanks=(
            "Historical scholarship cannot be reduced to a mechanical aggregation of archival chronicles. "
            "Rather, it demands a [1] interrogation of the socio-political biases underpinning primary sources. "
            "[2] researchers to accept historical treaties at face value, historiography would deteriorate into mere state propaganda. "
            "The imperative of critical scholarship is thus not merely to reconstruct historical timelines, but [3] the subterranean power dynamics that shaped those events."
        ),
        blanks=(
            BlankBlueprint(
                blank_id=1,
                topic="Rare academic adjectives for meticulousness",
                correct_answer="punctilious",
                distractors=("cursory", "perfunctory", "supercilious", "capricious"),
                rule="Punctilious means showing great attention to detail, precision, or correct scholarly rigor.",
                explanation="Punctilious conveys the rigorous, exacting interrogation required of historical sources.",
            ),
            BlankBlueprint(
                blank_id=2,
                topic="Inverted hypothetical conditional with Were",
                correct_answer="Were",
                distractors=("Had", "If", "Should", "Would"),
                rule="Inverted second conditional clauses front Were before the subject (Were researchers to accept...).",
                explanation="Were initiates the inverted hypothetical condition paired with the infinitive 'to accept'.",
            ),
            BlankBlueprint(
                blank_id=3,
                topic="Correlative syntactic parallelism",
                correct_answer="to elucidate",
                distractors=("elucidating", "elucidation of", "elucidated", "having elucidated"),
                rule="Correlative constructions with 'not merely to... but to...' require parallel infinitive structures.",
                explanation="To elucidate maintains syntactic parallelism with 'to reconstruct'.",
            ),
        ),
        level="ielts_8_9",
        full_text=(
            "Historical scholarship cannot be reduced to a mechanical aggregation of archival chronicles. "
            "Rather, it demands a punctilious interrogation of the socio-political biases underpinning primary sources. "
            "Were researchers to accept historical treaties at face value, historiography would deteriorate into mere state propaganda. "
            "The imperative of critical scholarship is thus not merely to reconstruct historical timelines, but to elucidate the subterranean power dynamics that shaped those events."
        ),
        paragraph_explanation=(
            "Paragraph Building (IELTS Band 8-9): Scholarly critique uses precise lexical adjectives ('punctilious'), inverted second conditionals ('Were researchers to accept...'), and correlative infinitives ('not merely to reconstruct... but to elucidate...')."
        ),
    ),
    ParagraphBlueprint(
        title="Macroeconomic Volatility and Fiscal Policy",
        text_with_blanks=(
            "In times of acute economic deceleration, conventional monetary easing often proves [1] due to structural liquidity traps. "
            "Under such precarious conditions, aggressive fiscal intervention becomes imperative to stimulate aggregate demand. "
            "[2] should central banks exacerbate consumer uncertainty through opaque communications. "
            "Had fiscal authorities deployed targeted infrastructure expenditures earlier, the protracted recession [3] far less debilitating today."
        ),
        blanks=(
            BlankBlueprint(
                blank_id=1,
                topic="Rare technical adjectives in economic analysis",
                correct_answer="inefficacious",
                distractors=("efficacious", "salutary", "propitious", "beneficent"),
                rule="Inefficacious means not producing the desired effect, ineffective, or futile in technical registers.",
                explanation="Inefficacious accurately describes monetary easing that fails due to liquidity traps.",
            ),
            BlankBlueprint(
                blank_id=2,
                topic="Emphatic negative fronting with inversion",
                correct_answer="On no account",
                distractors=("In some measure", "As a consequence", "For this purpose", "To that extent"),
                rule="Introductory negative adverbials like On no account trigger inverted modal-subject word order (On no account should central banks...).",
                explanation="On no account introduces the imperative prohibition while triggering inversion with 'should central banks'.",
            ),
            BlankBlueprint(
                blank_id=3,
                topic="Mixed counterfactual conditionals",
                correct_answer="would be",
                distractors=("will be", "would have been", "had been", "is"),
                rule="When a counterfactual past condition ('Had authorities deployed...') produces a present consequence ('today'), use would + base verb.",
                explanation="Would be accurately expresses the hypothetical present condition resulting from the past action.",
            ),
        ),
        level="ielts_8_9",
        full_text=(
            "In times of acute economic deceleration, conventional monetary easing often proves inefficacious due to structural liquidity traps. "
            "Under such precarious conditions, aggressive fiscal intervention becomes imperative to stimulate aggregate demand. "
            "On no account should central banks exacerbate consumer uncertainty through opaque communications. "
            "Had fiscal authorities deployed targeted infrastructure expenditures earlier, the protracted recession would be far less debilitating today."
        ),
        paragraph_explanation=(
            "Paragraph Building (IELTS Band 8-9): Advanced economic argumentation balances technical lexical precision ('inefficacious'), emphatic negative inversion ('On no account should...'), and mixed counterfactual conditional syntax ('Had authorities deployed... would be... today')."
        ),
    ),
]

