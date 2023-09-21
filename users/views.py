from django.shortcuts import render, redirect
from users.forms import TeaRegForm, StudRegForm
from users.models import Teacher, Student, MyUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
import cv2
import dlib
import imutils
from imutils import face_utils
from imutils.video import VideoStream
from imutils.face_utils import FaceAligner
import time
import os
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import numpy as np
from sklearn.manifold import TSNE
import datetime
import matplotlib.pyplot as plt
from matplotlib import rcParams


# Create your views here.

# create student dataset function
def create_dataset(username):
    id = username
    if (os.path.exists('media/face_recognition_data/training_dataset/{}/'.format(id)) == False):
        os.makedirs('media/face_recognition_data/training_dataset/{}/'.format(id))
    directory = 'media/face_recognition_data/training_dataset/{}/'.format(id)

    # Detect face
    # Loading the HOG face detector and the shape predictpr for allignment

    print("[INFO] Loading the facial detector")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(
        'media/face_recognition_data/shape_predictor_68_face_landmarks.dat')  # Add path to the shape predictor ######CHANGE TO RELATIVE PATH LATER
    fa = FaceAligner(predictor, desiredFaceWidth=96)
    # capture images from the webcam and process and detect the face
    # Initialize the video stream
    print("[INFO] Initializing Video stream")
    vs = VideoStream(src=0).start()

    # time.sleep(2.0) ####CHECK######

    # Our identifier
    # We will put the id here and we will store the id with a face, so that later we can identify whose face it is

    # Our dataset naming counter
    sampleNum = 0
    # Capturing the faces one by one and detect the faces and showing it on the window
    while (True):
        # Capturing the image
        # vs.read each frame
        frame = vs.read()
        # Resize each image
        frame = imutils.resize(frame, width=800)
        # the returned img is a colored image but for the classifier to work we need a greyscale image
        # to convert
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # To store the faces
        # This will detect all the images in the current frame, and it will return the coordinates of the faces
        # Takes in image and some other parameter for accurate result
        faces = detector(gray_frame, 0)
        # In above 'faces' variable there can be multiple faces so we have to get each and every face and draw a rectangle around it.

        for face in faces:
            print("inside for loop")
            (x, y, w, h) = face_utils.rect_to_bb(face)

            print(face)

            face_aligned = fa.align(frame, gray_frame, face)

            # Whenever the program captures the face, we will write that is a folder
            # Before capturing the face, we need to tell the script whose face it is
            # For that we will need an identifier, here we call it id
            # So now we captured a face, we need to write it in a file
            sampleNum = sampleNum + 1
            # Saving the image dataset, but only the face part, cropping the rest

            if face is None:
                print("face is none")
                continue

            cv2.imwrite(directory + '/' + str(sampleNum) + '.jpg', face_aligned)
            # student = Student.objects.filter(name = username)[0]
            # student.stud_image = directory + '/' + str(sampleNum) + '.jpg'
            # student.save()

            face_aligned = imutils.resize(face_aligned, width=400)
            # cv2.imshow("Image Captured",face_aligned)
            # @params the initial point of the rectangle will be x,y and
            # @params end point will be x+width and y+height
            # @params along with color of the rectangle
            # @params thickness of the rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            # Before continuing to the next loop, I want to give it a little pause
            # waitKey of 100 millisecond
            cv2.waitKey(50)

        # Showing the image in another window
        # Creates a window with window name "Face" and with the image img
        cv2.imshow("Add Images", frame)
        # Before closing it we need to give a wait command, otherwise the open cv wont work
        # @params with the millisecond of delay 1
        cv2.waitKey(1)
        # To get out of the loop
        if (sampleNum > 60):
            break

    # Stoping the videostream
    vs.stop()
    # destroying all the windows
    cv2.destroyAllWindows()


# after finishing training model, it will show the visualize picture
def vizualize_Data(embedded, targets, ):
    X_embedded = TSNE(n_components=2).fit_transform(embedded)

    for i, t in enumerate(set(targets)):
        idx = targets == t
        plt.scatter(X_embedded[idx, 0], X_embedded[idx, 1], label=t)

    plt.legend(bbox_to_anchor=(1, 1))
    rcParams.update({'figure.autolayout': True})
    plt.tight_layout()
    plt.savefig('training_visualisation.png', bbox_inches='tight')
    plt.close()


# train student's face photos model
def train():
    training_dir = 'media/face_recognition_data/training_dataset'
    count = 0
    for person_name in os.listdir(training_dir):
        curr_directory = os.path.join(training_dir, person_name)
        if not os.path.isdir(curr_directory):
            continue
        for imagefile in image_files_in_folder(curr_directory):
            count += 1

    X = []
    y = []
    i = 0

    for person_name in os.listdir(training_dir):
        print(str(person_name))
        curr_directory = os.path.join(training_dir, person_name)
        if not os.path.isdir(curr_directory):
            continue

        for imagefile in image_files_in_folder(curr_directory):
            print(str(imagefile))
            image = cv2.imread(imagefile)
            try:

                X.append((face_recognition.face_encodings(image)[0]).tolist())
                y.append(person_name)
                # y.append(os.path.splitext(os.path.split(imagefile)[1])[0])
                i += 1
            except:
                print("removed")
                os.remove(imagefile)

    targets = np.array(y)
    encoder = LabelEncoder()
    encoder.fit(y)
    y1 = encoder.transform(y)
    X1 = np.array(X)
    print("shape: " + str(X1.shape))
    np.save('media/face_recognition_data/classes.npy', encoder.classes_)
    svc = SVC(kernel='linear', probability=True)
    svc.fit(X1, y1)
    svc_save_path = "media/face_recognition_data/svc.sav"
    with open(svc_save_path, 'wb') as f:
        pickle.dump(svc, f)

    vizualize_Data(X1, targets)


# teacher register
def teacher_register(request):
    # if method is GET
    if request.method == "GET":
        teac_form = TeaRegForm()
        return render(request, 'teacher_register_page.html', {'teac_form': teac_form})
    # if method is POST
    elif request.method == "POST":
        teac_form = TeaRegForm(request.POST, request.FILES)
        # check if the form fulfills rules
        if teac_form.is_valid():
            name = request.POST.get("name", '')
            check_teacher_exist = Teacher.objects.filter(user__username=name)
            teac_email = request.POST.get("teac_email", '')
            password = request.POST.get("password", '')
            age = request.POST.get("age", '')
            gender = request.POST.get("gender", '')
            # check if the teacher's name exists
            if len(check_teacher_exist) != 0:
                error_info = 'The teacher name has existed'
                return render(request, 'teacher_register_page.html', {'teac_form': teac_form},
                              {'error_info': error_info})
            else:
                MyUser.objects.create(username=name, password=make_password(password))
                user = MyUser.objects.filter(username=name)[0]
                teac_form.cleaned_data['user'] = user
                teac_form.cleaned_data['teac_email'] = teac_email
                teac_form.cleaned_data['age'] = age
                teac_form.cleaned_data['gender'] = gender
                teac_form.cleaned_data.pop('name')
                teac_form.cleaned_data.pop('password')
                teac_form.cleaned_data.pop("re_password")
                teac_form.cleaned_data['password'] = password
                Teacher.objects.create(**teac_form.cleaned_data)
                return redirect('teacher_register_successful')
        else:
            return render(request, 'teacher_register_page.html', {'teac_form': teac_form})


# student register
def student_register(request):
    # if method is GET
    if request.method == "GET":
        stud_form = StudRegForm()
        return render(request, 'student_register_page.html', {'stud_form': stud_form})
    # if method is POST
    elif request.method == "POST":
        stud_form = StudRegForm(request.POST, request.FILES)
        # check if the form fulfills rules
        if stud_form.is_valid():
            name = request.POST.get("name", '')
            check_student_exist = Student.objects.filter(user__username=name)
            stud_email = request.POST.get("stud_email", '')
            password = request.POST.get("password", '')
            age = request.POST.get("age", '')
            gender = request.POST.get("gender", '')
            stud_image = request.FILES.get("stud_image", '')
            print(name, check_student_exist, stud_email, password, age, gender, stud_image)
            # check if the student's name exists
            if len(check_student_exist) != 0:
                error_info = 'The student name has existed'
                return render(request, 'student_register_page.html', {'stud_form': stud_form},
                              {'error_info': error_info})
            else:
                MyUser.objects.create(username=name, password=make_password(password))
                user = MyUser.objects.filter(username=name)[0]
                stud_form.cleaned_data['user'] = user
                stud_form.cleaned_data['stud_email'] = stud_email
                stud_form.cleaned_data['age'] = age
                stud_form.cleaned_data['gender'] = gender
                stud_form.cleaned_data.pop("re_password")
                stud_form.cleaned_data['stud_image'] = stud_image
                stud_form.cleaned_data.pop('name')
                stud_form.cleaned_data.pop('password')
                Student.objects.create(**stud_form.cleaned_data)
                stud_login = authenticate(username=name, password=password)
                login(request, stud_login)
                return redirect('create_student_dataset')
        else:
            error_info = stud_form.errors
            return render(request, 'student_register_page.html', {'error_info': error_info, 'stud_form': stud_form})


# after student finish registering, he/she will create the dataset
def create_student_dataset(request):
    if request.method == "GET":
        return render(request, "create_student_dataset.html")
    elif request.method == "POST":
        if request.user.is_authenticated:
            create_dataset(request.user.username)
            return redirect('create_student_dataset_successful')
        else:
            error_info = "No student login the system"
            return render(request, "create_student_dataset.html", {"error_info": error_info})


# After student create dataset successful, the function will be run
def create_student_dataset_successful(request):
    return render(request, "create_student_dataset_successful.html")


# After teacher register successful, the function will be run
def register_teacher_successful(request):
    return render(request, "register_teacher_successful.html")


# user logout
def user_logout(request):
    if request.method == "GET":
        return render(request, "user_logout.html")
    elif request.method == "POST":
        logout(request)
        return redirect('user_login')


# user login
def user_login(request):
    if request.user.is_authenticated:
        return redirect('user_logout')
    else:
        if request.method == "GET":
            return render(request, "user_login.html")
        elif request.method == "POST":
            name = request.POST.get("username", '')
            password = request.POST.get("password", '')
            student = Student.objects.filter(user__username=name)
            teacher = Teacher.objects.filter(user__username=name)
            # justify if the user exists
            if len(student) == 0 and len(teacher) == 0:
                failed_info = "The user doesn't exist"
                return render(request, "user_login_failed.html", {"failed_info":failed_info})
            else:
                user_login = authenticate(username=name, password=password)
                login(request, user_login)
            return redirect('user_login_successful')


# user login successful
def user_login_successful(request):
    return render(request, 'user_login_successful.html')