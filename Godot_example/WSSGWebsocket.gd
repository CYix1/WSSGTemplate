extends Node
# https://docs.godotengine.org/de/4.x/classes/class_websocketpeer.html
# The URL we will connect to
@export var websocket_url = "ws://127.0.0.1:8000/ws/basic/"

# Our WebSocketClient instance
var socket = WebSocketPeer.new()

func log_message(message):
	var time = "[color=#aaaaaa] %s [/color]" % Time.get_time_string_from_system()
	%TextClient.text += time + message + "\n"


func _ready():
	socket.connect_to_url(websocket_url)


func _process(_delta):

	socket.poll()
	var state = socket.get_ready_state()
	if state == WebSocketPeer.STATE_OPEN:
		while socket.get_available_packet_count():
			print("Packet: ", socket.get_packet().get_string_from_ascii())
	elif state == WebSocketPeer.STATE_CLOSING:
		# Keep polling to achieve proper close.
		pass
	elif state == WebSocketPeer.STATE_CLOSED:
		var code = socket.get_close_code()
		var reason = socket.get_close_reason()
		print("WebSocket closed with code: %d, reason %s. Clean: %s" % [code, reason, code != -1])
		set_process(false) # Stop processing.
	if Input.is_action_just_released("press_1"):
		send_chat_message()


func _exit_tree():
	socket.close()

func send_chat_message():
	socket.send_text("Ping")
