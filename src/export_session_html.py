"""
export a session from JSON to HTML
"""

# imports
import datetime
import json
from pathlib import Path

# packages
import jinja2

# project
from score_exam import score_exam


def session_to_html(json_data: dict) -> str:
    """
    convert a session to HTML
    """

    # setup jinja
    template_path = Path(__file__).parent / "session_template.html"
    template = jinja2.Template(template_path.read_text())
    template.environment.autoescape = True
    template.environment.trim_blocks = True
    template.environment.lstrip_blocks = True

    # render template
    return template.render(**json_data)


if __name__ == "__main__":
    # get the data path
    data_path = (
        Path(__file__).parent.parent / "results" / "questions-02" / "sessions-002"
    )

    # get the list of json files under here
    json_file_list = list(data_path.rglob("*.json"))

    # iterate through the files
    for json_file in json_file_list:
        # load the data
        with open(json_file, "r") as input_file:
            data = json.load(input_file)

        # set the session ID as the folder name above
        session_id = json_file.parent.name
        data["session_id"] = session_id

        # populate the duration variable by subtracting iso format end_time and start_time
        try:
            data["duration"] = datetime.datetime.fromisoformat(
                data["end_time"]
            ) - datetime.datetime.fromisoformat(data["start_time"])
        except:
            data["duration"] = None

        # merge the correct answer and correct/incorrect scoring onto the data dict
        exam_scored = score_exam(data)
        for i in range(len(data["questions"])):
            data["questions"][i]["correct_answer"] = exam_scored["correct_answer"][i]
            data["questions"][i]["is_correct"] = exam_scored["is_correct"][i]
            data["questions"][i]["question_section"] = exam_scored["question_section"][
                i
            ]
            data["questions"][i]["question_number"] = exam_scored["question_number"][i]

        # convert to HTML
        try:
            html = session_to_html(data)
        except Exception as error:
            print(f"Error: {error} with {json_file}")
            continue

        # write it back out into the same directory
        html_file = json_file.parent / f"session.html"
        print(html_file)
        html_file.write_text(html)
