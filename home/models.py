# filepath: /d:/VS_CODE/WebDev/Django/project1/home/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date,datetime
import os

class BasicDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profilepic = models.ImageField(upload_to='profile_pics/', null=True,default=None)
    phd_thesis_defended = models.CharField(max_length=3, choices=[('YES', 'Yes'), ('NO', 'No')],  null=True,default=None)
    specialization = models.CharField(max_length=255,  null=True,default=None)
    research_area = models.CharField(max_length=255,   null=True,default=None)
    position_applied_for = models.CharField(max_length=255,  null=True,default=None)
    visiting_faculty = models.CharField(max_length=3, choices=[('YES', 'Yes'), ('NO', 'No')],  null=True,default=None)
    previous_application = models.CharField(max_length=3, choices=[('YES', 'Yes'), ('NO', 'No')],  null=True,default=None)
    phd_title = models.TextField(  null=True,default=None)
    phd_defence_date = models.DateField(  null=True,default=None)
    candidate_full_name = models.CharField(max_length=255,  null=True,default=None)
    relative_relation = models.CharField(max_length=8, choices=[('FATHER', 'Father'), ('HUSBAND', 'Husband')],  null=True,default=None)
    relative_name = models.CharField(max_length=255,  null=True,default=None)
    dob = models.DateField(null=True,default=None)
    age = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):

        if isinstance(self.dob, str):
            self.dob = datetime.strptime(self.dob, "%Y-%m-%d").date()

        if self.dob:
            today = date.today()
            self.age = today.year - self.dob.year - (
                (today.month, today.day) < (self.dob.month, self.dob.day)
            )
            print(f"Calculated age: {self.age}")
        super().save(*args, **kwargs)

    gender = models.CharField(max_length=20, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('TRANSGENDER', 'Transgender')],  null=True,default=None)
    category = models.CharField(max_length=20, choices=[('UR', 'UR'), ('SC', 'SC'), ('ST', 'ST'), ('OBC', 'OBC'), ('EWS', 'EWS')],  null=True,default=None)
    category_certificate = models.FileField(upload_to="category_certificates/",  null=True,default=None)
    pwd_category = models.CharField(max_length=3, choices=[('YES', 'Yes'), ('NO', 'No')],  null=True,default=None)
    pwd_type = models.CharField(max_length=255,   null=True,default=None)
    pwd_certificate = models.FileField(upload_to="pwd_certificates/",   null=True,default=None)
    nationality = models.CharField(max_length=20,  null=True,default=None)
    pio_oci_none = models.CharField(max_length=10,   null=True,default=None)
    skype_details = models.CharField(max_length=255,   null=True,default=None)
    saved_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}_BasicDetails"

class CommunicationDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_address = models.EmailField(max_length=254, verbose_name="Email Address", blank=True)
    alternate_email_address = models.EmailField(max_length=254, verbose_name="Alternate Email Address",   null=True,default=None)
    mobile_no = models.CharField(max_length=255, verbose_name="Mobile Number (with country code)", blank=True)
    alternate_contact_number = models.CharField(max_length=255, verbose_name="Alternate Contact Number (with country code)",   null=True,default=None)
    permanent_address = models.TextField(verbose_name="Permanent Address", blank=True)
    correspondence_address = models.TextField(verbose_name="Correspondence Address", blank=True)
    saved_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}_CommunicationDetails"

class EducationDetails(models.Model):
    # PhD Details
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university_institute_phd = models.CharField(max_length=255, verbose_name="University/Institute (PhD)", blank=True)
    discipline_phd = models.CharField(max_length=255, verbose_name="Discipline (PhD)", blank=True)
    phd_mode = models.CharField(max_length=50, verbose_name="Mode (PhD)", choices=[
        ('REGULAR', 'Regular'),
        ('PART-TIME', 'Part-time'),
        ('DISTANCE', 'Distance')
    ], blank=True)
    grade_type_phd = models.CharField(max_length=50, verbose_name="Grade Type (PhD)", choices=[
        ('%age', '%age'),
        ('CGPA', 'CGPA'),
        ('None Awarded', 'None Awarded')
    ], blank=True)
    total_percentage_cgpa_phd = models.CharField(max_length=255, verbose_name="%age/CGPA (PhD)",  default= 0)
    start_date_phd = models.DateField(verbose_name="Start Date of PhD", blank=True)
    end_date_phd = models.DateField(verbose_name="End Date of PhD", blank=True)
    phd_doc = models.FileField(upload_to='phd_docs/', verbose_name="PhD Degree/DMC", blank=True)

    # Qualification Details (Master's)
    qualification_pg = models.CharField(max_length=255, verbose_name="Master's Degree",  null = True)
    board_university_pg = models.CharField(max_length=255, verbose_name="Board/University (Master's)",  null = True)
    duration_pg = models.CharField(max_length=255, verbose_name="Duration (Master's)",  null = True)
    passing_year_pg = models.CharField(max_length=255, verbose_name="Passing Year (Master's)",  null = True,default= 0)
    grade_type_pg = models.CharField(max_length=50, verbose_name="Grade Type (Master's)", choices=[
        ('%age', '%age'),
        ('CGPA', 'CGPA')
    ],  null = True)
    total_percentage_cgpa_pg = models.CharField(max_length=255, verbose_name="%age/CGPA (Master's)",  null = True,default= 0)
    subjects_pg = models.CharField(max_length=255, verbose_name="Subjects (Master's)",  null = True)
    pg_doc = models.FileField(upload_to='pg_docs/', verbose_name="Master's Degree/DMC",  null = True)

    # Graduation Details
    qualification_graduation = models.CharField(max_length=255, verbose_name="Graduation Degree",  null = True)
    board_university_graduation = models.CharField(max_length=255, verbose_name="Board/University (Graduation)",  null = True)
    duration_graduation = models.CharField(max_length=255, verbose_name="Duration (Graduation)",  null = True)
    passing_year_graduation = models.CharField(max_length=255, verbose_name="Passing Year (Graduation)",  null = True,default= 0)
    grade_type_graduation = models.CharField(max_length=50, verbose_name="Grade Type (Graduation)", choices=[
        ('%age', '%age'),
        ('CGPA', 'CGPA')
    ],  null = True)
    total_percentage_cgpa_graduation = models.CharField(max_length=255, verbose_name="%age/CGPA (Graduation)",  null = True,default= 0)
    subjects_graduation = models.CharField(max_length=255, verbose_name="Subjects (Graduation)",  null = True)
    graduation_doc = models.FileField(upload_to='graduation_docs/', verbose_name="Graduation Degree/DMC",  null = True)

    # Intermediate/12th Details
    board_university_12th = models.CharField(max_length=255, verbose_name="Board/University (12th)",  null = True)
    duration_12th = models.CharField(max_length=255, verbose_name="Duration (12th)",  null = True)
    passing_year_12th = models.CharField(max_length=255, verbose_name="Passing Year (12th)",  null = True,default= 0)
    grade_type_12th = models.CharField(max_length=50, verbose_name="Grade Type (12th)", choices=[
        ('%age', '%age'),
        ('CGPA', 'CGPA')
    ],  null = True)
    total_percentage_cgpa_12th = models.CharField(max_length=255, verbose_name="%age/CGPA (12th)",  null = True,default= 0)
    subjects_12th = models.CharField(max_length=255, verbose_name="Subjects (12th)",  null = True)
    doc_12th = models.FileField(upload_to='12th_docs/', verbose_name="12th Degree/DMC",  null = True)

    # 10th Details
    board_university_10th = models.CharField(max_length=255, verbose_name="Board/University (10th)",  null = True)
    duration_10th = models.CharField(max_length=255, verbose_name="Duration (10th)",  null = True)
    passing_year_10th = models.CharField(max_length=255, verbose_name="Passing Year (10th)",  null = True,default= 0)
    grade_type_10th = models.CharField(max_length=50, verbose_name="Grade Type (10th)", choices=[
        ('%age', '%age'),
        ('CGPA', 'CGPA')
    ],  null = True)
    total_percentage_cgpa_10th = models.CharField(max_length=255, verbose_name="%age/CGPA (10th)",  null = True,default= 0)
    subjects_10th = models.CharField(max_length=255, verbose_name="Subjects (10th)",  null = True)
    doc_10th = models.FileField(upload_to='10th_docs/', verbose_name="10th Degree/DMC",  null = True)

    # Optional Qualifications
    qualification_other1 = models.CharField(max_length=255, verbose_name="Other Qualification 1", blank=True ,null = True)
    board_university_other1 = models.CharField(max_length=255, verbose_name="Board/University (Other Qualification 1)",  null = True)
    duration_other1 = models.CharField(max_length=255, verbose_name="Duration (Other Qualification 1)",  null = True)
    passing_year_other1 = models.CharField(max_length=255, verbose_name="Passing Year (Other Qualification 1)",  null = True,default= 0)
    grade_type_other1 = models.CharField(max_length=50, verbose_name="Grade Type (Other Qualification 1)", choices=[
        ('%age', '%age'),
        ('CGPA', 'CGPA')
    ], blank=True)
    total_percentage_cgpa_other1 = models.CharField(max_length=255, verbose_name="%age/CGPA (Other Qualification 1)",  null = True,default= 0)
    subjects_other1 = models.CharField(max_length=255, verbose_name="Subjects (Other Qualification 1)",  null = True)
    doc_other1 = models.FileField(upload_to='other_docs_1/', verbose_name="Other Qualification 1 Degree/DMC",  null = True)

    qualification_other2 = models.CharField(max_length=255, verbose_name="Other Qualification 2",  null = True)
    board_university_other2 = models.CharField(max_length=255, verbose_name="Board/University (Other Qualification 2)",  null = True)
    duration_other2 = models.CharField(max_length=255, verbose_name="Duration (Other Qualification 2)",  null = True)
    passing_year_other2 = models.CharField(max_length=255, verbose_name="Passing Year (Other Qualification 2)",  null = True,default= 0)
    grade_type_other2 = models.CharField(max_length=50, verbose_name="Grade Type (Other Qualification 2)", choices=[
        ('%age', '%age'),
        ('CGPA', 'CGPA')
    ], blank=True)
    total_percentage_cgpa_other2 = models.CharField(max_length=255, verbose_name="%age/CGPA (Other Qualification 2)",  null = True,default= 0)
    subjects_other2 = models.CharField(max_length=255, verbose_name="Subjects (Other Qualification 2)",  null = True)
    doc_other2 = models.FileField(upload_to='other_docs_2/', verbose_name="Other Qualification 2 Degree/DMC",  null = True)

    academic_gap = models.CharField(max_length=3, choices=[('YES', 'Yes'), ('NO', 'No')],  null=True,default=None)
    academic_gap_reason = models.TextField(  null=True,default=None)
    academic_gap_from = models.DateField(  null=True,default=None)
    academic_gap_to = models.DateField(  null=True,default=None)
    academic_gap_duration_in_days = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):

        if isinstance(self.academic_gap_from, str):
            self.academic_gap_from = datetime.strptime(self.academic_gap_from, "%Y-%m-%d").date()
        if isinstance(self.academic_gap_to, str):
            self.academic_gap_to = datetime.strptime(self.academic_gap_to, "%Y-%m-%d").date()

        if self.academic_gap_from and self.academic_gap_to:
            self.academic_gap_duration_in_days = (self.academic_gap_to - self.academic_gap_from).days
            print(f"Calculated gap duration: {self.academic_gap_duration_in_days}")

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user.username}_EducationDetails"

def validate_pdf_file(file):
    ext = os.path.splitext(file.name)[1]
    valid_extensions = ['.pdf']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Only PDF files are allowed.')

    if file.size > 2 * 1024 * 1024:  # 2 MB limit
        raise ValidationError('File size must not exceed 2 MB.')

class ExperienceDetails(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_phd_experience_1 = models.JSONField()
    post_phd_experience_2 = models.JSONField()
    post_phd_experience_3 = models.JSONField()
    post_phd_experience_4 = models.JSONField()
    post_phd_experience_5 = models.JSONField()
    post_phd_experience_6 = models.JSONField()
    post_phd_experience_7 = models.JSONField()
    post_phd_experience_8 = models.JSONField()

    document_1 = models.FileField(upload_to='experience_docs/',validators=[validate_pdf_file],verbose_name="Upload Document",help_text="Upload one PDF file only..",null=True,default=None,blank=True)
    document_2 = models.FileField(upload_to='experience_docs/',validators=[validate_pdf_file],verbose_name="Upload Document",help_text="Upload one PDF file only..",null=True,default=None,blank=True)
    document_3 = models.FileField(upload_to='experience_docs/',validators=[validate_pdf_file],verbose_name="Upload Document",help_text="Upload one PDF file only..",null=True,default=None,blank=True)
    document_4 = models.FileField(upload_to='experience_docs/',validators=[validate_pdf_file],verbose_name="Upload Document",help_text="Upload one PDF file only..",null=True,default=None,blank=True)
    document_5 = models.FileField(upload_to='experience_docs/',validators=[validate_pdf_file],verbose_name="Upload Document",help_text="Upload one PDF file only..",null=True,default=None,blank=True)
    document_6 = models.FileField(upload_to='experience_docs/',validators=[validate_pdf_file],verbose_name="Upload Document",help_text="Upload one PDF file only..",null=True,default=None,blank=True)
    document_7 = models.FileField(upload_to='experience_docs/',validators=[validate_pdf_file],verbose_name="Upload Document",help_text="Upload one PDF file only..",null=True,default=None,blank=True)
    document_8 = models.FileField(upload_to='experience_docs/',validators=[validate_pdf_file],verbose_name="Upload Document",help_text="Upload one PDF file only..",null=True,default=None,blank=True)
        
    total_post_phd_experience_months = models.CharField(max_length=255,null=True,default=None, blank=True)
    total_post_phd_experience_years = models.CharField(max_length=255,null=True,default=None, blank=True)

    # Additional metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated At")

    def __str__(self):
        return f"{self.user.username}_ExperienceDetails"
    
class OtherDetails(models.Model):
    # Fields related to publications, patents, and books
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publications_in_refereed_journals = models.CharField(max_length=255,null=True,  default= 0)
    publications_in_proceedings_of_seminars_conferences = models.CharField(max_length=255,null=True,  default= '0',blank=True)
    books_and_monographs = models.CharField(max_length=255,null=True,  default= 0)
    book_chapters = models.CharField(max_length=255,null=True,  default= 0)
    patents_copyright_obtained = models.CharField(max_length=255,null=True,  default= 0)

    # Complete list of publications
    journals = models.TextField(null=True,default=None, blank=True)
    books = models.TextField(null=True,default=None, blank=True)
    conferences = models.TextField(null=True,default=None, blank=True)
    upload_best_10_publications = models.FileField(upload_to='publications/', null=True,default=None, blank=True)

    # Patents or products
    total_number_of_patents_only_awarded = models.CharField(max_length=255,null=True,  default= 0)
    patent_1 = models.CharField(max_length=255, null=True,default=None, blank=True)
    patent_2 = models.CharField(max_length=255, null=True,default=None, blank=True)
    patent_3 = models.CharField(max_length=255, null=True,default=None, blank=True)
    patent_4 = models.CharField(max_length=255, null=True,default=None, blank=True)
    patent_5 = models.CharField(max_length=255, null=True,default=None, blank=True)
    upload_list_of_patents = models.FileField(upload_to='patents/', null=True,default=None, blank=True)

    # Research guidance at doctorate level
    guidance_at_doctoral_level_singly = models.CharField(max_length=255,null=True,  default= 0)
    thesis_submitted = models.CharField(max_length=255,null=True,  default= 0)
    defended = models.CharField(max_length=255,null=True,  default= 0)
    guidance_at_doctoral_level_jointly = models.CharField(max_length=255,null=True,  default= 0)
    thesis_submitted_jointly = models.CharField(max_length=255,null=True,  default= 0)
    defended_jointly = models.CharField(max_length=255,null=True,  default= 0)

    # Consultancy projects
    pi_co_pi_consultancy_project_1 = models.JSONField(null=True,default=None,   help_text="JSON format: [{'role': 'PI', 'title': 'Title', 'sponsoring_agency': 'Agency', 'status': 'ONGOING', 'amount': 1000}]")
    pi_co_pi_consultancy_project_2 = models.JSONField(null=True,default=None, blank=True)
    pi_co_pi_consultancy_project_3 = models.JSONField(null=True,default=None, blank=True)
    pi_co_pi_consultancy_project_4 = models.JSONField(null=True,default=None, blank=True)
    pi_co_pi_consultancy_project_5 = models.JSONField(null=True,default=None, blank=True)
    list_of_consultancy_projects = models.FileField(upload_to='consultancy_projects/', null=True,default=None, blank=True)

    # Sponsored projects
    pi_co_pi_sponsored_project_1 = models.JSONField(null=True,default=None,   help_text="JSON format: [{'role': 'PI', 'title': 'Title', 'sponsoring_agency': 'Agency', 'status': 'COMPLETED', 'amount': 5000}]")
    pi_co_pi_sponsored_project_2 = models.JSONField(null=True,default=None, blank=True)
    pi_co_pi_sponsored_project_3 = models.JSONField(null=True,default=None, blank=True)
    pi_co_pi_sponsored_project_4 = models.JSONField(null=True,default=None, blank=True)
    pi_co_pi_sponsored_project_5 = models.JSONField(null=True,default=None, blank=True)
    list_of_sponsored_projects = models.FileField(upload_to='sponsored_projects/', null=True,default=None, blank=True)

    def __str__(self):
        return f"{self.user.username}_OtherDetails"
    
class GeneralDetails(models.Model):
    # Academic or professional awards
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    academic_or_professional_awards_honours = models.TextField(null=True,default=None, blank=True)
    
    # Other relevant information
    other_relevant_information = models.FileField(upload_to='relevant_info/', null=True,default=None, blank=True)

    # References details
    reference_1 = models.JSONField(null=True,default=None,   help_text="JSON format: [{'name': 'John Doe', 'designation': 'Professor', 'organization': 'XYZ University', 'email': 'john@example.com', 'phone_number': '1234567890'}]")
    reference_2 = models.JSONField(null=True,default=None, blank=True)
    reference_3 = models.JSONField(null=True,default=None, blank=True)

    # Expected date of joining
    joining_time_required = models.CharField(max_length=10, null=True,default=None, blank=True)

    def __str__(self):
        return f"{self.user.username}_GeneralDetails"