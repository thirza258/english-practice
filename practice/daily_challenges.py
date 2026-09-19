"""A deterministic daily vocabulary bank, with original examples and questions."""

from dataclasses import dataclass

from .course_types import Question


DAILY_ATTEMPT_KEY = "daily_challenge_attempt"


@dataclass(frozen=True)
class DailyChallenge:
    word: str
    word_class: str
    meaning: str
    example: str
    question: Question


DAILY_CHALLENGES = (
    DailyChallenge("consistent", "adjective", "Continuing in a similar, dependable way over time.", "Consistent practice helped her speak more confidently.", Question("Which habit best shows consistent practice?", ("Studying for ten minutes every weekday", "Studying once and never returning", "Changing your goal every hour"), 0, "A regular, dependable routine is consistent. The size of each session matters less than repeating it.")),
    DailyChallenge("evidence", "noun", "Information that supports or challenges a claim.", "The writer used survey results as evidence for the argument.", Question("Which sentence provides evidence for a rise in library use?", ("Libraries are wonderful places.", "Recorded visits rose from 400 to 600 per month.", "I would like a bigger library."), 1, "The recorded change supports the claim. A preference or general opinion does not demonstrate an increase.")),
    DailyChallenge("contrast", "noun / verb", "A difference between things, or the act of comparing their differences.", "In contrast to bus travel, cycling became more popular.", Question("Choose the best link: 'Car use fell. ___, cycling increased.'", ("For example", "Similarly", "In contrast"), 2, "The trends move in opposite directions, so in contrast introduces the difference.")),
    DailyChallenge("relevant", "adjective", "Directly connected to the subject or question being considered.", "A relevant example helps the reader understand your reason.", Question("Which example is relevant to a paragraph about evening library access?", ("A worker can study there after a late shift.", "Some books have blue covers.", "The library was painted last year."), 0, "The worker's access after a shift explains why evening opening matters.")),
    DailyChallenge("gradual", "adjective", "Happening slowly through small changes.", "There was a gradual improvement over several months.", Question("Which sequence best illustrates a gradual rise?", ("10, 80, 10, 80", "10, 12, 14, 16", "80, 60, 40, 20"), 1, "The second sequence rises in small regular steps. The first fluctuates and the third falls.")),
    DailyChallenge("clarify", "verb", "To make a meaning or explanation easier to understand.", "She added an example to clarify her point.", Question("Which revision helps clarify 'The service improved'?", ("The service improved very, very much.", "The improvement was an improvement.", "Average waiting time fell from twenty minutes to ten."), 2, "The concrete measure explains what improved and by how much.")),
    DailyChallenge("reliable", "adjective", "Able to be trusted to work well or give accurate information.", "A reliable bus service makes commuting easier.", Question("Which detail best supports the claim that a bus service is reliable?", ("It arrives on schedule on most days.", "Its seats are blue.", "Its route has a memorable name."), 0, "Arriving as expected is evidence of dependable service; colour and naming do not establish reliability.")),
    DailyChallenge("qualify", "verb", "To limit a statement so that it is more precise.", "The researcher qualified the claim by noting the small sample.", Question("Which sentence qualifies the claim 'Online learning helps everyone'?", ("Online learning helps absolutely everyone.", "Online learning can help learners who have suitable access and support.", "Learning is learning."), 1, "The condition limits who is likely to benefit, making the claim more precise.")),
    DailyChallenge("allocate", "verb", "To set aside time, money, or resources for a purpose.", "I allocate ten minutes to reviewing my mistakes.", Question("Which sentence uses allocate naturally?", ("I allocate happy after class.", "The passage allocates very blue.", "We allocate part of the budget to teacher training."), 2, "Allocate links a resource, such as a budget, to a purpose.")),
    DailyChallenge("infer", "verb", "To reach a conclusion from available information.", "We can infer that the event was popular because all seats were booked.", Question("All seats for a talk are booked. Which inference is best supported?", ("Demand has filled the available seats.", "Every resident wants to attend.", "The speaker will never give another talk."), 0, "Full booking supports a conclusion about available capacity, not the wishes of every resident or future talks.")),
    DailyChallenge("coherent", "adjective", "Organised so that the parts connect and are easy to follow.", "A coherent paragraph develops one main idea.", Question("Which order makes a paragraph most coherent?", ("Unrelated detail → conclusion → new topic", "Main point → explanation → relevant example", "Example → unrelated fact → repeated adjective"), 1, "The point, explanation, and example build on one another.")),
    DailyChallenge("sustain", "verb", "To keep something going over a period of time.", "Short, focused sessions can help sustain a study habit.", Question("Which plan is most likely to help sustain a study habit?", ("Study all night once, then stop.", "Set a goal with no time available for it.", "Choose a manageable daily session and review it each week."), 2, "A repeatable routine is easier to keep going than an exhausting one-off effort.")),
    DailyChallenge("proportion", "noun", "A part or share of a whole.", "The proportion of students who cycle increased.", Question("Twenty of a hundred students cycle. What proportion is this?", ("20%", "80%", "120%"), 0, "Twenty divided by one hundred is one fifth, or 20%.")),
    DailyChallenge("adapt", "verb", "To change an approach so that it fits new needs or conditions.", "She adapted her study plan after reviewing her mistakes.", Question("Which learner adapts a study plan?", ("One who ignores repeated errors", "One who adds listening review after noticing missed corrections", "One who repeats the same answers without checking"), 1, "The learner changes the plan in response to a specific need.")),
)


def challenge_for_day(day):
    return DAILY_CHALLENGES[day.toordinal() % len(DAILY_CHALLENGES)]
