import pandas as pd
import matplotlib.pyplot as plt
import io
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
import spacy
import openpyxl

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define TransactionCategorizer and its subclasses for different banks
class TransactionCategorizer:
    def __init__(self, detail):
        self.detail = detail.lower()

    def categorize(self):
        raise NotImplementedError("This method should be overridden by subclasses")

class StateBankOfIndiaCategorizer(TransactionCategorizer):
    def categorize(self):
        doc = nlp(self.detail)
        food_keywords = ["zomato", "swiggy", "ubereats", "foodpanda", "dominos", "mcdonalds", "pizza hut", "starbucks", "cafe coffee day"]
        travel_keywords = ["irctc", "makemytrip", "goibibo", "ola", "uber", "redbus", "yatra", "cleartrip", "airasia", "indigo", "spicejet", "vistara", "jetairways"]
        fundtransfer_keywords = ["neft", "rtgs", "imps", "upi", "transfer", "txn", "payment"]
        merchant_keywords = ["paytm", "amazon", "flipkart", "myntra", "snapdeal", "shopclues", "ebay", "jabong", "tatacliq", "bigbasket", "grofers", "reliance fresh", "more"]

        if any(token.text.lower() in food_keywords for token in doc):
            return "Food"
        elif any(token.text.lower() in travel_keywords for token in doc):
            return "Travel"
        elif any(token.text.lower() in fundtransfer_keywords for token in doc):
            return "Fund Transfer"
        elif any(token.text.lower() in merchant_keywords for token in doc):
            return "Shopping"
        else:
            return "Other"

class ICICIBankCategorizer(TransactionCategorizer):
    def categorize(self):
        doc = nlp(self.detail)
        food_keywords = ["zomato", "swiggy", "ubereats", "foodpanda", "dominos", "mcdonalds", "pizza hut", "starbucks", "cafe coffee day"]
        travel_keywords = ["irctc", "makemytrip", "goibibo", "ola", "uber", "redbus", "yatra", "cleartrip", "airasia", "indigo", "spicejet", "vistara", "jetairways"]
        fundtransfer_keywords = ["neft", "rtgs", "imps", "upi", "transfer", "txn", "payment"]
        merchant_keywords = ["paytm", "amazon", "flipkart", "myntra", "snapdeal", "shopclues", "ebay", "jabong", "tatacliq", "bigbasket", "grofers", "reliance fresh", "more"]

        if any(token.text.lower() in food_keywords for token in doc):
            return "Food"
        elif any(token.text.lower() in travel_keywords for token in doc):
            return "Travel"
        elif any(token.text.lower() in fundtransfer_keywords for token in doc):
            return "Fund Transfer"
        elif any(token.text.lower() in merchant_keywords for token in doc):
            return "Shopping"
        else:
            return "Other"

class KOTAKBankCategorizer(TransactionCategorizer):
    def categorize(self):
        doc = nlp(self.detail)
        food_keywords = ["zomato", "swiggy", "ubereats", "foodpanda", "dominos", "mcdonalds", "pizza hut", "starbucks", "cafe coffee day"]
        travel_keywords = ["irctc", "makemytrip", "goibibo", "ola", "uber", "redbus", "yatra", "cleartrip", "airasia", "indigo", "spicejet", "vistara", "jetairways"]
        fundtransfer_keywords = ["neft", "rtgs", "imps", "upi", "transfer", "txn", "payment"]
        merchant_keywords = ["paytm", "amazon", "flipkart", "myntra", "snapdeal", "shopclues", "ebay", "jabong", "tatacliq", "bigbasket", "grofers", "reliance fresh", "more"]

        if any(token.text.lower() in food_keywords for token in doc):
            return "Food"
        elif any(token.text.lower() in travel_keywords for token in doc):
            return "Travel"
        elif any(token.text.lower() in fundtransfer_keywords for token in doc):
            return "Fund Transfer"
        elif any(token.text.lower() in merchant_keywords for token in doc):
            return "Shopping"
        else:
            return "Other"

# Helper function to generate a pie chart with a legend including percentages
def generate_pie_chart_with_legend(df, category_column):
    category_counts = df[category_column].value_counts()
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        category_counts,
        labels=category_counts.index,
        autopct='%1.1f%%',
        startangle=90
    )
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Prepare legend labels with category names and percentages
    legend_labels = [f'{name} ({percent:.1f}%)' for name, percent in zip(category_counts.index, category_counts / category_counts.sum() * 100)]

    # Add legend below the pie chart
    plt.legend(
        wedges,
        legend_labels,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )

    # Adjust the size of the plot to make space for the legend
    fig.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

# Main screen class
class ExpenseAnalyzerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.result_label = Label(
            text="Upload an Excel file to categorize transactions. Supported formats: .xlsx",
            halign="center", size_hint=(1, 0.1), pos_hint={"center_y": 0.9},
            color=(0, 0, 0, 1)  # Black text color
        )
        self.layout.add_widget(self.result_label)

        self.bank_selector = MDTextField(
            hint_text="Select Bank",
            pos_hint={"center_x": 0.5, "top": 0.4},
            size_hint=(None, None),
            size=(200, 44)
        )
        self.layout.add_widget(self.bank_selector)

        bank_names = ["State Bank of India", "ICICI Bank", "HDFC Bank", "Axis Bank", "Kotak Mahindra Bank", 
                      "IndusInd Bank", "Yes Bank", "Punjab National Bank", "Bank of Baroda", "Canara Bank"]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": bank,
                "height": 44,
                "on_release": lambda x=bank: self.set_bank(x),
            } for bank in bank_names
        ]
        self.menu = MDDropdownMenu(
            caller=self.bank_selector,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.bank_selector.bind(focus=self.on_bank_selector_focus)

        excel_button = MDRaisedButton(
            text="Upload Statement in Excel",
            pos_hint={"center_x": 0.5, "top": 0.5},
            md_bg_color=get_color_from_hex('#4a148c'),
            text_color=(1, 1, 1, 1),  # White text color
            on_release=self.open_file_manager
        )
        
        self.layout.add_widget(excel_button)

        self.spinner = MDSpinner(size_hint=(None, None), size=(50, 50), active=False)
        self.layout.add_widget(self.spinner)

        self.note_label = Label(
            text="Supported banks: State Bank of India, ICICI Bank, HDFC Bank, Kotak Mahindra Bank, etc.",
            halign="center", size_hint=(1, 0.1), pos_hint={"center_y": 0.9},
            color=(0, 0, 0, 1)  # Black text color
        )
        self.layout.add_widget(self.note_label)

        self.pie_chart_image = Image(size_hint=(1, 0.5))
        self.layout.add_widget(self.pie_chart_image)

        self.tips_label = Label(
            text="",
            halign="center", size_hint=(1, 0.1),
            color=(0, 0, 0, 1)  # Black text color
        )
        self.layout.add_widget(self.tips_label)

        self.add_widget(self.layout)

    def on_bank_selector_focus(self, _, value):
        if value:
            self.menu.open()

    def set_bank(self, bank_name):
        self.bank_selector.text = bank_name
        self.menu.dismiss()

    def open_file_manager(self, instance):
        self.file_manager_open('excel')

    def file_manager_open(self, file_type):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_file
        )
        self.file_manager.show('/')
        self.file_type = file_type

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_file(self, path):
        self.exit_manager()
        self.spinner.active = True
        self.process_file(path, self.file_type)

    def generate_tips(self, category_counts):
        tips = {
            "Food": "Consider cooking more at home to save on dining out expenses.",
            "Travel": "Look for travel deals and plan your trips during off-peak times.",
            "Shopping": "Create a budget for shopping and stick to it to avoid overspending.",
            "Fund Transfer": "Review your fund transfers to ensure they are necessary and avoid unnecessary fees.",
            "Other": "Review your spending patterns and identify areas where you can cut back."
        }
        most_common_category = category_counts.idxmax()
        return tips.get(most_common_category, "Review your expenses to find savings opportunities.")

    def process_file(self, path, file_type):
        selected_bank = self.bank_selector.text
        
        if not selected_bank:
            self.result_label.text = "Please select a bank."
            self.spinner.active = False
            return

        try:
            if file_type == 'excel':
                if selected_bank == "Kotak Mahindra Bank":
                    dfs = pd.read_excel(path, skiprows=13, skipfooter=4, sheet_name=None)
                    sheet_name = list(dfs.keys())[0]
                    df = dfs[sheet_name]

                    possible_columns = ["Details", "Transaction Details", "Transaction", "Description"]
                    for col in possible_columns:
                        if col in df.columns:
                            df.rename(columns={col: "Details"}, inplace=True)
                            break
                    else:
                        self.result_label.text = "No transaction details column found. Ensure the file format matches the expected layout."
                        self.spinner.active = False
                        return

                    df['Category'] = df['Details'].apply(lambda x: KOTAKBankCategorizer(x).categorize())

                    category_counts = df['Category'].value_counts()
                    chart_buf = generate_pie_chart_with_legend(df, 'Category')
                    pie_chart_image = CoreImage(chart_buf, ext='png')
                    self.pie_chart_image.texture = pie_chart_image.texture

                    # Generate and display tips
                    tips = self.generate_tips(category_counts)
                    self.tips_label.text = f"Money-Saving Tip: {tips}"

                    self.result_label.text = "File processed successfully. Check the pie chart for categorization."

                else:
                    self.result_label.text = f"Functionality for {selected_bank} not implemented yet. Please select a supported bank."
                
            else:
                self.result_label.text = "Unsupported file type. Please upload an Excel file."

        except FileNotFoundError:
            self.result_label.text = "File not found. Please try again or check the file path."
            print("File not found error.")
        except pd.errors.EmptyDataError:
            self.result_label.text = "The file is empty or not readable. Please check the file content."
            print("Empty data error.")
        except pd.errors.ParserError:
            self.result_label.text = "Error parsing the file. Please check the file format."
            print("Parsing error.")
        except Exception as e:
            self.result_label.text = f"An unexpected error occurred: {e}. Please check the file and try again."
            print(f"Unexpected error: {e}")

        finally:
            self.spinner.active = False
