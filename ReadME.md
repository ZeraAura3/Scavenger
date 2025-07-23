# IIT Mandi Faculty Portal

A Django-based web application for managing faculty recruitment and application processes at IIT Mandi. This portal allows candidates to submit their applications with comprehensive details and documents for faculty positions.

## Features

### User Management
- **User Registration & Authentication**: Secure sign-up and login system
- **Password Reset**: Email-based password recovery functionality
- **User Profiles**: Comprehensive profile management

### Application Management
- **Multi-step Application Form**: 8-page application form covering:
  - Basic Details (Personal information, categories, specialization)
  - Communication Details (Contact information, addresses)
  - Education Details (Academic qualifications)
  - Experience Details (Professional experience with document uploads)
  - Other Details (Research, publications, patents, projects)
- **Draft Saving**: Save application progress at any stage
- **Document Upload**: Support for multiple document types including:
  - Profile pictures
  - Academic certificates (10th, 12th, Graduation, PG, PhD)
  - Category and PWD certificates
  - Experience documents
  - Research publications and patents
                                                                                                             
### Admin Features
- **Admin Panel**: Django admin interface for application management
- **PDF Generation**: Automatic generation of user application PDFs
- **Email Integration**: SMTP-based email system for notifications

## Technology Stack

- **Backend**: Django 5.1.4
- **Database**: SQLite3 (development)
- **Frontend**: HTML, CSS, JavaScript
- **Email**: SMTP integration with Gmail
- **File Storage**: Local media storage for uploaded documents

## Project Structure

```
project5/
├── home/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── urls.py            # URL patterns
│   └── migrations/        # Database migrations
├── project1/              # Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── templates/             # HTML templates
├── static/               # Static files (CSS, JS, images)
├── media/                # User uploaded files
└── manage.py             # Django management script
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd project5
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow
   ```

4. **Configure email settings**
   - Update email credentials in `project1/settings.py`
   - Replace `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` with your credentials

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### For Applicants
1. **Register**: Create an account using the sign-up page
2. **Login**: Access your dashboard after authentication
3. **Fill Application**: Complete the 8-page application form
4. **Upload Documents**: Submit required certificates and documents
5. **Save Drafts**: Save progress at any stage
6. **Submit**: Final submission of complete application

### For Administrators
1. **Admin Access**: Use Django admin panel for management
2. **Review Applications**: View and manage submitted applications
3. **Generate Reports**: Export application data as PDFs
4. **Email Communication**: Send notifications to applicants

## Database Models

### Key Models
- **BasicDetails**: Personal information, categories, specialization
- **CommunicationDetails**: Contact information and addresses
- **EducationDetails**: Academic qualifications and certificates
- **ExperienceDetails**: Professional experience with documents
- **OtherDetails**: Research work, publications, patents, projects
- **GeneralDetails**: Final submission and general information

## File Upload Categories

The application supports organized file uploads in the following categories:
- Profile pictures
- Academic documents (10th, 12th, graduation, PG, PhD)
- Category certificates
- PWD certificates
- Experience documents
- Publications
- Patents
- Project documents
- Other relevant documents

## Configuration

### Email Settings
Update the following in `settings.py`:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Media Storage
Files are stored in the `media/` directory with organized subdirectories for different document types.

## Security Features

- CSRF protection enabled
- Secure password validation
- File upload validation
- User authentication required for sensitive operations
- Debug mode disabled for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is developed for IIT Mandi's faculty recruitment process.

## Support

For technical support or questions, please contact the development team.

---

**Note**: This is a development version. Ensure proper security configurations before deploying to production.