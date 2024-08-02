class BaseUrlCrowler:
    main_ulr = None
    data_get_function = None
    links_params = {}

    @classmethod
    def get_data(cls) -> dict | str:
        """
        Uses self.data_get_function function to parse self.main_ulr
        :return: dict or str of api data
        """
        return cls.data_get_function(cls.main_ulr)

    @classmethod
    def parse_links(cls) -> list:
        """
        Custom for every crouler
        :return: List of links to vacancies
        """
        pass
