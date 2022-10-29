# import the necessary packages
from imutils.video import VideoStream
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import face_recognition
from tkinter import messagebox
import numpy as np
import imutils
import pickle
import time
import cv2
import os


def scanFace():
	# load the encoded faces and names
	print('[INFO] loading encodings...')
	with open('C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\ATM\\Liveness_detection\\\\encoded_faces.pickle', 'rb') as file:
		encoded_data = pickle.loads(file.read())

	# load our serialized face detector from disk
	print("[INFO] loading face detector...")
	path="C:\\Users\\newha\\OneDrive\\Desktop\\30-12-21\\Secure_Atm\\ATM\\Liveness_detection\\"
	os.chdir(path)
	protoPath = os.path.sep.join(["face_detector", "deploy.prototxt"])
	modelPath = os.path.sep.join(["face_detector","res10_300x300_ssd_iter_140000.caffemodel"])
	net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
	# load the liveness detector model and label encoder from disk
	print("[INFO] loading liveness detector...")
	model = load_model("liveness.model")
	le = pickle.loads(open("label_encoder", "rb").read())
	# initialize the video stream and allow the camera sensor to warmup
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

	# sequence count
	sequence_count = 0 
	fake_sequence = 0

	while True:
		# grab the frame from the threaded video stream and resize it
		# to have a maximum width of 600 pixels
		frame = vs.read()
		frame = imutils.resize(frame, width=800)
		cv2.putText(frame, "Press 'q' to quit", (20,35), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0,255,0), 2)
		# grab the frame dimensions and convert it to a blob
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,(300, 300), (104.0, 177.0, 123.0))
		# pass the blob through the network and obtain the detections and
		# predictions
		net.setInput(blob)
		detections = net.forward()

		# loop over the detections
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with the
			# prediction
			confidence = detections[0, 0, i, 2]
			# filter out weak detections
			if confidence > 0.5:
				# compute the (x, y)-coordinates of the bounding box for
				# the face and extract the face ROI
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				# ensure the detected bounding box does fall outside the
				# dimensions of the frame
				startX = max(0, startX)
				startY = max(0, startY)
				endX = min(w, endX)
				endY = min(h, endY)
				# extract the face ROI and then preproces it in the exact
				# same manner as our training data
				face = frame[startY:endY, startX:endX]
				face_to_recog = face # for recognition
				face = cv2.resize(face, (32, 32))
				#face recognition
				rgb = cv2.cvtColor(face_to_recog, cv2.COLOR_BGR2RGB)
				encodings = face_recognition.face_encodings(rgb)
				# initialize the default name if it doesn't found a face for detected faces
				name = 'Unknown'
				for encoding in encodings:
					matches = face_recognition.compare_faces(encoded_data['encodings'], encoding,tolerance=0.5)
					if True in matches:
						matchedIdxs = [i for i, b in enumerate(matches) if b]
						counts = {}
						for i in matchedIdxs:
							name = encoded_data['names'][i]
							counts[name] = counts.get(name, 0) + 1
						name = max(counts, key=counts.get)

				face = face.astype("float") / 255.0
				face = img_to_array(face)
				face = np.expand_dims(face, axis=0)
				# pass the face ROI through the trained liveness detector
				# model to determine if the face is "real" or "fake"
				preds = model.predict(face)[0]
				j = np.argmax(preds)
				label_name = le.classes_[j]
				# draw the label and bounding box on the frame
				label = "{}: {:.4f}".format(label_name, preds[j])
				
				if name == 'Unknown' or label_name == 'fake':
					sequence_count = 0
					fake_sequence+=1
				else:
					sequence_count += 1
					fake_sequence = 0
				print(f'[INFO] {name}, {label_name}, seq: {sequence_count}')
				
				if label_name == 'fake':
					cv2.putText(frame, "Don't try to Spoof !", (startX, endY + 25), 
									cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
				else:
					cv2.putText(frame, name, (startX, startY - 35), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,130,255),2 )
					cv2.putText(frame, label, (startX, startY - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
				cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
					# show the output frame and wait for a key press
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		# if the `q` key was pressed, break from the loop
		if sequence_count==10 :
			cv2.destroyAllWindows()
			vs.stop()
			return label_name,name
		elif fake_sequence == 10:
			cv2.destroyAllWindows()
			vs.stop()
			messagebox.showwarning("Alert! Please dont try to spoof!")
			return label_name,name
		if key == ord("q") :
			break
	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()






























# # load the encoded faces and names
# print('[INFO] loading encodings...')
# with open('C:\\Users\\Akash\\Desktop\\Secure_Atm\\ATM\\Liveness_detection\\encoded_faces.pickle', 'rb') as file:
#     encoded_data = pickle.loads(file.read())

# # load our serialized face detector from disk
# print("[INFO] loading face detector...")
# path="C:\\Users\\Akash\\Desktop\\Secure_Atm\\ATM\\Liveness_detection"
# os.chdir(path)
# protoPath = os.path.sep.join(["face_detector", "deploy.prototxt"])
# modelPath = os.path.sep.join(["face_detector","res10_300x300_ssd_iter_140000.caffemodel"])
# net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
# # load the liveness detector model and label encoder from disk
# print("[INFO] loading liveness detector...")
# model = load_model("liveness.model")
# le = pickle.loads(open("label_encoder", "rb").read())
# # initialize the video stream and allow the camera sensor to warmup
# print("[INFO] starting video stream...")
# vs = VideoStream(src=0).start()
# time.sleep(2.0)

# # sequence count
# sequence_count = 0 

# while True:
# 	# grab the frame from the threaded video stream and resize it
# 	# to have a maximum width of 600 pixels
# 	frame = vs.read()
# 	frame = imutils.resize(frame, width=600)
# 	cv2.putText(frame, "Press 'q' to quit", (20,35), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0,255,0), 2)
# 	# grab the frame dimensions and convert it to a blob
# 	(h, w) = frame.shape[:2]
# 	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,(300, 300), (104.0, 177.0, 123.0))
# 	# pass the blob through the network and obtain the detections and
# 	# predictions
# 	net.setInput(blob)
# 	detections = net.forward()

#     # loop over the detections
# 	for i in range(0, detections.shape[2]):
# 		# extract the confidence (i.e., probability) associated with the
# 		# prediction
# 		confidence = detections[0, 0, i, 2]
# 		# filter out weak detections
# 		if confidence > 0.5:
# 			# compute the (x, y)-coordinates of the bounding box for
# 			# the face and extract the face ROI
# 			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
# 			(startX, startY, endX, endY) = box.astype("int")
# 			# ensure the detected bounding box does fall outside the
# 			# dimensions of the frame
# 			startX = max(0, startX)
# 			startY = max(0, startY)
# 			endX = min(w, endX)
# 			endY = min(h, endY)
# 			# extract the face ROI and then preproces it in the exact
# 			# same manner as our training data
# 			face = frame[startY:endY, startX:endX]
# 			face_to_recog = face # for recognition
# 			face = cv2.resize(face, (32, 32))
# 			#face recognition
# 			rgb = cv2.cvtColor(face_to_recog, cv2.COLOR_BGR2RGB)
# 			encodings = face_recognition.face_encodings(rgb)
# 			# initialize the default name if it doesn't found a face for detected faces
# 			name = 'Unknown'
# 			for encoding in encodings:
# 				matches = face_recognition.compare_faces(encoded_data['encodings'], encoding,tolerance=0.5)
# 				if True in matches:
# 					matchedIdxs = [i for i, b in enumerate(matches) if b]
# 					counts = {}
# 					for i in matchedIdxs:
# 						name = encoded_data['names'][i]
# 						counts[name] = counts.get(name, 0) + 1
# 					name = max(counts, key=counts.get)

# 			face = face.astype("float") / 255.0
# 			face = img_to_array(face)
# 			face = np.expand_dims(face, axis=0)
# 			# pass the face ROI through the trained liveness detector
# 			# model to determine if the face is "real" or "fake"
# 			preds = model.predict(face)[0]
# 			j = np.argmax(preds)
# 			label_name = le.classes_[j]
# 			# draw the label and bounding box on the frame
# 			label = "{}: {:.4f}".format(label_name, preds[j])
			
# 			if name == 'Unknown' or label_name == 'fake':
# 				sequence_count = 0
# 			else:
# 				sequence_count += 1
# 			print(f'[INFO] {name}, {label_name}, seq: {sequence_count}')
			
# 			if label_name == 'fake':
# 				cv2.putText(frame, "Don't try to Spoof !", (startX, endY + 25), 
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
# 			else:
# 				cv2.putText(frame, name, (startX, startY - 35), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,130,255),2 )
# 				cv2.putText(frame, label, (startX, startY - 10),
# 				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
# 			cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
# 	        	# show the output frame and wait for a key press
# 	cv2.imshow("Frame", frame)
# 	key = cv2.waitKey(1) & 0xFF
# 	# if the `q` key was pressed, break from the loop
# 	if sequence_count==10:
# 		return name
# 	if key == ord("q") :
# 		break
# # do a bit of cleanup
# cv2.destroyAllWindows()
# vs.stop()
