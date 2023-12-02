import jwt


class AppToken:
    SECRET = 'sdflkdfsjflkes23084ip423k23öl423423+'

    def create(self, payload) -> str:
        return jwt.encode(payload, AppToken.SECRET, algorithm='HS512')

    def validate(self, _token_str):
        return jwt.decode(_token_str, AppToken.SECRET, algorithms=['HS512'])


