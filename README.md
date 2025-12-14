# University-Planner-App
This is a university management system built with Python and MySQL.

## Features
### Student Portal
- **Authentication**: Login/Register with secure credentials
- **Dashboard**: 
  - Today's classes with real-time status
  - Upcoming assignments (next 7 days)
  - Attendance warnings (<75%)
- **Subject Management**: Add, view, delete subjects with professor info
- **Attendance Tracking**:
  - Mark daily attendance
  - Automatic alerts when below 75%
  - Calculate classes needed to reach 75%
- **Assignment Management**:
  - Add/delete assignments with deadlines
  - Color-coded urgency indicators
  - Mark as complete
- **Timetable**: View weekly class schedule

## 🛠️Stack
- **Language**: Python 3.13.9
- **Database**: MySQL
- **Style**: Functional programming 
- **Libraries**: 
  - `mysql-connector-python` - Database connectivity
  - `tabulate` - Table formatting
  - `shutil` - Terminal width detection
  - `datetime`-Get current date and time from the system
