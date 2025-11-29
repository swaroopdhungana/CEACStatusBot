import json
import os
import datetime

import pytz

from CEACStatusBot.captcha import CaptchaHandle, OnnxCaptchaHandle
from CEACStatusBot.request import query_status

from .handle import NotificationHandle

DEFAULT_ACTIVE_HOURS = "00:00-23:59"


class NotificationManager:
    def __init__(
        self,
        location: str,
        number: str,
        passport_number: str,
        surname: str,
        captchaHandle: CaptchaHandle = OnnxCaptchaHandle("captcha.onnx"),
    ) -> None:
        self.__handleList = []
        self.__location = location
        self.__number = number
        self.__captchaHandle = captchaHandle
        self.__passport_number = passport_number
        self.__surname = surname
        self.__status_file = "status_record.json"

    def _get_hour_range(self) -> list:
        active_hours = os.getenv("ACTIVE_HOURS")
        if active_hours is None:
            active_hours = DEFAULT_ACTIVE_HOURS
        start_str, end_str = active_hours.split("-")
        start = datetime.datetime.strptime(start_str, "%H:%M").time()
        end = datetime.datetime.strptime(end_str, "%H:%M").time()
        if start > end:
            raise ValueError("Start time must be before end time, got start: {start}, end: {end}")
        return start, end

    def addHandle(self, notificationHandle: NotificationHandle) -> None:
        self.__handleList.append(notificationHandle)

    def send(self) -> None:
        res = query_status(
            self.__location,
            self.__number,
            self.__passport_number,
            self.__surname,
            self.__captchaHandle,
        )
        current_status = res["status"]
        print(f"Current status: {current_status} - Last updated: {res['case_last_updated']}")
        # Load the previous statuses from the file
        statuses = self.__load_statuses()

        # Check if status has changed
        should_notify = False
        if not statuses:
            should_notify = True
        elif statuses[-1]["status"] != current_status:
            should_notify = True
        
        if should_notify:
            self.__save_current_status(res)
            self.__send_notifications(res)
        else:
            print(f"Status unchanged ({current_status}). No notification sent.")


    def __load_statuses(self) -> list:
        if os.path.exists(self.__status_file):
            with open(self.__status_file, "r") as file:
                return json.load(file).get("statuses", [])
        return []

    def __save_current_status(self, res: dict) -> None:
        statuses = self.__load_statuses()
        statuses.append({
            "time": res["time"],
            "status": res["status"],
            "last_updated_date": res["case_last_updated"]
        })

        with open(self.__status_file, "w") as file:
            json.dump({"statuses": statuses}, file)

    def __send_notifications(self, res: dict) -> None:
        if res["status"] == "Refused":
            try:
                TIMEZONE = os.environ["TIMEZONE"]
                localTimeZone = pytz.timezone(TIMEZONE)
                localTime = datetime.datetime.now(localTimeZone)
            except pytz.exceptions.UnknownTimeZoneError:
                print("UNKNOWN TIMEZONE Error, use default")
                localTime = datetime.datetime.now()
            except KeyError:
                print("TIMEZONE Error")
                localTime = datetime.datetime.now()

            active_hour_start, active_hour_end = self._get_hour_range()
            start_dt = datetime.datetime.combine(localTime.date(), active_hour_start, tzinfo=localTimeZone)
            end_dt = datetime.datetime.combine(localTime.date(), active_hour_end, tzinfo=localTimeZone)
            if not (start_dt <= localTime <= end_dt):
                print(
                    f"Outside active hours {os.getenv('ACTIVE_HOURS', DEFAULT_ACTIVE_HOURS)}. "
                    "No notification sent for Refused status."
                )
                return

        for notificationHandle in self.__handleList:
            notificationHandle.send(res)
