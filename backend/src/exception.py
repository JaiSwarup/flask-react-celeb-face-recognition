import sys
import src.logger as logging

def error_message_details(error, error_details:sys):
    _, _, exc_tb = error_details.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error in file: " + filename + "\nat line: " + str(exc_tb.tb_lineno) + "\nwith error message: " + str(error)
    return error_message

class BaseException(Exception):
    def __init__(self, error_message, error_details:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_details)
    
    def __str__(self):
        return self.error_message

if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        logging.error("Error occured")
        raise BaseException(e, sys)