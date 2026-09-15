from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class WritingPromptBlueprint:
    """A writing task the learner is asked to respond to.

    ``useful_vocabulary`` and ``model_outline`` stay hidden while the learner
    writes and are revealed together with the IELTS report, following the same
    hidden-topic principle the sentence and paragraph modes use.

    Vocabulary suggestions are optional, and outlines show one possible way to
    organise an answer. Keep titles stable within each level so wording edits
    can be applied to the corresponding saved prompt.
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
            "in the afternoon, and in the evening. Say which part of the day you enjoy most and why."
        ),
        level="beginner",
        min_words=80,
        suggested_minutes=20,
        guidance=(
            "Group your ideas into short paragraphs about the different parts of your day.",
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
            "Write about a person you admire. Say who the person is and what they are like. "
            "Give an example of something they have done and explain why you admire them."
        ),
        level="beginner",
        min_words=80,
        suggested_minutes=20,
        guidance=(
            "Introduce the person and say how you know them or know about them.",
            "Use adjectives to describe character: kind, patient, hard-working, honest.",
            "Give one short example of something the person did.",
            "Use because to explain your reasons.",
        ),
        useful_vocabulary=(
            "kind", "patient", "hard-working", "generous", "look up to",
            "take care of", "for example", "that is why",
        ),
        model_outline=(
            "Paragraph 1: who the person is. Paragraph 2: their character, with an example of what they did. "
            "Paragraph 3: why you admire them."
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
            "Begin by saying where the place is.",
            "Describe what you can see there and the activities you enjoy.",
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
            "Write about a meal you enjoy. Describe its main ingredients, how to make it, "
            "and when you usually eat it."
        ),
        level="beginner",
        min_words=80,
        suggested_minutes=20,
        guidance=(
            "Start by naming the meal.",
            "List the main ingredients using and, with, also.",
            "Describe the steps in order: first, then, next, finally.",
            "Finish by saying when you usually eat it.",
        ),
        useful_vocabulary=(
            "ingredients", "delicious", "sweet", "spicy", "first",
            "then", "finally", "traditional",
        ),
        model_outline=(
            "Paragraph 1: the meal and its main ingredients. Paragraph 2: the simple steps used to make it. "
            "Paragraph 3: when you usually eat it."
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
            "Begin by naming your hometown and saying where it is.",
            "Describe the weather and the people who live there.",
            "Mention two or three interesting places.",
            "Finish with one improvement you would like and the reason.",
        ),
        useful_vocabulary=(
            "small town", "busy", "friendly", "market", "park",
            "clean", "noisy", "I would like",
        ),
        model_outline=(
            "Paragraph 1: the name and location of your hometown. Paragraph 2: weather, people, and places. "
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
            "Explain what will be different from your usual weekend.",
        ),
        useful_vocabulary=(
            "usually", "at the weekend", "going to", "next Saturday", "but",
            "this time", "prefer", "relax",
        ),
        model_outline=(
            "Paragraph 1: your usual weekend routine. Paragraph 2: your plan for next weekend. "
            "Paragraph 3: the main similarities or differences."
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
            "Use linking words where they help explain a contrast, an addition, or a result.",
        ),
        useful_vocabulary=(
            "flexibility", "commute", "productivity", "isolation", "work-life balance",
            "in addition", "as a result", "on the other hand",
        ),
        model_outline=(
            "Introduction: paraphrase the topic and state that the trend brings both benefits and drawbacks. "
            "Body 1: advantages such as saved commuting time, flexible hours, and lower office costs. "
            "Body 2: drawbacks such as isolation, blurred boundaries, and weaker teamwork. "
            "Conclusion: summarise the main advantages and disadvantages."
        ),
    ),
    WritingPromptBlueprint(
        title="Social Media and Friendship",
        task_type="discussion",
        prompt=(
            "Some people believe that social media has made friendships weaker, while others "
            "think it helps people stay connected. Discuss both views and give your own opinion."
        ),
        level="intermediate",
        min_words=180,
        suggested_minutes=30,
        guidance=(
            "Introduce both views and make your own position clear at the start.",
            "Support each view with a concrete example.",
            "Explain how your reasons support your opinion as you discuss the two views.",
            "Keep one main idea per paragraph.",
        ),
        useful_vocabulary=(
            "superficial", "keep in touch", "face-to-face", "meaningful", "notification",
            "whereas", "nevertheless", "in my view",
        ),
        model_outline=(
            "Introduction: introduce both views and state your opinion. Body 1: explain how social media could "
            "weaken friendships, with an example. Body 2: explain how it could sustain friendships, with an "
            "example and a connection to your position. Conclusion: restate the opinion your reasons support."
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
            "State whether you agree fully, partly, or not at all, and keep your position consistent.",
            "Develop two main reasons, each with an explanation or example.",
            "If you mention an opposing view, explain how it affects your argument.",
            "Use cause and effect language: leads to, results in, therefore.",
        ),
        useful_vocabulary=(
            "congestion", "emissions", "fares", "infrastructure", "affordable",
            "therefore", "consequently", "to a large extent",
        ),
        model_outline=(
            "Introduction: introduce the spending choice and state your position. Body 1: explain one reason "
            "with an example. Body 2: develop a second reason, considering a limitation if relevant. "
            "Conclusion: explain the extent of your agreement based on those reasons."
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
            "Introduce both views and state your own opinion.",
            "Explain the reasoning behind each view, not just the view itself.",
            "Use examples from education or your own experience.",
            "Keep your opinion consistent through the discussion and conclusion.",
        ),
        useful_vocabulary=(
            "fluency", "curriculum", "pronunciation", "motivation", "immersion",
            "whereas", "in contrast", "arguably",
        ),
        model_outline=(
            "Introduction: introduce both views and state your opinion. Body 1: explain the argument for "
            "starting in primary school. Body 2: explain the argument for starting in secondary school and "
            "relate the comparison to your view. Conclusion: summarise the reasons supporting your opinion."
        ),
    ),
    WritingPromptBlueprint(
        title="Online Shopping and Local Shops",
        task_type="problem_solution",
        prompt=(
            "In some towns, local shops are losing customers to online retailers. "
            "What problems can this cause for town centres, and what could be done to address them?"
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
            "Conclusion: summarise how the proposed measures could address these problems."
        ),
    ),
    WritingPromptBlueprint(
        title="Everyday Environmental Habits",
        task_type="problem_solution",
        prompt=(
            "Many people find it difficult to change their daily habits to protect the environment. "
            "What obstacles do they face, and what could help them change these habits?"
        ),
        level="intermediate",
        min_words=180,
        suggested_minutes=30,
        guidance=(
            "Identify the obstacles before suggesting ways to overcome them.",
            "Explain how each suggestion addresses an obstacle you have described.",
            "Support claims with everyday examples.",
            "Use impersonal structures: it is often argued that, people tend to.",
        ),
        useful_vocabulary=(
            "recycle", "carbon footprint", "convenience", "incentive", "awareness",
            "tend to", "one reason for this", "in practice",
        ),
        model_outline=(
            "Introduction: introduce the difficulty of changing everyday habits. Body 1: explain obstacles "
            "such as cost, limited facilities, or lack of information. Body 2: suggest practical support for "
            "the obstacles you chose. Conclusion: summarise how this support could help people act."
        ),
    ),
    WritingPromptBlueprint(
        title="School Uniforms",
        task_type="advantages_disadvantages",
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
            "Some people think governments should limit the use of machines and software that replace workers. "
            "Others think these technologies should be encouraged because they can create new opportunities. "
            "Discuss both views and give your own opinion."
        ),
        level="advanced",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Introduce the debate and state your own position clearly.",
            "Explain how each approach could affect workers and businesses, using relevant examples.",
            "Consider both immediate job losses and possible longer-term opportunities.",
            "Connect your evaluation of the two views to the opinion you gave in the introduction.",
        ),
        useful_vocabulary=(
            "job displacement", "retraining", "productivity", "transition", "labour market",
            "employment opportunities", "in the short term", "provided that",
        ),
        model_outline=(
            "Introduction: introduce both views and state your opinion. Body 1: explain why limiting automation "
            "might protect workers, with an example. Body 2: explain why encouraging it might create benefits, "
            "and compare these with the concerns already discussed. Conclusion: draw together the reasons "
            "for your position, including any conditions you have explained."
        ),
    ),
    WritingPromptBlueprint(
        title="Urban Growth and Quality of Life",
        task_type="problem_solution",
        prompt=(
            "As cities grow, housing, transport, and public services can struggle to meet residents' needs. "
            "What problems can this cause, and what measures could address them?"
        ),
        level="advanced",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Choose a few significant problems and explain their effects on residents.",
            "Connect each proposed measure to a problem you have described.",
            "Explain who could take action and consider practical limits such as cost or space.",
            "Use cautious language for uncertain outcomes, and keep references between ideas clear.",
        ),
        useful_vocabulary=(
            "affordable housing", "congestion", "infrastructure", "public services", "urban planning",
            "population growth", "as a result", "in the long term",
        ),
        model_outline=(
            "Introduction: introduce the pressures caused by urban growth. Body 1: explain two connected "
            "problems and their effects on residents. Body 2: propose measures for those problems, explaining "
            "how they could work and any practical limits. Conclusion: summarise the response you recommend."
        ),
    ),
    WritingPromptBlueprint(
        title="Public Funding for the Arts",
        task_type="opinion",
        prompt=(
            "Some people believe governments should spend money on healthcare and education instead of "
            "funding museums, theatres, and other arts organisations. To what extent do you agree or disagree?"
        ),
        level="advanced",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "State the extent of your agreement and keep it clear throughout the essay.",
            "Explain why your spending priorities would benefit the public.",
            "If you raise an opposing view, explain how it affects your position.",
            "Use relevant examples and avoid claims that go beyond what you can support.",
        ),
        useful_vocabulary=(
            "budget allocation", "cultural heritage", "public services", "access to the arts", "opportunity cost",
            "on balance", "to some extent", "in contrast",
        ),
        model_outline=(
            "Introduction: introduce the funding choice and state your position. Body 1: explain one reason "
            "for that position, with a relevant example. Body 2: develop another reason or explain a limit to "
            "your agreement, considering the competing use of funds. Conclusion: restate the extent of your "
            "agreement using the reasoning you have developed."
        ),
    ),
    WritingPromptBlueprint(
        title="Global English and Smaller Languages",
        task_type="discussion",
        prompt=(
            "Some people believe the growing use of English threatens languages spoken by smaller communities. "
            "Others believe English can spread while these languages remain in everyday use. "
            "Discuss both views and give your own opinion."
        ),
        level="advanced",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Explain both the possible threat to local languages and how languages might coexist.",
            "Use examples from settings such as home, school, work, or the media.",
            "Consider whether the effects could differ between communities.",
            "State your opinion at the start and support it through the comparison.",
        ),
        useful_vocabulary=(
            "international communication", "mother tongue", "language preservation", "bilingual education",
            "community identity", "future generations", "meanwhile", "in this respect",
        ),
        model_outline=(
            "Introduction: introduce both views and state your opinion. Body 1: explain how greater use of "
            "English could reduce the use of a local language. Body 2: explain how communities might continue "
            "using both, and assess the conditions that matter. Conclusion: summarise your view based on "
            "the situations you have discussed."
        ),
    ),
    WritingPromptBlueprint(
        title="Prevention or Treatment",
        task_type="opinion",
        prompt=(
            "Some people believe governments should spend more on preventing illness than on treating "
            "people who are already ill. To what extent do you agree or disagree?"
        ),
        level="advanced",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Address the relative spending priority and state the extent of your agreement.",
            "Explain the likely effects of your preferred approach on patients and public health.",
            "Use examples you can explain clearly; exact spending figures are not needed.",
            "Consider both present needs and future benefits when supporting your position.",
        ),
        useful_vocabulary=(
            "preventive care", "early intervention", "public health", "treatment costs", "health education",
            "long-term benefits", "access to care", "by contrast",
        ),
        model_outline=(
            "Introduction: introduce the spending choice and state your position. Body 1: develop a reason "
            "for your preferred priority, with an example. Body 2: explain a second reason or a limit to your "
            "agreement, considering the needs of people affected. Conclusion: state the balance your "
            "argument supports."
        ),
    ),
    WritingPromptBlueprint(
        title="Degrees Delivered Online",
        task_type="advantages_disadvantages",
        prompt=(
            "More universities now offer degree courses that can be completed entirely online. "
            "What are the advantages and disadvantages of this development for students and universities?"
        ),
        level="advanced",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Include effects on both students and universities.",
            "Explain advantages and disadvantages instead of listing them without support.",
            "Use examples such as access to courses, student support, or practical training.",
            "Organise related ideas together and summarise the main benefits and drawbacks at the end.",
        ),
        useful_vocabulary=(
            "accessibility", "distance learning", "student support", "tuition fees", "practical training",
            "flexibility", "whereas", "in addition",
        ),
        model_outline=(
            "Introduction: introduce fully online degrees. Body 1: explain advantages for students and "
            "universities, with examples. Body 2: explain disadvantages for these groups, considering "
            "different kinds of courses where relevant. Conclusion: summarise the main benefits and drawbacks."
        ),
    ),
    WritingPromptBlueprint(
        title="Consumption and Sustainability",
        task_type="discussion",
        prompt=(
            "Some people believe protecting the environment requires people to buy and use fewer goods. "
            "Others think cleaner technology and more efficient production can solve environmental problems "
            "without reducing consumption. Discuss both views and give your own opinion."
        ),
        level="advanced",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Explain how buying fewer goods could reduce environmental damage.",
            "Explain how cleaner production could help and consider its possible limits.",
            "Use everyday examples of products, energy use, or waste to develop the comparison.",
            "Keep your own opinion clear while assessing both views.",
        ),
        useful_vocabulary=(
            "consumption", "energy efficiency", "resource use", "reuse", "waste reduction",
            "production methods", "over time", "in practice",
        ),
        model_outline=(
            "Introduction: introduce both views and state your opinion. Body 1: explain the case for "
            "reducing consumption, with an example. Body 2: explain the case for cleaner production and "
            "compare its potential and limits with the first approach. Conclusion: state whether one "
            "approach or a combination is better supported by your reasons."
        ),
    ),
    # -------------------------------------------------------------------------
    # IELTS BAND 8 - 9
    # -------------------------------------------------------------------------
    WritingPromptBlueprint(
        title="The Pace of Technological Change",
        task_type="opinion",
        prompt=(
            "Some people believe that technological change happens too quickly for governments and "
            "individuals to influence it. To what extent do you agree or disagree?"
        ),
        level="ielts_8_9",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "State the extent of your agreement and develop it consistently through the essay.",
            "Consider the influence of both governments and individuals, using examples you can explain.",
            "Distinguish between influencing how a technology is used and stopping its development.",
            "Choose precise vocabulary and sentence structures that express your meaning naturally.",
        ),
        useful_vocabulary=(
            "regulation", "consumer demand", "innovation", "public policy", "adoption",
            "commercial interests", "over time", "to some extent",
        ),
        model_outline=(
            "Introduction: introduce the claim and state your position. Body 1: assess the influence of "
            "governments, with an example and any relevant limits. Body 2: assess the influence of individuals "
            "and explain how it supports or qualifies your position. Conclusion: draw together your reasons "
            "and state the extent of your agreement."
        ),
    ),
    WritingPromptBlueprint(
        title="Curiosity-Driven Research",
        task_type="opinion",
        prompt=(
            "Some people believe that governments should fund scientific research only when it is likely "
            "to produce practical benefits. To what extent do you agree or disagree?"
        ),
        level="ielts_8_9",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Address the word only: explain whether practical benefits should be a condition of funding.",
            "Distinguish between immediate uses and benefits that may emerge later.",
            "Consider limited budgets and uncertainty when developing your reasons.",
            "Use examples you understand; named studies or specialist scientific knowledge are not needed.",
        ),
        useful_vocabulary=(
            "basic research", "practical applications", "long-term benefits", "research funding",
            "scientific knowledge", "unexpected discoveries", "budget priorities", "uncertainty",
        ),
        model_outline=(
            "Introduction: introduce the proposed funding rule and state your position. Body 1: develop "
            "one reason for your agreement or disagreement, with an example. Body 2: develop another reason "
            "or a limit to your position, considering uncertain outcomes and competing priorities. "
            "Conclusion: explain whether, and to what extent, the rule should apply."
        ),
    ),
    WritingPromptBlueprint(
        title="Global Media and Local Culture",
        task_type="discussion",
        prompt=(
            "Some people believe that international films, television programmes, and online media make "
            "local cultures less distinctive. Others think these media give people new ways to develop "
            "and share their own culture. Discuss both views and give your own opinion."
        ),
        level="ielts_8_9",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Explain how international media could both influence local traditions and provide opportunities.",
            "Develop the two views with specific examples of cultural practices or media content.",
            "State your opinion clearly and explain any circumstances in which the effects may differ.",
            "Link your ideas through clear references and logical connections.",
        ),
        useful_vocabulary=(
            "cultural identity", "local traditions", "global audiences", "cultural exchange", "representation",
            "adaptation", "creative industries", "in this way",
        ),
        model_outline=(
            "Introduction: introduce both views and state your opinion. Body 1: explain how international "
            "media could weaken cultural distinctiveness, with an example. Body 2: explain how it could "
            "support local cultural expression and compare the conditions behind the two effects. "
            "Conclusion: summarise the judgement supported by your discussion."
        ),
    ),
    WritingPromptBlueprint(
        title="Preserving Historic Buildings",
        task_type="opinion",
        prompt=(
            "Some people believe that cities should prioritise preserving old buildings over building "
            "new homes and public facilities. To what extent do you agree or disagree?"
        ),
        level="ielts_8_9",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Address the proposed priority and state the extent of your agreement.",
            "Explain which features could make an old building worth preserving.",
            "Consider residents' needs and the costs of the choices you discuss.",
            "Support your position with examples and make any exceptions clear.",
        ),
        useful_vocabulary=(
            "heritage", "renovation", "housing shortage", "public facilities", "maintenance costs",
            "historical significance", "land use", "community needs",
        ),
        model_outline=(
            "Introduction: introduce the competing priorities and state your position. Body 1: explain "
            "one reason for that position, with an example. Body 2: develop a second reason or a limit to "
            "your agreement, comparing the value of preservation with residents' needs. Conclusion: state "
            "the priority your argument supports and any exceptions already explained."
        ),
    ),
    WritingPromptBlueprint(
        title="Funding Space Exploration",
        task_type="discussion",
        prompt=(
            "Some people think governments should spend money on space exploration because it supports "
            "scientific progress. Others believe this money should be used to solve problems on Earth. "
            "Discuss both views and give your own opinion."
        ),
        level="ielts_8_9",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Explain the reasoning behind each spending priority and state your own position.",
            "Consider possible benefits, costs, and the time needed for benefits to appear.",
            "Use relevant examples without inventing figures or relying on technical knowledge.",
            "Make your final judgement follow from the comparison you have developed.",
        ),
        useful_vocabulary=(
            "scientific progress", "public investment", "technological advances", "research costs",
            "competing priorities", "long-term benefits", "immediate needs", "on balance",
        ),
        model_outline=(
            "Introduction: introduce both views and state your opinion. Body 1: explain the case for "
            "funding space exploration, including a potential benefit and its limits. Body 2: explain the "
            "case for spending on problems on Earth and compare the priorities. Conclusion: summarise "
            "the allocation of resources your reasoning supports."
        ),
    ),
    WritingPromptBlueprint(
        title="Measuring National Progress",
        task_type="opinion",
        prompt=(
            "Economic growth is often used to judge how much a country is progressing. "
            "To what extent do you agree that it is the best way to measure national progress?"
        ),
        level="ielts_8_9",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "State whether economic growth is the best measure and explain the extent of your agreement.",
            "Explain what growth can indicate about people's lives and what it may leave out.",
            "Compare it with relevant alternatives, developing the comparison rather than listing measures.",
            "Support your judgement with clear examples; exact national statistics are not required.",
        ),
        useful_vocabulary=(
            "living standards", "quality of life", "economic output", "public health", "inequality",
            "environmental impact", "wellbeing", "indicators",
        ),
        model_outline=(
            "Introduction: introduce economic growth as a measure and state your position. Body 1: assess "
            "what growth can tell us about progress, with an example. Body 2: compare it with another "
            "relevant measure and explain how that comparison supports your position. Conclusion: state "
            "whether growth is the best measure, or whether your reasons support a broader approach."
        ),
    ),
    WritingPromptBlueprint(
        title="Universities and Employability",
        task_type="discussion",
        prompt=(
            "Some people think the main purpose of university education is to prepare students for employment. "
            "Others believe universities should also help students develop knowledge and skills that benefit "
            "society more widely. Discuss both views and give your own opinion."
        ),
        level="ielts_8_9",
        min_words=250,
        suggested_minutes=40,
        guidance=(
            "Explain the reasoning behind both views and make your own position clear.",
            "Use examples of how university courses or activities could serve each purpose.",
            "Consider where the purposes might compete and where they could support each other.",
            "Develop your argument across paragraphs, with reasons for any priorities you recommend.",
        ),
        useful_vocabulary=(
            "graduate employment", "career preparation", "critical thinking", "independent research",
            "transferable skills", "social contribution", "curriculum", "in the long term",
        ),
        model_outline=(
            "Introduction: introduce both views and state your opinion. Body 1: explain the case for "
            "preparing students for employment, with an example. Body 2: explain the wider purposes of "
            "higher education and consider how they relate to career preparation. Conclusion: summarise "
            "the role of universities that your discussion supports."
        ),
    ),
]
