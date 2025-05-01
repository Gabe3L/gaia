class CommandConfig:
    COMMAND_CONFIDENCE_THRESHOLD: float = 0.2

    GREETINGS = {"hello gaia", "hey gaia", "gaia",
             "wake up gaia", "you there gaia", "time to work gaia"}
    GREETING_RESPONSES = [
        "Always there for you, sir.",
        "I am ready, sir.",
        "Your wish is my command.",
        "How can I help you, sir?",
        "I am online and ready, sir."
    ]

    CALENDAR_COMMANDS = {"what do i have", "do i have plans", "am i busy"}
    MUSIC_COMMANDS = {"play music", "hit some music"}
    LOCATION_COMMANDS = {"where am i", "current location", "where i am"}
    SHUTDOWN_COMMANDS = {"goodbye", "offline", "bye"}
    NOTE_COMMANDS = {"take a note", "write this"}
    FILLER_WORDS = {"please", "can you", "could you",
                    "would you", "hey", "gaia", "tell me", "show me"}
    
    CLASS_NAMES = [
        "greeting", "date", "time", "weather", "music", "joke", 
        "news", "note", "location", "wiki", "calendar", "system", 
        "shutdown", "website", "launch", "google", "youtube"
    ]