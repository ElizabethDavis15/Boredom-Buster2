from random import sample, shuffle
from dataclasses import dataclass
from drafter import *
from bakery import assert_equal

set_website_title("Boardom Buster")
set_site_information(
    author="Elizabeth Davis",
    description="Discover new hobbies and overcome boredom.",
    sources="Thanks to the Drafter docs.",
    planning=["Final Project 0_ Pick a Problem.pdf", "CS1 Final Project 1_Design.pdf"],
    links=["https://github.com/ElizabethDavis15/Boredom-Buster2"]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class Activity:
    title: str
    mood: str
    location: str
    setting: str
    cost: int

@dataclass
class State:
    selected_mood: str
    budget_max: int
    selected_group: str
    selected_location: str
    browse_location: str
    browse_mood: str
    browse_setting: str
    browse_cost: int
    activities: List[Activity]

INITIAL_ACTIVITIES: List[Activity] = [
    Activity("Board Game Night", "Medium", "At Home", "Group", 20),
    Activity("Local Library Visit", "Low", "Indoor Public", "Solo/Group", 0),
    Activity("Cycling Trip", "High", "Outdoor", "Solo/Group", 0),
    Activity("Craft Project", "Medium", "At Home", "Solo", 12),
    Activity("Learn Origami", "Low", "At Home", "Solo", 2),
    Activity("Write a Short Story", "Medium", "At Home", "Solo", 0),
    Activity("Stargazing Night", "Low", "Outdoor", "Solo/Group", 0),
    Activity("Visit a Science Museum", "Medium", "Indoor Public", "Solo/Group", 18),
    Activity("Cooking New Recipe", "Medium", "At Home", "Solo/Group", 15),
]


def helper_filter_activities(activities: List[Activity], mood: str, budget: int, group: str, location: str) -> List[Activity]:
    filtered: List[Activity] = []
    for act in activities:  
        mood_match = (act.mood == mood)
        budget_match = (act.cost <= budget)
        location_match = (act.location == location)
        group_match = (group in act.setting or act.setting == "Solo/Group" or group == "Both")
        
        if mood_match and budget_match and location_match and group_match:
            filtered.append(act)
    return filtered


def helper_setting_matches(act_setting: str, filter_setting: str) -> bool:
    """Helper function to check if activity setting matches the browse filter."""
    if filter_setting == "All":
        return True
    if filter_setting == "Solo" and "Solo" in act_setting:
        return True
    if filter_setting == "Group" and "Group" in act_setting:
        return True
    return act_setting == filter_setting


def helper_index() -> List[Any]:
    return [
        Header("BOREDOM BUSTER", 1),
        Paragraph("Stuck for things to do? Find your ideal activity."),
        Button("Home", "index"),
        Button("About", "about"),
        Button("Finder", "finder"),
        Button("Browse", "browse"),
        Button("FAQ", "faq"),
        Button("Contact", "contact"),
        HorizontalRule(),
    ]


@route
def index(state: State) -> Page:
    """Display the home page of the Boredom Buster application."""
    nav = helper_index()
    content = [
        *nav,
        Header("Welcome to Boredom Buster", 2),
        Paragraph("Discover new hobbies and overcome boredom."),
        Button("Get Started", "finder"),
    ]
    return Page(state, content)


@route
def about(state: State) -> Page:
    """Display the about page explaining the application purpose."""
    nav = helper_index()
    content = [
        *nav,
        Header("About Boredom Buster", 2),
        Paragraph("Helps users discover activities based on mood, budget, and setting."),
    ]
    return Page(state, content)


@route
def contact(state: State) -> Page:
    """Display the contact support page."""
    nav = helper_index()
    content = [
        *nav,
        Header("Contact Us", 2),
        Paragraph("Have questions? Reach out to egdavis@udel.edu"),
    ]
    return Page(state, content)


@route
def faq(state: State) -> Page:
    """Display the frequently asked questions page with 6 questions."""
    nav = helper_index()
    content = [
        *nav,
        Header("Frequently Asked Questions", 2),
        Paragraph("Q1: Is this application completely free to use?"),
        Paragraph("A1: Yes, Boredom Buster is 100% free for exploring activities."),
        Paragraph("Q2: How do I filter activities by my budget?"),
        Paragraph("A2: Use the Personal Activity Finder to type your maximum budget."),
        Paragraph("Q3: Can I find activities to do with friends?"),
        Paragraph("A3: Yes, select 'Group' or 'Both' under the Social Setting option."),
        Paragraph("Q4: Are all suggested activities suitable for beginners?"),
        Paragraph("A4: Absolutely! Most activities require no prior experience."),
        Paragraph("Q5: How do I reset or change my preferences?"),
        Paragraph("A5: Simply go back to the Finder tab and update your selections."),
    ]
    return Page(state, content)


@route
def finder(state: State, 
           mood_input: str = "Medium", 
           budget_input: str = "25",
           group_input: str = "Solo",
           location_input: str = "At Home") -> Page:
    """Process user search filters with 4 input fields."""
    state.selected_mood = mood_input          
    state.selected_group = group_input        
    state.selected_location = location_input  
    state.budget_max = int(budget_input)      

    nav = helper_index()

    content = [
        *nav,
        Header("Personal Activity Finder", 2),
        Paragraph("Tell us what you like:"),
        SelectBox("mood_input", ["Low", "Medium", "High"], state.selected_mood),                    
        TextBox("budget_input", str(state.budget_max)),   
        SelectBox("group_input", ["Solo", "Group", "Both"], state.selected_group),                   
        SelectBox("location_input", ["At Home", "Indoor Public", "Outdoor"], state.selected_location),                
        Button("View Recommendations", "recommendation"),
    ]
    return Page(state, content)


@route
def browse(state: State, loc_input: str = "All", mood_inp: str = "All", set_inp: str = "All", cost_inp: str = "50") -> Page:
    state.browse_location = loc_input
    state.browse_mood = mood_inp
    state.browse_setting = set_inp
    if cost_inp.isdigit():
        state.browse_cost = int(cost_inp)
    else:
        state.browse_cost = 50

    filtered_activities = []
    for act in state.activities:  
        loc_match = (state.browse_location == "All" or act.location == state.browse_location)
        mood_match = (state.browse_mood == "All" or act.mood == state.browse_mood)
        setting_match = helper_setting_matches(act.setting, state.browse_setting)
        cost_match = (act.cost <= state.browse_cost)

        if loc_match and mood_match and setting_match and cost_match:
            filtered_activities.append(act)

    nav = helper_index()

    content = [
        *nav,
        Header("Browse Activities", 2),
        Paragraph(f"Found {len(filtered_activities)} matching activities."),
        SelectBox("loc_input", ["All", "At Home", "Indoor Public", "Outdoor"], state.browse_location),
        SelectBox("mood_inp", ["All", "Low", "Medium", "High"], state.browse_mood),
        SelectBox("set_inp", ["All", "Solo", "Group"], state.browse_setting),
        TextBox("cost_inp", str(state.browse_cost)),
        Button("Apply Filters", "browse"),
        Table(filtered_activities),
        Button("Back to Finder", "finder"),
    ]
    return Page(state, content)


@route
def recommendation(state: State) -> Page:
    """Display a random tailored activity recommendation from matching preferences."""
    nav = helper_index()
    matched = helper_index(state.activities, state.selected_mood, state.budget_max, state.selected_group, state.selected_location)
    
    if len(matched) > 0:
        chosen_activity = random.choice(matched)
        rec_text = chosen_activity.title
    else:
        rec_text = "No exact match found for your specific combination. Try adjusting your filters in the Finder."

    content = [
        *nav,
        Header("Your Activity Recommendation", 2),
        Paragraph(rec_text),
        Button("Back to Finder", "finder"),
        Button("Browse All", "browse"),
    ]
    return Page(state, content)


if __name__ == "__main__":
    initial_state = State("Medium", 25, "Solo", "At Home", "All", "All", "All", 50, list(INITIAL_ACTIVITIES))
    start_server(initial_state)
