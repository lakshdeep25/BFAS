from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.label import  MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import Screen
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from config import get_db_collection
from kivy.uix.slider import Slider
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.uix.button import MDIconButton
from expense_analyzer import ExpenseAnalyzerScreen
from budget_planner import BudgetPlannerScreen, ResultsScreen, SIPCalculatorScreen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button


class BFAS(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Purple'
        self.theme_cls.primary_hue = '900'

        self.screen_manager = ScreenManager()

        # Main menu screen
        self.main_menu = Screen(name='main_menu')
        main_layout = BoxLayout(orientation='vertical')

        # Expense Analyzer button
        exp_analyzer_btn = Button(text='Expense Analyzer', size_hint_y=None, height=50)
        exp_analyzer_btn.bind(on_release=self.start_analyzing)
        main_layout.add_widget(exp_analyzer_btn)

        # Budget Planner button
        budget_planner_btn = Button(text='Plan Budget', size_hint_y=None, height=50)
        budget_planner_btn.bind(on_release=self.plan_budget)  # Connect to the Budget Planner screen
        main_layout.add_widget(budget_planner_btn)
        

        self.main_menu.add_widget(main_layout)
        self.screen_manager.add_widget(self.main_menu)
        
        # Set ScreenManager to self.manager for accessibility in other methods
        self.manager = self.screen_manager
        
        # Main screen layout
        self.main_layout = FloatLayout()
        
        # Add a label widget using MDLabel for the welcome text
        self.main_layout.add_widget(MDLabel(
            text='Welcome To,',
            halign='left',
            theme_text_color="Primary",
            font_style='H4',
            bold=True,
            color=get_color_from_hex('#4a148c'),  # Set text color to #4a148c
            size_hint=(0.8, None),
            height=100,
            pos_hint={'center_x': 0.5, 'top': 0.7},
            font_name='./fonts/Roboto-Bold.ttf'  # Specify the path to Roboto-Bold.ttf
        ))

        # Add a label for additional text
        self.main_layout.add_widget(MDLabel(
            text='Analyze Your Finances Efficiently !!',
            halign='left',
            theme_text_color="Primary",
            font_style='H5',
            color=get_color_from_hex('#4a148c'),  # Set text color to #4a148c
            size_hint=(0.8, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.6},
            font_name='./fonts/Roboto-Regular.ttf'  # Specify the path to Roboto-Regular.ttf
        ))

        # Add Sign Up and Login buttons
        button_layout = BoxLayout(
            orientation='horizontal',
            spacing=20,
            size_hint=(0.8, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.5}
        )
        button_layout.add_widget(MDRaisedButton(
            text='Sign Up',
            size_hint=(0.5, None),
            height=50,
            on_release=self.on_signup
        ))
        button_layout.add_widget(MDRaisedButton(
            text='Login',
            size_hint=(0.5, None),
            height=50,
            on_release=self.on_login  # Connect to on_login method
        ))

        self.main_layout.add_widget(button_layout)

        return self.main_layout

    def on_signup(self, _):
        self.signup_screen = Screen(name='signup')
        
        # Create a BoxLayout for signup inputs
        signup_box = BoxLayout(orientation='vertical', padding=40, spacing=20, 
                               size_hint=(None, None), size=(400, 400), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        # Add text fields for username, mobile number, password, and confirm password
        self.username_field = MDTextField(
            hint_text='Enter Username',
            required=True,
            helper_text_mode='on_focus'
        )
        signup_box.add_widget(self.username_field)
        
        # Add a label for username availability message
        self.username_availability_label = MDLabel(
            text='',
            halign='left',
            theme_text_color="Primary",
            font_style='Body2',
            color=get_color_from_hex('#FF0000'),  # Set text color to red
            size_hint=(None, None),
            height=20,
            pos_hint={'center_x': 0.5}
        )
        signup_box.add_widget(self.username_availability_label)
        
        self.mobile_number_field = MDTextField(
            hint_text='Enter 10 Digit mobile number',
            required=True,
            helper_text_mode='on_focus'
        )
        signup_box.add_widget(self.mobile_number_field)
        
        self.password_field = MDTextField(
            hint_text='Enter Password (Must Contain Letters, Numbers And Special Characters.)',
            required=True,
            helper_text_mode='on_focus',
            password=True
        )
        signup_box.add_widget(self.password_field)
        
        self.confirm_password_field = MDTextField(
            hint_text='Confirm Password',
            required=True,
            helper_text_mode='on_focus',
            password=True
        )
        signup_box.add_widget(self.confirm_password_field)
        
        # Add a signup button
        signup_box.add_widget(MDRaisedButton(
            text='Create Account',
            size_hint=(None, None),
            width=200,
            height=50,
            on_release=self.validate_signup_with_loading_spinner  # Changed to use loading spinner method
        ))

        self.signup_screen.add_widget(signup_box)
        self.main_layout.clear_widgets()  # Remove main screen widgets
        self.main_layout.add_widget(self.signup_screen)  # Add signup screen

    def validate_signup_with_loading_spinner(self, _):
        # Show loading spinner while creating account
        self.show_loading_spinner()
        
        # Simulate delay before checking and creating account
        Clock.schedule_once(self.create_account_with_loading_spinner, 2)  # Simulate a delay of 2 seconds

    def show_loading_spinner(self):
        # Function to show a loading spinner while processing
        self.spinner = MDSpinner(
            size_hint=(None, None),
            size=(46, 46),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.main_layout.add_widget(self.spinner)

    def create_account_with_loading_spinner(self, _):
        # Simulated account creation logic
        username = self.username_field.text.strip()
        password = self.password_field.text.strip()
        confirm_password = self.confirm_password_field.text.strip()
        mobile_number = self.mobile_number_field.text.strip()
        
        # Check if password meets criteria (letters, numbers, special characters)
        if not self.validate_password(password):
            print("Password must contain letters, numbers, and special characters.")
            self.hide_loading_spinner()
            return
        
        # Check if passwords match
        if password != confirm_password:
            print("Passwords do not match.")
            self.hide_loading_spinner()
            return
        
        # Check if username is available in MongoDB
        if not self.username_available(username):
            error_message = f"The username '{username}' is not available. Please choose another."
            self.username_availability_label.text = error_message
            print(error_message)
            self.hide_loading_spinner()
            return
        
        # Check if mobile number already exists in MongoDB
        if not self.mobile_number_available(mobile_number):
            print(f"Mobile number '{mobile_number}' already exists.")
            Snackbar(text=f"Mobile number '{mobile_number}' already exists.").show()
            self.hide_loading_spinner()
            return
        
        # Create account if all checks pass
        self.create_account(username, password, mobile_number)
        
        # Navigate to personal details screen
        self.show_personal_details_screen(username, mobile_number)

    def validate_password(self, password):
        # Implement your password validation criteria here
        # Example: Password must contain at least one letter, one number, one special character
        import re
        if re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            return True
        else:
            return False

    def username_available(self, username):
        # Query MongoDB to check if username exists
        collection = get_db_collection()
        query = {'username': username}
        result = collection.find_one(query)
        return result is None

    def mobile_number_available(self, mobile_number):
        # Query MongoDB to check if mobile number exists
        collection = get_db_collection()
        query = {'mobile_number': mobile_number}
        result = collection.find_one(query)
        return result is None

    def create_account(self, username, password, mobile_number):
        # Function to create account in MongoDB
        collection = get_db_collection()
        user_data = {
            'username': username,
            'password': password,
            'mobile_number': mobile_number
        }
        collection.insert_one(user_data)
        print(f"Account created for '{username}'!")

    def show_personal_details_screen(self, username, mobile_number):
        self.personal_details_screen = Screen(name='personal_details')
        
        # Create a BoxLayout for personal details inputs
        personal_details_box = BoxLayout(orientation='vertical', padding=40, spacing=20, 
                                         size_hint=(None, None), size=(400, 600), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        # Add text fields for full name, date of birth, gender, email, father's name, and address
        full_name_field = MDTextField(
            hint_text='Enter Full Name',
            required=True,
            helper_text_mode='on_focus'
        )
        personal_details_box.add_widget(full_name_field)
        
        dob_field = MDTextField(
            hint_text='Enter Date of Birth (DD-MM-YYYY)',
            required=True,
            helper_text_mode='on_focus'
        )
        personal_details_box.add_widget(dob_field)
        
    
        gender_Field = MDTextField(
            hint_text='Enter Gender',
            readonly=True,
            helper_text_mode ='on_focus'
        )
        personal_details_box.add_widget(gender_Field)
        
        email_field = MDTextField(
            hint_text='Enter Email ID',
            required=True,
            helper_text_mode='on_focus'
        )
        personal_details_box.add_widget(email_field)
        
        father_name_field = MDTextField(
            hint_text='Enter Father\'s Name',
            required=True,
            helper_text_mode='on_focus'
        )
        personal_details_box.add_widget(father_name_field)
        
        address_field = MDTextField(
            hint_text='Enter Address',
            required=True,
            helper_text_mode='on_focus'
        )
        personal_details_box.add_widget(address_field)
        
        # Add a submit button
        personal_details_box.add_widget(MDRaisedButton(
            text='Submit',
            size_hint=(None, None),
            width=200,
            height=50,
            on_release=lambda x: self.submit_personal_details(username, mobile_number, full_name_field.text.strip(),
                                                              dob_field.text.strip(), gender_Field.text.strip(),
                                                              email_field.text.strip(), father_name_field.text.strip(),
                                                              address_field.text.strip())
        ))

        self.personal_details_screen.add_widget(personal_details_box)
        self.main_layout.clear_widgets()  # Remove signup screen widgets
        self.main_layout.add_widget(self.personal_details_screen)  # Add personal details screen

    def submit_personal_details(self, username, mobile_number, full_name, dob, gender, email, father_name, address):
        # Implement logic to validate and submit personal details
        # For demonstration, we'll just print the details
        print(f"Personal details submitted:\nFull Name: {full_name}\nDate of Birth: {dob}\nGender: {gender}\nEmail: {email}\nFather's Name: {father_name}\nAddress: {address}")
        # Update UI or navigate to next screen
        self.show_home_screen()
    

    def show_home_screen(self):
        if not hasattr(self, 'home_screen'):
            self.home_screen = Screen(name='home')

            # Create a toolbar for the home screen
            toolbar = MDToolbar(title="BFAS", pos_hint={"top": 1})
            toolbar.right_action_items = [
                ["home", lambda x: self.goto_home()],
                ["information", lambda x: self.goto_about()],
                ["account", lambda x: self.goto_contact()],
                ["star", lambda x: self.goto_rating()],
                ["logout", lambda x: self.goto_logout()]
            ]
            self.home_screen.add_widget(toolbar)

            # Create a BoxLayout for home screen content
            home_box = BoxLayout(orientation='vertical', padding=40, spacing=20, 
                                 size_hint=(None, None), size=(400, 400), pos_hint={'center_x': 0.5, 'center_y': 0.5})

            # Add a label for additional text
            home_box.add_widget(MDLabel(
                text='Welcome, BFAS',
                halign='center',
                theme_text_color="Primary",
                font_style='H4',
                color=get_color_from_hex('#4a148c'),
                size_hint=(0.8, None),
                height=50,
                pos_hint={'center_x': 0.5, 'top': 0.8},
                font_name='./fonts/Roboto-Regular.ttf'
            ))

            # First Expense Analyzer section
            self.home_screen.add_widget(self.analyzer_create_section(
                title='Expense Analyzer',
                description='Analyze your expenses and manage your budget effectively.',
                button_text='Start Analyzing',
                button_callback=self.start_analyzing,
            ))

            # Second Budget Planner section
            self.home_screen.add_widget(self.budget_create_section(
                title='Budget Planner',
                description='Plan and Create Budgets to Achieve your Financial goals.',
                button_text='Plan Budget',
                button_callback=self.plan_budget,
            ))

        self.main_layout.clear_widgets()  # Clear the main layout
        self.main_layout.add_widget(self.home_screen)  # Add the home screen

    def goto_home(self):
        self.show_home_screen()

    def goto_about(self):
        if not hasattr(self, 'about_screen'):
            self.about_screen = Screen(name='about')

        # Create a toolbar for the about screen
            toolbar = MDToolbar(title="About", pos_hint={"top": 1})
            toolbar.left_action_items = [["arrow-left", lambda x: self.goto_home()]]
            self.about_screen.add_widget(toolbar)

        # Create a layout for the about screen content
            about_layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)

        # Add an introduction label
            about_layout.add_widget(MDLabel(
            text='Welcome to BFAS - Budget and Finance Analyzer System',
            halign='center',
            theme_text_color="Primary",
            font_style='H5',
            size_hint=(1, None),
            height=dp(30)
        ))

        # Add a features section
            about_layout.add_widget(MDLabel(
            text='Features:',
            halign='left',
            theme_text_color="Primary",
            font_style='H6',
            size_hint=(1, None),
            height=dp(30)
        ))

            features = [
            '1. Analyze your finances efficiently.',
            '2. Track your expenses and income.',
            '3. Get personalized financial advice.',
            '4. Easy-to-use interface.',
            '5. Secure and private.'
        ]
            for feature in features:
                about_layout.add_widget(MDLabel(
                text=feature,
                halign='left',
                theme_text_color="Secondary",
                size_hint=(1, None),
                height=dp(24)
            ))

        # Add a purpose section
            about_layout.add_widget(MDLabel(
            text='Purpose:',
            halign='left',
            theme_text_color="Primary",
            font_style='H6',
            size_hint=(1, None),
            height=dp(30)
        ))

            about_layout.add_widget(MDLabel(
            text='The purpose of BFAS is to help users manage their finances by '
                 'providing tools for tracking expenses, analyzing spending patterns, '
                 'and offering advice on how to save money and achieve financial goals.',
            halign='left',
            theme_text_color="Secondary",
            size_hint=(1, None),
            height=dp(60)
        ))

        # Add the layout to the about screen
            self.about_screen.add_widget(about_layout)

        self.main_layout.clear_widgets()  # Clear the main layout
        self.main_layout.add_widget(self.about_screen)  # Add the about screen


        self.main_layout.clear_widgets()  # Clear the main layout
        self.main_layout.add_widget(self.about_screen)  # Add the about screen

    def goto_contact(self):
        if not hasattr(self, 'contact_screen'):
            self.contact_screen = Screen(name='contact')

        # Create a toolbar for the contact screen
            toolbar = MDToolbar(title="Contact", pos_hint={"top": 1})
            toolbar.left_action_items = [["arrow-left", lambda x: self.goto_home()]]
            self.contact_screen.add_widget(toolbar)

        # Create a vertical box layout for the contact details
            contact_layout = BoxLayout(orientation='vertical', padding=20, spacing=5)

        # Add contact information labels
            contact_layout.add_widget(MDLabel(
                text='Phone: +1234567890',
                halign='center',
                font_style='Subtitle1'
        ))
            contact_layout.add_widget(MDLabel(
                text='Email: contact@bfas.com',
                halign='center',
                font_style='Subtitle1'
        ))
            contact_layout.add_widget(MDLabel(
                text='Address: 123 Finance Street, Money City',
                halign='center',
                font_style='Subtitle1'
        ))

        # Add the layout to the screen
        self.contact_screen.add_widget(contact_layout)

    # Clear the main layout and switch to the contact screen
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.contact_screen)

    def goto_rating(self):
        if not hasattr(self, 'rating_screen'):
            self.rating_screen = Screen(name='rating')

        # Create a toolbar for the rating screen
        toolbar = MDToolbar(title="Rating", pos_hint={"top": 1})
        toolbar.left_action_items = [["arrow-left", lambda x: self.goto_home()]]
        self.rating_screen.add_widget(toolbar)

        # Create a BoxLayout to hold the label, stars, and submit button
        main_layout = BoxLayout(orientation='vertical', spacing=20, padding=20)

        # Add a placeholder label
        main_layout.add_widget(MDLabel(
            text='Rate our app:',
            halign='center',
            font_style='H5',
            size_hint_y=None,
            height=50
        ))

        # Add a star rating component
        star_rating = BoxLayout(orientation='horizontal', spacing=10)
        self.stars = []
        for i in range(1, 6):  # Create 5 star icons
            star_icon = MDIconButton(
                icon='star-outline',
                user_font_size='48sp',
                on_release=lambda x, rating=i: self.submit_rating(rating)  # Handle star click
            )
            star_rating.add_widget(star_icon)
            self.stars.append(star_icon)

        # Add the star rating to the main layout
        main_layout.add_widget(star_rating)

        # Add a submit button
        submit_button = MDRaisedButton(
            text="Submit",
            pos_hint={'center_x': 0.5},
            on_release=lambda x: self.submit_rating_final()
        )
        main_layout.add_widget(submit_button)

        self.rating_screen.add_widget(main_layout)

        self.main_layout.clear_widgets()  # Clear the main layout
        self.main_layout.add_widget(self.rating_screen)  # Add the rating screen

    def submit_rating(self, rating):
        # Handle rating submission (e.g., save to database or show a message)
        print(f"User rated: {rating} stars")
        
        # Update the star icons based on the selected rating
        for idx, star_icon in enumerate(self.stars, start=1):
            if idx <= rating:
                star_icon.icon = 'star'
            else:
                star_icon.icon = 'star-outline'

    def submit_rating_final(self):
        # Logic for final rating submission (e.g., save to database, show thank you message)
        print("Rating submitted")
        # Here you can add additional logic for what happens after the rating is submitted


    def goto_logout(self):
        # Implement your logout logic here
        self.on_login()
    
    def analyzer_create_section(self, title, description, button_text, button_callback):
        section_layout = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(300, 200),
            padding=(20, 20, 20, 20),
            spacing=10,
            pos_hint={'center_x': 0.5,'top':0.7}
        )

        title_label = MDLabel(
            text=title,
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint=(1, None),
            height=dp(40),
            font_size=20
        )
        section_layout.add_widget(title_label)

        description_label = MDLabel(
            text=description,
            halign='center',
            theme_text_color='Secondary',
            font_style='Body1',
            size_hint=(1, None),
            height=dp(60),
            font_size=14
        )
        section_layout.add_widget(description_label)

        button = MDRaisedButton(
            text=button_text,
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5},
            on_release=button_callback
        )
        section_layout.add_widget(button)

        return section_layout 

    def budget_create_section(self, title, description, button_text, button_callback):
        section_layout = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(300, 200),
            padding=(20, 20, 20, 20),
            spacing=10,
            pos_hint={'center_x': 0.5,'top':0.4}
        )

        title_label = MDLabel(
            text=title,
            halign='center',
            theme_text_color='Primary',
            font_style='H5',
            size_hint=(1, None),
            height=dp(40),
            font_size=20
        )
        section_layout.add_widget(title_label)

        description_label = MDLabel(
            text=description,
            halign='center',
            theme_text_color='Secondary',
            font_style='Body1',
            size_hint=(1, None),
            height=dp(60),
            font_size=14
        )
        section_layout.add_widget(description_label)

        button = MDRaisedButton(
            text=button_text,
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5},
            on_release=button_callback
        )
        section_layout.add_widget(button)

        return section_layout

    def start_analyzing(self, _):
        self.expense_analyzer_screen = ExpenseAnalyzerScreen(name='expense_analyzer')
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.expense_analyzer_screen)

    def plan_budget(self, _):
        self.budget_planner_screen = BudgetPlannerScreen(name='budget_planner')
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.budget_planner_screen)
    
     
    def on_login(self, _):
        self.login_screen = Screen(name='login')
        
        # Create a BoxLayout for login inputs
        login_box = BoxLayout(orientation='vertical', padding=40, spacing=20, 
                              size_hint=(None, None), size=(400, 300), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        # Add text fields for username and password
        self.login_username_field = MDTextField(
            hint_text='Enter username',
            required=True,
            helper_text_mode='on_focus'
        )
        login_box.add_widget(self.login_username_field)
        
        self.login_password_field = MDTextField(
            hint_text='Enter password',
            required=True,
            helper_text_mode='on_focus',
            password=True
        )
        login_box.add_widget(self.login_password_field)
        
        # Add a login button
        login_button = MDRaisedButton(
            text='Login',
            size_hint=(None, None),
            width=200,
            height=50,
            on_release=self.validate_login
        )
        login_box.add_widget(login_button)

        self.login_screen.add_widget(login_box)
        self.main_layout.clear_widgets()  # Remove main screen widgets
        self.main_layout.add_widget(self.login_screen)  # Add login screen

    def validate_login(self, _):
        username = self.login_username_field.text.strip()
        password = self.login_password_field.text.strip()
        
        # Simulate loading spinner
        self.show_loading_spinner()
        
        # Simulate delay before checking login credentials (replace with actual logic)
        Clock.schedule_once(lambda dt: self.check_and_navigate(username, password), 2)

    def check_and_navigate(self, username, password):
        # Simulate login validation (replace with actual login logic)
        if self.check_login(username, password):
            self.hide_loading_spinner()
            self.show_home_screen()
        else:
            self.hide_loading_spinner()
            Snackbar(text="Invalid username or password.").show()

    def check_login(self, username, password):
        # Simulate login check (replace with actual database validation)
        collection = get_db_collection()
        query = {'username': username, 'password': password}
        result = collection.find_one(query)
        return result is not None

    def hide_loading_spinner(self):
        # Function to hide the loading spinner
        if hasattr(self, 'spinner'):
            self.main_layout.remove_widget(self.spinner)           

if __name__ == '__main__':
    print("Running the app...")
    BFAS().run()

