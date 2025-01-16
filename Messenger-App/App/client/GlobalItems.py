# Used throughout 'GUI.py' & 'Client.py'
logged_in = False
CREDENTIAL_CACHE_FILE_LOCATION = "client\\cache.txt"
IPS_FILE_LOCATION = "Shared\\details"

request_out_buffer = []
request_in_buffer = []

# This buffer differs. 
"""It contains a processed feedback (from the server) for what action to take next in the application side"""
interpreted_server_feedback_buffer = []
window_event_trigger_buffer = []