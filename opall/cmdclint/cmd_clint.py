from clint.textui import prompt, puts, colored, validators
import importlib


class ErrorArgument(Exception):
    pass


class CmdClint(object):

    def __init__(self):
        self._read_conf()
        self.current_function = None
        self.pre_function = None

    def _read_conf(self):
        self._function_list = list()
        self._cmd_list = list()
        self._available_args = list()

        cmd1 = {"executable_name": "MysqlQuery",
                "executable": "MysqlQuery",
                "module": "cmdclint.cmds",
                "args": ["host_string", "password",
                         "mysql_user", "mysql_password",
                         "mysql_query_sql"]}
        self._cmd_list.append(cmd1)
        cmd1 = {"executable_name": "MysqlCreateUser",
                "executable": "MysqlCreateUser",
                "module": "cmdclint.cmds",
                "args": ["host_string", "password",
                         "mysql_user", "mysql_password",
                         "mysql_create_user_name",
                         "mysql_create_user_password", "mysql_host"]}
        self._cmd_list.append(cmd1)

        arg = {"name": "host_string",
               "description": "current remote system hostname",
               "promote": "Please enter remote system host", "promote_default": "localhost"}
        self._available_args.append(arg)

        arg = {"name": "password",
               "description": "remote system password",
               "promote": "Please enter remote system password", "promote_default": "yihan"}

        self._available_args.append(arg)
        arg = {"name": "mysql_user",
               "description": "mysql login user",
               "promote": "Please enter mysql login user",
               "promote_default": "yihan"}

        self._available_args.append(arg)
        arg = {"name": "mysql_password",
               "description": "mysql login user password",
               "promote": "Please enter mysql login user password", "promote_default": "yihan123"}

        self._available_args.append(arg)
        arg = {"name": "mysql_query_sql",
               "description": "mysql query sql",
               "promote": "Please enter mysql query sql",
               "promote_default": "select count(*) from mysql.user"}

        self._available_args.append(arg)

        fun = {"name": "test", "description": "query mysql.user table",
               "executable_name": "MysqlQuery",
               "args": [["host_string", "localhost", ""],
                        ["password", "yihan", ""],
                        ["mysql_user", "root", ""],
                        ["mysql_password", "root", ""],
                        ["mysql_query_sql", "select * from mysql.user", ""]]}

        self._function_list.append(fun)

    def _get_arg_setup(self, arg_name):
        for arg in self._available_args:
            if arg_name == arg["name"]:
                return arg
            else:
                raise ErrorArgument

    def _get_arg_value(self, arg):

        if arg[1] == "@ENTER":
            arg_setup = self._get_arg_setup(arg[0])
            val = prompt.query(
                '%s[%s]: ' % (arg_setup.promote, arg_setup.promote_default), validators=[])
            return val
        else:
            return arg[1]

    def _read(self):
        inst_options = list()
        for idx, fun in enumerate(self._function_list):
            option = dict()
            option["selector"] = str(idx)
            option["prompt"] = '%s : %s' % (fun["name"], fun["description"])
            option["return"] = fun
            inst_options.append(option)

        select_fun = prompt.options("Select a function", inst_options)

        for idx, arg in enumerate(select_fun["args"]):
            arg[2] = self._get_arg_value(arg)

        return select_fun

    def _get_executable(self, executable_name):
        for cmd in self._cmd_list:
            if cmd["executable_name"] == executable_name:
                return cmd

    def run(self):
        if self.current_function:
            cmd = self._get_executable(
                self.current_function["executable_name"])
            print cmd["executable"]

            _module = importlib.import_module(cmd["module"])
            _class = getattr(_module, cmd["executable"])
            obj = _class()

            args_dict = dict()
            for arg in self.current_function['args']:
                args_dict[arg[0]] = arg[2]

            obj.set_env(args_dict)

            print obj.env

            print obj.env_error_list

            obj.execute()

    def server_forever(self):
        while True:
            self.current_function = self._read()
            self.run()
