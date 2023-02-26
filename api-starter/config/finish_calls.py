import uuid, os, colander
from fastapi import HTTPException
from pydantic import ValidationError
from loguru import logger


class LogObj(colander.MappingSchema):
    log_obj_keys = colander.SchemaNode(colander.List(),validator=colander.ContainsOnly(
        [
            'request_url',
            'bearer_msid',
            'isErr',
            'which_error',
            'func_location',
            'at_func',
            'bad_obj_title',
            'bad_obj_value',
            'ext_api_name',
            'ext_api_code'
        ]
    ))

class WhichError(colander.MappingSchema):
    which_error = colander.SchemaNode(colander.String(),validator=colander.OneOf(
        [
            "none_type",
            "no_option",
            "bad_data",
            "bad_token",
            "hide_creds",
            "not_found",
            "login_unauthorized",
            "too_many",
            "override",
            "bad_status",
            "complete"
        ]
    ))

class FinishCall:
    def __init__(self, log_obj: dict):
        self.log_obj = log_obj
        # Self Defined
        self.namespace = os.environ['K8S_POD_NAMESPACE']
        self.pod = os.environ['K8S_POD_NAME']
        self.uuid = str(uuid.uuid4())
        # Provided
        self.request_url = log_obj['request_url'] or None
        self.bearer_msid = log_obj['bearer_msid'] or None
        self.isErr = log_obj['isErr'] or None
        self.which_error = log_obj['which_error'] or None
        self.func_location = log_obj['func_location'] or None
        self.at_func = log_obj['at_func'] or None
        self.bad_obj_title = log_obj['bad_obj_title'] or None
        self.bad_obj_value = log_obj['bad_obj_value'] or None
        self.ext_api_name = log_obj['ext_api_name'] or None
        self.ext_api_code = log_obj['ext_api_code'] or None
        self.bad_msg = []

    async def wrap_up(self):
        isLogObjKeysValid, log_obj_errs = await self.validate_log_obj_keys()
        if isLogObjKeysValid:
            isWhichErrorValuesValid, which_error_errs = await self.validate_which_error_values()
            if isWhichErrorValuesValid:
                return await self.process_it()
            else:
                raise ValueError(which_error_errs)
        else:
            raise ValueError(log_obj_errs)

    async def validate_log_obj_keys(self):
        log_obj_keys = []
        for key in self.log_obj.keys():
            log_obj_keys.append(key)

        cstruct = {"log_obj_keys":log_obj_keys}
        schema = LogObj()
        try:
            valid_log_obj_keys = schema.deserialize(cstruct)
            return True, valid_log_obj_keys
        except colander.Invalid as ex:
            return False, ex.asdict()

    async def validate_which_error_values(self):
        cstruct = {"which_error": self.which_error}
        schema = WhichError()
        try:
            valid_which_error_values = schema.deserialize(cstruct)
            return True, valid_which_error_values
        except colander.Invalid as ex:
            return False, ex.asdict()

    async def process_it(self):
        if self.which_error == "none_type":
            logger_code = "API_CATCH"; status_code = 500
            msg = f"Function executed on {self.at_func} reported object {self.bad_obj_title} returned type 'None'."

        elif self.which_error == "no_option":
            logger_code = "API_CATCH"; status_code = 500
            msg = f"Function executed on {self.at_func} reported no option for {self.bad_obj_title}: {self.bad_obj_value} available."

        elif self.which_error == "bad_data":
            logger_code = "API_CATCH"; status_code = 500
            msg = f"Function executed on {self.at_func} reported {self.bad_obj_title} was formatted incorrectly:\n\n {self.bad_obj_value} \n"

        elif self.which_error == "bad_token":
            logger_code = "API_INCOMPLETE"; status_code = 401
            msg = f"Function executed on {self.at_func} reported {self.bad_obj_title} found: {self.bad_obj_value}."

        elif self.which_error == "hide_creds":
            logger_code = "API_CATCH"; status_code = 500
            msg = f"Function executed on {self.at_func} reported {self.bad_obj_title}: not hidden."

        elif self.which_error == "not_found":
            logger_code = "API_NOTFOUND"; status_code = 404
            msg = f"Function exectuted on {self.at_func} reported that info on {self.bad_obj_title} was {self.bad_obj_value}."

        elif self.which_error == "login_unauthorized":
            logger_code = "API_NOTFOUND"; status_code = 403
            msg = f"Function executed on {self.at_func} reported that{self.bad_obj_title} {self.bad_obj_value}."

        elif self.which_error == "too_many":
            logger_code = "API_INCOMPLETE"; status_code = 400
            msg = f"Function executed on {self.at_func} reported that info on {self.bad_obj_title} was {self.bad_obj_value}."

        elif self.which_error == "override":
            logger_code = "API_INCOMPLETE"; status_code = 400
            msg = f"Function executed on {self.at_func} reported manual stop on route: {self.bad_obj_title} of {self.bad_obj_value}"

        elif self.which_error == "bad_status":
            logger_code = "API_INCOMPLETE"; status_code = 400
            msg = f"Function executed on {self.at_func} reported {self.ext_api_name} API bad status code of {self.ext_api_code}."

        elif self.which_error == "complete":
            logger_code = "API_COMPLETE"; status_code = 200
            msg = f"Function executed on {self.at_func} returned successfully."

        else:
            return None

        log_type = logger_code + "." + self.which_error
        try:
            #TODO: Replace this statement with splunk function defined in app_server_logging.py
            logger.log(f"{logger_code}", f"\n  URL : {self.request_url}\n  UUID: {self.uuid}\n  USER: {self.bearer_msid}\n  Path: {self.func_location}\n  Func: {self.at_func}\n  API : {self.ext_api_name}\n  Type: {log_type}\n  Msg : {msg}\n  External API Code: {self.ext_api_code}\n  Return Code: {status_code}")
        except ValueError as ex:
            raise ValidationError(f"Logging Failed: {ex}")

        if self.isErr == True:
            raise HTTPException(status_code=status_code, detail=[
                {
                    "loc":[
                        f"url: {self.request_url}",
                        f"uuid: {self.uuid}",
                        f"user: {self.bearer_msid}",
                        f"namespace: {self.namespace}",
                        f"pod: {self.pod}",
                        f"path: {self.func_location}",
                        f"function: {self.at_func}",
                        f"object: {self.bad_obj_title}",
                        f"value: {self.bad_obj_value}",
                        f"api: {self.ext_api_name}",
                        f"code: {self.ext_api_code}",
                        f"return_code: {status_code}"
                    ],
                    "msg": f"{msg}",
                    "type":f"{log_type}"
                }
            ])
        else:
            return None
# ---------------------------------------------------------------------------- #

# EOF