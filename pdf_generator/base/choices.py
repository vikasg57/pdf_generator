class StateStatuses:
    ACTIVE = 0
    INACTIVE = 1


STATE_CHOICES = (
    (StateStatuses.ACTIVE, "ACTIVE"),
    (StateStatuses.INACTIVE, "INACTIVE")
)

CONTENT_TYPE = {
    'JPG': 'image/jpeg',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'JPEG': 'image/jpeg',
    'png': 'image/png',
    'PNG': 'image/png',
    'pdf': 'application/pdf',
    'PDF': 'application/pdf',
}


class BaseChoices:
    @staticmethod
    def get_choice_value(choices, choice_str):
        for choice in choices:
            if choice[1] == choice_str:
                return choice[0]

    @staticmethod
    def get_choice_str(choices, choice):
        return choices[choice][1]
