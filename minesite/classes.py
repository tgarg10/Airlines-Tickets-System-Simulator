class verify:
    def __init__(self, username = '', password = '', name = '', confirmpassword='', email='', fromplace ='',toplace=''):
        self.username = username
        self.password = password
        self.name = name
        self.confirmpassword = confirmpassword
        self.email = email
        self.fromplace = fromplace
        self.toplace = toplace
        self.errors = []
    def r_name(self):
        if self.name == "":
            self.errors += ["Enter a Name."]
        elif not self.name.isalpha():
            if  " " not in self.name:
                self.errors += ["Enter a valid Name"]
        elif len(self.name)>32:
            self.errors += ["Maximum Length for Names: 32"]
        else:
            pass
    def r_username(self):
        if self.username == "":
            self.errors += ["Enter a Username."]
        elif not self.username.isalnum():
            self.errors += ["Enter a valid Username"]
        elif len(self.username)>32:
            self.errors += ["Maximum Length for Usernames: 32"]
        else:
            pass
    def r_password(self):
        if self.password == "":
            self.errors += ["Enter a Password."]
        elif len(self.password)>32:
            self.errors += ["Maximum Length for Passwords: 32"]
        else:
            pass
    def r_confirmpassword(self):
        if self.confirmpassword == "":
            self.errors += ["Confirm Password"]
        elif self.password != self.confirmpassword:
            self.errors += ["Passwords don't match!"]
        else:
            pass
    def r_email(self):
        if len(self.email)>32:
            self.errors += ["Maximum Length for Passwords: 32"]

    def r_fromplace(self):
        if self.fromplace == "":
            self.errors += ["Enter Country of Departure"]
        elif not self.fromplace.isalpha():
            if  " " not in self.fromplace:
                self.errors += ["Enter a valid Departure Country"]
        elif len(self.fromplace)>32:
            self.errors += ["Maximum Length for Departure Country: 32"]
        else:
            pass

    def r_toplace(self):
        if self.toplace == "":
            self.errors += ["Enter Country of Arrival"]
        elif not self.toplace.isalpha():
            if  " " not in self.toplace:
                self.errors += ["Enter a valid Arrival Country"]
        elif len(self.toplace)>32:
            self.errors += ["Maximum Length for Arrival Country: 32"]
        else:
            pass

    def r_errors(self):
        return self.errors

