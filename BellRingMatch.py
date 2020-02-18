import config
import xlrd
from xlutils.copy import copy
from datetime import datetime
from datetime import date
from datetime import time as dtime
from datetime import timedelta
from pytz import timezone

time_dict = {
    "周一 6:00-7:00pm":1,"周一 7:00-8:00pm":2,"周一 8:00-9:00pm":3,"周一 9:00-10:00pm":4,
    "周二 6:00-7:00pm":5,"周二 7:00-8:00pm":6, "周二 8:00-9:00pm":7,"周二 9:00-10:00pm":8,
    "周三 6:00-7:00pm":9,"周三 7:00-8:00pm":10,"周三 8:00-9:00pm":11,"周三 9:00-10:00pm":12,
    "周四 6:00-7:00pm":13,"周四 7:00-8:00pm":14,"周四 8:00-9:00pm":15,"周四 9:00-10:00pm":16,
    "周五 6:00-7:00pm":17,"周五 7:00-8:00pm":18,"周五 8:00-9:00pm":19,"周五 9:00-10:00pm":20
}

bell_ringer_xls_dict = {
    "application_time":0, "name":1, "email":2, "WID":3, "gender":4, "topic":6, "faculty":7,
    "need":8, "condition":9, "availability":10, "other_info":11
}

listener_xls_dict = {
    "application_time":0, "email":1, "availability":2, "name":3
}

internal_testing_application_time_dict = {
    "auto_tester1": datetime(2020,2,10,15, minute = 0),
    "auto_tester2": datetime(2020,2,10,15, minute = 5),
    "auto_tester3": datetime(2020,2,11,16, minute = 50),
    "auto_tester4": datetime(2020,2,11,17, minute = 50),
    "auto_tester5": datetime(2020,2,11,21, minute = 0),
    "auto_tester6": datetime(2020,2,11,21, minute = 10),
    "auto_tester7": datetime(2020,2,11,21, minute = 20),
    "auto_tester8": datetime(2020,2,11,21, minute = 30),
    "auto_tester9": datetime(2020,2,12,17, minute = 0),
    "auto_tester10":datetime(2020,2,12,17, minute = 20),
    "auto_tester11":datetime(2020,2,12,17, minute = 30),
    "auto_tester12":datetime(2020,2,12,17, minute = 35),
    "auto_tester13":datetime(2020,2,12,17, minute = 40),
    "auto_tester14":datetime(2020,2,12,17, minute = 45),
    "auto_tester15":datetime(2020,2,12,17, minute = 55)
}
# avail_after info starts after this colom in Listener.xls
START_COL_AVAIL_AFTER = 4

class Person:
    def __init__(self, application_time, name, availability, email, 
                WID = "", topic = "", gender = "", need = "", condition = "", other_info = "",
                listener_num = "", avail_after = "", file_dir = ""):
        # mandatory variables
        self.application_time = application_time
        self.name = name
        self.availability = availability
        self.email = email
        # optional varaibles
        self.WID = WID
        self.topic = topic
        self.gender = gender
        self.need = need
        self.condition = condition
        self.other_info = other_info
        self.listener_num = listener_num
        # listener specific variable 
        # The listener will be only available after this date in a time slot
        self.avail_after = avail_after # A dictionary {time value + START_COL_AVAIL_AFTER : available after date}
        self.file_dir = file_dir

    # Find proper listener for a bell_ringer
    # --> If a listener has been selected, it will be moved to the end the the candidate list to lower its chance of being seleted again```
    # --> If we cannot match a bell_ringer with a listener, then return -1
    def find_listener(self, listeners):
        # Check if the bell ringer can be matched on the same date
        # Don't match any pairs within 1 hour of application time 
        offset_num = 0
        start_date = self.application_time.date()
        if self.application_time.time() > dtime(20,0):
            start_date = start_date + timedelta(days=1)
        elif self.application_time.time() > dtime(19,0):
            offset_num = 3
        elif self.application_time.time() > dtime(18,0):
            offset_num = 2
        elif self.application_time.time() > dtime(17,0):
            offset_num = 1
        start_weekday = start_date.isoweekday()
        start_time_slot = 1 + (start_weekday - 1) * 4 + offset_num
        # Reorder availability list so that the first element is the next potential time slot after start_weekend
        reordered_availability = self.availability[:]
        for time_slot in self.availability:
            if time_slot >= start_time_slot:
                break
            reordered_availability.pop(0)
            reordered_availability.append(time_slot)

        # Match a listener with the same availability
        continue_finding_listeners = True # Flag indicates if need to loop through listeners again
        loop_number = 0 # How many times it has looped
        while continue_finding_listeners:
            continue_finding_listeners = False # Dont loop again if no listener's time_slot matches
            for time in reordered_availability:
                for listener in listeners:
                    if time in listener.availability:
                        # Calculate matched date = start_date + date diff
                        matched_weekday = (time - 1) // 4 + 1
                        delta_days = matched_weekday - start_weekday
                        if delta_days < 0:
                            delta_days += 7
                        delta_days += 7 * loop_number
                        matched_date = start_date + timedelta(days = delta_days)

                        # Check is the listener is available ( if listener is already busy on this day)
                        if (time + START_COL_AVAIL_AFTER in listener.avail_after and
                            matched_date <= listener.avail_after[time + START_COL_AVAIL_AFTER] ):
                            continue_finding_listeners = True
                            continue

                        # Update matched listener's avail_after
                        listener.avail_after[time + START_COL_AVAIL_AFTER] = matched_date
                        if not config.DISABLE_FREEZING:
                            rb = xlrd.open_workbook(listener.file_dir)
                            wb = copy(rb)
                            sheet = wb.get_sheet(0)
                            sheet.write(listener.listener_num, time + START_COL_AVAIL_AFTER, matched_date)
                            wb.save(listener.file_dir)

                        return (listener, matched_date, convert_enum_to_availabilty(time))

            loop_number += 1
            # Don't match after 2 weeks from about application time
            # (actually 2 weeks from the first available bell ringer time_slot)
            if loop_number >= 2:
                break
        return -1

    def print_person(self):
        print("name =", self.name,"; Wechat ID =", self.WID, "; Email =", self.email)

#Match all bell ringers with proper listeners
#result is in the format [[bell_ringer, matched_listener, date, time], [bell_ringer, -1, -1, -1], ...]
def match_all(listeners, bell_ringers):
    matching_result_list = [] 
    for b in bell_ringers:
        print("-->Matching Result:")
        matched_result = b.find_listener(listeners)
        #print out result
        if matched_result == -1:
            print("     Bell Ringer:  ", b.name)
            print("     Submitted on: ", b.application_time.strftime("%Y-%m-%d, %H:%M:%S %Z"))
            print("     Cannot find a Listener!")
            matching_result_list.append([b, -1, -1, -1])
        else:
            print("     Bell Ringer:  ", b.name)
            print("     Submitted on: ", b.application_time.strftime("%Y-%m-%d, %H:%M:%S %Z"))
            print("     Listener:     ", matched_result[0].name)
            print("     At Time:      ", matched_result[1], matched_result[2])
            matching_result_list.append([b, matched_result[0], matched_result[1].isoformat(), matched_result[2]])
    return matching_result_list

#------------Conversions------------
#convert availablity string to an enum according to time_dict
def convert_availability(avail):
    new_avail = []
    for time in avail.split(','):
        new_avail.append(time_dict[time])
    return new_avail

#convert value in time_dict back to its value(convert enum availability to string availability)
def convert_enum_to_availabilty(enum_availability):
    for item in time_dict.items():
        if item[1] == enum_availability:
            return item[0]
    return -1

def convert_float_to_datetime(float_time):
    return datetime(*xlrd.xldate_as_tuple(float_time, 0))

def convert_float_to_date(float_time):
    return datetime.date(convert_float_to_datetime(float_time))

#------------End of conversions------------

# Read Listener or bellRinger from a xls file
def read_xls(file_name, is_listener = False, startLine = 1):
    wb = xlrd.open_workbook(file_name)
    sheet = wb.sheet_by_index(0)
    info = []
    for i in range(startLine, sheet.nrows):
        if is_listener:
            # get avail_after_dict
            avail_after_dict = {}
            for offset in range(1,21):  
                index = offset + START_COL_AVAIL_AFTER
                if index >= sheet.ncols:
                    break
                cell = sheet.cell_value(i, index)
                if cell != "":
                    cell = convert_float_to_date(cell)
                    avail_after_dict[index] = cell
            # Construct Person instance
            # Get applicaiton time in toronto
            app_time = convert_float_to_datetime(sheet.cell_value(i, listener_xls_dict["application_time"]))
            application_time_china = timezone('Asia/Shanghai').localize(app_time)
            application_time_toronto = application_time_china.astimezone(timezone('Canada/Eastern'))
            info.append(Person
                (   application_time_toronto,
                    str(sheet.cell_value(i, listener_xls_dict["name"])),
                    convert_availability(sheet.cell_value(i, listener_xls_dict["availability"])), 
                    str(sheet.cell_value(i, listener_xls_dict["email"])),                         
                    # Optional arguments
                    listener_num        = i,
                    avail_after         = avail_after_dict,
                    file_dir            = file_name
                )
            )
        else:
            # Bell Ringer
            # Get applicaiton time in toronto
            app_time = convert_float_to_datetime(sheet.cell_value(i, bell_ringer_xls_dict["application_time"]))
            application_time_china = timezone('Asia/Shanghai').localize(app_time)
            application_time_toronto = application_time_china.astimezone(timezone('Canada/Eastern'))
            # If running in internal testing mode, replace application by testing application time
            if config.INTERNAL_TESTING:
                application_time_toronto = internal_testing_application_time_dict[sheet.cell_value(i, bell_ringer_xls_dict["name"])]
                application_time_toronto = timezone('Canada/Eastern').localize(application_time_toronto)

            # Construct Person instance
            info.append(Person
                (   application_time_toronto,                                                                       #application_time
                    str(sheet.cell_value(i, bell_ringer_xls_dict["name"])),                                         #Name
                    convert_availability(sheet.cell_value(i, bell_ringer_xls_dict["availability"])),                #Availability 
                    str(sheet.cell_value(i, bell_ringer_xls_dict["email"])),                                        #Email
                    # Optional arguments
                    WID           = str(sheet.cell_value(i, bell_ringer_xls_dict["WID"])),                          #WID
                    topic         = str(sheet.cell_value(i, bell_ringer_xls_dict["topic"])),                        #Topic
                    gender        = str(sheet.cell_value(i, bell_ringer_xls_dict["gender"])),                       #gender
                    need          = str(sheet.cell_value(i, bell_ringer_xls_dict["need"])),                         #need
                    condition     = str(sheet.cell_value(i, bell_ringer_xls_dict["condition"])),                    #condition
                    other_info    = str(sheet.cell_value(i, bell_ringer_xls_dict["other_info"])),                   #other_info
                )
            )               
    return info

# Read new bell ringers from xls
def read_new_ringer(newForm_name, oldForm_name):
    print("Read new bell ringers ...")
    newPerson_start_line, have_new_people = newAppliers(newForm_name, oldForm_name)
    info = []
    if have_new_people:
        print("   Found new bell ringers")
        print("   newPerson_start_line =", newPerson_start_line)
        info = read_xls(newForm_name, startLine = newPerson_start_line)
    else:
        print("   Does not find any new bell ringers")
    return info

def read_listener(listener_form):
    return read_xls(listener_form, is_listener = True)

#Only get new ringers info 
#1. Assume new people will always be added to the end of the form
#2. Assume any applicant in the form can be deleted. 
def newAppliers(newForm_name, oldForm_name):
    #get new form
    tmp = xlrd.open_workbook(newForm_name)
    newForm = tmp.sheet_by_index(0)
	#get old form
    tmp = xlrd.open_workbook(oldForm_name)
    oldForm = tmp.sheet_by_index(0)
	
    #new form is empty
    if (newForm.nrows <= 1):
        return 1, False

    #Look for new applicants
    have_new_people = False
    newPerson_start_line = newForm.nrows
    newForm_row_id = newForm.nrows-1
    if (newForm.nrows > oldForm.nrows):
        have_new_people = True
        newForm_row_id = oldForm.nrows-1
        newPerson_start_line = oldForm.nrows
    while (newForm_row_id > 0):
        cur_applicant = newForm.cell_value(newForm_row_id,0)
        is_new_applicant = True
        # Number of people before the same person in newForm cannot be larger than the number
        # in oldForm based on assumption 1
        oldForm_row_id = oldForm.nrows - 1
        while (oldForm_row_id >= newForm_row_id):
            cur_oldApplicant = oldForm.cell_value(oldForm_row_id, 0)
            if (cur_oldApplicant != cur_applicant):
                oldForm_row_id -= 1
            else:
                is_new_applicant = False
                break				    
        if (is_new_applicant):
            have_new_people = True
            newPerson_start_line -= 1
        else:
            break		
        newForm_row_id -= 1

    return newPerson_start_line, have_new_people
    