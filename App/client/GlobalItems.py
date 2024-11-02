# Used throughout 'GUI.py' & 'Client.py'
logged_in = False

send_server_msg_buffer = []
recv_server_msg_buffer = []

# This buffer differs. It contains a processed feedback for what action to take next after looking at what the server has responded with
interpreted_server_feedback_buffer = []