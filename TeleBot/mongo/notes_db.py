from TeleBot.mongo import db

notesdb = db.notes


async def save_note(chat_id, note_name, content, text, data_type):
    note_data = {
        'note_name': note_name,
        'content': content,
        'text': text,
        'data_type': data_type
    }

    existing_note = await notesdb.find_one({'chat_id': chat_id, 'notes.note_name': note_name})
    if existing_note:
        return 
    else:
        await notesdb.update_one(
            {'chat_id': chat_id},
            {'$push': {'notes': note_data}},
            upsert=True
        )


async def clear_note(chat_id, note_name):
    result = await notesdb.update_one(
        {'chat_id': chat_id},
        {'$pull': {'notes': {'note_name': note_name}}}
    )
    return result.modified_count > 0


async def get_notes_list(chat_id):
    note_list = await notesdb.find_one({'chat_id': chat_id}, {'_id': 0, 'notes.note_name': 1})
    if note_list:
        notes = note_list.get('notes', [])
        return [note.get('note_name') for note in notes]
    else:
        return []

async def remove_all_notes(chat_id: int) -> bool:
    await notesdb.update_one(
        {'chat_id': chat_id},
        {'$unset': {'notes': ''}},
    )


async def is_note_exist(chat_id, note_name):
    existing_note = await notesdb.find_one({'chat_id': chat_id, 'notes.note_name': note_name})
    x = True if existing_note  else False
    return x


async def get_note_data(chat_id, note_name):
    note_data = await notesdb.find_one(
        {'chat_id': chat_id, 'notes.note_name': note_name},
        {'_id': 0, 'notes.$': 1}
    )
    if note_data:
        note = note_data['notes'][0]
        content = note.get('content')
        text = note.get('text')
        data_type = note.get('data_type')
        return content, text, data_type
    else:
        return None, None, None