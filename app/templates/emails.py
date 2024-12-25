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

