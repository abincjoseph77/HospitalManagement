from django.shortcuts import render,redirect,HttpResponse
from dasapp.models import DoctorReg,Specialization,CustomUser,Appointment,Page
import random
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail

def USERBASE(request):
    
    return render(request, 'userbase.html')

def Index(request):
    doctorview = DoctorReg.objects.all()
    page = Page.objects.all()

    context = {'doctorview': doctorview,
    'page':page,
    }
    return render(request, 'index.html',context)



def newappoinment(request):
    doctorview = DoctorReg.objects.all()
    page = Page.objects.all()

    context = {'doctorview': doctorview,
    'page':page,
    }
    return render(request, 'patient/newappoinment.html',context)


def create_appointment(request):
    doctorview = DoctorReg.objects.all()
    page = Page.objects.all()

    if request.method == "POST":
        appointmentnumber = random.randint(100000000, 999999999)
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        mobilenumber = request.POST.get('mobilenumber')
        date_of_appointment = request.POST.get('date_of_appointment')
        time_of_appointment = request.POST.get('time_of_appointment')
        doctor_id = request.POST.get('doctor_id')
        additional_msg = request.POST.get('additional_msg')

        # Retrieve the DoctorReg instance using the doctor_id
        doc_instance = DoctorReg.objects.get(id=doctor_id)

        # Validate that date_of_appointment is greater than today's date
        try:
            appointment_date = datetime.strptime(date_of_appointment, '%Y-%m-%d').date()
            today_date = datetime.now().date()

            if appointment_date <= today_date:
                # If the appointment date is not in the future, display an error message
                messages.error(request, "Please select a date in the future for your appointment")
                return redirect('appointment')  # Redirect back to the appointment page
        except ValueError:
            # Handle invalid date format error
            messages.error(request, "Invalid date format")
            return redirect('appointment')  # Redirect back to the appointment page

        # Create a new Appointment instance with the provided data
        appointmentdetails = Appointment.objects.create(
            appointmentnumber=appointmentnumber,
            fullname=fullname,
            email=email,
            mobilenumber=mobilenumber,
            date_of_appointment=date_of_appointment,
            time_of_appointment=time_of_appointment,
            doctor_id=doc_instance,
            additional_msg=additional_msg
        )
 # EMAIL SENDING CODE - START
        doctor_name = f"Dr. {doc_instance.admin.first_name} {doc_instance.admin.last_name}"
        
        email_message = f"""
Dear {fullname},

YOUR APPOINTMENT IS CONFIRMED!

Appointment Number: {appointmentnumber}
Doctor: {doctor_name}
Specialization: {doc_instance.specialization_id.sname}
Date: {date_of_appointment}
Time: {time_of_appointment}

IMPORTANT REMINDERS:
- Please arrive 15 minutes before your appointment time
- Bring all relevant medical documents and reports
- Bring your ID proof
- Bring previous prescriptions (if any)
- Please come on time

If you need to reschedule or cancel, please contact us at {mobilenumber}

Thank you!
Hospital Management Team
"""
        
        try:
            send_mail(
                f'Appointment Reminder - {date_of_appointment} at {time_of_appointment}',
                email_message,
                'abincjoseph77@gmail.com',
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email sending failed: {e}")
        # EMAIL SENDING CODE - END
        # Display a success message
        messages.success(request, "Your Appointment Request Has Been Sent. We Will Contact You Soon")

        return redirect('appointment')

    context = {'doctorview': doctorview,
    'page':page}
    return render(request, 'patient/newappoinment.html', context)


def User_Search_Appointments(request):
    page = Page.objects.all()
    
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(fullname__icontains=query) | Appointment.objects.filter(appointmentnumber__icontains=query)
            messages.info(request, "Search against " + query)
            context = {'patient': patient, 'query': query, 'page': page}
            return render(request, 'search-appointment.html', context)
        else:
            print("No Record Found")
            context = {'page': page}
            return render(request, 'search-appointment.html', context)
    
    # If the request method is not GET
    context = {'page': page}
    return render(request, 'search-appointment.html', context)
def View_Appointment_Details(request,id):
    page = Page.objects.all()
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails,
    'page': page

    }

    return render(request,'user_appointment-details.html',context)



