import pytest
import datetime
from note import Note
from note import ReminderNote
from note import NotesManager
from note import TextNote

'''Testing the 'display' feature of the Base class- Note 
    I will use 'assert' to confirm the display function actually include ID, content and time created 
'''

def test_note_display():
    content = "This is a display test to see if the function works properly"
    note = Note(content)    #getting an instance of class Note
    result = note.display()     #using the display method
    assert "ID: 1" in result        #confirming an ID of 1 is assigned 
    assert content in result        #to confirm the content is in result
    assert "created at" in result


def test_textnote_display():
    content = "This is a text note display test to see if the function works properly"
    note = TextNote(content)        #an instance of TextNote
    result = note.display()     #saving the display method of note as result
    assert "ID: 2" in result        # confirming an ID of 2 is assigned 
    assert content in result        #to confirm the content is in result
    assert "created at" in result       #to confirm created at is in result

def test_remindernote_display():        # testin the display of the reminder note
    content= "This is a reminder note display test to see if the function works properly"
    reminder_date_and_time = "28-2-2025 9:00"
    reminder_note=ReminderNote(content, reminder_date_and_time)     #reminder note takes two attributes
    result = reminder_note.display()        # saving the display method of note as result
    assert "ID: 3" in result        # confirming an ID of 3 is assigned 
    assert content in result        #to confirm the content is in result
    assert "created at" in result
    assert reminder_date_and_time in result

def test_notesmanager_add_text_note():      # testing the add_note method for text notes
    manager= NotesManager()     #an instance of the NoteManager
    note_type= "text"
    content = "This is a text note display test to see if the function works properly"
    manager.add_note(note_type, content)        #using the add_note method to add the note type and the content
    assert isinstance(manager.notes[0], TextNote)       # to confirm the added note is an instance of TextNote


"""
Testing adding a reminder note through NotesManager.
Checks that the note is added and contains the correct reminder date.
"""
def test_notesmanager_add_reminder_note():      # testing the add_note method for reminder notes
    manager= NotesManager()     #an instance of the NoteManager
    note_type= "reminder"       # the type of note to be added
    content = "This is a reminder note display test to see if the function works properly"
    reminder_date_and_time = "28-2-2025 9:00"
    manager.add_note(note_type, content, reminder_date_and_time)        #using the add_note method to add the note type, the content and the reminder_date_and_time
    assert isinstance(manager.notes[0], ReminderNote)       #isistance checks if the added note is a type of the ReminderNote
    assert manager.notes[0].content == "This is a reminder note display test to see if the function works properly"
    assert manager.notes[0].reminder_date_and_time == reminder_date_and_time
    

"""
Testing adding a note with an invalid note type.
Expects an error message and verifies that no note is added.
"""
def test_add_invalid_note():        #to add a note not of type 'text' or 'reminder'
    manager = NotesManager()
    lenght= len(manager.notes)      #to check the previous number of notes in the note manager before adding a new note
    result = manager.add_note("image", "Note of type image should not be added")        #specifying type as 'image'
    assert result == "Please choose a note type"        #the expected result is 'Please choose a note type'
    assert len(manager.notes) == lenght  # To confirm the note was not stored in the note manager. The number of notes should be the same

"""
Testing deleting an existing note.
Uses capsys to capture printed output and verifies the deletion message.
"""
def test_delete_existing_note(capsys):      # to delete note 
    manager = NotesManager()
    lenght= len(manager.notes)      #to check the previous number of notes in the note manager before adding a new note
    manager.add_note("text", "No more negativity and procastination in my life")
    note_id = manager.notes[0].id       #the id of the note we intend to delete
    manager.delete_note(note_id)        # the delete_note method
    captured = capsys.readouterr().out      #capsys is a pytest fixture that will capture output printed to the console.
    assert len(manager.notes) == lenght  # To confirm the note has been deleted and the lenght remains the same as before adding the note
    assert f"Note with ID {note_id} has been deleted" in captured      #to confirm the successful delete message is printed in the console


"""
Testing attempting to delete a note that does not exist.
Captures output to verify that the appropriate message is printed.
"""
def test_delete_nonexisting_note(capsys):   # deleteing a note with non existing ID
    manager = NotesManager()
    manager.add_note("text", "This is me learning pytest")   # This ensures that there is at least one note in the NotesManager
    lenght= len(manager.notes)
    manager.delete_note(8)  # Using non-existing note ID
    captured = capsys.readouterr().out  #capsys is a pytest fixture that will capture output printed to the console.
    assert len(manager.notes) == lenght  # To confirm the note is not deleted
    assert "No note with ID" in captured        #to confirm the unsuccesful delete message is printed in the console


"""
Testing the show_notes method.
Captures output and verifies that all notes are displayed.
"""
def test_show_notes(capsys):        # testing the show_notes method
    manager = NotesManager()
    manager.add_note("text", "This is me learning pytest")      #added a text note
    manager.add_note("reminder", "I must submit my task before deadline", "28-2-2025 11:59")        #added a reminder note
    manager.show_notes()        #calling the show notes method
    captured = capsys.readouterr().out
    assert "This is me learning pytest" in captured     # to confirm the first note is printed on console
    assert "I must submit my task before deadline" in captured      # to confirm the second note is printed on the console
    assert "28-2-2025 11:59" in captured        # to confirm the reminder_date_and_time is on the console


"""
Testing searching for notes that contain a specific keyword.
Only notes with the keyword should be displayed.
"""
def test_search_notes_found(capsys):        # testing the search note method using existing keyword
    manager = NotesManager()
    manager.add_note("text", "Ramadan wish list")       # added a note
    manager.add_note("text", "Meeting notes")       # added another note
    manager.search_notes("list")        # searching for the keyword 'list'
    captured = capsys.readouterr().out
    assert "Ramadan wish list" in captured      # to confirm it brought the note containing keyword
    assert "Meeting notes" not in captured      # to confirm it doesn't bring a stored note not containing keyword


"""
Testing searching for a keyword that is not found in any note.
Verifies that the appropriate message is printed.
"""
def test_search_notes_not_found(capsys):        # testing the search note method using non-existing keyword
    manager = NotesManager()
    manager.add_note("text", "This is a shopping list")     # added a note
    manager.search_notes("Ramadan")     # searching for non-existing keyword
    captured = capsys.readouterr().out
    assert "No note contain" in captured        # to confirm unsuccesful search note message is printed