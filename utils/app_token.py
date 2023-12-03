import jwt


class AppToken:
    """
    using symmetric shared secret for jwt. Having such a short secret is not secure
    but doesn't make a difference in this context
    """

    SECRET = 'sdflkdfsjflkes23084ip423k23öl423423+'

    def create(self, payload) -> str:
        """

        :param payload: dict containing jwt payload (booking_reference)
        :return: str jwt token containing booking_reference
        """

        return jwt.encode(payload, AppToken.SECRET, algorithm='HS512')

    def validate(self, _token_str):
        """

        :param _token_str: encoded token
        :return: decoded payload containing booking_reference
        """

        return jwt.decode(_token_str, AppToken.SECRET, algorithms=['HS512'])
