from pydantic import BaseModel

# -------------- Classes used for returning specific data errors ------------- #
class ErrorMessage:
    """Model used to define return data from error message."""
    def __init__(self, err_loc:list, err_msg:str, err_type:str):
        self.err_loc = err_loc
        self.err_msg = err_msg
        self.err_type = err_type
    def get_error_message(self):
        return {
            "loc":self.err_loc,
            "msg": self.err_msg,
            "type": self.err_type
        }
# --------------------- Model used for FastAPI responses --------------------- #
class ErrResponse(BaseModel):
    """Model used in FastAPI responses section of main.py to show schema on UI."""
    loc: list
    msg: str
    type: str
# ---------------------------------------------------------------------------- #

# EOF