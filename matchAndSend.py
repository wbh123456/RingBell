import BellRingMatch as m
import gmailAuto as g

#get bell ringers and listeners
bellRingers = m.read_xls('Data/newForm.xls')
listeners = [m.Person(43773.1,"Tiger","1",[2,3]),m.Person(43773.1,"Bob","2",[5,10]),m.Person(43773.1,"Jenny","3",[18,19,20]),m.Person(43773.1,"Helen","4",[16])]
print("bellRingers: ")
for i in bellRingers:
    i.print_person()
print("Listeners:")
for i in listeners:
    i.print_person()

#match
matching_result_list = m.match_all(listeners, bellRingers)

#send gmail
for matching_result in matching_result_list:
    # matching_resilt format :  [bell_ringer, matched_listener, time]
    if matching_result[1] == -1:
        content = "Sorry, we cannot find a listener for you"
    else :
        content = ("We have found you listener!\n   Your listener: " + matching_result[1].name + 
        "\n   Wechat ID: " + matching_result[1].WID + 
        "\n   At time: " + str(matching_result[2]))
        
    receiver = matching_result[0].email

    print("Sending email to " + matching_result[0].name + " at " + receiver + " ... ")
    g.sendGmail(content, receiver)

