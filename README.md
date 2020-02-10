# RingBell
A program that automatically books appointments for the applicant who has registered a mental health conselling service. The program uses selenium to extract registration forms and is deployed on an Amazon EC2 Windows instance.

*This program is designed for online mental health conselling service with EmpoerChange Club of University of Toronto.*

#### Bell Ringer (applicant)
A `bell ringer` is a person who has signed up for a mental health counselling service with *EmpoerChange Club* of *University of Toronto*. The person has to submit a registration form online in order to be considered as an applicant.

#### Listener (counselor)
A `listener` is a stuff or volunteer of the *EmpoerChange Club* who is eligible to provide the mental health counselling service.

#### Matching Process
Scheduled to run every 10 min:
  1. Login to https://www.askform.cn/ and extract `bell ringer` registration forms.
  2. Match any new `bell ringer` with an appropriate `listener` (based on service type and available time).
  3. Send Email to both matched `bell ringer` and `listener` about the appointment result, including basic information of each other, date and time of the appointment.
  
## Running the program
### Prerequites
- Interpreter: Python3
- Module: datetime, selenium, xlrd, xlutils
### Run:
```
python main.py [arguments]
```
#### Accepted arguments
`--release_mode`
`--internal_testing_mode`
`--disable_email_sending`
`--disable_freezing`
`--test_examples`

## Matching Algorithm

  
## Testing
#### Example teseting
#### Git Action
  
 
## Todo list:
- [ ] Implement auto testing feature
- [ ] Hide some info
- [ ] Use mogodb for data
- [ ] Fix config function for command line option (extend it/make it more intuitive)
- [ ] Implement error handling of wrong email input
