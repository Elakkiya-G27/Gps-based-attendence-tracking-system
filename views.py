from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User, StaffAttendance, StudentAttendance
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer 
from .models import AttendanceRecord
from rest_framework.views import APIView
from urllib.parse import unquote
from django.utils import timezone
import random
from django.core.mail import send_mail
OTP_EXPIRY_TIME = 300  # OTP valid for 5 minutes

otp_store = {}  

staff_dict = {
    "C6509": "ABIRAMI S K",
    "C6011": "ADLENE ANUSHA J",
    "C6553": "AMSA SREE GAYATHRI D",
    "C6559": "ANISHA C D",
    "C5075": "ANUSHA T",
    "C5816": "ARUL ANAND N",
    "C5933": "ARUL JOTHI S",
    "V50371": "ARUNKUMAR BALAKRISHNAN",
    "C3517": "GOPIKA RANI N",
    "V50370": "ILANGO KRISHNAMURTHI",
    "C1646": "INDUMATHI D",
    "C6010": "JAYASHREE L S",
    "C1154": "KARPAGAM G R",
    "C1708": "KAVITHA C",
    "C1700": "LOVELYN ROSE S",
    "C6562": "NAVINA N",
    "C5782": "PRAKASH J",
    "C6476": "PRIYA G",
    "C3146": "RAMESH A C",
    "C3518": "SANTHI V",
    "C6560": "SARAN KIRTHIC R",
    "C5227": "SARANYA K G",
    "C5042": "SATHIYAPRIYA K",
    "C6439": "SIVARANJANI S",
    "C1510": "SUDHA SADASIVAM G",
    "C6127": "SURIYA S",
    "C5966": "THIRUMAHAL R",
    "C3247": "VIJAYALAKSHMI S"
}



@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Generate token or session here if needed
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def staff(request):
    if request.method == 'POST':
        staff_name = request.data.get('staff_name')
        batch = request.data.get('batch')
        classroom = request.data.get('classroom')
        subject = request.data.get('subject')
        generated_code = request.data.get('generated_code')

        # Create and save the attendance record
        attendance = StaffAttendance(
            staff_name=staff_name,
            batch=batch,
            classroom=classroom,
            subject=subject,
            generated_code=generated_code
        )
        attendance.save()

        return Response({"message": "Attendance data saved successfully"})
@api_view(['POST'])
def store_student_data(request):
    # Extract data from request
    if request.method == 'POST':
        student_name = request.data.get('studentName')
        roll_number = request.data.get('rollNumber')
        batch=request.data.get('batch')
        staff_name = request.data.get('staffName')
        subject_code = request.data.get('subjectCode')
        status = request.data.get('status')
        location = request.data.get('location')
        code = request.data.get('code')
        
        staff = next((key for key, value in staff_dict.items() if value == staff_name), None)
        # Create a new StudentAttendance entry
        attendance = StudentAttendance(
            student_name=student_name,
            roll_number=roll_number,
            batch=batch,
            staff_name=staff,
            subject_code=subject_code,
            status=status,
            location=location,
            code=code
        )
        attendance.save()
        return Response({"message": "Attendance recorded successfully!"})


@api_view(['POST'])
def record_attendance(request):
    # Extracting data from request
    date = request.data.get('date')
    staff_name = request.data.get('staff_name')
    subject = request.data.get('subject')
    batch = request.data.get('batch')

    Location = {"GRDLAB": {"Latitude": 11, "Longitude": 77}}
    LATITUDE_RANGE = (11, 14)
    LONGITUDE_RANGE = (76, 80)
    stud_dict = {
    "22z201": "Abinav P",
    "22z202": "Abinaya B",
    "22z203": "Abinaya Suresh",
    "22z204": "Abirami M",
    "22z206": "Adish Kumar S",
    "22z208": "Aksharaa P",
    "22z209": "Anandkumar N S",
    "22z210": "Anbu Selvan M",
    "22z211": "Aravindhkrishnan P",
    "22z212": "Aravinth Cheran K S",
    "22z213": "Arulmozhi B",
    "22z214": "Bragadeesh V",
    "22z215": "Dhakkshin S R",
    "22z216": "Dheekshitha R",
    "22z217": "Elakkiya G",
    "22z218": "Gayathri K S",
    "22z219": "Geetha P K",
    "22z220": "Gobika R",
    "22z221": "Gokul G",
    "22z222": "Hariharan D",
    "22z223": "Harish K",
    "22z224": "Harshini S P",
    "22z225": "Hemanthkumar V",
    "22z226": "Iniyaa N",
    "22z227": "Jayavarshini S S",
    "22z228": "Jeevashakthi V",
    "22z229": "Kabhinyasri S V",
    "22z231": "Karthik Srinivas S",
    "22z232": "Kishoreadhith V",
    "22z233": "M Raj Ragavender",
    "22z234": "Maddi Srinivasa Padmavathi",
    "22z235": "Madhisha S",
    "22z236": "Manojkumar K",
    "22z237": "Manoranjan A",
    "22z238": "Mithra K M",
    "22z239": "Mohamed Muzammil J",
    "22z240": "Monish Rajan L",
    "22z241": "Moumitha K",
    "22z242": "Naveen Ragav K",
    "22z243": "O Keerthi",
    "22z244": "Pramodini P",
    "22z245": "Pranavji K",
    "22z246": "Prateekshaa T",
    "22z247": "Pratish Mithra J",
    "22z248": "Pream S",
    "22z249": "Prithvin K C",
    "22z250": "Rajailakkiyan I B",
    "22z251": "Ramapriya S",
    "22z252": "Rithaniyaa B",
    "22z253": "Rithvik K",
    "22z254": "Rohith Prakash",
    "22z255": "S Akash",
    "22z256": "S Karthikeyan",
    "22z257": "Sandeep K",
    "22z258": "Sandhiya R",
    "22z259": "Sanjitha R",
    "22z260": "Snesha B",
    "22z261": "Sreeraghavan R",
    "22z262": "Sri Dev S",
    "22z263": "Srihari K K",
    "22z264": "Sruthi S",
    "22z265": "Sudhanbalaji M",
    "22z266": "Thakshin Kumar T",
    "22z267": "Thamina Anzum A",
    "22z268": "Tharigalakshmi S",
    "22z269": "Theetchanaa Ra",
    "22z270": "Varshini R",
    "22z271": "Vigneshwaran P",
    "22z272": "Vijeyasri T",
    "22z273": "Vinithaa P",
    "22z274": "Vishnu Barath K",
    "22z275": "Vivekanand M U",
    "22z276": "Yohith Mukilan N",
    "22z277": "Krishanu Dey",
    "22z278": "Mukesh E",
    "22z279": "Praneeth M",
    "22z280": "Sibi Senthil",
    "22z433": "Santosh T K",
    "23z431": "Dwarkesh",
    "23z432": "Kapil Arif K",
    "23z433": "Naveen P",
    "23z434": "Praveen G",
    "23z435": "Sudharsan S",
    "23z436": "Vasanth Kumar S B",
    "23z438": "Dharshini V"
    }

    
    # List of roll numbers
    rollNoList = ['22z201', '22z202', '22z203', '22z204',  '22z206', '22z208',  '22z209', '22z210', '22z211', '22z212', '22z213', '22z214', '22z215', '22z216',  '22z217', '22z218', '22z219', '22z220', '22z221', '22z222', '22z223', '22z224',  '22z225', '22z226', '22z227', '22z228', '22z229',  '22z231', '22z232',  '22z233', '22z234', '22z235', '22z236', '22z237', '22z238', '22z239', '22z240',  '22z241', '22z242', '22z243', '22z244', '22z245', '22z246', '22z247', '22z248',  '22z249', '22z250', '22z251', '22z252', '22z253', '22z254', '22z255', '22z256',  '22z257', '22z258', '22z259', '22z260', '22z261', '22z262', '22z263', '22z264',  '22z265', '22z266', '22z267', '22z268', '22z269', '22z270', '22z271', '22z272',  '22z273', '22z274', '22z275', '22z276', '22z277', '22z278', '22z279', '22z280',

                  '22z433','23z431','23z432', '23z433', '23z434', '23z435', '23z438']

    # Fetching staff attendance record for validation
    staff_attendances = StaffAttendance.objects.filter(date=date, staff_name=staff_name, subject=subject, batch=batch)
    
    for roll_number in rollNoList:
        student_attendance = StudentAttendance.objects.filter(roll_number=roll_number, date=date, subject_code=subject, batch=batch).first()
        code1 = "Failed"
        result = "Absent"
        loc_val = "Failed"

        # Process if student attendance record exists
        if student_attendance:
            for staff in staff_attendances:
                latitude = student_attendance.location.get('latitude')
                longitude = student_attendance.location.get('longitude')

                # Location validation
                if LATITUDE_RANGE[0] <= latitude <= LATITUDE_RANGE[1] and LONGITUDE_RANGE[0] <= longitude <= LONGITUDE_RANGE[1]:
                    loc_val = "Passed"
                else:
                    loc_val = "Failed"
                
                # Code validation
                if student_attendance.code == staff.generated_code:
                    code1 = "Passed"
                    if student_attendance.status == "Present" and loc_val == "Passed":
                        result = "Present"
                if student_attendance.status == "Absent":
                    result = "Absent"
                if student_attendance.status == "Present" and (student_attendance.code != staff.generated_code or loc_val == "Failed"):
                    result = "Doubt"
                
        # If no student attendance record, defaults will apply (Absent, Failed, etc.)
        AttendanceRecord.objects.create(
            staff_name=staff_name,
            student_name=stud_dict.get(str(roll_number)),
            roll_number=roll_number,
            batch=batch,
            course_code=subject,
            attendance_status=result,
            code_validation=code1,
            location_validation=loc_val,
            date=date
        )

    return Response({"message": "Attendance records updated successfully!"})
@api_view(['POST'])
def view_attendance(request):
    staff_name = request.data.get('staff_name')
    subject_code = request.data.get('subject_code')
    date = request.data.get('date')
    batch=request.data.get('batch')

    # Filter AttendanceRecord matching staff_name, subject_code, and date
    records = AttendanceRecord.objects.filter(staff_name=staff_name, course_code=subject_code, date=date,batch=batch)
    result = [
        {
            'student_name': record.student_name,
            'roll_number': record.roll_number,
            'course_code': record.course_code,
            'attendance_status': record.attendance_status,
            'code_validation': record.code_validation,
            'location_validation':record.location_validation,
            'date': record.date
        }
        for record in records
    ]
    return Response(result)
@api_view(['PUT'])
def update_attendance_status(request, roll_number):
    course_code = request.data.get('course_code')
    date = request.data.get('date')

    try:
        # Match the roll number, course code, and date
        record = AttendanceRecord.objects.get(roll_number=roll_number, course_code=course_code, date=date)
        
        # Update the attendance status if found
        record.attendance_status = request.data.get('attendance_status', record.attendance_status)
        record.save()
        
        return Response({"message": "Attendance status updated successfully."})
    except AttendanceRecord.DoesNotExist:
        return Response({"error": "Record not found."}, status=404)

@api_view(['POST'])
def send_reset_otp(request):
    roll_number = request.data.get('roll_number')
    email = f"{roll_number}@psgtech.ac.in"

    # Check if the user exists
    try:
        user = User.objects.get(username=roll_number)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    # Generate OTP
    otp = random.randint(100000, 999999)
    otp_store[roll_number] = {'otp': otp, 'expiry': timezone.now() + timezone.timedelta(seconds=OTP_EXPIRY_TIME)}

    # Send OTP to email
    send_mail(
        subject="Password Reset OTP",
        message=f"Your OTP for password reset is {otp}. It will expire in 5 minutes.",
        from_email="noreply@example.com",
        recipient_list=[email],
        fail_silently=False,
    )

    return Response({"message": "OTP sent to your email"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def reset_password(request):
    roll_number = request.data.get('roll_number')
    otp = int(request.data.get('otp'))
    new_password = request.data.get('new_password')

    # Validate the OTP
    if roll_number not in otp_store:
        return Response({"error": "OTP has not been requested or expired"}, status=status.HTTP_400_BAD_REQUEST)

    stored_otp_data = otp_store[roll_number]
    if timezone.now() > stored_otp_data['expiry']:
        return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

    if stored_otp_data['otp'] != otp:
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

    # Reset the password
    try:
        user = User.objects.get(username=roll_number)
        user.password = make_password(new_password)
        user.save()

        # Remove OTP after successful password reset
        del otp_store[roll_number]

        return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
