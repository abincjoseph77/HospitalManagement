from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from dasapp.models import Specialization,DoctorReg,Appointment,Page
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

@login_required(login_url='/')
def ADMINHOME(request):
    doctor_count = DoctorReg.objects.all().count
    specialization_count = Specialization.objects.all().count
    context = {
        'doctor_count':doctor_count,
        'specialization_count':specialization_count,

    } 
    return render(request,'admin/adminhome.html',context)

@login_required(login_url='/')
def SPECIALIZATION(request):
    if request.method == "POST":
        specializationname = request.POST.get('specializationname')
        specialization =Specialization(
            sname=specializationname,
        )
        specialization.save()
        messages.success(request,'Specialization  Added Succeesfully!!!')
        return redirect("add_specilizations")
    return render(request,'admin/specialization.html')

def MANAGESPECIALIZATION(request):
    specialization_list = Specialization.objects.all()  # Fetch all specializations
    
    # Pagination logic
    paginator = Paginator(specialization_list, 5)  # 5 specializations per page
    page_number = request.GET.get('page')  # Get the page number from request
    specializations = paginator.get_page(page_number)  # Get the current page
    
    context = {'specialization': specializations}  # Pass paginated data
    return render(request, 'admin/manage_specialization.html', context)

def DELETE_SPECIALIZATION(request,id):
    specialization = Specialization.objects.get(id=id)
    specialization.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    
    return redirect('manage_specilizations')

login_required(login_url='/')
def UPDATE_SPECIALIZATION(request,id):
    specialization = Specialization.objects.get(id=id)
    
    context = {
         'specialization':specialization,
    }

    return render(request,'admin/update_specialization.html',context)

login_required(login_url='/')

def UPDATE_SPECIALIZATION_DETAILS(request):
        if request.method == 'POST':
          sep_id = request.POST.get('sep_id')
          sname = request.POST.get('sname')
          sepcialization = Specialization.objects.get(id=sep_id) 
          sepcialization.sname = sname
          sepcialization.save()   
          messages.success(request,"Your specialization detail has been updated successfully")
          return redirect('manage_specilizations')
        return render(request, 'admin/update_specialization.html')

@login_required(login_url='/')
def DoctorList(request):
    doctorlist = DoctorReg.objects.all()
    
    # Pagination: 5 doctors per page
    paginator = Paginator(doctorlist, 5)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    context = {'doctorlist': page_obj}  
    print(doctorlist)
    return render(request, 'admin/doctor-list.html', context)


@login_required(login_url='/')
def Doctors_List(request):
    doctorlist = DoctorReg.objects.all()
    
    # Pagination: 5 doctors per page
    paginator = Paginator(doctorlist, 5)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    context = {'doctorlist': page_obj}  
    return render(request, 'patient/doctor-list.html', context)

def ViewDoctorDetails(request,id):
    doctorlist1=DoctorReg.objects.filter(id=id)
    context={'doctorlist1':doctorlist1

    }

    return render(request,'admin/doctor-details.html',context)



@login_required(login_url='/')
def ViewDoctorAppointmentList(request, id):
    patientdetails = Appointment.objects.filter(doctor_id=id)

    # Pagination: Show 5 appointments per page
    paginator = Paginator(patientdetails, 5)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    context = {'patientdetails': page_obj}  
    return render(request, 'admin/doctor_appointment_list.html', context)


def ViewPatientDetails(request,id):
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails

    }

    return render(request,'admin/patient_appointment_details.html',context)



@login_required(login_url='/')
def Search_Doctor(request):
    query = request.GET.get('query', '').strip()  # Get search query

    # Clear old messages before adding new search messages
    storage = messages.get_messages(request)
    storage.used = True  # Mark all previous messages as used (clears them)

    searchdoc = DoctorReg.objects.none()  # Default empty queryset

    if query:
        # Filter doctors based on mobile number, first name, or last name
        searchdoc = DoctorReg.objects.filter(mobilenumber__icontains=query) | \
                    DoctorReg.objects.filter(admin__first_name__icontains=query) | \
                    DoctorReg.objects.filter(admin__last_name__icontains=query)

        if searchdoc.exists():
            messages.info(request, f"Search results for '{query}'")
        else:
            messages.error(request, f"No records found for '{query}'")

    # Pagination (5 results per page)
    paginator = Paginator(searchdoc, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/search-doctor.html', {'searchdoc': page_obj, 'query': query})

@login_required(login_url='/')
def Doctor_Between_Date_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    doctor = []

    if start_date and end_date:
        try:
            # Convert string to datetime and make timezone-aware
            start_dt = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            end_dt = make_aware(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1))  # Include entire day

            # Filter doctors between start and end datetime range
            doctor = DoctorReg.objects.filter(regdate_at__gte=start_dt, regdate_at__lt=end_dt)

        except ValueError:
            return render(request, 'admin/doctor-between-date.html', {
                'doctor': [],
                'error_message': 'Invalid date format',
                'start_date': start_date,
                'end_date': end_date
            })

    return render(request, 'admin/doctor-between-date.html', {
        'doctor': doctor,
        'start_date': start_date,
        'end_date': end_date
    })

@login_required(login_url='/')
def WEBSITE_UPDATE(request):
    page = Page.objects.all()
    context = {"page":page,

    }
    return render(request,'admin/website.html',context)

@login_required(login_url='/')
def UPDATE_WEBSITE_DETAILS(request):
    if request.method == 'POST':
          web_id = request.POST.get('web_id')
          pagetitle = request.POST['pagetitle']
          address = request.POST['address']
          aboutus = request.POST['aboutus']
          email = request.POST['email']
          mobilenumber = request.POST['mobilenumber']
          page =Page.objects.get(id=web_id)
          page.pagetitle = pagetitle
          page.address = address
          page.aboutus = aboutus
          page.email = email
          page.mobilenumber = mobilenumber
          page.save()
          messages.success(request,"Your website detail has been updated successfully")
          return redirect('website_update')
    return render(request,'admin/website.html')

