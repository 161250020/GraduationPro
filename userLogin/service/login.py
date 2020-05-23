from userLogin.dao.user import User


class Login:
    @staticmethod
    def userLogin(email, password):
        data = User.userLogin(email)

        loginResult = 'true'
        isManager = 'false'
        if data is None:
            loginResult = '该用户不存在！'
        else:
            if data['password'] != password:
                loginResult = '密码错误！'
            else:
                if data['isManager'] != 'false':
                    isManager = 'true'
        return loginResult, isManager
