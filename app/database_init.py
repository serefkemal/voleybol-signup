from app.extensions import db
from app.models import Player

def init_db():
    # Create admin users
    admins = [
        {
            'name': 'Seref',
            'email': 'serefkemal@gmail.com',
            'phone': '(536) 684 43 97',
            'password': 'serefpwd',
            'role': 'admin'
        },
        {
            'name': 'Hakan',
            'email': 'hakanemail@gmail.com',
            'phone': '(506) 538 79 25',
            'password': 'hakanpwd',
            'role': 'admin'
        },
        {
            'name': 'Eren',
            'email': 'erenemail@gmail.com',
            'phone': '(539) 518 35 04',
            'password': 'erenpwd',
            'role': 'admin'
        },
    ]

    for admin_data in admins:
        existing_admin = Player.query.filter_by(email=admin_data['email']).first()
        if not existing_admin:
            admin = Player(
                name=admin_data['name'],
                email=admin_data['email'],
                phone=admin_data['phone'],
                role='admin'
            )
            admin.set_password(admin_data['password'])
            db.session.add(admin)
    
    db.session.commit()