from ignis import widgets
from datetime import date
import calendar

class Calendar(widgets.Box):
    def __init__(self, **kwargs):

        self.today = date.today()
        self.current_year = self.today.year
        self.current_month = self.today.month
        self.current_day = self.today.day
        self.first_weekday = 0

        self.prev_button = widgets.Button(
            child=widgets.Label(label="◀"),
            on_click=self.prev_month,
            css_classes=["dashboard-widget-prev-month-button"]
        )
        self.next_button = widgets.Button(
            child=widgets.Label(label="▶"),
            on_click=self.next_month,
            css_classes=["dashboard-widget-next-month-button"]
        )
        self.month_label = widgets.Label(label="", css_classes=["dashboard-widget-month-label"])
        self.header = widgets.CenterBox(
            # halign="center",
            start_widget=self.prev_button,
            center_widget=self.month_label,
            end_widget=self.next_button,
            # child=[self.prev_button, self.month_label, self.next_button],
            css_classes=["dashboard-widget-calendar-header"]
        )

        self.weekday_row = widgets.Box(spacing=5, halign="center", css_classes=["dashboard-widget-calendar-weekdays"])
        for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            lbl = widgets.Label(label=d, css_classes=["dashboard-widget-weekday-label"])
            lbl.set_width_request(32)
            lbl.set_height_request(32)
            lbl.set_valign("center")
            lbl.set_halign("center")
            self.weekday_row.append(lbl)

        self.grid = widgets.Box(vertical=True, spacing=4, css_classes=["dashboard-widget-calendar-grid"])

        super().__init__(
            vertical=True,
            css_classes=["dashboard-widget-calendar"],
            child=[
                self.header,
                self.weekday_row,
                self.grid
            ]
        )

        self.update_calendar()

    def update_calendar(self):
        self.month_label.set_text(f"{calendar.month_name[self.current_month]} {self.current_year}")

        self.grid.child = []  # type: ignore

        cal = calendar.Calendar(firstweekday=self.first_weekday)
        month_days = cal.monthdayscalendar(self.current_year, self.current_month)

        while len(month_days) < 6:
            month_days.append([0] * 7)

        for week in month_days:
            week_row = widgets.Box(spacing=5)
            for day in week:
                if day == 0:
                    lbl = widgets.Label(label="", css_classes=["dashboard-widget-day-empty"])
                else:
                    lbl = widgets.Label(label=str(day), css_classes=["dashboard-widget-day-label"])
                    if (
                        day == self.current_day
                        and self.current_month == self.today.month
                        and self.current_year == self.today.year
                    ):
                        lbl.add_css_class("dashboard-widget-current-day")
                week_row.append(lbl)
            self.grid.append(week_row)

    def prev_month(self, *_):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar()

    def next_month(self, *_):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar()
