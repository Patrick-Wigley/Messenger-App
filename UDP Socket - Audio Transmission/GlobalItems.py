import queue
# USED FOR SENDING
frames_buffer_in = queue.Queue()

# USED FOR OUTPUTTING
frames_buffer_out = queue.Queue(maxsize=2000)