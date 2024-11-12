

# Класс data для хранения и аптейда данных пользователя
class Data:
    def __init__(self):
        self.user_pic_data = ''
        self.cloth_pic_data = ''

    def update_data(self, user_pic_data='', cloth_pic_data=''):
        self.user_pic_data = user_pic_data
        self.cloth_pic_data = cloth_pic_data

    def get_data(self):
        return self.user_pic_data, self.cloth_pic_data



