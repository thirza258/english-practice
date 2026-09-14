from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class WritingPromptBlueprint:
    """A writing task the learner is asked to respond to.

    ``useful_vocabulary`` and ``model_outline`` stay hidden while the learner
    writes and are revealed together with the IELTS report, following the same
    hidden-topic principle the sentence and paragraph modes use.
    """

    title: str
    task_type: str
    prompt: str
    level: str
    min_words: int
    suggested_minutes: int
    guidance: Sequence[str]
    useful_vocabulary: Sequence[str]
    model_outline: str


WRITING_PROMPT_BANK: list[WritingPromptBlueprint] = [
    # -------------------------------------------------------------------------
    # BEGINNER (A1 - A2)
    # -------------------------------------------------------------------------
    WritingPromptBlueprint(
        title="My Daily Routine",
        task_type="descriptive",
        prompt=(
            "Describe a normal day in your life. Write about what you do in the morning, "
            "in the afternoon, and in the evening, and say which part of the day you enjoy most."
        ),
        level="beginner",
        min_words=80,
        suggested_minutes=20,
        guidance=(
            "Write at least three short paragraphs: morning, afternoon, evening.",
            "Use the simple present tense for habits (I wake up, she cooks).",
            "Join ideas with and, but, because, so, then, after that.",
            "Finish with one sentence saying which part of the day you like best and why.",
        ),
        useful_vocabulary=(
            "usually", "in the morning", "after that", "before", "at the same time",
            "in the evening", "every day", "finally",
        ),
        model_outline=(
            "Paragraph 1: when you wake up and your morning activities. "
            "Paragraph 2: what you do during the day (study, work, meals). "
            "Paragraph 3: your evening routine and the part of the day you enjoy most, with a reason."
        ),
    ),
    WritingPromptBlueprint(
        title="A Person I Admire",
        task_type="descriptive",
        prompt=(
            "Write about a person you admire. Explain who the person is, what they are like, "
            "and why this person is important to you."
        ),
        level="beginner",
        min_words=80,
        suggested_minutes=20,
        guidance=(
            "Introduce the person in the first sentence (name and relationship).",
            "Use adjectives to describe character: kind, patient, hard-working, honest.",
            "Give one short example of something the person did.",
            "Use because to explain your reasons.",
        ),
        useful_vocabulary=(
            "kind", "patient", "hard-working", "generous", "look up to",
            "take care of", "for example", "that is why",
        ),
        model_outline=(
            "Paragraph 1: who the person is. Paragraph 2: what they look like and what they are like. "
            "Paragraph 3: one example of their behaviour and why you admire them."
        ),
    ),
    WritingPromptBlueprint(
        title="My Favourite Place",
        task_type="descriptive",
        prompt=(
            "Describe a place you like to visit. Say where it is, what you can see and do there, "
            "and how you feel when you are in this place."
        ),
        level="beginner",
        min_words=80,
        suggested_minutes=20,
        guidance=(
            "Say where the place is and how you get there.",
            "Describe what you can see, hear, and smell.",
            "Use prepositions of place: near, next to, in front of, between.",
            "End with how the place makes you feel.",
        ),
        useful_vocabulary=(
            "quiet", "crowded", "beautiful", "next to", "far from",
            "relaxed", "peaceful", "spend time",
        ),
        model_outline=(
            "Paragraph 1: name and location of the place. Paragraph 2: what it looks like and what you do there. "
            "Paragraph 3: your feelings and why you return."
        ),
    ),
    WritingPromptBlueprint(
        title="Food I Like to Eat",
        task_type="descriptive",
        prompt=(
            "Write about a meal you enjoy. Explain what it is, how it is made, "
            "and when you usually eat it."
        ),
        level="beginner",
        min_words=80,
        suggested_minutes=20,
        guidance=(
            "Name the dish and say where it comes from.",
            "List the main ingredients using and, with, also.",
            "Describe the steps in order: first, then, next, finally.",
            "Say when and with whom you eat it.",
        ),
        useful_vocabulary=(
            "ingredients", "delicious", "sweet", "spicy", "first",
            "then", "finally", "traditional",
        ),
        model_outline=(
            "Paragraph 1: the dish and where it comes from. Paragraph 2: ingredients and how it is cooked. "
            "Paragraph 3: when you eat it and why you like it."
        ),
    ),
    WritingPromptBlueprint(
        title="A Day I Remember",
        task_type="narrative",
        prompt=(
            "Write about a day you will always remember. Say when it happened, what you did, "
            "and why this day was special for you."
        ),
        level="beginner",
        min_words=80,
        suggested_minutes=20,
        guidance=(
            "Use the simple past tense: went, saw, ate, felt.",
            "Tell the events in the order they happened.",
            "Use time words: last year, in the morning, after that, at the end.",
            "Explain your feelings at the end of the story.",
        ),
        useful_vocabulary=(
            "last year", "suddenly", "after that", "excited", "surprised",
            "at the end", "I will never forget", "happy",
        ),
        model_outline=(
            "Paragraph 1: when and where it happened. Paragraph 2: what happened, step by step. "
            "Paragraph 3: how you felt and why you remember it."
        ),
    ),
    WritingPromptBlueprint(
        title="My Hometown",
        task_type="descriptive",
        prompt=(
            "Describe your hometown. Write about the people, the weather, and the places there, "
            "and say one thing you would like to improve about it."
        ),
        level="beginner",
        min_words=80,
        suggested_minutes=20,
        guidance=(
            "Say where your hometown is and how big it is.",
            "Describe the weather and the people who live there.",
            "Mention two or three interesting places.",
            "Finish with one improvement you would like and the reason.",
        ),
        useful_vocabulary=(
            "small town", "busy", "friendly", "market", "park",
            "clean", "noisy", "I would like",
        ),
        model_outline=(
            "Paragraph 1: location and size. Paragraph 2: weather, people, and places. "
            "Paragraph 3: one improvement you want and why."
        ),
    ),
    WritingPromptBlueprint(
        title="Weekend Plans",
        task_type="descriptive",
        prompt=(
            "What do you usually do at the weekend, and what are you going to do next weekend? "
            "Compare your normal weekend with your plan."
        ),
        level="beginner",
        min_words=80,
        suggested_minutes=20,
        guidance=(
            "Use the simple present for your usual weekend.",
            "Use going to or will for your plan.",
            "Compare the two with but, however, this time.",
            "Say which one you prefer.",
        ),
        useful_vocabulary=(
            "usually", "at the weekend", "going to", "next Saturday", "but",
            "this time", "prefer", "relax",
        ),
        model_outline=(
            "Paragraph 1: your usual weekend routine. Paragraph 2: your plan for next weekend. "
            "Paragraph 3: the difference and which you prefer."
        ),
    ),
    # -------------------------------------------------------------------------
    # INTERMEDIATE (B1 - B2)
    # -------------------------------------------------------------------------
    WritingPromptBlueprint(
        title="Working From Home",
        task_type="advantages_disadvantages",
        prompt=(
            "More companies now allow their staff to work from home. "
            "What are the advantages and disadvantages of this development? "
            "Give reasons for your answer and include relevant examples."
        ),
        level="intermediate",
        min_words=180,
        suggested_minutes=30,
        guidance=(
            "Write an introduction that rephrases the question in your own words.",
            "Devote one body paragraph to advantages and one to disadvantages.",
            "Open each body paragraph with a clear topic sentence.",
            "Use linking words: however, in addition, as a result, for instance.",
        ),
        useful_vocabulary=(
            "flexibility", "commute", "productivity", "isolation", "work-life balance",
            "in addition", "as a result", "on the other hand",
        ),
        model_outline=(
            "Introduction: paraphrase the topic and state that the trend brings both benefits and drawbacks. "
            "Body 1: advantages such as saved commuting time, flexible hours, and lower office costs. "
            "Body 2: drawbacks such as isolation, blurred boundaries, and weaker teamwork. "
            "Conclusion: a balanced judgement."
        ),
    ),
    WritingPromptBlueprint(
        title="Social Media and Friendship",
        task_type="opinion",
        prompt=(
            "Some people believe that social media has made friendships weaker, while others "
            "think it helps people stay connected. Discuss both views and give your own opinion."
        ),
        level="intermediate",
        min_words=180,
        suggested_minutes=30,
        guidance=(
            "Present both views fairly before giving your own opinion.",
            "Support each view with a concrete example.",
            "Signal your position clearly: in my view, I would argue that.",
            "Keep one main idea per paragraph.",
        ),
        useful_vocabulary=(
            "superficial", "keep in touch", "face-to-face", "meaningful", "notification",
            "whereas", "nevertheless", "in my view",
        ),
        model_outline=(
            "Introduction: summarise both positions. Body 1: the view that social media weakens friendship. "
            "Body 2: the view that it sustains connection. Conclusion: your own reasoned opinion."
        ),
    ),
    WritingPromptBlueprint(
        title="Public Transport or Private Cars",
        task_type="opinion",
        prompt=(
            "Some people argue that cities should spend money on public transport rather than "
            "on building new roads for private cars. To what extent do you agree or disagree?"
        ),
        level="intermediate",
        min_words=180,
        suggested_minutes=30,
        guidance=(
            "State your position in the introduction and keep it consistent.",
            "Give two or three supporting reasons, each in its own paragraph.",
            "Acknowledge the opposing argument briefly before answering it.",
            "Use cause and effect language: leads to, results in, therefore.",
        ),
        useful_vocabulary=(
            "congestion", "emissions", "fares", "infrastructure", "affordable",
            "therefore", "consequently", "to a large extent",
        ),
        model_outline=(
            "Introduction: paraphrase plus a clear position. Body 1: strongest reason with an example. "
            "Body 2: second reason. Body 3: the opposing argument and your response. Conclusion: restate the position."
        ),
    ),
    WritingPromptBlueprint(
        title="Learning a Second Language",
        task_type="discussion",
        prompt=(
            "Some educators believe children should start learning a foreign language in primary school, "
            "while others say it is better to begin in secondary school. Discuss both views and state your opinion."
        ),
        level="intermediate",
        min_words=180,
        suggested_minutes=30,
        guidance=(
            "Explain the reasoning behind each view, not just the view itself.",
            "Use examples from education or your own experience.",
            "Compare with while, whereas, in contrast.",
            "Make your own opinion unmistakable in the conclusion.",
        ),
        useful_vocabulary=(
            "fluency", "curriculum", "pronunciation", "motivation", "immersion",
            "whereas", "in contrast", "arguably",
        ),
        model_outline=(
            "Introduction: introduce both sides. Body 1: the early-start argument. "
            "Body 2: the later-start argument. Conclusion: your opinion with a justification."
        ),
    ),
    WritingPromptBlueprint(
        title="Online Shopping and Local Shops",
        task_type="problem_solution",
        prompt=(
            "The growth of online shopping has caused many shops in town centres to close. "
            "What problems does this create, and what measures could reduce them?"
        ),
        level="intermediate",
        min_words=180,
        suggested_minutes=30,
        guidance=(
            "Dedicate one paragraph to problems and one to measures.",
            "Make sure each measure answers a problem you raised.",
            "Use modal verbs for recommendations: should, could, ought to.",
            "Develop your ideas instead of simply listing them.",
        ),
        useful_vocabulary=(
            "retail", "small businesses", "employment", "incentive", "town centre",
            "one solution would be", "in order to", "as a consequence",
        ),
        model_outline=(
            "Introduction: describe the trend. Body 1: problems such as job losses, emptier town centres, and less "
            "community life. Body 2: measures such as lower rents, mixed-use spaces, and local delivery hubs. "
            "Conclusion: which measure matters most."
        ),
    ),
    WritingPromptBlueprint(
        title="Everyday Environmental Habits",
        task_type="problem_solution",
        prompt=(
            "People are often told to change their daily habits to protect the environment, "
            "yet many do not. Why is this the case, and what could encourage people to act?"
        ),
        level="intermediate",
        min_words=180,
        suggested_minutes=30,
        guidance=(
            "Give reasons before suggesting solutions.",
            "Make the link between each cause and its remedy explicit.",
            "Support claims with everyday examples.",
            "Use impersonal structures: it is often argued that, people tend to.",
        ),
        useful_vocabulary=(
            "recycle", "carbon footprint", "convenience", "incentive", "awareness",
            "tend to", "one reason for this", "in practice",
        ),
        model_outline=(
            "Introduction: state the gap between advice and behaviour. Body 1: reasons such as cost, convenience, and "
            "low awareness. Body 2: encouragements such as education, discounts, and clearer labelling. "
            "Conclusion: a realistic assessment."
        ),
    ),
    WritingPromptBlueprint(
        title="School Uniforms",
        task_type="opinion",
        prompt=(
            "Many schools require students to wear a uniform. Do the benefits of this policy "
            "outweigh the drawbacks? Give reasons and relevant examples."
        ),
        level="intermediate",
        min_words=180,
        suggested_minutes=30,
        guidance=(
            "Answer the exact question: do the benefits outweigh the drawbacks?",
            "Weigh the two sides rather than simply listing them.",
            "Use comparative language: more significant than, outweigh, minor.",
            "Keep your conclusion consistent with your body paragraphs.",
        ),
        useful_vocabulary=(
            "equality", "self-expression", "discipline", "belonging", "peer pressure",
            "outweigh", "on balance", "admittedly",
        ),
        model_outline=(
            "Introduction: the policy and your overall judgement. Body 1: benefits such as equality, focus, and lower "
            "cost. Body 2: drawbacks such as limited self-expression and the expense of specific items. "
            "Conclusion: the weighed verdict."
        ),
    ),
    # -------------------------------------------------------------------------
    # ADVANCED (C1 - C2)
    # -------------------------------------------------------------------------
    WritingPromptBlueprint(
        title="Automation and Employment",
        task_type="discussion",
        prompt=(
            "Automation is expected to replace a substantial proportion of existing jobs. "
            "Some argue that this change should be slowed, while others believe it should be welcomed "
            "and its benefits shared widely. Discuss both positions and give your own view."
        ),
        level="advanced",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Establish the terms of the debate precisely in the introduction.",
            "Develop each position with a mechanism, not merely an assertion.",
            "Concede the strongest opposing point before answering it.",
            "Vary sentence structure: fronted adverbials, participle clauses, conditionals.",
        ),
        useful_vocabulary=(
            "displacement", "retraining", "productivity gains", "transition", "labour market",
            "albeit", "insofar as", "it follows that",
        ),
        model_outline=(
            "Introduction: define the tension between protection and acceleration. "
            "Body 1: the case for slowing automation, including transition costs and regional decline. "
            "Body 2: the case for welcoming it, including productivity and shared gains. "
            "Body 3: your synthesis with a qualified position. Conclusion: the decisive consideration."
        ),
    ),
    WritingPromptBlueprint(
        title="Urban Growth and Quality of Life",
        task_type="problem_solution",
        prompt=(
            "Rapid urban growth has improved economic opportunity but placed pressure on housing, transport, "
            "and public services. Analyse the most serious consequences and evaluate possible responses."
        ),
        level="advanced",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Prioritise consequences rather than listing every possible one.",
            "Evaluate each response, including its limitations.",
            "Use hedging where evidence is uncertain: may, is likely to, tends to.",
            "Link paragraphs with referencing expressions: this pressure, such measures.",
        ),
        useful_vocabulary=(
            "density", "zoning", "affordability", "mitigate", "public provision",
            "consequently", "notwithstanding", "to that end",
        ),
        model_outline=(
            "Introduction: frame urban growth as a trade-off. Body 1: the most serious consequence, analysed causally. "
            "Body 2: a secondary consequence. Body 3: responses evaluated with their limits. "
            "Conclusion: the response with the best balance of cost and benefit."
        ),
    ),
    WritingPromptBlueprint(
        title="Public Funding for the Arts",
        task_type="opinion",
        prompt=(
            "Some maintain that public money should be directed to healthcare and education rather than "
            "to museums, theatres, and orchestras. To what extent do you agree with this view?"
        ),
        level="advanced",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Take a defensible position and qualify it explicitly.",
            "Distinguish between different kinds of cultural spending.",
            "Use concessive structures: while it is true that, granted that.",
            "Avoid absolute claims that you cannot defend.",
        ),
        useful_vocabulary=(
            "discretionary spending", "cultural heritage", "intangible", "custodianship", "wider benefit",
            "granted that", "conversely", "on these grounds",
        ),
        model_outline=(
            "Introduction: the competing claims on public funds and your position. "
            "Body 1: the strongest case for prioritising healthcare and education. "
            "Body 2: what would be lost without cultural funding. "
            "Body 3: a principled criterion for allocation. Conclusion: your qualified verdict."
        ),
    ),
    WritingPromptBlueprint(
        title="Global English and Smaller Languages",
        task_type="discussion",
        prompt=(
            "The dominance of English in science, commerce, and the internet is said to accelerate "
            "the decline of smaller languages. Examine this claim and discuss what, if anything, should be done."
        ),
        level="advanced",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Test the claim rather than accepting it uncritically.",
            "Separate correlation from causation in your reasoning.",
            "Refer to counter-examples where they exist.",
            "Use nominalisation to compress ideas: the decline of, the spread of.",
        ),
        useful_vocabulary=(
            "lingua franca", "language shift", "revitalisation", "transmission", "prestige",
            "arguably", "in this respect", "far from being",
        ),
        model_outline=(
            "Introduction: state the claim and signal that it requires qualification. "
            "Body 1: evidence supporting the claim. Body 2: complicating evidence. "
            "Body 3: what policy could achieve, and its limits. Conclusion: a measured judgement."
        ),
    ),
    WritingPromptBlueprint(
        title="Prevention or Treatment",
        task_type="opinion",
        prompt=(
            "Health systems spend far more on treating illness than on preventing it. "
            "Should this balance be reversed? Argue your case with reasons and examples."
        ),
        level="advanced",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Address the trade-off directly rather than praising both options.",
            "Reason quantitatively even without exact figures.",
            "Anticipate the objection about short political time horizons.",
            "Maintain a consistently formal register.",
        ),
        useful_vocabulary=(
            "screening", "long-term returns", "behavioural change", "allocation", "public health",
            "were governments to", "not only ... but also", "by contrast",
        ),
        model_outline=(
            "Introduction: the current imbalance and your position. Body 1: the case for prevention. "
            "Body 2: why treatment retains its claim. Body 3: the objection about political incentives, answered. "
            "Conclusion: the balance you would defend."
        ),
    ),
    WritingPromptBlueprint(
        title="Degrees Delivered Online",
        task_type="advantages_disadvantages",
        prompt=(
            "Universities increasingly deliver degrees entirely online. "
            "Assess the benefits and costs of this shift for students, institutions, and society."
        ),
        level="advanced",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Treat the three groups distinctly rather than blurring them.",
            "Weigh benefits against costs instead of listing them separately.",
            "Use evaluative adjectives: marginal, decisive, negligible, substantial.",
            "Close with a judgement, not a summary.",
        ),
        useful_vocabulary=(
            "accessibility", "completion rates", "accreditation", "cohort", "teaching quality",
            "whereas", "in the aggregate", "crucially",
        ),
        model_outline=(
            "Introduction: the shift and the criteria for judging it. Body 1: students. "
            "Body 2: institutions. Body 3: society. Conclusion: where the balance falls."
        ),
    ),
    WritingPromptBlueprint(
        title="Consumption and Sustainability",
        task_type="discussion",
        prompt=(
            "It is often claimed that sustainability cannot be achieved without reducing consumption. "
            "Others argue that improvements in efficiency are sufficient. Evaluate both claims."
        ),
        level="advanced",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Explain the mechanism behind each claim before judging it.",
            "Address the rebound effect if you argue for efficiency.",
            "Sustain one line of argument across the whole essay.",
            "Employ parallel structures for emphasis.",
        ),
        useful_vocabulary=(
            "decoupling", "rebound effect", "circular economy", "resource use", "sufficiency",
            "insofar as", "it is precisely", "on this reading",
        ),
        model_outline=(
            "Introduction: the two competing claims. Body 1: the argument for reducing consumption. "
            "Body 2: the efficiency argument and the rebound objection. Body 3: your evaluation. "
            "Conclusion: which claim survives scrutiny."
        ),
    ),
    # -------------------------------------------------------------------------
    # IELTS BAND 8 - 9
    # -------------------------------------------------------------------------
    WritingPromptBlueprint(
        title="The Pace of Technological Change",
        task_type="opinion",
        prompt=(
            "Some commentators contend that technological development is an autonomous force to which "
            "societies must simply adapt. Others insist that its direction reflects deliberate collective choices. "
            "To what extent do you agree that technological change is beyond collective control?"
        ),
        level="ielts_8_9",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Define what would count as evidence for and against the claim.",
            "Sustain a single thesis and return to it at each stage of the argument.",
            "Deploy low-frequency lexis precisely rather than decoratively.",
            "Vary syntax with inversion, cleft sentences, and mixed conditionals.",
        ),
        useful_vocabulary=(
            "contingent", "path dependency", "malleable", "inexorable", "deliberation",
            "notwithstanding", "were it not for", "far from being inevitable",
        ),
        model_outline=(
            "Introduction: delimit the claim and stake a thesis. Body 1: the strongest version of the autonomy case. "
            "Body 2: historical counter-evidence of deliberate steering. Body 3: reconcile the two through a mechanism "
            "such as path dependency. Conclusion: the precise extent of your agreement."
        ),
    ),
    WritingPromptBlueprint(
        title="Curiosity-Driven Research",
        task_type="opinion",
        prompt=(
            "Public research funding is increasingly allocated to projects with demonstrable practical application. "
            "Assess whether curiosity-driven enquiry can be justified under such criteria."
        ),
        level="ielts_8_9",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Examine the evaluation criterion itself, not merely its outcomes.",
            "Use historical examples where basic research produced unforeseen applications.",
            "Employ the mandative subjunctive where appropriate: it is imperative that funding be.",
            "Avoid rhetorical questions as substitutes for argument.",
        ),
        useful_vocabulary=(
            "serendipity", "utilitarian", "incommensurable", "attenuate", "foundational",
            "it is imperative that", "were funding to be", "precisely because",
        ),
        model_outline=(
            "Introduction: the funding criterion and your thesis. Body 1: why the criterion is intuitive. "
            "Body 2: why it misdescribes how discovery proceeds. Body 3: an alternative allocation principle. "
            "Conclusion: the justification you defend."
        ),
    ),
    WritingPromptBlueprint(
        title="Global Media and Local Culture",
        task_type="discussion",
        prompt=(
            "Global media is often said to be eroding cultural distinctiveness. Others observe that local "
            "cultures adapt and reinterpret imported forms. Evaluate these competing accounts."
        ),
        level="ielts_8_9",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Examine the assumptions each account makes about cultural change.",
            "Use concrete cultural examples to test abstract claims.",
            "Exploit fronting and inversion for emphasis: rarely has, only when.",
            "Resist an unearned both-sides conclusion.",
        ),
        useful_vocabulary=(
            "hybridity", "vernacular", "homogenisation", "reinterpretation", "distinctiveness",
            "rarely has", "far from eroding", "to the extent that",
        ),
        model_outline=(
            "Introduction: the two accounts and your position. Body 1: the erosion account and its evidence. "
            "Body 2: the adaptation account and its evidence. Body 3: a criterion that separates them. "
            "Conclusion: which account explains more."
        ),
    ),
    WritingPromptBlueprint(
        title="Preserving Historic Buildings",
        task_type="opinion",
        prompt=(
            "Conserving historic buildings consumes resources that could fund new housing and public facilities. "
            "Assess whether conservation can be justified when cities face pressing contemporary needs."
        ),
        level="ielts_8_9",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Avoid treating heritage value as self-evident; argue for it.",
            "Distinguish between conservation, restoration, and adaptive reuse.",
            "Concede the opportunity cost explicitly before answering it.",
            "Sustain an information-dense, nominalised academic register.",
        ),
        useful_vocabulary=(
            "adaptive reuse", "opportunity cost", "irreplaceable", "continuity", "stewardship",
            "granted that", "it does not follow that", "on these grounds",
        ),
        model_outline=(
            "Introduction: the trade-off and your thesis. Body 1: the case that current needs should prevail. "
            "Body 2: what conservation secures that new building cannot. Body 3: a criterion for deciding between "
            "them. Conclusion: your scoped judgement."
        ),
    ),
    WritingPromptBlueprint(
        title="Funding Space Exploration",
        task_type="discussion",
        prompt=(
            "Space exploration is defended as a driver of scientific progress and criticised as a costly "
            "distraction from problems on Earth. Evaluate the strength of each position."
        ),
        level="ielts_8_9",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Assess the reasoning of each position, not merely its conclusion.",
            "Question whether the two aims genuinely compete for the same resources.",
            "Use precise quantifying language: a negligible fraction, disproportionate.",
            "Reach a conclusion that follows from the argument you have made.",
        ),
        useful_vocabulary=(
            "spillover", "negligible", "disproportionate", "prestige", "long-horizon",
            "insofar as", "by the same token", "it is far from clear that",
        ),
        model_outline=(
            "Introduction: the competing positions and your thesis. Body 1: the scientific and technological case. "
            "Body 2: the objection from terrestrial priorities. Body 3: whether the trade-off is real. "
            "Conclusion: which position is better supported."
        ),
    ),
    WritingPromptBlueprint(
        title="Measuring National Progress",
        task_type="opinion",
        prompt=(
            "Economic output remains the principal measure of national progress, although it captures neither "
            "wellbeing nor environmental cost. Assess whether it should be replaced by broader indicators."
        ),
        level="ielts_8_9",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Explain what the current measure does well before criticising it.",
            "Address the practical objection that broader indicators resist measurement.",
            "Use conditional inversion: were such indicators adopted.",
            "Keep claims proportionate to the evidence you can offer.",
        ),
        useful_vocabulary=(
            "aggregate", "proxy", "externality", "commensurable", "wellbeing",
            "were such measures to", "not merely", "on no account",
        ),
        model_outline=(
            "Introduction: the measure, its limits, and your thesis. Body 1: why output remains useful. "
            "Body 2: what it systematically omits. Body 3: whether alternatives can be measured reliably. "
            "Conclusion: the reform you would defend."
        ),
    ),
    WritingPromptBlueprint(
        title="Universities and Employability",
        task_type="discussion",
        prompt=(
            "Universities are increasingly judged by the employment outcomes of their graduates. "
            "Discuss whether this expectation is compatible with the wider purposes of higher education."
        ),
        level="ielts_8_9",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Identify where the two purposes conflict in practice, not only in theory.",
            "Argue for a priority ordering and defend it.",
            "Use correlative structures: not merely ... but rather.",
            "Ensure every paragraph advances the thesis rather than restating it.",
        ),
        useful_vocabulary=(
            "vocational", "intellectual formation", "instrumental", "metric", "curriculum",
            "not merely", "but rather", "were universities to",
        ),
        model_outline=(
            "Introduction: the two purposes and the tension between them. Body 1: the legitimacy of the employment "
            "expectation. Body 2: what a purely instrumental measure omits. Body 3: where the conflict is real and "
            "how it should be resolved. Conclusion: your defended ordering."
        ),
    ),
]
