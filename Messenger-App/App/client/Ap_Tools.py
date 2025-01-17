import GlobalItems
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client.UDPCalling.Send import begin_send_audio_data
from client.UDPCalling.Receive import begin_recv_audio_data
from Shared.SharedTools import (CMD, format_ic_cmd)


# Decorators
def loop_function(func):
    """ Params will be inputted in list """
    def inner(**kwargs):
        while True:
            if kwargs:
                loop_again = func(list(kwargs.values()))
            else:
                loop_again = func()
            if not loop_again:
                break
            #print("Looping function again" if loop_again else "Breaking function loop" )
    return inner
# END OF Decorators

# File Managements - (Cache)
def save_ip_details(ip, server_ip):
    with open("Shared\\details", "w") as file:
        file.write(f"{ip},{server_ip}")
        file.close()

def save_credentials_cache(username_and_password: list) -> None:
    # stores login for when logging in again
    with open(GlobalItems.CREDENTIAL_CACHE_FILE_LOCATION, "w") as cached_login:
        # NOTE: FINISH USING JSON
        username, password = username_and_password[0], username_and_password[1]
        cached_login.write(f"{username},{password}")
        cached_login.close()
# END OF File Managements - (Cache)

class HandleIncommingCommands:
    """ Handlers for INCOMMING COMMANDS - Informs PYQT6 Window of updates from server """
    @classmethod
    def handle_call_person(cls, args, my_ip) -> None:    
        if args[0] == False:
            print("Person cannot be called right now")
        else:
            # Shall receive OTHER PERSONS IPV4 to dial in
            print(f"CAN CALL - calling IPV4: {args}")
            begin_send_audio_data(args[0])
            
            print(f"MY IP IS: {my_ip}")
            begin_recv_audio_data(my_ip)

    @classmethod
    def handle_get_chats(cls, args) -> None:
        if args[0] != False:
            GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.GETSAVECONTACTCHATS, args))
        else:
            GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.GETSAVECONTACTCHATS, False))

    @classmethod
    def handle_save_contact(cls, args) -> None:
        if args[0] == True:
            print("Server sucessfuly saved contact")
            GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.SAVECONTACT, True))
        else:
            print("Something went wrong when attempting to save contact")
            GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.SAVECONTACT, False))

    @classmethod
    def handle_search_contacts(cls, args) -> None:
        print(f"Received: {args}")
        if args[0]:
            # Found results
            GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.SEARCHCONTACT, args))
        else:
            # Did NOT find results
            GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(CMD.SEARCHCONTACT, False))


    @classmethod
    def update_window_event_trigger(cls, cmd, args=None) -> None:
        """ Used to handle incomming commands which don't do any unique processing """
        if args:
            GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(cmd, args))
        else:
            GlobalItems.window_event_trigger_buffer.append(format_ic_cmd(cmd))


if __name__ == "__main__":
    print(f"{__name__} is not ran directly.")