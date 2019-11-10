import xlrd

time_dict = {
    "周一 6:00-7:00pm":1,"周一 7:00-8:00pm":2,"周一 8:00-9:00pm":3,"周一 9:00-10:00pm":4,
    "周二 6:00-7:00pm":5,"周二 7:00-8:00pm":6, "周二 8:00-9:00pm":7,"周二 9:00-10:00pm":8,
    "周三 6:00-7:00pm":9,"周三 7:00-8:00pm":10,"周三 8:00-9:00pm":11,"周三 9:00-10:00pm":12,
    "周四 6:00-7:00pm":13,"周四 7:00-8:00pm":14,"周四 8:00-9:00pm":15,"周四 9:00-10:00pm":16,
    "周五 6:00-7:00pm":17,"周五 7:00-8:00pm":18,"周五 8:00-9:00pm":19,"周五 9:00-10:00pm":20
}

class Person:
    def __init__(self, application_time, name, WID, availability , email = "", topic = ""):
        self.application_time = application_time
        self.name = name
        self.WID = WID
        self.availability = availability
        self.topic = topic
        self.email = email

    # Find proper listener for a bell_ringer
    # --> If a listener has been selected, it will be moved to the end the the candidate list to lower its chance of being seleted again```
    # --> If we cannot match a bell_ringer with a listener, then return -1
    def find_listener(self, listeners):
        for time in self.availability:
            listener_index = 0
            for listener in listeners:
                if time in listener.availability:
                    listeners.pop(listener_index)
                    listeners.append(listener)
                    return (listener,time)
                listener_index += 1
        return -1

    def print_person(self):
        print("name =", self.name,"; Wechat ID =", self.WID, "; Topic =", self.topic)


def match_all(listeners, bell_ringers):
    matching_result_list = [] #result is in the format [[bell_ringer, matched_listener, time], [], ...]
    for b in bell_ringers:
        print("Matching Result:")
        matched_result = b.find_listener(listeners)
        #print out result
        if matched_result == -1:
            print("     Cannot find a Listener!")
            matching_result_list.append([b, -1, -1])
        else:
            print("     Bell Ringer: ", b.name)
            print("     Listener:    ", matched_result[0].name)
            print("     At Time:     ", matched_result[1])
            matching_result_list.append([b, matched_result[0], matched_result[1]])
    return matching_result_list

def convert_availability(avail):
    new_avail = []
    for time in avail.split(','):
        new_avail.append(time_dict[time])
    return new_avail

#read Listener or bellRinger from a xls file
def read_xls(file_name):
    wb = xlrd.open_workbook(file_name)
    sheet = wb.sheet_by_index(0)
    info = []
    for i in range(1, sheet.nrows): 
        info.append(Person
            (   sheet.cell_value(i, 0),                         #application_time
                sheet.cell_value(i, 1),                         #Name
                sheet.cell_value(i, 2),                         #WID
                convert_availability(sheet.cell_value(i, 5)),   #Availability 
                sheet.cell_value(i, 3),                         #Email
                sheet.cell_value(i, 4)                          #Topic
            )
        );
                            
    return info
    