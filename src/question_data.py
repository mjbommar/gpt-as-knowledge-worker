"""
This module provides convenience functions for parsing the questions from source text file and
returning them as a list of dictionary objects with the following keys:
    - question_type: the type of question - multiple_choice, short_answer, amount
    - question: the question text
    - choices: if question_type is multiple_choice, this is a dictionary with each choice as a key and
                  the value is the choice text
    - answer: the answer to the question

Each testlet starts with <S>
Each question starts with <Q>
Each answer begins with <A>

"""

# imports
from pathlib import Path


def parse_question_source(question_file: Path) -> list[dict]:
    """return a list of dictionaries containing the questions and answers in the dictionary format:
    {
        "question_type": "multiple_choice",
        "question": "What is the capital of the United States?",
        "choices": {
            "1": "New York",
            "2": "Washington, D.C.",
            "3": "Los Angeles",
            "4": "Chicago"
        },
        "answer": "2"
    }
    from
    <Q>What is the capital of the United States?
    1. New York
    2. Washington, D.C.
    3. Los Angeles
    4. Chicago
    <A>2
    """
    # load the question file
    if not question_file.exists():
        raise FileNotFoundError(f"File {question_file} not found")
    question_text_buffer = question_file.read_text()

    # store all questions
    question_list = []
    section_count = 1

    # split the buffer into testlets
    testlet_position_start = question_text_buffer.find("<S>")
    while testlet_position_start != -1:
        # get the end
        testlet_position_end = question_text_buffer.find(
            "<S>", testlet_position_start + 1
        )
        if testlet_position_end != -1:
            testlet_text = question_text_buffer[
                testlet_position_start:testlet_position_end
            ]
        else:
            testlet_text = question_text_buffer[testlet_position_start:]
        testlet_position_start = testlet_position_end

        # get the first line of the testlet, which is the question section name
        section_name = testlet_text.splitlines()[0].replace("<S>", "").strip()
        section_count = 1

        # now split the testlet text into questions
        question_position_start = testlet_text.find("<Q>")
        while question_position_start != -1:
            # get the end
            question_position_end = testlet_text.find(
                "<Q>", question_position_start + 1
            )
            if question_position_end != -1:
                question_text = testlet_text[
                    question_position_start:question_position_end
                ]
            else:
                question_text = testlet_text[question_position_start:]
            question_position_start = question_position_end

            # setup question record
            question_record = {
                "question_section": section_name,
                "question_number": section_count,
                "question_type": None,
                "question": None,
                "choices": None,
                "answer": None,
            }
            section_count += 1

            # find the answer in this body
            answer_position_start = question_text.find("<A>")
            if answer_position_start != -1:
                answer_text = question_text[answer_position_start + 3 :]
                question_text = question_text[:answer_position_start]

                # remove the <Q> and initial number if present
                if question_text.startswith("<Q>"):
                    question_text = question_text[3:]
                # check first token if it's a number
                question_tokens = question_text.split()
                if question_tokens[0][0:-1].isdigit():
                    question_text = question_text[
                        question_text.find(question_tokens[0])
                        + len(question_tokens[0]) :
                    ]
                question_record["question"] = question_text.strip()
            else:
                raise ValueError("No answer found in question")

            # determine the question type based on whether it's a choice 1-4, an amount with $ or (), or a short answer
            # or if it's in A, B, C, D
            if answer_text.strip().isnumeric() or answer_text.strip().lower() in [
                "a",
                "b",
                "c",
                "d",
            ]:
                question_record["question_type"] = "multiple_choice"
                question_record["answer"] = answer_text.strip()
            elif answer_text.strip().startswith("$") or answer_text.strip().startswith(
                "("
            ):
                question_record["question_type"] = "amount"
                question_record["answer"] = answer_text.strip()
                # if it's surrounded by (), remove them and replace with initial -
                if question_record["answer"].startswith("(") and question_record[
                    "answer"
                ].endswith(")"):
                    question_record["answer"] = "-" + question_record["answer"][1:-1]
                # remove the $ and ,
                question_record["answer"] = (
                    question_record["answer"].replace("$", "").replace(",", "")
                )
            else:
                # NOTE: the only current question of this type has two options, split with a semi-colon ;
                question_record["question_type"] = "short_answer"
                question_record["answer"] = answer_text.strip().split(";")

            # if it's multiple choice, find the choices
            choices = {}
            if question_record["question_type"] == "multiple_choice":
                # parse the multipl choice options
                choice_start_line = None

                for i, line in enumerate(question_text.splitlines()):
                    line_tokens = line.strip().split()
                    if len(line_tokens) == 0:
                        continue

                    # parse if not empty
                    first_token = line_tokens[0]
                    if (
                        first_token[0:-1].isnumeric()
                        or first_token[0].lower() in ["a", "b", "c", "d"]
                    ) and first_token[-1] == ".":
                        # set choice start line
                        if choice_start_line is None:
                            choice_start_line = i

                        # split the choice into key and value
                        choice_key = first_token[0:-1]
                        choice_value = " ".join(line_tokens[1:]).strip()
                        choices[choice_key] = choice_value

                # update the question text to include only up to the choice list
                question_record["question"] = "\n".join(
                    question_text.splitlines()[0:choice_start_line]
                ).strip()

            # add the choices to the record
            question_record["choices"] = choices

            # add the question record to the list
            question_list.append(question_record)

    return question_list
