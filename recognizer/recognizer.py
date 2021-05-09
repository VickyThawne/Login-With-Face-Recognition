import cv2
import face_recognition
import os
import numpy as np

from django.conf import settings

def recognizer(details):

    known_face_encodings = []   # User uploaded image's encodings
    known_face_locations = []   # User uploaded image's locations
    known_face_lables = []      # User uploaded image's lables
    
    video_face_encodings = []   # video capture ma je malya e face nu encoding
    video_face_locations = []   # video capture ma je malya e face nu encoding
    
    je_video_ma_malya_enu_naam = []
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
	
    base_dir = os.getcwd() # ek pachal
    image_dir = os.path.join(base_dir,"{}\{}\{}".format('media','User_images',details['gender']))
    

    for root, dirs, files in os.walk(image_dir):
        for f in files:
            if f.endswith('jpg') or f.endswith('png'):
                path = os.path.join(root, f)  # file no path 
                img = face_recognition.load_image_file(path)
                
                known_lable = f[:len(f)-4]
                known_face_lables.append(known_lable)  # janita face na lable taiyar
                
                known_encoding = face_recognition.face_encodings(img)
                known_face_encodings.append(known_encoding)  # janita face na encodings taiyar
                
    
    # video par kaam chalu
    
    cap = cv2.VideoCapture(0)   #start the video camera
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    while True:
        
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        if ret:
            try:
                video_face_location = face_recognition.face_locations(frame)
                video_face_encoding = face_recognition.face_encodings(frame,
                                            video_face_location
                                        )
                
                
                for face_enc in video_face_encoding:
                    
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
                    
                # jo video ma thobdu malyu pan verified nathi to
                if len(je_video_ma_malya_enu_naam) == 0:
                    for (top, right, bottom, left) in video_face_locations:
                        cv2.rectangle(frame, (left,top),(right,bottom), (0,0,255), 2)

                        # cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame, 'Unknown', (left, top), font, 0.8, (255,255,255),1)
                        
                #jo video ma thobdu malyu ane verified 6e
                else:
                    for (top, right, bottom, left), name in video_face_locations, je_video_ma_malya_enu_naam:
                        cv2.rectangle(frame, (left,top),(right,bottom), (0,0,255), 2)

                        # cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame, name , (left, top), font, 0.8, (255,255,255),1)
                   
            except:
                pass
            
            # chalo have video batai do....
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imshow("Face Recognition Panel", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    # stop everything and destroy windows
    
    cap.release()
    cv2.destroyAllWindows()
    
    return je_video_ma_malya_enu_naam, known_face_lables
    
# ---------------------------------------------------------------------- #
                              