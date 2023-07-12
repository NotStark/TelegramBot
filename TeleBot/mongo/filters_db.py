from TeleBot.mongo import db

filtersdb = db.filters

async def get_filters_list(chat_id: int):
    chat = await filtersdb.find_one({'chat_id': chat_id})
    if chat :
        try :
            filters_name = [filters['filter_name'] for filters in chat['filters']]
        except KeyError:
            filters_name = []
        return filters_name
    return []

async def add_filter(chat_id: int, filter_name: str, content: str, text: str, data_type: int) -> bool:
    filter_data = await filtersdb.find_one({'chat_id': chat_id})

    if not filter_data:
        await filtersdb.insert_one({
            'chat_id': chat_id,
            'filters': [{
                'filter_name': filter_name,
                'content': content,
                'text': text,
                'data_type': data_type
            }]
        })
    else:
        filters_name = await get_filters_list(chat_id)
        if filter_name not in filters_name:
            await filtersdb.update_one(
                {'chat_id': chat_id},
                {
                    '$addToSet': {
                        'filters': {
                            'filter_name': filter_name,
                            'content': content,
                            'text': text,
                            'data_type': data_type
                        }
                    }
                },
                upsert=True
            )
        else:
            await filtersdb.update_one(
                {'chat_id': chat_id, 'filters.filter_name': filter_name},
                {
                    '$set': {
                        'filters.$.filter_name': filter_name,
                        'filters.$.content': content,
                        'filters.$.text': text,
                        'filters.$.data_type': data_type
                    }
                }
            )


async def stop_filter(chat_id: int, filter_name: str) -> bool:
    result = await filtersdb.update_one(
        {'chat_id': chat_id},
        {'$pull': {'filters': {'filter_name': filter_name}}},
    )
    return result.modified_count > 0

async def remove_all_filters(chat_id: int) -> bool:
    await filtersdb.update_one(
        {'chat_id': chat_id},
        {'$unset': {'filters': ''}},
    )

async def get_filter(chat_id: int, filter_name: str) :
    filter_data = await filtersdb.find_one(
        {'chat_id': chat_id, 'filters.filter_name': filter_name},
        {'filters.$': 1}
    )
    if filter_data:
        return filter_data['filters'][0]
    else:
        return None