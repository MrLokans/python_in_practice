import pickle


class Url(object):

    @classmethod
    def shorten(cls, long_url):
        """Shortens long url"""

        instance = cls()
        instance.long_url = long_url
        instance.short_url = instance.__create_short_url()
        Url.__save_url_mapping(instance)
        return instance

    @classmethod
    def get_by_short_url(cls, short_url):
        url_mapping = Url.load_url_mapping()
        return url_mapping.get(short_url)

    def __create_short_url(self):
        last_short_url = Url.__load_last_short_url()
        short_url = self.__increment_string(last_short_url)
        Url.__save_last_short_url(short_url)
        return short_url

    def __increment_string(self, string):
        """Increments stringm so that 'a' becomes 'b', 'az' becomes 'ba', and etc"""

        # possible unicode errors in python2?
        assert isinstance(string, str)
        if not string:
            return 'a'

        last_char = string[-1]

        if last_char != 'z':
            return string[:-1] + chr(ord(last_char) + 1)

        # elegant recursive solution
        return self.__increment_string(string[:-1] + 'a')

    @staticmethod
    def __load_last_short_url():
        try:
            return pickle.load(open("last_short_url.pickle", "rb"))
        except IOError:
            return ''

    @staticmethod
    def __save_last_short_url(url):
        pickle.dump(url, open("last_short_url.pickle", "wb"))

    @staticmethod
    def __load_url_mapping():
        try:
            return pickle.load(open("url_mapping.pickle", "rb"))
        except IOError:
            return {}

    @staticmethod
    def __save_url_mapping(instance):
        url_mapping = Url.__load_url_mapping()
        url_mapping[instance.short_url] = instance
        pickle.dump(url_mapping, open("url_mapping.pickle", "wb"))
