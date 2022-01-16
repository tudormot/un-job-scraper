


class AutomationInterface:
    def get_html_from_url(self, url:str, drop_consent_button:bool=True)->str:
        raise "this should be overriden by actual automation implementation"

    def get_url_after_button_press(self, initial_url,
                                   button_id='more-info-button') -> str:
        raise "this should be overriden by actual automation implemenation"