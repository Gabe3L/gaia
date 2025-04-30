from apis.offline import note

class NoteHandler:
    def handle(self, user_command: dict, speaker):
        note.write_note(user_command.get("text"))
        speaker.speak("Note saved.")