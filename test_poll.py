import requests as req
from typing import Any
from time import sleep

BOT_TOKEN: str = "7301809343:AAEVbHnroHgIype01zHr6A-W0a6Dmfk1-bA"
CHAT_ID: str = "1297466029"

question_text: str = "Test question? (15 seconds)"
question_options: list[str] = ["option1", "option2", "option3"]


def send_poll(send_to: str, bot_id: str, question_text_: str, question_options_: list[str], anonymous: bool = False,
              multiple_answers: bool = False) -> dict[str, str]:
    send_request_to_poll = f"https://api.telegram.org/bot{bot_id}/sendPoll"

    payload_: dict[str, str] = {"chat_id": send_to,
                                "question": question_text_,
                                "options": question_options_,
                                "is_anonymous": anonymous,
                                "allows_multiple_answers": multiple_answers}

    response_to_send_poll = req.post(send_request_to_poll, json=payload_)
    poll_date_ = response_to_send_poll.json()

    return poll_date_


def stop_poll(send_to: str, bot_id: str, date: dict[Any]) -> dict[Any]:
    stop_request_to_poll = f"https://api.telegram.org/bot{bot_id}/stopPoll"

    stop_payload_: dict[str, str] = {"chat_id": send_to,
                                     "message_id": date["result"]["message_id"]}

    stop_response_ = req.post(stop_request_to_poll, json=stop_payload_)
    stop_date_ = stop_response_.json()

    return  stop_date_


def send_result_of_poll_to(send_to: str, bot_id: str, date: list[dict[Any]]) -> None:
    results_: str = ""

    for i in range(len(date)):
        for j in range(len(date[i]["result"]["options"])):
            for key, value in date["result"]["options"][j].items():
                if key == "text":
                    results_ += f"{value}: "
                elif key == "voter_count":
                    results_ += f"{value}\n"

    send_message = f"https://api.telegram.org/bot{bot_id}/sendMessage"

    message_payload: dict[str, str] = {"chat_id": send_to,
                                       "text": results_}

    req.post(send_message, json=message_payload)


dataA1 = send_poll("929123339", "7301809343:AAEVbHnroHgIype01zHr6A-W0a6Dmfk1-bA", "Question text?", ["option1", "option2", "option3"], True, False)
dataB1 = send_poll("1297466029", "7301809343:AAEVbHnroHgIype01zHr6A-W0a6Dmfk1-bA", "Question text?", ["option1", "option2", "option3"], True, False)
sleep(3)
dateA2 = stop_poll("929123339", "7301809343:AAEVbHnroHgIype01zHr6A-W0a6Dmfk1-bA", dataA1)
dateB2 = stop_poll("1297466029", "7301809343:AAEVbHnroHgIype01zHr6A-W0a6Dmfk1-bA", dataB1)
print(dateA2["result"]["options"], dateB2["result"]["options"])
