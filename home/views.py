from .forms import BasicDetailsForm,CommunicationDetailsForm,EducationDetailsForm,ExperienceDetailsForm,OtherDetailsForm,GeneralDetailsForm
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.utils.dateparse import parse_date
from django.core.mail import EmailMessage
from django.http import HttpResponse
import logging
import os
from home.admin import generate_user_pdfs, send_email_with_pdfs

@never_cache
def index(request):
    if request.user.is_anonymous:
        return render(request,'1 Before Login.html')
    return render(request,'2 After Login.html')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('1 Before Login.html')



def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return render(request,'2 After Login.html')
        else:
            # return render('alerts.html', {'message' :'Invalid Credentials'})
            return redirect('/')
            
    return render(request,'2 After Login.html')


def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']

        # Validate inputs
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('sign_up')

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('sign_up')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('sign_up')

        # Create the user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),  # Hash the password
        )
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect('/')  # Redirect to login page
    
    return render(request,'sign_up.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        sender_email = request.POST.get('email')  # Get the sender's email
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Additional message details
        full_message = f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message}"

        # Send mail with sender's email
        email = EmailMessage(
            subject,
            full_message,
            sender_email,  # Use sender's email as 'from_email'
            ['arendra6268@gmail.com'],  # Replace with your fixed recipient email(s)
            reply_to={'Reply-To': sender_email}  # Add a 'Reply-To' header to the email
        )
        email.send()
        return HttpResponse("Thank you for your message!")
    return render(request, 'contact.html')

@login_required
def logoutUser(request):
    logout(request)
    return render(request,'1 Before Login.html')

def rolling(request):
    return render(request,'3 Rolling.html')

def faculty(request):
    return render(request,'4 faculty.html')

@login_required
def myAccount(request):
    return render(request,'5 account.html')

def page1(request):
    return render(request,'PAGE 1 OF 8.html')

def page2(request):
    return render(request,'PAGE 2 OF 8.html')

def page3(request): 
    return render(request,'PAGE 3 OF 8.html')

def page4(request):     
    return render(request,'PAGE 4 OF 8.html')  
 
def page6(request):     
    return render(request,'PAGE 6 OF 8.html')

def page7(request):
    return render(request,'PAGE 7 OF 8.html')

def page8(request):
    return render(request,'PAGE 8 OF 8.html')


def roll_adv(request):
    return render(request,'roll_adv.html')
def faculty_adv(request):
    return render(request,'faculty_adv.html')







from .models import BasicDetails, CommunicationDetails, EducationDetails, ExperienceDetails, OtherDetails, GeneralDetails


logger = logging.getLogger(__name__)

@login_required
@csrf_protect
def basicDetails(request):
    # try:
    #     instance = basicDetails.objects.get(user=request.user)
    # except basicDetails.DoesNotExist:
    #     instance = None

    if request.method == 'POST':
        form_data = request.POST.dict()
        request.session['faculty_form_page1'] = form_data
        
        # Handle file uploads
        if request.FILES:
            # Store file information in session
            files_data = {}
            for file_key in request.FILES:
                files_data[file_key] = request.FILES[file_key].name
            request.session['faculty_form_page1_files'] = files_data
        
        skype_details = request.POST.get('skype_id')
        profilepic = request.POST.get('files[profilepic]')
        phd_thesis_defended = request.POST.get('defended_your_phd_thesis')
        specialization = request.POST.get('broad_area_of_specialization')
        research_area = request.POST.get('other_specific_research_area')
        position_applied_for = request.POST.get('position_applied_for')
        visiting_faculty = request.POST.get('willing_for_visiting_faculty')
        previous_application = request.POST.get('previously_applied_for_a_faculty_position_in_iit_mandi')
        phd_title = request.POST.get('title_of_phd_thesis')
        phd_defence_date = request.POST.get('date_of_phd_defence')
        candidate_full_name = request.POST.get('candidate_full_name')
        relative_relation = request.POST.get('father_husband')
        relative_name = request.POST.get('full_name')
        dob = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        category = request.POST.get('category')

        category_certificate = request.FILES.get('files[upload_category_certificate]')
        pwd_category = request.POST.get('pwd_category', '')
        pwd_type = request.POST.get('pwd_type', '')
        pwd_certificate = request.FILES.get('files[doc_pwd]')
        nationality = request.POST.get('nationality')
        pio_oci_none = request.POST.get('are_you_pio_oci_none')

        logger.info(f"User: {request.user}")
        draft = BasicDetails(
        skype_details = skype_details,
        profilepic = profilepic,
        phd_thesis_defended = phd_thesis_defended,
        specialization = specialization,
        research_area = research_area,
        position_applied_for = position_applied_for,
        visiting_faculty = visiting_faculty,
        previous_application = previous_application,
        phd_title = phd_title,
        phd_defence_date = phd_defence_date,
        candidate_full_name = candidate_full_name,
        relative_relation = relative_relation,
        relative_name = relative_name,
        dob = dob,
        gender = gender,
        category = category,
        category_certificate = category_certificate,
        pwd_category = pwd_category,
        pwd_type = pwd_type,
        pwd_certificate = pwd_certificate,
        nationality = nationality,
        pio_oci_none = pio_oci_none
        )
        draft.user = request.user
        draft.save()
        # if request.is_ajax():
        #     return JsonResponse({'message': 'Draft saved successfully.'})

        messages.success(request, "Draft saved successfully!")
    # else:
    #     form = BasicDetailsForm(instance=instance)

    # return render(request, 'PAGE 1 OF 8.html', {'form': form})  # Replace with your current page's URL name
    return redirect("page2")


def communicationDetails(request):
    # try:
    #     instance = CommunicationDetails.objects.get(user=request.user)
    # except CommunicationDetails.DoesNotExist:
    #     instance = None

    if request.method == 'POST':

        form_data = request.POST.dict()
        request.session['faculty_form_page2'] = form_data
        
        # Handle file uploads
        if request.FILES:
            # Store file information in session
            files_data = {}
            for file_key in request.FILES:
                files_data[file_key] = request.FILES[file_key].name
            request.session['faculty_form_page2_files'] = files_data

        email_address = request.POST.get('email_address')
        alternate_email_address = request.POST.get('alternate_email_address')
        mobile_no = request.POST.get('mobile_no')
        alternate_contact_number = request.POST.get('alternate_contact_number')
        permanent_address = request.POST.get('permanent_address')
        correspondence_address = request.POST.get('correspondence_address')

        logger.info(f"User: {request.user}")

        draft = CommunicationDetails(
            email_address=email_address,
            alternate_email_address=alternate_email_address,
            mobile_no=mobile_no,
            alternate_contact_number=alternate_contact_number,
            permanent_address=permanent_address,
            correspondence_address=correspondence_address
        )
        draft.user = request.user
        draft.save()
    # else:
    #     form = CommunicationDetailsForm(instance=instance)
    #     messages.success(request, "Draft saved successfully!")
    # return render(request, 'PAGE 2 OF 8.html', {'form': form})  # Replace with your current page's URL name
    return redirect('page3')

def educationDetails(request):
    if request.method == 'POST':

        form_data = request.POST.dict()
        request.session['faculty_form_page3'] = form_data
        
        # Handle file uploads
        if request.FILES:
            # Store file information in session
            files_data = {}
            for file_key in request.FILES:
                files_data[file_key] = request.FILES[file_key].name
            request.session['faculty_form_page3_files'] = files_data

        university_institute_phd = request.POST.get('university_institute_phd')
        discipline_phd = request.POST.get('discipline_phd')
        phd_mode = request.POST.get('phd_mode')
        grade_type_phd = request.POST.get('grade_type')
        total_percentage_cgpa_phd = request.POST.get('total_percentage_cgpa_phd')
        start_date_phd = request.POST.get('start_date_phd')
        end_date_phd = request.POST.get('end_date_phd')
                # Check if dates are provided
        if not start_date_phd:
            messages.error(request, "Start Date of PhD is required.")
            return render(request, 'PAGE 3 OF 8.html')

        if not end_date_phd:
            messages.error(request, "End Date of PhD is required.")
            return render(request, 'PAGE 3 OF 8.html')

        # Parse the date strings to date objects
        start_date_phd = parse_date(start_date_phd)
        end_date_phd = parse_date(end_date_phd)

        # Validate parsed dates
        if not start_date_phd:
            messages.error(request, "Invalid format for Start Date of PhD. Use YYYY-MM-DD.")
            return render(request, 'PAGE 3 OF 8.html')

        if not end_date_phd:
            messages.error(request, "Invalid format for End Date of PhD. Use YYYY-MM-DD.")
            return render(request, 'PAGE 3 OF 8.html')
        phd_doc = request.FILES.get('files[phd_doc]')

        qualification_pg = request.POST.get('qualification_pg')
        board_university_pg = request.POST.get('board_university_pg')
        duration_pg = request.POST.get('duration_pg')
        passing_year_pg = request.POST.get('passing_year_pg')
        grade_type_pg = request.POST.get('grade_type_pg')
        total_percentage_cgpa_pg = request.POST.get('total_percentage_cgpa_pg')
        subjects_pg = request.POST.get('subjects_pg')
        pg_doc = request.FILES.get('files[pg_doc]')

        qualification_graduation = request.POST.get('qualification_graduation')
        board_university_graduation = request.POST.get('board_university_graduation')
        duration_graduation = request.POST.get('duration_graduation')
        passing_year_graduation = request.POST.get('passing_year_graduation')
        grade_type_graduation = request.POST.get('grade_type_graduation')
        total_percentage_cgpa_graduation = request.POST.get('total_percentage_cgpa_graduation')
        subjects_graduation = request.POST.get('subjects_graduation')
        graduation_doc = request.FILES.get('files[graduation_doc]')

        board_university_12th = request.POST.get('board_university_12th')
        duration_12th = request.POST.get('duration_12th')
        passing_year_12th = request.POST.get('passing_year_12th')
        grade_type_12th = request.POST.get('grade_type_12th')
        total_percentage_cgpa_12th = request.POST.get('total_percentage_cgpa_12th')
        subjects_12th = request.POST.get('subjects_12th')
        doc_12th = request.FILES.get('files[12th_doc]')

        board_university_10th = request.POST.get('board_university_10th')
        duration_10th = request.POST.get('duration_10th')
        passing_year_10th = request.POST.get('passing_year_10th')
        grade_type_10th = request.POST.get('grade_type_10th')
        total_percentage_cgpa_10th = request.POST.get('total_percentage_cgpa_10th')
        subjects_10th = request.POST.get('subjects_10th')
        doc_10th = request.FILES.get('files[10th_doc]')

        qualification_other1 = request.POST.get('qualification_other1')
        board_university_other1 = request.POST.get('board_universtiy_qualification_other1')
        duration_other1 = request.POST.get('duration_qualification_other1')
        passing_year_other1 = request.POST.get('passing_year_qualification_other1')
        grade_type_other1 = request.POST.get('grade_type_qualification_other1')
        total_percentage_cgpa_other1 = request.POST.get('total_percentage_cgpa_qualification_other1')
        subjects_other1 = request.POST.get('subjects_qualification_other1')
        doc_other1 = request.FILES.get('files[qualification_other1_doc]')

        qualification_other2 = request.POST.get('qualification_other2')
        board_university_other2 = request.POST.get('board_universtiy_qualification_other2')
        duration_other2 = request.POST.get('duration_qualification_other2')
        passing_year_other2 = request.POST.get('passing_year_qualification_other2')
        grade_type_other2 = request.POST.get('grade_type_qualification_other2')
        total_percentage_cgpa_other2 = request.POST.get('total_percentage_cgpa_qualification_other2')
        subjects_other2 = request.POST.get('subjects_qualification_other2')
        doc_other2 = request.FILES.get('files[qualification_other2_doc]')

        academic_gap = request.POST.get('academicgap')
        academic_gap_reason = request.POST.get('academicGapReason')
        academic_gap_from = request.POST.get('academicGapFrom')
        academic_gap_to = request.POST.get('academicGapTill')

        logger.info(f"User: {request.user}")

        draft = EducationDetails(

            university_institute_phd=university_institute_phd,
            discipline_phd=discipline_phd,
            phd_mode=phd_mode,
            grade_type_phd=grade_type_phd,
            total_percentage_cgpa_phd=total_percentage_cgpa_phd,
            start_date_phd=start_date_phd,
            end_date_phd=end_date_phd,
            phd_doc=phd_doc,

            qualification_pg=qualification_pg,
            board_university_pg=board_university_pg,
            duration_pg=duration_pg,
            passing_year_pg=passing_year_pg,
            grade_type_pg=grade_type_pg,
            total_percentage_cgpa_pg=total_percentage_cgpa_pg,
            subjects_pg=subjects_pg,
            pg_doc=pg_doc,

            qualification_graduation=qualification_graduation,
            board_university_graduation=board_university_graduation,
            duration_graduation=duration_graduation,
            passing_year_graduation=passing_year_graduation,
            grade_type_graduation=grade_type_graduation,
            total_percentage_cgpa_graduation=total_percentage_cgpa_graduation,
            subjects_graduation=subjects_graduation,
            graduation_doc=graduation_doc,

            board_university_12th=board_university_12th,
            duration_12th=duration_12th,
            passing_year_12th=passing_year_12th,
            grade_type_12th=grade_type_12th,
            total_percentage_cgpa_12th=total_percentage_cgpa_12th,
            subjects_12th=subjects_12th,
            doc_12th=doc_12th,
            
            board_university_10th=board_university_10th,
            duration_10th=duration_10th,
            passing_year_10th=passing_year_10th,
            grade_type_10th=grade_type_10th,
            total_percentage_cgpa_10th=total_percentage_cgpa_10th,
            subjects_10th=subjects_10th,
            doc_10th=doc_10th,

            qualification_other1=qualification_other1,
            board_university_other1=board_university_other1,
            duration_other1=duration_other1,
            passing_year_other1=passing_year_other1,
            grade_type_other1=grade_type_other1,
            total_percentage_cgpa_other1=total_percentage_cgpa_other1,
            subjects_other1=subjects_other1,
            doc_other1=doc_other1,

            qualification_other2=qualification_other2,
            board_university_other2=board_university_other2,
            duration_other2=duration_other2,
            passing_year_other2=passing_year_other2,
            grade_type_other2=grade_type_other2,
            total_percentage_cgpa_other2=total_percentage_cgpa_other2,
            subjects_other2=subjects_other2,
            doc_other2=doc_other2,

            academic_gap = academic_gap,
            academic_gap_reason = academic_gap_reason,
            academic_gap_from = academic_gap_from,
            academic_gap_to = academic_gap_to
        )
        draft.user = request.user
        draft.save()

        messages.success(request, "Draft saved successfully!")
    return redirect('page4')  # Replace with your current page's URL name

def experienceDetails(request):
    if request.method == 'POST':
        form_data = request.POST.dict()
        request.session['faculty_form_page4'] = form_data
        
        # Handle file uploads
        if request.FILES:
            # Store file information in session
            files_data = {}
            for file_key in request.FILES:
                files_data[file_key] = request.FILES[file_key].name
            request.session['faculty_form_page4_files'] = files_data

        info = []
        for i in range(1,9):
            info.append([request.POST.get(f'organization_name_exp_{i}'), request.POST.get(f'designation_exp_{i}'), request.POST.get(f'from_exp_{i}'), request.POST.get(f'to_exp_{i}'), request.POST.get(f'grade_pay_exp_{i}'), request.POST.get(f'gross_pay_exp_{i}'), request.POST.get(f'duties_performed_exp_{i}')])
        total_post_phd_experience_months = request.POST.get('total_months_exp_post_phd')
        total_post_phd_experience_years = request.POST.get('total_years_exp_post_phd')

        documents = []
        for i in range(1, 9):
            documents.append(request.FILES.get(f'files[exp_0{i}_doc]'))

        logger.info(f"User: {request.user}")

        draft = ExperienceDetails(
            post_phd_experience_1 = {
                'organization_name': info[0][0],
                'designation': info[0][1],
                'date_of_joining': info[0][2],
                'date_of_leaving': info[0][3],
                'pay_level':info[0][4],
                'gross_monthly_emolument': info[0][5],
                'duties_performed': info[0][6]
            },
            document_1 = documents[0],
            post_phd_experience_2 = {
                'organization_name': info[1][0],
                'designation': info[1][1],
                'date_of_joining': info[1][2],
                'date_of_leaving': info[1][3],
                'pay_level':info[1][4],
                'gross_monthly_emolument': info[1][5],
                'duties_performed': info[1][6]
            },
            document_2 = documents[1],
            post_phd_experience_3 = {
                'organization_name': info[2][0],
                'designation': info[2][1],
                'date_of_joining': info[2][2],
                'date_of_leaving': info[2][3],
                'pay_level':info[2][4],
                'gross_monthly_emolument': info[2][5],
                'duties_performed': info[2][6]
            },
            document_3 = documents[2],
            post_phd_experience_4 = {
                'organization_name': info[3][0],
                'designation': info[3][1],
                'date_of_joining': info[3][2],
                'date_of_leaving': info[3][3],
                'pay_level':info[3][4],
                'gross_monthly_emolument': info[3][5],
                'duties_performed': info[3][6]
            },
            document_4 = documents[3],
            post_phd_experience_5 = {
                'organization_name': info[4][0],
                'designation': info[4][1],
                'date_of_joining': info[4][2],
                'date_of_leaving': info[4][3],
                'pay_level':info[4][4],
                'gross_monthly_emolument': info[4][5],
                'duties_performed': info[4][6]
            },
            document_5 = documents[4],
            post_phd_experience_6 = {
                'organization_name': info[5][0],
                'designation': info[5][1],
                'date_of_joining': info[5][2],
                'date_of_leaving': info[5][3],
                'pay_level':info[5][4],
                'gross_monthly_emolument': info[5][5],
                'duties_performed': info[5][6]
            },
            document_6 = documents[5],
            post_phd_experience_7 = {
                'organization_name': info[6][0],
                'designation': info[6][1],
                'date_of_joining': info[6][2],
                'date_of_leaving': info[6][3],
                'pay_level':info[6][4],
                'gross_monthly_emolument': info[6][5],
                'duties_performed': info[6][6]
            },
            document_7 = documents[6],
            post_phd_experience_8 = {
                'organization_name': info[7][0],
                'designation': info[7][1],
                'date_of_joining': info[7][2],
                'date_of_leaving': info[7][3],
                'pay_level':info[7][4],
                'gross_monthly_emolument': info[7][5],
                'duties_performed': info[7][6]
            },
            document_8 = documents[7],
            total_post_phd_experience_months = total_post_phd_experience_months,
            total_post_phd_experience_years = total_post_phd_experience_years
        )

        draft.user = request.user
        draft.save()

        messages.success(request, "Draft saved successfully!")
    return redirect('page6')  # Replace with your current page's URL name

def otherDetails(request):
    if request.method == 'POST':
        form_data = request.POST.dict()
        request.session['faculty_form_page5'] = form_data
        
        # Handle file uploads
        if request.FILES:
            # Store file information in session
            files_data = {}
            for file_key in request.FILES:
                files_data[file_key] = request.FILES[file_key].name
            request.session['faculty_form_page5_files'] = files_data

        publications_in_refereed_journals = request.POST.get('publications_in_refereed_journals')
        publications_in_proceedings_of_seminars_conferences = request.POST.get('publications_in_proceedings_of_seminars_conferences')
        books_and_monographs = request.POST.get('books_and_monographs')
        book_chapters = request.POST.get('book_chapters')
        patents_copyright_obtained = request.POST.get('patents_copyright_obtained')

        journals = request.POST.get('journals')
        books = request.POST.get('books')
        conferences = request.POST.get('conferences')
        upload_best_10_publications = request.FILES.get('files[upload_best_10_publications]')

        total_number_of_patents_only_awarded = request.POST.get('total_number_of_patents_only_awarded')
        patent_1 = request.POST.get('patents_1')
        patent_2 = request.POST.get('patents_2')
        patent_3 = request.POST.get('patents_3')
        patent_4 = request.POST.get('patents_4')
        patent_5 = request.POST.get('patents_5')
        upload_list_of_patents = request.FILES.get('files[upload_list_of_patents]')

        guidance_at_doctoral_level_singly = request.POST.get('guidance_at_doctoral_level_singly')
        thesis_submitted = request.POST.get('thesis_submitted')
        defended = request.POST.get('defended')
        guidance_at_doctoral_level_jointly = request.POST.get('guidance_at_doctoral_level_jointly')
        thesis_submitted_jointly = request.POST.get('thesis_submitted_jointly')
        defended_jointly = request.POST.get('defended_jointly')

        pi_co_piconsultancy_projects = []
        for i in range(1, 6):
            pi_co_piconsultancy_projects.append([request.POST.get(f'pi_co_pi_consultancy_project_{i}'), request.POST.get(f'title_consultancy_project_{i}'), request.POST.get(f'sponsoring_agency_consultancy_project_{i}'), request.POST.get(f'status_consultancy_project_{i}'), request.POST.get(f'amount_consultancy_project_{i}')])

        list_of_consultancy_projects = request.FILES.get('files[list_of_consultancy_projects]')

        pi_co_pi_sponsored_projects = []
        for i in range(1, 6):
            pi_co_pi_sponsored_projects.append([request.POST.get(f'pi_co_pi_sponsored_project_{i}'), request.POST.get(f'title_sponsored_project_{i}'), request.POST.get(f'sponsoring_agency_sponsored_project_{i}'), request.POST.get(f'status_sponsored_project_{i}'), request.POST.get(f'amount_sponsored_project_{i}')])

        list_of_sponsored_projects = request.FILES.get('files[list_of_sponsored_projects]')

        logger.info(f"User: {request.user}")

        draft = OtherDetails(
            publications_in_refereed_journals=publications_in_refereed_journals,
            publications_in_proceedings_of_seminars_conferences=publications_in_proceedings_of_seminars_conferences,
            books_and_monographs=books_and_monographs,
            book_chapters=book_chapters,
            patents_copyright_obtained=patents_copyright_obtained,

            journals=journals,
            books=books,
            conferences=conferences,
            upload_best_10_publications=upload_best_10_publications,

            total_number_of_patents_only_awarded=total_number_of_patents_only_awarded,
            patent_1=patent_1,
            patent_2=patent_2,
            patent_3=patent_3,
            patent_4=patent_4,
            patent_5=patent_5,
            upload_list_of_patents=upload_list_of_patents,

            guidance_at_doctoral_level_singly=guidance_at_doctoral_level_singly,
            thesis_submitted=thesis_submitted,
            defended=defended,
            guidance_at_doctoral_level_jointly=guidance_at_doctoral_level_jointly,
            thesis_submitted_jointly=thesis_submitted_jointly,
            defended_jointly=defended_jointly,

            pi_co_pi_consultancy_project_1 = {
                'pi_co_pi': pi_co_piconsultancy_projects[0][0],
                'title': pi_co_piconsultancy_projects[0][1],
                'sponsoring_agency': pi_co_piconsultancy_projects[0][2],
                'status': pi_co_piconsultancy_projects[0][3],
                'amount': pi_co_piconsultancy_projects[0][4]
            },
            pi_co_pi_consultancy_project_2 = {
                'pi_co_pi': pi_co_piconsultancy_projects[1][0],
                'title': pi_co_piconsultancy_projects[1][1],
                'sponsoring_agency': pi_co_piconsultancy_projects[1][2],
                'status': pi_co_piconsultancy_projects[1][3],
                'amount': pi_co_piconsultancy_projects[1][4]
            },
            pi_co_pi_consultancy_project_3 = {
                'pi_co_pi': pi_co_piconsultancy_projects[2][0],
                'title': pi_co_piconsultancy_projects[2][1],
                'sponsoring_agency': pi_co_piconsultancy_projects[2][2],
                'status': pi_co_piconsultancy_projects[2][3],
                'amount': pi_co_piconsultancy_projects[2][4]
            },
            pi_co_pi_consultancy_project_4 = {
                'pi_co_pi': pi_co_piconsultancy_projects[3][0],
                'title': pi_co_piconsultancy_projects[3][1],
                'sponsoring_agency': pi_co_piconsultancy_projects[3][2],
                'status': pi_co_piconsultancy_projects[3][3],
                'amount': pi_co_piconsultancy_projects[3][4]
            },
            pi_co_pi_consultancy_project_5 = {
                'pi_co_pi': pi_co_piconsultancy_projects[4][0],
                'title': pi_co_piconsultancy_projects[4][1],
                'sponsoring_agency': pi_co_piconsultancy_projects[4][2],
                'status': pi_co_piconsultancy_projects[4][3],
                'amount': pi_co_piconsultancy_projects[4][4]
            },
            list_of_consultancy_projects=list_of_consultancy_projects,

            pi_co_pi_sponsored_project_1 = {
                'pi_co_pi': pi_co_pi_sponsored_projects[0][0],
                'title': pi_co_pi_sponsored_projects[0][1],
                'sponsoring_agency': pi_co_pi_sponsored_projects[0][2],
                'status': pi_co_pi_sponsored_projects[0][3],
                'amount': pi_co_pi_sponsored_projects[0][4]
            }, 
            pi_co_pi_sponsored_project_2 = {
                'pi_co_pi': pi_co_pi_sponsored_projects[1][0],
                'title': pi_co_pi_sponsored_projects[1][1],
                'sponsoring_agency': pi_co_pi_sponsored_projects[1][2],
                'status': pi_co_pi_sponsored_projects[1][3],
                'amount': pi_co_pi_sponsored_projects[1][4]
            },
            pi_co_pi_sponsored_project_3 = {
                'pi_co_pi': pi_co_pi_sponsored_projects[2][0],
                'title': pi_co_pi_sponsored_projects[2][1],
                'sponsoring_agency': pi_co_pi_sponsored_projects[2][2],
                'status': pi_co_pi_sponsored_projects[2][3],
                'amount': pi_co_pi_sponsored_projects[2][4]
            },
            pi_co_pi_sponsored_project_4 = {
                'pi_co_pi': pi_co_pi_sponsored_projects[3][0],
                'title': pi_co_pi_sponsored_projects[3][1],
                'sponsoring_agency': pi_co_pi_sponsored_projects[3][2],
                'status': pi_co_pi_sponsored_projects[3][3],
                'amount': pi_co_pi_sponsored_projects[3][4]
            },
            pi_co_pi_sponsored_project_5 = {
                'pi_co_pi': pi_co_pi_sponsored_projects[4][0],
                'title': pi_co_pi_sponsored_projects[4][1],
                'sponsoring_agency': pi_co_pi_sponsored_projects[4][2],
                'status': pi_co_pi_sponsored_projects[4][3],
                'amount': pi_co_pi_sponsored_projects[4][4]
            },
            list_of_sponsored_projects=list_of_sponsored_projects,

        )
        draft.user = request.user
        draft.save()

        messages.success(request, "Draft saved successfully!")
    return redirect('page7')  # Replace with your current page's URL name

def generalDetails(request):
    if request.method == 'POST':
        form_data = request.POST.dict()
        request.session['faculty_form_page6'] = form_data
        
        # Handle file uploads
        if request.FILES:
            # Store file information in session
            files_data = {}
            for file_key in request.FILES:
                files_data[file_key] = request.FILES[file_key].name
            request.session['faculty_form_page6_files'] = files_data
        academic_or_professional_awards_honours = request.POST.get('academic_or_professional_awards_honours')
        other_relevant_information = request.POST.get('files[other_relevant_information]')
        references = []
        for i in range(1, 4):
            references.append([request.POST.get(f'name_reference_{i}'), request.POST.get(f'designation_reference_{i}'), request.POST.get(f'organization_reference_{i}'), request.POST.get(f'email_reference_{i}'), request.POST.get(f'phonenumber_reference_{i}')])

        joining_time_required = request.POST.get('joining_time_required')


        logger.info(f"User: {request.user}")

        draft = GeneralDetails(
            academic_or_professional_awards_honours=academic_or_professional_awards_honours,
            other_relevant_information=other_relevant_information,
            reference_1 = {
                'name': references[0][0],
                'designation': references[0][1],
                'organization': references[0][2],
                'email': references[0][3],
                'phonenumber': references[0][4]
            },
            reference_2 = {
                'name': references[1][0],
                'designation': references[1][1],
                'organization': references[1][2],
                'email': references[1][3],
                'phonenumber': references[1][4]
            },
            reference_3 = {
                'name': references[2][0],
                'designation': references[2][1],
                'organization': references[2][2],
                'email': references[2][3],
                'phonenumber': references[2][4]
            },
            joining_time_required=joining_time_required
        )
        draft.user = request.user
        draft.save()

        pdfs = generate_user_pdfs(request.user)

        # Send the email with the PDFs attached
        send_email_with_pdfs(request.user, pdfs)

        messages.success(request, "Draft saved successfully, and email sent with your details!")
    return redirect('page8')  # Replace with your current page's URL name


from django.shortcuts import render, redirect
from django.http import JsonResponse


def load_form_page1(request):
    # Get saved data from session
    saved_data = request.session.get('faculty_form_page1', {})
    saved_files = request.session.get('faculty_form_page1_files', {})
    context = {
        'saved_data': saved_data,
        'saved_files': saved_files
    }
    return render(request, 'your_template.html', context)

def load_form_page2(request):
    # Get saved data from session
    saved_data = request.session.get('faculty_form_page2', {})
    saved_files = request.session.get('faculty_form_page2_files', {})
    context = {
        'saved_data': saved_data,
        'saved_files': saved_files
    }
    return render(request, 'your_template.html', context)


def load_form_page3(request):
    # Get saved data from session
    saved_data = request.session.get('faculty_form_page3', {})
    saved_files = request.session.get('faculty_form_page3_files', {})
    context = {
        'saved_data': saved_data,
        'saved_files': saved_files
    }
    return render(request, 'your_template.html', context)


def load_form_page4(request):
    # Get saved data from session
    saved_data = request.session.get('faculty_form_page4', {})
    saved_files = request.session.get('faculty_form_page4_files', {})
    context = {
        'saved_data': saved_data,
        'saved_files': saved_files
    }
    return render(request, 'your_template.html', context)
def load_form_page5(request):
    # Get saved data from session
    saved_data = request.session.get('faculty_form_page5', {})
    saved_files = request.session.get('faculty_form_page5_files', {})
    context = {
        'saved_data': saved_data,
        'saved_files': saved_files
    }
    return render(request, 'your_template.html', context)

def load_form_page6(request):
    # Get saved data from session
    saved_data = request.session.get('faculty_form_page6', {})
    saved_files = request.session.get('faculty_form_page6_files', {})
    context = {
        'saved_data': saved_data,
        'saved_files': saved_files
    }
    return render(request, 'your_template.html', context)


def load_form_page7(request):
    # Get saved data from session
    saved_data = request.session.get('faculty_form_page7', {})
    saved_files = request.session.get('faculty_form_page7_files', {})
    context = {
        'saved_data': saved_data,
        'saved_files': saved_files
    }
    return render(request, 'your_template.html', context)

def save_draft7(request):
    if request.method == 'POST':
        # Save form data to session
        form_data = request.POST.dict()
        request.session['faculty_form_page7'] = form_data
        
        # Handle file uploads
        if request.FILES:
            # Store file information in session
            files_data = {}
            for file_key in request.FILES:
                files_data[file_key] = request.FILES[file_key].name
            request.session['faculty_form_page7_files'] = files_data
            
        return JsonResponse({'status': 'success'})
    
    return redirect('form_page7')
