class SearchCache:
    def __init__(self):
        self.search_data_dict = {}

    def add_new_queue(self, user_id: int, queue: list):
        self.search_data_dict.update({user_id: SearchData(queue)})

    def pop_queue(self, user_id):
        if user_id in self.search_data_dict:
            search_data = self.search_data_dict[user_id]
            data = search_data.queue.pop(0)
            if isinstance(data, int):
                search_data.last_user = data
            else:
                search_data.last_user = data.user_id
            return data
        return None

    def get_last_user(self, user_id):
        if user_id in self.search_data_dict:
            return self.search_data_dict[user_id].last_user
        return None

    def check_if_not_empty(self, user_id):
        return (
            user_id in self.search_data_dict
            and len(self.search_data_dict[user_id].queue) > 0
        )


class SearchData:
    def __init__(self, queue: list):
        self.queue = queue
        self.last_user = None
