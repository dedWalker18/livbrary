from .models import Users
from jinja2 import Template
from celery import current_app as celery_inst
from .timestamps import *
from celery.schedules import crontab
import requests, pyshorteners, pdfkit
from .mail import *
from .monthlyreport import *

celery_inst.set_current()


@celery_inst.task()
def send_reminder():
        users = Users.query.all()
        allUserEmail = {user.username: [user.email, user.last_logged] for user in users}
        emailList = {}

        today = date_today()
        for key, value in allUserEmail.items():
            logged_date = value[1].date()
            if logged_date != today:
                emailList[key] = value[0]
                
        with open(r"templates/mailtemplates/dailyReminder.html") as file:
            temp = Template(file.read())

        for user, email_id in emailList.items():
            message = temp.render(user=user)
            sub = f"REMINDER from Livbrary"
            send_email(to=email_id, subject=sub, msg=message)
            print(f"------Reminder Sent to {user}-------")

        return "Successfull !!!"


def generate_pdf(usr, template):
    month = date_today().strftime("%B")
    file_name = f"templates/rendered_examples/monthly_report_{usr}_{month}.pdf"
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    pdfkit.from_string(template, f'{file_name}', 
                       options={"enable-local-file-access": ""}, 
                       configuration=config)
    
    return file_name


@celery_inst.task()
def monthly_report():
    users = Users.query.all()
    with open(r"templates/mailtemplates/monthlyReminder.html") as file:
        msg_temp = Template(file.read())

    with open(r"templates/mailtemplates/monthlyReport.html") as file:
        pdf_temp = Template(file.read())

    today = date_today()
    month = date_today().strftime("%B")

    done_users = []

    for user in users:
        un = user.username
        account_details = accountDetails(un)
        book_details = BookDetails(un)
        activity_details = activities(un)
        message = msg_temp.render(user=un)
        pdf_html = pdf_temp.render(today=today,
                                month=month,
                                account_details=account_details,
                                book_details=book_details,
                                username=un,
                                activity=activity_details
                                )

        sub = f"Monthly Report from Livbrary"

        if user not in done_users:
            pdf_path = generate_pdf(usr=un, template=pdf_html)
            send_email(to=user.email, subject=sub, msg=message, attachment=pdf_path)
            
            done_users.append(user)

        print(f"------MONTHLY REPORT SENT FOR {un}---------")

    return "Successfull !!!"


def generate_pdf_news(today, template):
    file_name = f"templates/rendered_examples/daily_news_{today}.pdf"
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    pdfkit.from_string(template, f'{file_name}', 
                       options={"enable-local-file-access": ""}, 
                       configuration=config)
    
    return file_name


@celery_inst.task()
def daily_news():
    api_key = ""                        ##Add Your API KEY FOR NEWS API
    resopnse = requests.get("https://newsapi.org/v2/top-headlines?country=IN&apiKey=" + api_key)
    resopnse = resopnse.json()

    articles = resopnse["articles"]
    article = []

    for each in articles:
        source = each["source"]["name"] or "Undisclosed"
        author = each["author"] or "Undisclosed"
        url = each["url"]
        short_url = pyshorteners.Shortener().tinyurl.short(url)
        article.append({
            "Source" : source,
            "Author" : author,
            "Title" : each["title"],
            "Description" : each["description"],
            "Url" : short_url,
            }
        )
    
    today = date_today()

    with open(r"templates/mailtemplates/newsHeadline_pdf.html") as file:
        pdf_temp = Template(file.read())

    pdf_html = pdf_temp.render(today = today, article = article)
    pdf_path = generate_pdf_news(today=today, template=pdf_html)

    if pdf_path:
        print(f"-----News Report Generated for {today}------")
    
    return "Successfull !!"
