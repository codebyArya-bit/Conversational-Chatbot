# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    """User login form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """User registration form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    student_id = StringField('Student ID', validators=[Optional(), Length(max=20)])
    department = SelectField('Department', choices=[
        ('', 'Select Department'),
        ('computer_science', 'Computer Science'),
        ('information_technology', 'Information Technology'),
        ('electronics', 'Electronics Engineering'),
        ('mechanical', 'Mechanical Engineering'),
        ('civil', 'Civil Engineering'),
        ('electrical', 'Electrical Engineering'),
        ('business', 'Business Administration'),
        ('mathematics', 'Mathematics'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('other', 'Other')
    ], validators=[Optional()])
    year_of_study = SelectField('Year of Study', choices=[
        ('', 'Select Year'),
        ('1st_year', '1st Year'),
        ('2nd_year', '2nd Year'),
        ('3rd_year', '3rd Year'),
        ('4th_year', '4th Year'),
        ('graduate', 'Graduate'),
        ('faculty', 'Faculty/Staff')
    ], validators=[Optional()])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class DeviceSpecForm(FlaskForm):
    """Device specification form."""
    device_name = StringField('Device Name/Model', validators=[DataRequired(), Length(max=100)])
    device_type = SelectField('Device Type', choices=[
        ('laptop', 'Laptop'),
        ('desktop', 'Desktop Computer'),
        ('mobile', 'Mobile Phone'),
        ('tablet', 'Tablet'),
        ('printer', 'Printer'),
        ('router', 'Router/Network Device'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    operating_system = StringField('Operating System', validators=[DataRequired(), Length(max=100)])
    processor = StringField('Processor/CPU', validators=[Optional(), Length(max=100)])
    ram = StringField('RAM (Memory)', validators=[Optional(), Length(max=50)])
    storage = StringField('Storage (Hard Drive/SSD)', validators=[Optional(), Length(max=100)])
    graphics_card = StringField('Graphics Card', validators=[Optional(), Length(max=100)])
    network_adapter = StringField('Network Adapter', validators=[Optional(), Length(max=100)])
    other_specs = TextAreaField('Other Specifications', validators=[Optional()], widget=TextArea())
    is_primary = BooleanField('This is my primary device')
    submit = SubmitField('Save Device Specifications')

class SupportTicketForm(FlaskForm):
    """Support ticket creation form."""
    title = StringField('Issue Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Detailed Description', validators=[
        DataRequired(), 
        Length(min=20, message='Please provide a detailed description (at least 20 characters)')
    ], widget=TextArea())
    category = SelectField('Category', choices=[
        ('hardware', 'Hardware Issues'),
        ('software', 'Software Problems'),
        ('network', 'Network/Internet Issues'),
        ('account', 'Account/Login Problems'),
        ('email', 'Email Issues'),
        ('printing', 'Printing Problems'),
        ('virus', 'Virus/Security Issues'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low - Can wait'),
        ('medium', 'Medium - Normal priority'),
        ('high', 'High - Urgent'),
        ('urgent', 'Urgent - Critical issue')
    ], validators=[DataRequired()], default='medium')
    submit = SubmitField('Submit Ticket')

class ChatFeedbackForm(FlaskForm):
    """Chat feedback form to determine if issue was resolved."""
    was_helpful = SelectField('Was this response helpful?', choices=[
        ('yes', 'Yes, my issue was resolved'),
        ('partial', 'Partially helpful, but I need more assistance'),
        ('no', 'No, I still need help')
    ], validators=[DataRequired()])
    feedback_text = TextAreaField('Additional Comments', validators=[Optional()], widget=TextArea())
    escalate_to_support = BooleanField('I would like to escalate this to technical support')
    submit = SubmitField('Submit Feedback')

class AdminLoginForm(FlaskForm):
    """Admin login form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Admin Sign In')

class TicketUpdateForm(FlaskForm):
    """Form for admins to update support tickets."""
    status = SelectField('Status', choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ], validators=[DataRequired()])
    assigned_to = StringField('Assigned To', validators=[Optional(), Length(max=100)])
    resolution_notes = TextAreaField('Resolution Notes', validators=[Optional()], widget=TextArea())
    submit = SubmitField('Update Ticket')