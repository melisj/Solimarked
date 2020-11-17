import jwt


class jwt_Token:
    class ServiceNotAllowed(Exception):
        pass
    

    def __init__(self, jwt, key, service, alg='HS256'):
        self.key = key
        self.alg = alg
        self.token = jwt
        self.service = service


    def check_service(self):
        try:
            token = jwt.decode(self.token, self.key, self.alg)

            if self.service not in token["sub"]:
                raise KeyError("Service not allowed")
            
            else:
                return True

        except:
            return False
        
