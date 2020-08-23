import os
import environment
import pymongo
import BellRingMatch as m
import config

def update_database():
    """
    Choose the collection that wants to be updated. Establish database cooonection.
    :return:
    """
    # Establish connection to databse
    client = pymongo.MongoClient(environment.MONGO_URL)
    db = client.RingBellDB

    # Obtain which database want to update
    collection = input("Please type in which database you want to update:\n "
                       "'INTERNAL_TESTING', 'MATCHING_ALGORITHM_TESTING', 'EXAMPLE' or 'RELEASE'?")

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    if collection == "INTERNAL_TESTING":
        listener_collection = db['internal_testing_listener_collection']
        bellringer_collection = db['internal_testing_bellringer_collection']

        rel_path_bellringer_Form = "internal_testing_data/newForm.xls"
        rel_path_listeners = "internal_testing_data/Listeners.xls"

    elif collection == "MATCHING_ALGORITHM_TESTING":
        listener_collection = db['algorithm_testing_listener_collection']
        bellringer_collection = db['algorithm_testing_bellringer_collection']

        rel_path_bellringer_Form = "matching_algorithm_testing_data/newForm.xls"
        rel_path_listeners = "matching_algorithm_testing_data/Listeners.xls"

    elif collection == "EXAMPLE":
        listener_collection = db['example_listener_collection']
        bellringer_collection = db['example_bellringer_collection']

        rel_path_bellringer_Form = "example/newForm.xls"
        rel_path_listeners = "example/Listeners.xls"

    elif collection == "RELEASE":
        print("**********************************************")
        print("*******ADDING TO RELEASE COLLECTION!**********")
        listener_collection = db['release_listener_collection']
        bellringer_collection = db['release_bellringer_collection']

        rel_path_bellringer_Form = "Data/newForm.xls"
        rel_path_listeners = "Data/Listeners.xls"

    else:
        raise ValueError("Wrong Collection Name entered:", collection)

    # Updating BellRingers or Listeners?
    collection_input = input("Do you want to update Bell Ringers or Listeners?\n"
                           "Enter (Bell Ringers / Listeners):")

    if collection_input == "Bell Ringers":
        bellRingers = m.get_new_bellringer(rel_path_bellringer_Form, bellringer_collection)
        confirm = input("Are you sure you want to add the above bell ringers to {} ?".format(collection_input))
        if confirm == "YES":
            m.add_bellringers_to_database(bellRingers, bellringer_collection)
            print("Action Success!")
        else:
            print("Abort")

    elif collection_input == "Listeners":
        listeners = m.read_xls(rel_path_listeners, is_listener=True)
        for l in listeners:
            l.print_person()
        confirm = input("Are you sure you want to add the above listeners to {} ?".format(collection_input))
        if confirm == "YES":
            m.add_listeners_to_database(rel_path_listeners, listener_collection)
            print("Action Success!")
        else:
            print("Abort")

    else:
        raise ValueError("Wrong input:", collection_input)

    return


if __name__ == '__main__':
    config.config("")
    update_database()