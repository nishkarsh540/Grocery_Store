# tasks.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import csv
from io import StringIO
from datetime import datetime
from celery_config import celery
from app import db, Product, User, Order
from celery.schedules import crontab


def calculate_total_orders(user_id):
    total_orders = Order.query.filter_by(
        user_id=user_id, status='Purchased').count()
    return total_orders


def calculate_total_expenditure(user_id):
    orders = Order.query.filter_by(user_id=user_id, status='Purchased').all()
    total_expenditure = sum(order.total for order in orders)
    return total_expenditure


@celery.task
def generate_monthly_report():
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year
    users = User.query.filter_by(role='user').all()
    for user in users:
        total_orders = calculate_total_orders(user.id)
        total_expenditure = calculate_total_expenditure(user.id)

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Monthly Activity Report</title>
        </head>
        <body>
            <h1>Monthly Activity Report - {current_month} {current_year}</h1>
            <p>Hello {user.name},</p>
            <p>Here's your activity summary for the month of {current_month} {current_year}:</p>
            <ul>
                <li>Total Orders: {total_orders}</li>
                <li>Total Expenditure: ${total_expenditure}</li>
            </ul>
            <p>Thank you for using our services!</p>
            <p>Best regards,</p>
            <p>Grocery Team</p>
        </body>
        </html>
        """
        send_email(user.email, html_content)


def send_email(to_email, html_content):
    from_email = 'nishkarshs33@gmail.com'
    subject = 'Monthly Activity Report'

    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    part1 = MIMEText(html_content, 'html')
    msg.attach(part1)

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'nishkarshs33@gmail.com'
    smtp_password = 'khsgumzsiotjbrqw'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())


@celery.task
def export_product_details_as_csv(created_user_id):
    products = Product.query.filter_by(created_user_id=created_user_id).all()

    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(["Name", "Category", "Expiry Date",
                        "Manufacture Date", "Price", "Unit", "Quantity", "Sold Quantity"])

    for product in products:
        csv_writer.writerow([
            product.name,
            product.category.name,
            str(product.expiry_date),
            str(product.manufacture_date),
            str(product.price),
            product.unit,
            str(product.quantity),
            product.sold_quantity
        ])

    base_dir = os.path.abspath(os.path.dirname(__file__))
    csv_file_path = os.path.join(base_dir, "csv/product_report.csv")
    with open(csv_file_path, 'w') as csv_file:
        csv_file.write(csv_buffer.getvalue())

    return csv_buffer.getvalue()
