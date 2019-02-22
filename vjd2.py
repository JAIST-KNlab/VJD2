import tobii_research as tr
import cv2, time, datetime, math

#frame default size
frame_w = 1920 / 1.5
frame_h = 1080 / 1.5

#count
staycount = 0
last_side = "s"
ksize = 0
	
#get EyeTrackerObject
found_eyetrackers = tr.find_all_eyetrackers()
print(found_eyetrackers)

my_eyetracker = found_eyetrackers[0]

print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)

#prepare image and blur
img = cv2.imread("A2.jpg")
img3 = cv2.imread("A3.jpg")


cv2.imshow('motif',img)
#wait for key enter
print("Ready: push any key,then start")
cv2.waitKey()

#draw circle on gaze point
def disp_gaze_circle(gaze_data):
	both_gaze_point_on_display_area = [(gaze_data['left_gaze_point_on_display_area'][0] + gaze_data['right_gaze_point_on_display_area'][0]) / 2, (gaze_data['left_gaze_point_on_display_area'][1] + gaze_data['right_gaze_point_on_display_area'][1]) / 2]    
	img = np.full((frame_w, frame_h, 3), 128, dtype=np.uint8)
    cv2.circle(img, (both_gaze_point_on_display_area[0] * frame_w, both_gaze_point_on_display_area[1] * frame_h) , 20, (0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
    cv2.imshow("image",img)
    cv2.waitKey(3)

def generate_motif(_ks):
	img = cv2.imread("A2.jpg")
	if _ks % 2 == 0:#フレームサイズを奇数固定(ルール)
		_ks = _ks- 1
	if _ks < 0 :#顔が遠すぎればぼかさない元画像を表示
		_ks = 1
		
	cv2.imshow('new',cv2.GaussianBlur(img,(_ks,_ks),0))
	cv2.waitKey(3)

#define call bacll for monitoring gaze
def gaze_data_callback(gaze_data):
	global last_side
	global staycount
	global ksize

	# Print gaze points of left and right eye
	print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
	gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
	gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))

	both_gaze_point_on_display_area = [(gaze_data['left_gaze_point_on_display_area'][0] + gaze_data['right_gaze_point_on_display_area'][0]) / 2, (gaze_data['left_gaze_point_on_display_area'][1] + gaze_data['right_gaze_point_on_display_area'][1]) / 2]    
	if(not math.isnan(both_gaze_point_on_display_area[0])):
		if both_gaze_point_on_display_area[0] > 0.5:
			current_side = "r"
		else:
			current_side = "l"
		print(current_side)
	if current_side == last_side:
		staycount += 1
		print(staycount)
		if staycount >= 10:
			staycount = 0
			if current_side == "r":
				ksize = 50
			else:
				ksize = 0
	else:
		staycount = 0
	last_side = current_side
	generate_motif(ksize)
	

#start motif showing
print("Start: " + str(datetime.datetime.now()))

#acquired gaze data from eye tracker
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, disp_gaze_circle, as_dictionary=True)

time.sleep(15)

my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)


