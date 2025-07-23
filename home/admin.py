from django.contrib import admin
from home.models import BasicDetails, CommunicationDetails, EducationDetails, ExperienceDetails, OtherDetails, GeneralDetails
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.db import models
from io import BytesIO
import csv
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Image, SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader

def generate_user_pdfs(user):
    """
    Generates 5 PDFs for the given user.

    Args:
        user: User instance for whom the PDFs will be generated.

    Returns:
        A dictionary where keys are filenames and values are file contents (in bytes).
    """
    sections = {
        "Basic Details": BasicDetails.objects.filter(user=user),
        "Communication Details": CommunicationDetails.objects.filter(user=user),
        "Education Details": EducationDetails.objects.filter(user=user),
        "Experience Details": ExperienceDetails.objects.filter(user=user),
        "Other Details": OtherDetails.objects.filter(user=user),
    }

    pdfs = {}

    for section_name, queryset in sections.items():
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        pdf.setFont("Helvetica", 12)
        y = 800
        pdf.drawString(100, y, f"{section_name} for {user.username}:")
        y -= 20

        for record in queryset:
            for field in record._meta.fields:
                field_name = field.verbose_name or field.name
                field_value = getattr(record, field.name, "N/A")
                pdf.drawString(120, y, f"{field_name}: {field_value}")
                y -= 20
                if y < 100:
                    pdf.showPage()
                    y = 800

        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        pdfs[f"{user.username}_{section_name.replace(' ', '_')}.pdf"] = buffer.read()

    return pdfs


def send_email_with_pdfs(user, pdfs):
    """
    Sends an email with the generated PDFs attached.

    Args:
        user: User instance to whom the email will be sent.
        pdfs: Dictionary of filenames and their contents.
    """
    subject = "Your Submitted Details"
    body = f"""
    Dear {user.username},

    Thank you for your submission. Attached are the PDFs for your details.

    Best regards,
    Your Team
    """
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email="your_email@example.com",  # Replace with your email
        to=[user.email],  # User's email address
    )

    for filename, content in pdfs.items():
        email.attach(filename, content, "application/pdf")

    email.send()


# def export_as_pdf(detail_type):
#     def export_pdf(modeladmin, request, queryset):

#         if not queryset.exists():
#             return HttpResponse("No data selected for export.", content_type="text/plain")

#         # Get the username of the first user in the queryset
#         first_record = queryset.first()
#         user = first_record.user.username if hasattr(first_record, "user") else "unknown_user"

#         # Create a response object for the PDF
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename={user}_{detail_type}.pdf'

#         # Create the PDF object
#         pdf = canvas.Canvas(response)
#         pdf.setFont("Helvetica", 12)

#         try:
#             basic_details = BasicDetails.objects.get(user=first_record.user)
#             if basic_details.profilepic:
#                 profilepic_path = basic_details.profilepic.path  # Get the file path
#                 pdf.drawImage(ImageReader(profilepic_path), 100, 700, width=100, height=100)
#         except BasicDetails.DoesNotExist:
#             pass  # If no picture is found, continue without it
    
#         y = 800
#         pdf.drawString(100, y, f"{detail_type} for {user}:")
#         y -= 20

#         # Write each record in the section
#         for record in queryset:
#             for field in record._meta.fields:
#                 field_name = field.verbose_name or field.name  # Field label or name
#                 field_value = getattr(record, field.name, "N/A")  # Field value
#                 pdf.drawString(120, y, f"{field_name}: {field_value}")
#                 y -= 20

#                 if y < 100:  # Add a new page if space runs out
#                     pdf.showPage()
#                     y = 800

#         # Finalize and save the PDF
#         pdf.showPage()
#         pdf.save()
#         return response

#     export_pdf.short_description = f"Export {detail_type} as PDF"
#     return export_pdf


def export_as_pdf(detail_type): 
    def export_pdf(modeladmin, request, queryset):
        if not queryset.exists():
            return HttpResponse("No data selected for export.", content_type="text/plain")

        first_record = queryset.first()
        user = first_record.user.username if hasattr(first_record, "user") else "unknown_user"

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={user}_{detail_type}.pdf'

        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Title with proper formatting
        title = Paragraph(f"<b>{detail_type.upper()}</b>", styles["Title"])
        elements.append(title)
        elements.append(Spacer(1, 10))

        # Profile picture & name alignment
        profilepic_path = None
        try:
            basic_details = BasicDetails.objects.get(user=first_record.user)
            if basic_details.profilepic:
                profilepic_path = basic_details.profilepic.path
        except BasicDetails.DoesNotExist:
            pass  

        if profilepic_path:
            # Create an image object
            profile_img = Image(profilepic_path, width=80, height=80)  # Adjust size as needed

            # Create a table layout with profile picture on the right
            user_info_table = Table([
                [Paragraph(f"<b>{user}</b>", styles["Heading2"]), profile_img]
            ], colWidths=[300, 80])

            user_info_table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),  # Align profile picture to the right
            ]))

            elements.append(user_info_table)
        else:
            elements.append(Paragraph(f"<b>{user}</b>", styles["Heading2"]))

        elements.append(Spacer(1, 20))

        # Table Data for user details
        table_data = []

        for record in queryset:
            for field in record._meta.fields:
                field_name = field.verbose_name or field.name.replace("_", " ").title()
                field_value = getattr(record, field.name, "N/A")
                table_data.append([Paragraph(f"<b>{field_name}</b>", styles["BodyText"]), field_value])

        # Create the main details table
        table = Table(table_data, colWidths=[150, 300])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)
        return response

    export_pdf.short_description = f"Export {detail_type} as PDF"
    return export_pdf


def export_as_csv(detail_type):
    def export_csv(modeladmin, request, queryset):
        # Get the logged-in user's username
        if not queryset.exists():
            return HttpResponse("No data selected for export.", content_type="text/plain")

        # Get the username of the first user in the queryset
        first_record = queryset.first()
        user = first_record.user.username if hasattr(first_record, "user") else "unknown_user"

        # Create a response object for the CSV file
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={user}_{detail_type}.csv"'

        # Create a CSV writer
        writer = csv.writer(response)

        # Write header row (field names)
        if queryset.exists():
            fields = [field.verbose_name or field.name for field in queryset.model._meta.fields]
            writer.writerow(fields)

            # Write data rows (field values)
            for record in queryset:
                row = [getattr(record, field.name, "N/A") for field in queryset.model._meta.fields]
                writer.writerow(row)

        else:
            writer.writerow(["No data available for export"])

        return response

    export_csv.short_description = f"Export {detail_type} as CSV"
    return export_csv

class BasicDetailsAdmin(admin.ModelAdmin):
    actions = [export_as_pdf("Basic Details"), export_as_csv("Basic Details")]


class CommunicationDetailsAdmin(admin.ModelAdmin):
    actions = [export_as_pdf("Communication Details"), export_as_csv("Communication Details")] 

class EducationDetailsAdmin(admin.ModelAdmin):
    actions = [export_as_pdf("Education Details"), export_as_csv("Education Details")]

class ExperienceDetailsAdmin(admin.ModelAdmin):
    actions = [export_as_pdf("Experience"), export_as_csv("Experience")]

class OtherDetailsAdmin(admin.ModelAdmin):
    actions = [export_as_pdf("Other Details"), export_as_csv("Other Details")]

class GeneralDetailsAdmin(admin.ModelAdmin):
    actions = [export_as_pdf("General Details"), export_as_csv("General Details")]

# Register your models here.
admin.site.register(BasicDetails, BasicDetailsAdmin)
admin.site.register(CommunicationDetails, CommunicationDetailsAdmin)
admin.site.register(EducationDetails, EducationDetailsAdmin)
admin.site.register(ExperienceDetails, ExperienceDetailsAdmin)
admin.site.register(OtherDetails, OtherDetailsAdmin)
admin.site.register(GeneralDetails, GeneralDetailsAdmin)
