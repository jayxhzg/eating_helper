from fsm import TocMachine

def CreateFSM():
    machine = TocMachine(
        states=["user", "menu", "description", "select_type", "select_location", "show_result", "select_detail"],
        transitions=[
            {
                "trigger": "advance",
                "source": ["user", "description", "select_type", "select_location", "show_result", "select_detail"],
                "dest": "menu",
                "conditions": "is_going_to_menu",
            },
            {
                "trigger": "advance",
                "source": "menu",
                "dest": "description",
                "conditions": "is_going_to_description",
            },
            {
                "trigger": "advance",
                "source": "menu",
                "dest": "select_type",
                "conditions": "is_going_to_select_type",
            },
            {
                "trigger": "advance",
                "source": "menu",
                "dest": "select_location",
                "conditions": "is_going_to_select_location",
            },
            {
                "trigger": "advance",
                "source": "select_type",
                "dest": "select_location",
                "conditions": "is_going_to_select_location",
            },
            {
                "trigger": "advance",
                "source": "select_location",
                "dest": "show_result",
                "conditions": "is_going_to_show_result",
            },
            {
                "trigger": "advance",
                "source": ["show_result", "select_detail"],
                "dest": "select_detail",
                "conditions": "is_going_to_select_detail",
            },
            # {"trigger": "go_back", "source": ["description, show_result"], "dest": "user"},
        ],
        initial="user",
        auto_transitions=False,
        show_conditions=True,
    )
    return machine