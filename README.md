![Sanity Check](https://github.com/wbh123456/RingBell/workflows/Sanity%20Check/badge.svg)
# RingBell
The back-end system for mental health counselling service appointment booking with EmpowerChange Club. The program intelligently looks for the most appropriate counselor for every applicant, then sends email to confirm the appointment. 

- *The system is deployed on Github CI/CD pipeline, and is sceduled to run every 10 minutes.*
- *The system currently uses MongoDB as the database.*
- *The system is designed for online mental health conselling service with EmpowerChange Club of University of Toronto only.*

### Bell Ringer (applicant)
A `bell ringer` is a person who has registered for mental health counselling service with *EmpowerChange Club*.

### Listener (counselor)
A `listener` is a staff or a volunteer of the *EmpowerChange Club* who is eligible to provide mental health counselling service.

### Matching Process
Scheduled to run every 10 min:
  1. Extract `bell ringer` registration forms from https://www.askform.cn/.
  2. Match new `bell ringer` with appropriate `listener` (based on service type and available time).
  3. Update database.
  3. Send Emails to both `bell ringer` and `listener`.
  
## Running the program
### Prerequites
- Interpreter: Python3.7
- datetime, selenium, xlrd, xlutils, pymongo
### How to run the system:
```
python main.py [--options]
```
#### Some options
`--matching_algorithm_testing_mode`
`--internal_testing_mode`
`--disable_email_sending`
`--disable_freezing`  
For a complete set of options, please check config.py
