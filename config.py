# Booking configurations
BOOKING_CONFIG = {
    'date': '2024-12-14',          # Format: YYYY-MM-DD
    'time': '17:00',               # Format: HH:MM (24-hour)
    'participant': 'Alex Huang',    # Participant name
    'court_type': 'indoor',        # 'indoor' or 'outdoor'
    'dry_run': True                # Set to False to enable actual bookings
}

# Time slots available for booking (for validation)
VALID_COURT_TYPES = ['indoor', 'outdoor']