import datetime     #this is necessary because of the timestamp
class Note:     #the base class
    id = 1  

    def __init__(self, content):
        self.id=Note.id
        Note.id += 1
        self.content=content
        self.created_at=datetime.datetime.now()     #this adds current timestamp to each note added

    def display(self):
        return f"ID: {self.id} {self.content}\ncreated at {self.created_at}"

class TextNote(Note):       #The subclass of Note
    def __init__(self, content):
        super().__init__(content)

    def display(self):
        return f"{super().display()}"

class ReminderNote(Note):       #Subclass of Note with additional feature:reminder_date_and_time
    def __init__(self, content, reminder_date_and_time):
        super().__init__(content)       #inheriting the initiated content of Class Note
        self.reminder_date_and_time=reminder_date_and_time      #adding reminder date and time as it was not part of Class Note

    def display(self):
        return f"{super().display()}\nreminder date and time: {self.reminder_date_and_time}"    #inheriting display method of Note and additional attribute
    

class NotesManager:     #Initiating the class NotesManager
    def __init__(self):
        self.notes=[]

    def add_note(self, note_type, content, reminder_date_and_time=None):
        if note_type.lower()=="text":
            note=TextNote(content)
        elif note_type.lower()=="reminder":
            note=ReminderNote(content, reminder_date_and_time)
        else:
            return "Please choose a note type"
        self.notes.append(note)     #adding all note to notes
    
    def delete_note(self, note_id):     #defining the delete method to take note ID
        for note in self.notes:
            if note.id == note_id:
                self.notes.remove(note)
                print(f"Note with ID {note_id} has been deleted.")
            else:
                print(f"No note with ID  {note_id}")

    def show_notes(self):
        for note in self.notes:
            print(note.display())       #Using the display method defined in class "Note"
    
    def search_notes(self, keyword):
        result=[]
        for note in self.notes:
            if keyword in note.content:
                result.append(note)
            
        if not result:
            print(f"No note contain  {keyword}")
        else:
            for note in result:
                print(note.display())

#Use case
my_notes = NotesManager()

print("This is a Smart Notes Manager. \nBelow are the functions available\n1. Add note \n2. Delete note \n3. Show all notes \n4. Search all notes for a given keyword")
consent=input("Do you want to use the notes Manager? (Y/N): ")
while consent.lower()=="y":

    option = int(input("What function do you want to use? 1, 2, 3 or 4? "))
    if option ==1:
        type=input("What type of note, 'text' or 'reminder'? ")
        if type.lower()=="text":
            param=input("Type the note: ")
            my_notes.add_note("text", param)
            print("Your note has been added")
        elif type.lower()=="reminder":
            param=input("Type the note: ")
            remind=input("Enter the reminder date: ")
            my_notes.add_note("text", param, remind)
            print("Your reminder note has been added")
    elif option==2:
        my_notes.show_notes()
        param=input("Enter the ID of the note you wish to delete: ")
        my_notes.delete_note(param)

    elif option==3:
        my_notes.show_notes()

    elif option==4:
        key=input("Enter the word you wish to search for: ")
        my_notes.search_notes(key)
    else:
        print("Your input doesn't match any of the options")
        consent=input("Do you want to use the notes Manager? (Y/N): ")

print("Enjoy your day")
