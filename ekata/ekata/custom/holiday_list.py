# import frappe
# from datetime import datetime, timedelta
# from frappe.model.document import Document


# @frappe.whitelist()
# def send_notifications_mail():
#     subject = f"Reminder:  test mail"
#     recipients = "priyanka.d@indictranstech.com"
#     message = "Dear Priyanka! This is test email "
#     print("\n\n subject--",subject,"\n message--",message,"\n\n recipients--",recipients)
#     frappe.sendmail(recipients=recipients, subject=subject, message=message)



import frappe
from datetime import datetime, timedelta
from frappe.model.document import Document


@frappe.whitelist()
def send_notifications_mail():
    # frappe.sendmail("priyanka.d@indictranstech.com","test_mail","HELLO")
    current_date = datetime.now().date()
    target_date = current_date + timedelta(days=1)
    
    holiday_dt = frappe.db.sql(""" SELECT  h.holiday_date,h.description 
        FROM `tabHoliday List` hl, `tabHoliday` h 
                    WHERE h.parent = hl.name and hl.send_daily_reminder = 1 """,as_dict=1)

    emp_list = frappe.db.get_list('Employee',filters=[["status","=","Active"],["user_id","is","set"]],fields =['prefered_email','employee_name','user_id'])
    # print("\n\nemp_list--",emp_list)
    for emp in emp_list:
        emp_role = frappe.get_roles(emp['user_id'])
        if 'Bank Holiday User' in emp_role:
            print("\n\nemp_role --",emp_role)
            print("\n\n in Bank Holiday User--")
            for holiday in holiday_dt:
                if holiday.holiday_date == target_date:
                    subject = f"Reminder:  '{holiday['description']}' is tomorrow"
                    recipients = emp['prefered_email']

                    message = f"""Dear {emp['employee_name']}! This email is to remind you about the upcoming holidays.
                    \n\n Below is the list of upcoming holidays for you:\n\n\n'{holiday['description']}'"""
                    print("\n\n subject--",subject,"\n message--",message,"\n\n recipients--",recipients)
                    frappe.sendmail(recipients=recipients, subject=subject, message=message)

 
 # holiday_list = frappe.db.get_list('Holiday List',filters={'send_daily_reminder':'1'},fields=['name'])
    
# holiday_list = frappe.db.get_list('Holiday ',filters={'parent':'','holiday_date': target_date},fields=['parent','description','holiday_date'])
    # emp_list = frappe.db.get_list('Employee',filters={'status': 'Active','prefered_email':email},fields=['prefered_email','employee_name'])
    # emp_list = frappe.db.get_value('Employee',{'status': 'Active','prefered_email':email},['prefered_email','employee_name'])
   
