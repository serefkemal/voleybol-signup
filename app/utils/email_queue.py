# app/utils/email_queue.py
from queue import Queue
import threading
import time
from flask_mail import Message
from jinja2 import Template

class EmailQueue:
    def __init__(self, app, mail):
        self.queue = Queue()
        self.app = app
        self.mail = mail
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()
    
    def add_to_queue(self, template_name, recipient, **kwargs):
        self.queue.put({
            'template': template_name,
            'recipient': recipient,
            'kwargs': kwargs
        })
    
    def _process_queue(self):
        while True:
            try:
                if not self.queue.empty():
                    email_data = self.queue.get()
                    with self.app.app_context():
                        self._send_email(
                            email_data['template'],
                            email_data['recipient'],
                            **email_data['kwargs']
                        )
                time.sleep(1)  # Prevent CPU overuse
            except Exception as e:
                self.app.logger.error(f"Error processing email queue: {str(e)}")

    def _send_email(self, template_name, recipient, **kwargs):
        try:
            template = EMAIL_TEMPLATES[template_name]
            subject = Template(template['subject']).render(**kwargs)
            body = Template(template['body']).render(**kwargs)
            
            msg = Message(
                subject=subject,
                recipients=[recipient],
                body=body
            )
            self.mail.send(msg)
            self.app.logger.info(f"Email sent to {recipient}: {template_name}")
        except Exception as e:
            self.app.logger.error(f"Failed to send email to {recipient}: {str(e)}")
