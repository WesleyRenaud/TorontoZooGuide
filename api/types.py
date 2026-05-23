from __future__ import annotations

import sqlite3
from datetime import date, datetime
from typing import TypeAlias

Connection: TypeAlias = sqlite3.Connection
Cursor: TypeAlias = sqlite3.Cursor
Row: TypeAlias = sqlite3.Row
DateInput: TypeAlias = str | date | datetime | None
DateKey: TypeAlias = str
MonthInput: TypeAlias = str | int
VisitMonth: TypeAlias = int
VisitDay: TypeAlias = int
VisitYear: TypeAlias = int
Coordinate: TypeAlias = float
ScheduleTimeKey: TypeAlias = str | None
SeasonalMultiplier: TypeAlias = float | None
