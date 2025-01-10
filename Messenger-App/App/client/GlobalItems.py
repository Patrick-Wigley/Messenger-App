# Used throughout 'GUI.py' & 'Client.py'
logged_in = False
server_pub_key = ""

send_server_msg_buffer = []
recv_server_msg_buffer = []

# This buffer differs. 
"""It contains a processed feedback (from the server) for what action to take next in the application side"""
interpreted_server_feedback_buffer = []