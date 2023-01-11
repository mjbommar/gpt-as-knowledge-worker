"""
Run a CPA exam session with prompt style 001.
"""

# imports
import datetime
import json
import time
from pathlib import Path
from typing import Iterator

# packages
import openai
import pandas
import tqdm

# set the key
openai.api_key = (Path(__file__).parent / ".openai_key").read_text()

# local imports
from question_data import parse_question_source
from prompts import *


def get_parameter_sets() -> Iterator[dict]:
    """Generate a set of parameter sets."""
    for temperature in [
        0.0,
    ]:  # 0.0, 0.5, 1.0
        for max_tokens in [
            256,
        ]:  # 16, 128
            for top_p in [
                1,
            ]:  # 1, 0.75
                for best_of in [
                    1,
                ]:  # 1, 2, 4
                    for frequency_penalty in [
                        0,
                    ]:
                        for presence_penalty in [
                            0,
                        ]:
                            yield {
                                "temperature": temperature,
                                "max_tokens": max_tokens,
                                "top_p": top_p,
                                "best_of": best_of,
                                "frequency_penalty": frequency_penalty,
                                "presence_penalty": presence_penalty,
                            }


def get_next_session_path() -> Path:
    """Get the next session path."""
    session_number = 1

    while True:
        session_id = f"cpa-exam-{session_number:03d}"
        session_path = (
            Path(__file__).parent.parent / "results" / "questions-02" / "sessions-002"
        )
        session_path.mkdir(exist_ok=True)
        session_path = session_path / session_id

        # skip if exists
        if session_path.exists():
            session_number += 1
            continue

        # otherwise continue
        session_path.mkdir(exist_ok=True)
        return session_path


def main():
    # iterate through questions and generate prompt
    question_file = Path(__file__).parent.parent / "data" / "questions_02.txt"
    question_list = parse_question_source(question_file)
    question_set_name = question_file.name

    # set samples per value
    num_samples_per_set = 1

    """
    These prompts are only relevant for the test REG section:
        generate_prompt_001,
        generate_prompt_002,
        generate_prompt_003,
        generate_prompt_004,
        generate_prompt_005,
        generate_prompt_006,
        generate_prompt_007,
        generate_prompt_008,
        generate_prompt_009,
        generate_prompt_010,
        
    These prompts are not tested for old models:
        generate_prompt_011,
        generate_prompt_012,
        generate_prompt_014,
        generate_prompt_015,
        generate_prompt_016,
        generate_prompt_017,
        generate_prompt_018,
        generate_prompt_019,
        generate_prompt_020,        
    """

    prompt_list = [
        generate_prompt_020,
    ]

    model_list = [
        "text-ada-001",
        "text-babbage-001",
        "text-curie-001",
        "text-davinci-001",
    ]

    # iterate through parameter values
    for model_name in model_list:
        for parameter_kwargs in get_parameter_sets():
            for sample_id in range(num_samples_per_set):
                for prompt_method in prompt_list:
                    # set up the session path iteratively
                    session_path = get_next_session_path()

                    # status update
                    # print(f"Running with prompt method {str(prompt_method.__name__)}, parameters: {parameter_kwargs}")

                    # generate the prompts
                    exam_data = {
                        "model_name": model_name,
                        "question_set": question_set_name,
                        "prompt_method": str(prompt_method.__name__),
                        "parameters": parameter_kwargs,
                        "start_time": datetime.datetime.now().isoformat(),
                        "end_time": None,
                        "questions": [],
                    }

                    # iterate through questions and generate prompt
                    question_prog_bar = tqdm.tqdm(question_list, desc="Questions")
                    for question in question_prog_bar:
                        # set description
                        question_prog_bar.set_description(
                            f"Q{question['question_number']}, prompt method {str(prompt_method.__name__)}, parameters: {parameter_kwargs}"
                        )
                        # generate the prompt
                        prompt = prompt_method(question)

                        # setup question data
                        question_data = {
                            "question_input": question,
                            "model_prompt": prompt,
                            "model_response": None,
                        }

                        # try to query the API, retry on failure, else log the failed response
                        try:
                            question_data["model_response"] = openai.Completion.create(
                                model=model_name,
                                prompt=question_data["model_prompt"],
                                **parameter_kwargs,
                            )
                        except Exception as e:
                            question_prog_bar.set_description(
                                f"First error, retrying in 5: {e}"
                            )
                            question_data["model_response"] = None

                            # sleep and retry
                            time.sleep(5)

                            try:
                                question_data[
                                    "model_response"
                                ] = openai.Completion.create(
                                    model=model_name,
                                    prompt=question_data["model_prompt"],
                                    **parameter_kwargs,
                                )
                            except Exception as f:
                                question_prog_bar.set_description(
                                    f"Second error, retrying in 10: {f}"
                                )
                                question_data["model_response"] = None

                                # sleep and retry
                                time.sleep(10)

                                try:
                                    question_data[
                                        "model_response"
                                    ] = openai.Completion.create(
                                        model=model_name,
                                        prompt=question_data["model_prompt"],
                                        **parameter_kwargs,
                                    )
                                except Exception as g:
                                    print(
                                        f"Third error, skipping question {question}: {g}"
                                    )
                                    question_data["model_response"] = None
                        finally:
                            # log the current state of the exam
                            exam_data["questions"].append(question_data)
                            with open(
                                session_path / "exam_data.json", "wt", encoding="utf-8"
                            ) as output_file:
                                json.dump(exam_data, output_file)

                    # save final state
                    exam_data["end_time"] = datetime.datetime.now().isoformat()
                    with open(
                        session_path / "exam_data.json", "wt", encoding="utf-8"
                    ) as output_file:
                        json.dump(exam_data, output_file)


if __name__ == "__main__":
    main()
