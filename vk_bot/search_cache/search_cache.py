class SearchCache:
    def __init__(self):
        self.search_data_dict = {}

    def add_new_queue(self, user_id: int, queue: list):
        self.search_data_dict.update({user_id: SearchData(queue)})

    def pop_queue(self, user_id):
        search_data = self.search_data_dict[user_id]
        data = search_data.queue.pop(0)
        if data is int:
            search_data.last_user = data
        else:
            search_data.last_user = data.user_id
        return data

    def get_last_user(self, user_id):
        return self.search_data_dict[user_id].last_user


class SearchData:
    def __init__(self, queue: list):
        self.queue = queue
        self.last_user = None
