extends Node2D
#https://docs.godotengine.org/en/stable/tutorials/networking/http_request_class.html
#just some basic variables
var url= "http://127.0.0.1:8000/rest/"

#just something to delay some requests
var can_request : bool = true

#connect the event what should happen if the request is completed
func _ready():
	$HTTPRequest.request_completed.connect(_on_request_completed)

#example on_completed_event
func _on_request_completed(result, response_code, headers, body):
	var json = JSON.parse_string(body.get_string_from_utf8())
	print(json)
	can_request=true

#KeyInput press_1=A and press_2=S
func _process(delta):
	if can_request:
		if Input.is_action_just_released("press_1"):			
			can_request=false
			receive_data_from_server()
		if Input.is_action_just_released("press_2"):
			can_request=false
			send_data_to_server()
		
#no data to the server, example: signout
func receive_data_from_server():
	print("receive")
	
	var new_url=url+"signout/"
	var response = $HTTPRequest.request(new_url)
	print(response)


#data to the server, example: signin
func send_data_to_server():
	print("send")
	var new_url=url+"signin/"
	var data_to_send={
		"username":  "USERNAME",
		"password":  "PASSWORD",
		"password1": "PASSWORD_COPY"} # second one is needed for django
	var json = JSON.stringify(data_to_send)
	var headers = ["Content-Type: application/json"]
	var response= $HTTPRequest.request(new_url, headers, HTTPClient.METHOD_POST, json)
	
