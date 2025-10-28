# dasapp/management/commands/send_reminders.py

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from dasapp.models import Appointment 

class Command(BaseCommand):
    help = 'Send appointment reminders 15 minutes before appointment time'

    def handle(self, *args, **kwargs):
        now = datetime.now()

        # Time window: appointments happening in 14–16 minutes
        start_time = now + timedelta(minutes=14)
        end_time = now + timedelta(minutes=16)

        upcoming_appointments = Appointment.objects.filter(
            date_of_appointment=start_time.date(),
            time_of_appointment__gte=start_time.time(),
            time_of_appointment__lte=end_time.time(),
            reminder_sent=False
        )

        count = 0
        for appointment in upcoming_appointments:
            try:
                doctor_name = f"Dr. {appointment.doctor_id.admin.first_name} {appointment.doctor_id.admin.last_name}"

                reminder_message = f"""
Dear {appointment.fullname},

⏰ URGENT REMINDER: YOUR APPOINTMENT IS IN 15 MINUTES!

Appointment Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Appointment Number: {appointment.appointmentnumber}
👨‍⚕️ Doctor: {doctor_name}
🏥 Specialization: {appointment.doctor_id.specialization_id.sname}
📅 Date: TODAY - {appointment.date_of_appointment}
🕐 Time: {appointment.time_of_appointment}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 PLEASE START COMING NOW!

Don't forget to bring:
All medical documents and reports
ID proof
Previous prescriptions

See you soon!
Hospital Management Team
"""

                send_mail(
                    subject=f'⏰ Appointment Reminder - {appointment.time_of_appointment}',
                    message=reminder_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[appointment.email],
                    fail_silently=False,
                )

                appointment.reminder_sent = True
                appointment.save()

                count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Reminder sent to {appointment.fullname}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Failed to send reminder to {appointment.fullname}: {e}'))

        if count == 0:
            self.stdout.write(self.style.WARNING('No reminders to send at this time.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ Successfully sent {count} reminder(s)'))
