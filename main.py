import threading

from customtkinter import (
    set_appearance_mode,
    set_default_color_theme,
    CTk,
    CTkButton,
    CTkEntry,
    CTkLabel,
    CTkOptionMenu,
    StringVar,
    CTkScrollableFrame,
)
from utils.tools import update_config, get_udemylink
from sbase import SB

set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

category_list = [
    "All",
    "Teaching & Academics",
    "Development Business",
    "IT & Software",
    "Marketing",
    "Finance and acconting",
    "Office Productivity",
    "Business",
    "Design",
    "Personal Development",
    "Photography & Video",
    "Life Style",
    "Music",
]

app = CTk()
app.geometry("400x500")

cfg = update_config()


def clean_frame():
    """Clears the output frame!"""
    for frame in output_frame.winfo_children():
        frame.destroy()


def save_func():
    """Saves the details to config.yml!"""
    cfg = {
        "email": email_field.get(),
        "password": password_field.get(),
        "search": search_field.get(),
        "category": clicked.get(),
    }
    update_config(cfg)


def save_click():
    """Saves the details to config.yml!"""
    threading.Thread(target=save_func).start()  # To avoid freezing of GUI
    clean_frame()
    CTkLabel(
        output_frame, text="Options Saved Successfully!", justify="left"
    ).pack()  # Specify the type of pack method


def enroll_func():
    clean_frame()
    email = email_field.get()
    password = password_field.get()
    search = search_field.get()
    category = clicked.get()

    with SB(uc=True) as sb:
        enrolled = []
        already_got = 0

        sb.driver.get("https://www.udemy.com/")
        sb.click('a[data-purpose="header-login"]')
        sb.get_element('[name="email"]').send_keys(email)
        sb.get_element('[name="password"]').send_keys(password)
        sb.click('button:contains("Log in")')
        sb.sleep(1)
        if "Log In" in sb.driver.title:
            CTkLabel(
                output_frame, text="Invalid Email or Password.", justify="left"
            ).pack()
            return
        CTkLabel(output_frame, text="Logged in, Successfully...", justify="left").pack()
        CTkLabel(
            output_frame, text="Trying to enroll in courses...\n", justify="left"
        ).pack()

        for url in get_udemylink(searchby=search, category=category):
            CTkLabel(
                output_frame, text=f"Trying to enroll in {url['name']}:", justify="left"
            ).pack()
            sb.driver.open(url["url"])
            try:
                button = sb.get_element(
                    "div.sidebar-container--purchase-section--2DONZ div div div:nth-of-type(5) button"
                )
            except:
                CTkLabel(output_frame, text="Invalid URL!", justify="left").pack()
                continue

            if button.text == "Share":
                CTkLabel(output_frame, text="Already Enrolled!", justify="left").pack()

            elif button.text == "Enroll now":
                sb.driver.click(
                    "div.sidebar-container--purchase-section--2DONZ div div div:nth-of-type(5) button"
                )
                sb.driver.click(
                    "#udemy > div.ud-main-content-wrapper > div.ud-main-content > div > div > div > aside > div > div > div.marketplace-checkout--button-term-wrapper--2_M-- > div.checkout-button--checkout-button--container--RQKAM > button"
                )
                enrolled.append(url)
                CTkLabel(
                    output_frame, text="Successfully Enrolled!", justify="left"
                ).pack()
                sb.sleep(1)

            elif button.text == "Buy now":
                already_got += 1
                CTkLabel(
                    output_frame, text="Course is not free!", justify="left"
                ).pack()

        CTkLabel(
            output_frame,
            text=f"Succesfully enrolled in {len(enrolled)}\n Already Bought {already_got} courses\n Unable to get {25-already_got-len(enrolled)}",
            justify="left",
        ).pack()


def enroll_click():
    """Enrolls in the courses, using ID provided!"""
    clean_frame()
    CTkLabel(output_frame, text="Trying to Login to Udemy...", justify="left").pack()
    threading.Thread(target=enroll_func).start()  # To avoid freezing of GUI


def search_func():
    """Searches for the courses, and outputs them!"""
    courses = ""
    for index, item in enumerate(
        get_udemylink(searchby=search_field.get(), category=clicked.get())
    ):
        courses += f'{index+1}. {item["name"]}\n'
    clean_frame()
    courses_label = CTkLabel(output_frame, text=courses, justify="left")
    courses_label.pack()


def search_click():
    """Searches for the courses, and outputs them!"""
    clean_frame()
    CTkLabel(output_frame, text="Searching...", justify="left").pack()
    threading.Thread(target=search_func).start()


clicked = StringVar()  # For OptionMenu
clicked.set(cfg["category"])

# -------------------Fields-------------------#
email_field = CTkEntry(
    app,
    placeholder_text="Email",
)
if cfg["email"] != "":
    email_field.insert(0, cfg["email"])
email_field.grid(row=0, column=1, padx=20)

password_field = CTkEntry(app, placeholder_text="Password", show="*")
if cfg["password"] != "":
    password_field.insert(0, cfg["password"])
password_field.grid(row=1, column=1)

search_field = CTkEntry(
    app,
    placeholder_text="Search",
)
if cfg["search"] != "":
    search_field.insert(0, cfg["search"])
search_field.grid(
    row=2,
    column=1,
)

category_list = CTkOptionMenu(app, variable=clicked, values=category_list)
if cfg["category"] != "":
    category_list.set(cfg["category"])
category_list.grid(
    row=3,
    column=1,
)
# -------------------Buttons-------------------#
CTkButton(app, text="Save Details.", command=save_click).grid(
    row=0,
    column=2,
)

CTkButton(app, text="Enroll", command=enroll_click).grid(
    row=1,
    column=2,
)

CTkButton(app, text="🔎 Search", command=search_click).grid(
    row=2,
    column=2,
)

CTkButton(app, text="Exit", command=app.destroy, fg_color="#777777").grid(
    row=3,
    column=2,
)

# -------------------Output Frame-------------------#
output_frame = CTkScrollableFrame(
    app,
    width=400,
    height=350,
)
output_frame.grid(row=4, column=1, columnspan=2, ipadx=5, ipady=5)


app.mainloop()
