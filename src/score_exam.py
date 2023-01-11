"""
Read the exam session JSON files, score the questions, and output a
CSV file with the question number, question type, answer, and parameters.
"""

# imports
import datetime
import json
from pathlib import Path

# packages
import pandas


def parse_gpt_response(response: str) -> dict:
    """Parse the response from the API with numeric choices and return a dictionary like this:
    {
        "answer": "A",
        "explanation": "The answer is A because ..."
    }

    All response styles should have the following field:
        - Choice:
        OR
        - Amount:
        OR
        - Answer:
        OR
        First Choice:
        Second Choice:
        Third Choice:
        Explanation:

    The following fields are optional:
        - Explanation:
    """
    # split the response into lines
    if response is None:
        return {
            "answer": None,
            "explanation": None,
        }

    response_lines = response.splitlines()
    num_lines = len(response_lines)

    response = {
        "answer": None,
        "second_answer": None,
        "third_answer": None,
        "explanation": None,
    }

    for i, line in enumerate(response_lines):
        # check for the answer
        line = line.strip()

        if "Option" in line and ":" in line:
            line = line.replace("Option", "")

        line_tokens = line.split()
        if len(line_tokens) == 0:
            continue

        # check for the answer
        # any `continue` lines below are for answers that do not follow prompts and are therefore coded as no response
        if line_tokens[0].startswith("Choice"):
            if len(line_tokens) < 2:
                continue
            response["answer"] = (
                line_tokens[1]
                .replace(".", "")
                .replace(":", "")
                .replace(",", "")
                .strip()
            )
        elif line_tokens[0].startswith("Best"):
            if len(line_tokens) < 3:
                continue
            response["answer"] = (
                line_tokens[2]
                .replace(".", "")
                .replace(":", "")
                .replace(",", "")
                .strip()
            )
        elif line_tokens[0].startswith("Amount"):
            if len(line_tokens) < 2:
                continue
            response["answer"] = line_tokens[1].strip()
        elif line_tokens[0].startswith("Answer"):
            if len(line_tokens) < 2:
                continue
            response["answer"] = (
                line_tokens[1]
                .replace(".", "")
                .replace(":", "")
                .replace(",", "")
                .strip()
            )
        elif line_tokens[0].startswith("Explanation"):
            if len(line_tokens) < 2:
                continue
            response["explanation"] = " ".join(line_tokens[1:])
            break
        elif line_tokens[0].startswith("First"):
            if len(line_tokens) < 3:
                continue
            response["answer"] = (
                line_tokens[2]
                .replace(".", "")
                .replace(":", "")
                .replace(",", "")
                .strip()
            )
        elif line_tokens[0].startswith("Second"):
            if len(line_tokens) < 3:
                continue
            response["second_answer"] = (
                line_tokens[2]
                .replace(".", "")
                .replace(":", "")
                .replace(",", "")
                .strip()
            )
        elif line_tokens[0].startswith("Third"):
            if len(line_tokens) < 3:
                continue
            response["third_answer"] = (
                line_tokens[2]
                .replace(".", "")
                .replace(":", "")
                .replace(",", "")
                .strip()
            )
        else:
            if i == 0 and len(line_tokens) <= 2:
                response["answer"] = (
                    line_tokens[0]
                    .replace(".", "")
                    .replace(":", "")
                    .replace(",", "")
                    .strip()
                )
            elif i == 0 and len(line_tokens) > 2:
                if line_tokens[0].strip(".").isnumeric():
                    response["answer"] = (
                        line_tokens[0]
                        .replace(".", "")
                        .replace(":", "")
                        .replace(",", "")
                        .strip()
                    )
                elif line_tokens[0].strip(".").lower() in ["a", "b", "c", "d"]:
                    response["answer"] = (
                        line_tokens[0]
                        .replace(".", "")
                        .replace(":", "")
                        .replace(",", "")
                        .strip()
                    )
            elif i == 0 and line.startswith("Option"):
                response["answer"] = (
                    line_tokens[1]
                    .replace(".", "")
                    .replace(":", "")
                    .replace(",", "")
                    .strip()
                )
            elif i == 0 and len(line_tokens) > 2 and "$" in line_tokens[-1]:
                response["answer"] = (
                    line_tokens[-1]
                    .replace(".", "")
                    .replace(":", "")
                    .replace(",", "")
                    .strip()
                )
            else:
                if "Worst" in line or "Ex" in line:
                    continue
                if response["answer"] is None:
                    # these are required for older models that don't follow instructions well
                    if line.strip().split()[0] in ["A.", "B.", "C.", "D."]:
                        response["answer"] = line.strip().split()[0].strip(".").strip()
                    else:
                        print(f"Could not parse answer: {line}")
                        print(line.split()[0])

    # return dictionary
    return response


def score_exam(exam_data: dict) -> pandas.DataFrame:
    """
    Read an exam JSON data dictionary, parse all questions, and
    return per-exam dataframe.
    :param exam_data:
    :return:
    """

    exam_question_list = []

    # iterate through all questions, parse the model response, and compare against the correct answer
    for question in exam_data["questions"]:
        # get the model response as text and parse it
        try:
            model_answer_text = question["model_response"]["choices"][0]["text"]
        except (KeyError, TypeError):
            model_answer_text = None

        # parse the model response
        model_response_data = parse_gpt_response(model_answer_text)

        # compare answer to question_input correct answer
        correct_answer = question["question_input"]["answer"]

        # compare answers based on question type
        answer_correct = False
        second_correct = False
        third_correct = False
        if model_response_data["answer"] is not None:
            if question["question_input"]["question_type"] == "multiple_choice":
                # multiple choice
                if model_response_data["answer"] == correct_answer:
                    answer_correct = True
                if model_response_data["second_answer"] == correct_answer:
                    second_correct = True
                if model_response_data["third_answer"] == correct_answer:
                    third_correct = True
            elif question["question_input"]["question_type"] == "short_answer":
                # short answer
                if isinstance(correct_answer, list):
                    if model_response_data["answer"] in correct_answer:
                        answer_correct = True
                elif isinstance(correct_answer, str):
                    if model_response_data["answer"] == correct_answer:
                        answer_correct = True
            elif question["question_input"]["question_type"] == "amount":
                # strip dollar signs, (, ), and commas from both sides
                correct_answer = (
                    correct_answer.replace("$", "")
                    .replace("(", "")
                    .replace(")", "")
                    .replace(",", "")
                )
                model_answer = (
                    model_response_data["answer"]
                    .replace("$", "")
                    .replace("(", "")
                    .replace(")", "")
                    .replace(",", "")
                )
                if correct_answer == model_answer:
                    answer_correct = True

        # calculate duration
        try:
            session_duration = (
                datetime.datetime.fromisoformat(exam_data["end_time"])
                - datetime.datetime.fromisoformat(exam_data["start_time"])
            ).total_seconds()
        except:
            session_duration = None

        # append data to result list
        exam_question_list.append(
            {
                "question_section": question["question_input"]["question_section"]
                if "question_section" in question["question_input"]
                else None,
                "question_number": len(exam_question_list) + 1,
                "question_type": question["question_input"]["question_type"],
                "model_answer": model_response_data["answer"],
                "model_second_answer": None,
                "model_third_answer": None,
                "correct_answer": correct_answer,
                "model_explanation": model_response_data["explanation"],
                "is_correct": answer_correct,
                "is_second_correct": second_correct,
                "is_third_correct": third_correct,
                # top two answers
                "is_top_two_correct": answer_correct or second_correct,
                # top three answers
                "is_top_three_correct": answer_correct
                or second_correct
                or third_correct,
                # parameters here
                "model_name": exam_data["model_name"]
                if "model_name" in exam_data
                else None,
                "prompt_method": exam_data["prompt_method"]
                if "prompt_method" in exam_data
                else None,
                "temperature": exam_data["parameters"]["temperature"],
                "max_tokens": exam_data["parameters"]["max_tokens"],
                "top_p": exam_data["parameters"]["top_p"],
                "best_of": exam_data["parameters"]["best_of"],
                "frequency_penalty": exam_data["parameters"]["frequency_penalty"],
                "presence_penalty": exam_data["parameters"]["presence_penalty"],
                "duration": session_duration,
            }
        )

    # return dataframe
    return pandas.DataFrame(exam_question_list)


def main():
    # get the list of exam sessions
    base_result_path = Path(__file__).parent.parent / "results" / "questions-02"
    result_path = base_result_path / "sessions-001"

    # combine all exams
    exam_df_list = []

    # iterate through session exams, read JSON file, and score
    for exam_path in result_path.iterdir():
        # check if there's an exam json file
        if exam_path.is_file():
            continue
        exam_json_path = exam_path / "exam_data.json"
        if not exam_json_path.exists():
            print(f"Exam JSON file not found at {str(exam_json_path)}")
            continue

        # read the exam data
        with open(exam_json_path, "r") as exam_json_file:
            exam_data = json.load(exam_json_file)

        # score the exam
        exam_df = score_exam(exam_data)
        # add the session name
        exam_df["session_name"] = exam_path.name
        # track the exams
        exam_df_list.append(exam_df)

    # concat all together
    exam_df = pandas.concat(exam_df_list, ignore_index=True)

    # save to CSV
    exam_df.to_csv(result_path / "exam_results.csv", index=False)

    # number of exams
    print("Exam Sessions:", exam_df["session_name"].nunique())
    print("Number of Prompts:", exam_df["prompt_method"].nunique())
    print("Number of Questions:", exam_df["question_number"].nunique())
    # print headline accuracy rate
    accuracy_rate = exam_df["is_correct"].mean()
    print(f"Headline Accuracy Rate: {accuracy_rate:.2%}")

    # top two accuracy rate
    top_two_accuracy_rate = exam_df["is_top_two_correct"].mean()
    print(f"Top Two Accuracy Rate: {top_two_accuracy_rate:.2%}")

    # top three accuracy rate
    top_two_accuracy_rate = exam_df["is_top_three_correct"].mean()
    print(f"Top Three Accuracy Rate: {top_two_accuracy_rate:.2%}")

    # accuracy by prompt
    first_by_prompt = exam_df.groupby(["prompt_method"])["is_correct"].mean()
    top_two_by_prompt = exam_df.groupby(["prompt_method"])["is_top_two_correct"].mean()
    top_three_by_prompt = exam_df.groupby(["prompt_method"])[
        "is_top_three_correct"
    ].mean()
    # combine the three
    accuracy_by_prompt = pandas.concat(
        [first_by_prompt, top_two_by_prompt, top_three_by_prompt], axis=1
    )
    print(accuracy_by_prompt)


if __name__ == "__main__":
    main()
