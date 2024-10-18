from datetime import datetime

class TimeConsult:
    def __init__(self) -> None:
        self.competence = f'{datetime.now().month:02}.{datetime.now().year}' if not datetime.now().month.__eq__(1) else f'12.{datetime.now().year - 1}'
        self.actual_year = f'{datetime.now().year}'
        self.actual_month = f'{datetime.now().month:02}'
