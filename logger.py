from datetime import datetime
from time import timezone

class Logger:
    def __init__(self, access_log_file = './access_log.txt', error_log_file = './error_log.txt'):
        self.access_log_file = access_log_file
        self.error_log_file = error_log_file
    def formated_date(self):
        return datetime.now().strftime("%d/%b/%Y:%H:%M:%S ") + str(-timezone)
    def formated_message(self, req, res, ip):
        return "%s - - [%s] \"%s %s %s\" %s %s" % (ip, self.formated_date(), req.get_method(), req.get_path(),req.get_version(), res.get_status(), res.get_body_len())
    def formated_error(self, req, error, ip):
        return "%s - - [%s] \"%s %s %s\" ERROR: %s" % (ip, self.formated_date(),req.get_method(), req.get_path(),req.get_version() , error)
    def error_log(self, req, error, ip):
        err = self.formated_error(req, error, ip)
        with open(self.error_log_file, "a+") as f:
            f.write(err + "\r\n")
        print(err)
    def access_log(self, req, res, ip):
        msg = self.formated_message(req, res, ip)
        with open(self.access_log_file, "a+") as f:
            f.write(msg + "\r\n")
        print(msg)