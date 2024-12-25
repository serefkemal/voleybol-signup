# app/templates/emails.py
EMAIL_TEMPLATES = {
    'signup_confirmation': {
        'subject': 'Welcome to This Week\'s Volleyball Game!',
        'body': """
Hi {{ player_name }},

Thank you for signing up for this week's volleyball game!

Game Details:
📅 Date: {{ game_date }}
🕐 Time: {{ game_start_time }} - {{ game_end_time }}
📍 Location: {{ game_location }}

You are player #{{ position }} for this game.
Maximum players: {{ max_players }}

Important Notes:
- Please arrive 10 minutes early for warm-up
- Bring both dark and light colored shirts
- Don't forget to bring water

If you need to cancel, please use the cancel button on the signup page.

See you on the court!
"""
    },
    'cancellation_confirmation': {
        'subject': 'Volleyball Game Signup Cancellation',
        'body': """
Hi {{ player_name }},

Your signup for the volleyball game on {{ game_date }} has been cancelled.

We hope to see you at future games!

Best regards,
The Volleyball Team
"""
    },
    'organizer_update': {
        'subject': 'Volleyball Game: Player Update',
        'body': """
Current Player List for {{ game_date }}:

{{ player_list }}

Total Players: {{ player_count }}/{{ max_players }}

Recent Changes:
{{ recent_change }}
"""
    }
}

# Modified send_signup_notifications function for app.py
def send_signup_notifications(player, game):
    try:
        # Format game details
        game_date = game.date.strftime('%A, %B %d, %Y')
        game_start = game.start_time.strftime('%I:%M %p')
        game_end = game.end_time.strftime('%I:%M %p')
        
        # Get player position
        player_position = PlayerGameSignup.query.filter_by(
            game_id=game.id,
            is_cancelled=False
        ).count()
        
        # Queue confirmation email to player
        email_queue.add_to_queue(
            'signup_confirmation',
            player.email,
            player_name=player.name,
            game_date=game_date,
            game_start_time=game_start,
            game_end_time=game_end,
            game_location=game.location,
            position=player_position,
            max_players=app.config['MAX_PLAYERS']
        )
        
        # Queue update email to organizers
        player_list = get_player_list(game.id)
        for organizer in app.config['ORGANIZERS']:
            email_queue.add_to_queue(
                'organizer_update',
                organizer,
                game_date=game_date,
                player_list=player_list,
                player_count=player_position,
                max_players=app.config['MAX_PLAYERS'],
                recent_change=f"Added: {player.name}"
            )
            
    except Exception as e:
        app.logger.error(f"Error sending signup notifications: {str(e)}")

# Helper function to get formatted player list
def get_player_list(game_id):
    signups = PlayerGameSignup.query.filter_by(
        game_id=game_id,
        is_cancelled=False
    ).join(Player).order_by(PlayerGameSignup.signup_time).all()
    
    return "\n".join([
        f"{i+1}. {signup.player.name} ({signup.signup_time.strftime('%I:%M %p')})"
        for i, signup in enumerate(signups)
    ])

# Initialize email queue in app.py
email_queue = EmailQueue(app, mail)