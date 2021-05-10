import cv2
import face_recognition
import os
import numpy as np

from django.conf import settings

def recognizer(details, username, unique_id):

    known_face_encodings = []   # User uploaded image's encodings
    known_face_locations = []   # User uploaded image's locations
    known_face_lables = []      # User uploaded image's lables
    
    video_face_encodings = []   # video capture ma je malya e face nu encoding
    video_face_locations = []   # video capture ma je malya e face nu encoding
    
    je_video_ma_malya_enu_naam = []
    
    best_match_index = None
    
    proceed_login = False
    
    # ----------------------------------------------------------------------- #
    
    base_dir = os.path.dirname(os.path.abspath('__file__'))
	
    base_dir = os.getcwd() # ek pachal

    image_dir = os.path.join(base_dir,"{}\{}\{}".format('media','User_images',details['gender']))
    
        

    for root, dirs, files in os.walk(image_dir):
        for f in files:
            if f.endswith('jpg') or f.endswith('png'):
                path = os.path.join(root, f)  # file no path 
                img = face_recognition.load_image_file(path)
                
                known_lable = f[:len(f)-4]
                known_face_lables.append(known_lable)  # janita face na lable taiyar
                
                known_location = face_recognition.face_locations(img, model='hog')
                known_face_locations.append(known_location)
                
                known_encoding = face_recognition.face_encodings(img, known_location)
                if not len(known_encoding):
                    print(known_lable, "can't be encoded")
                    continue
                else:
                    known_face_encodings.append(known_encoding)  # janita face na encodings taiyar
    
    # ----------------------------------------------------------------------- #
                
    print('known_face_encodings')
    print(known_face_encodings)
    # video par kaam chalu
    try:
        cap = cv2.VideoCapture(0)   #start the video camera
    except:
        cap = cv2.VideoCapture(1)
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    while True:
        
        ret, frame = cap.read()
        small_frame = cv2.resize(frame, (0,0), fx=0.5, fy= 0.5)
        rgb_small_frame = small_frame[:,:,::-1]
        
        if ret:
            
            video_face_location = face_recognition.face_locations(rgb_small_frame, model='hog')
            video_face_encoding = face_recognition.face_encodings(rgb_small_frame,
                                        video_face_location
                                    )
            if not len(video_face_encoding):
                print("video_face_encoding can't be encoded")
                continue
            else:
                video_face_encoding = video_face_encoding[0]
            
            
            for face_enc in video_face_encoding:
                
                try:
                    matches = face_recognition.compare_faces(
                        known_face_encodings,
                        np.array(face_enc),
                        tolerance = 0.6
                    )
                    face_distance = face_recognition.face_distances(known_face_encodings, face_enc)
                    
                    best_match_index = np.argmin(face_distance)
                    
                    if matches[best_match_index]:
                        name = known_face_lables[best_match_index]
                        je_video_ma_malya_enu_naam.append()
                
                except:
                    print('compairing went wrong..')
                
            # jo video ma thobdu malyu pan verified nathi to
            if len(je_video_ma_malya_enu_naam) == 0:
                for (top, right, bottom, left) in video_face_locations:
                    
                    top*=2
                    right*=2
                    bottom*=2
                    left*=2
                    
                    cv2.rectangle(frame, (left,top),(right,bottom), (0,0,255), 2)

                    # cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, 'Unknown', (left, top), font, 0.8, (255,255,255),1)
                    
            #jo video ma thobdu malyu ane verified 6e
            else if (user.username+unique_id) in name:
                for (top, right, bottom, left), name in video_face_locations, je_video_ma_malya_enu_naam:
                    
                    top*=2
                    right*=2
                    bottom*=2
                    left*=2
                    cv2.rectangle(frame, (left,top),(right,bottom), (0,0,255), 2)

                    # cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name , (left, top), font, 0.8, (255,255,255),1)
                    
                    proceed_login = True
                    
            else:
                for (top, right, bottom, left) in video_face_locations:
                    
                    top*=2
                    right*=2
                    bottom*=2
                    left*=2
                    
                    cv2.rectangle(frame, (left,top),(right,bottom), (0,0,255), 2)

                    # cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, 'Login Failed', (left, top), font, 0.8, (255,255,255),1)
                   
    # ----------------------------------------------------------------------- #
     
            # chalo have video batai do....
            cv2.imshow("Face Recognition Panel", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    # stop everything and destroy all windows
    cap.release()
    cv2.destroyAllWindows()
    
    return je_video_ma_malya_enu_naam, known_face_lables, proceed_login
    
# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #

def Recognizer(details):
	video = cv2.VideoCapture(0)

	known_face_encodings = []
	known_face_names = []

	# base_dir = os.path.dirname(os.path.abspath(__file__))
	# image_dir = os.path.join(base_dir, "static")
	# image_dir = os.path.join(image_dir, "profile_pics")

	# base_dir = os.getcwd()
	base_dir = os.path.dirname(os.path.abspath(__file__))
	# os.chdir("..")
	base_dir = os.getcwd()
	image_dir = os.path.join(base_dir,"{}\{}\{}".format('media','User_images',details['gender']))
	# print(image_dir)
	names = []


	for root,dirs,files in os.walk(image_dir):
		for file in files:
			if file.endswith('jpg') or file.endswith('png'):
				path = os.path.join(root, file)
				img = face_recognition.load_image_file(path)
				label = file[:len(file)-4]
				img_encoding = face_recognition.face_encodings(img)[0]
				known_face_names.append(label)
				known_face_encodings.append(img_encoding)

	face_locations = []
	face_encodings = []


	while True:	
	
		check, frame = video.read()
		small_frame = cv2.resize(frame, (0,0), fx=0.5, fy= 0.5)
		rgb_small_frame = small_frame[:,:,::-1]

		face_locations = face_recognition.face_locations(rgb_small_frame)
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
		face_names = []


		for face_encoding in face_encodings:

			matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance = 0.6)

			face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)	
			
			try:
				matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance = 0.6)

				face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
				best_match_index = np.argmin(face_distances)

				if matches[best_match_index]:
					name = known_face_names[best_match_index]
					face_names.append(name)
					if name not in names:
						names.append(name)
			except:
				pass

		if len(face_names) == 0:
			for (top,right,bottom,left) in face_locations:
				top*=2
				right*=2
				bottom*=2
				left*=2

				cv2.rectangle(frame, (left,top),(right,bottom), (0,0,255), 2)

				# cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
				font = cv2.FONT_HERSHEY_DUPLEX
				cv2.putText(frame, 'Unknown', (left, top), font, 0.8, (255,255,255),1)
		else:
			for (top,right,bottom,left), name in zip(face_locations, face_names):
				top*=2
				right*=2
				bottom*=2
				left*=2

				cv2.rectangle(frame, (left,top),(right,bottom), (0,255,0), 2)

				# cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
				font = cv2.FONT_HERSHEY_DUPLEX
				cv2.putText(frame, name, (left, top), font, 0.8, (255,255,255),1)

		cv2.imshow("Face Recognition Panel",frame)

		if cv2.waitKey(1) == ord('s'):
			break

	video.release()
	cv2.destroyAllWindows()
	return names