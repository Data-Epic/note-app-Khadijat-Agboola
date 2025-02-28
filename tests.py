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
    note = Note(content)
    result = note.display()
    assert "ID: 1" in result
    assert content in result
    assert "created at" in result


def test_textnote_display():
    content = "This is a text note display test to see if the function works properly"
    note = TextNote(content)
    result = note.display()
    assert "ID: 2" in result
    assert content in result
    assert "created at" in result

def test_remindernote_display():
    content= "This is a reminder note display test to see if the function works properly"
    reminder_date_and_time = "28-2-2025 9:00"
    reminder_note=ReminderNote(content, reminder_date_and_time)
    result = reminder_note.display()
    assert "ID: 3" in result
    assert content in result
    assert "created at" in result
    assert reminder_date_and_time in result

def test_notesmanager_add_text_note():
    manager= NotesManager()
    note_type= "text"
    content = "This is a text note display test to see if the function works properly"
    manager.add_note(note_type, content)
    assert isinstance(manager.notes[0], TextNote)


"""
Testing adding a reminder note through NotesManager.
Checks that the note is added and contains the correct reminder date.
"""
def test_notesmanager_add_reminder_note():
    manager= NotesManager()
    note_type= "reminder"
    content = "This is a reminder note display test to see if the function works properly"
    reminder_date_and_time = "28-2-2025 9:00"
    manager.add_note(note_type, content, reminder_date_and_time)
    assert isinstance(manager.notes[0], ReminderNote)
    assert manager.notes[0].content == "This is a reminder note display test to see if the function works properly"
    assert manager.notes[0].reminder_date_and_time == reminder_date_and_time
    

"""
Testing adding a note with an invalid note type.
Expects an error message and verifies that no note is added.
"""
def test_add_invalid_note():
    manager = NotesManager()
    result = manager.add_note("image", "Note of type image should not be added")
    assert result == "Please choose a note type"
    assert len(manager.notes) == 0  # To confirm the note was not stored in the note manager. That is the number of notes should be zero

"""
Testing deleting an existing note.
Uses capsys to capture printed output and verifies the deletion message.
"""
def test_delete_existing_note(capsys):
    manager = NotesManager()
    manager.add_note("text", "No more negativity and procastination in my life")
    note_id = manager.notes[0].id
    manager.delete_note(note_id)
    captured = capsys.readouterr().out
    assert len(manager.notes) == 0  # To confirm the note has been deleted
    assert f"Note with ID {note_id} has been deleted" in captured


"""
Testing attempting to delete a note that does not exist.
Captures output to verify that the appropriate message is printed.
"""
def test_delete_nonexisting_note(capsys):
    manager = NotesManager()
    manager.add_note("text", "This is me learning pytest")   # This ensures that there is at least one note in the NotesManager
    manager.delete_note(8)  # Using non-existing note ID
    captured = capsys.readouterr().out  #capsys is a pytest fixture that will capture output printed to the console.
    assert len(manager.notes) == 1  # To confirm the note is not deleted
    assert "No note with ID" in captured


"""
Testing the show_notes method.
Captures output and verifies that all notes are displayed.
"""
def test_show_notes(capsys):
    manager = NotesManager()
    manager.add_note("text", "This is me learning pytest")
    manager.add_note("reminder", "I must submit my task before deadline", "28-2-2025 11:59")
    manager.show_notes()
    captured = capsys.readouterr().out
    assert "This is me learning pytest" in captured
    assert "I must submit my task before deadline" in captured
    assert "28-2-2025 11:59" in captured


"""
Testing searching for notes that contain a specific keyword.
Only notes with the keyword should be displayed.
"""
def test_search_notes_found(capsys):
    manager = NotesManager()
    manager.add_note("text", "Ramadan wish list")
    manager.add_note("text", "Meeting notes")
    manager.search_notes("list")
    captured = capsys.readouterr().out
    assert "Ramadan wish list" in captured
    assert "Meeting notes" not in captured


"""
Testing searching for a keyword that is not found in any note.
Verifies that the appropriate message is printed.
"""
def test_search_notes_not_found(capsys):
    manager = NotesManager()
    manager.add_note("text", "This is a shopping list")
    manager.search_notes("Ramadan")
    captured = capsys.readouterr().out
    assert "No note contain" in captured