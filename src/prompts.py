"""
This file defines prompts for the text completion API that vary the following:
 * Response format (MCQ best response, best/worst, rank-order, rank-order top three,  short answer, amount)
 * Contextualization, e.g., situate the model in a specific role, situation, jurisdiction, etc.
 * Justification, e.g., ask the model to explain its answer

Note prompt_001 -> 010 is for Assessment 1 on the "real" Regulation (REG) exam.
Subsequent prompts are meant to be used for Assessment 2 on the 200+ question bank across all areas.
"""


def generate_prompt_001(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 001"""
    question_prompt = (
        f"""Please answer the following CPA exam question in this format:\n"""
    )

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""Choice: <CHOICE>\n\n"""

        question_prompt += f"""{question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"

        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "short_answer":
        question_prompt += f"""Answer: <ANSWER>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "amount":
        question_prompt += f"""Amount: <AMOUNT>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_002(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 002"""
    question_prompt = (
        f"""Please answer the following CPA exam question in this format:\n"""
    )

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""Choice: <CHOICE>\nExplanation: <EXPLANATION>\n\n"""

        question_prompt += f"""{question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"

        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "short_answer":
        question_prompt += f"""Answer: <ANSWER>\nExplanation: <EXPLANATION>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "amount":
        question_prompt += f"""Amount: <AMOUNT>\nExplanation: <EXPLANATION>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_003(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 003"""
    question_prompt = f"""Imagine you are an accountant in the United States.  Please answer the question below in this format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""Choice: <CHOICE>\n\n"""

        question_prompt += f"""{question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"

        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "short_answer":
        question_prompt += f"""Answer: <ANSWER>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "amount":
        question_prompt += f"""Amount: <AMOUNT>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_004(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 004"""
    question_prompt = f"""Imagine you are an accountant in the United States.  Please answer the question below in this format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""Choice: <CHOICE>\nExplanation: <EXPLANATION>\n\n"""

        question_prompt += f"""{question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"

        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "short_answer":
        question_prompt += f"""Answer: <ANSWER>\nExplanation: <EXPLANATION>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "amount":
        question_prompt += f"""Amount: <AMOUNT>\nExplanation: <EXPLANATION>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_005(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 005"""
    question_prompt = f"""Imagine you are an accountant in the United States.  Please answer the question below in this format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""Best Choice: <CHOICE>\nWorst Choice: <CHOICE>\nExplanation: <EXPLANATION>\n\n"""

        question_prompt += f"""{question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"

        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "short_answer":
        question_prompt += f"""Answer: <ANSWER>\nExplanation: <EXPLANATION>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "amount":
        question_prompt += f"""Amount: <AMOUNT>\nExplanation: <EXPLANATION>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_006(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 006"""
    question_prompt = f"""Imagine you are a tax professional in the United States. Please answer the question below in this format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""Best Choice: <CHOICE>\nWorst Choice: <CHOICE>\nExplanation: <EXPLANATION>\n\n"""

        question_prompt += f"""{question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"

        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "short_answer":
        question_prompt += f"""Answer: <ANSWER>\nExplanation: <EXPLANATION>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "amount":
        question_prompt += f"""Amount: <AMOUNT>\nExplanation: <EXPLANATION>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_007(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 007"""
    question_prompt = f"""Imagine you are a legal professional in the United States. Please answer the question below in this format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""Best Choice: <CHOICE>\nWorst Choice: <CHOICE>\n\n"""

        question_prompt += f"""{question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"

        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "short_answer":
        question_prompt += f"""Answer: <ANSWER>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "amount":
        question_prompt += f"""Amount: <AMOUNT>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_008(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 007"""
    question_prompt = f"""Imagine you are a legal professional in the United States. Please answer the question below in this format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""Best Choice: <CHOICE>\nWorst Choice: <CHOICE>\nExplanation: <EXPLANATION>\n\n"""

        question_prompt += f"""Question: {question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"

        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "short_answer":
        question_prompt += f"""Answer: <ANSWER>\nExplanation: <EXPLANATION>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "amount":
        question_prompt += f"""Amount: <AMOUNT>\nExplanation: <EXPLANATION>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_009(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 009"""
    question_prompt = f"""Imagine you are a tax professional in the United States. Please answer the question below in this format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""Best Choice: <CHOICE>\nWorst Choice: <CHOICE>\nExplanation: <EXPLANATION>\n\n"""

        question_prompt += f"""Question: {question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"

        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "short_answer":
        question_prompt += f"""Answer: <ANSWER>\nExplanation: <EXPLANATION>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "amount":
        question_prompt += f"""Amount: <AMOUNT>\nExplanation: <EXPLANATION>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_010(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 010"""
    question_prompt = f"""Imagine you are an accountant in the United States.  Please answer the question below in this format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""Best Choice: <CHOICE>\nWorst Choice: <CHOICE>\nExplanation: <EXPLANATION>\n\n"""

        question_prompt += f"""Question: {question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"

        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "short_answer":
        question_prompt += f"""Answer: <ANSWER>\nExplanation: <EXPLANATION>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    elif question_data["question_type"] == "amount":
        question_prompt += f"""Amount: <AMOUNT>\nExplanation: <EXPLANATION>\n\n"""
        question_prompt += f"""{question_data['question']}\n"""
        question_prompt += f"""\nAnswer:"""
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_011(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 011"""
    question_prompt = f"""Please answer the following CPA exam question in this rank order format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""First Choice: <LETTER>\nSecond Choice: <LETTER>\nThird Choice: <LETTER>\nExplanation: <EXPLANATION>\n\n"""

        question_prompt += f"""Question: {question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"
        question_prompt += "####\n"
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_012(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 012"""
    question_prompt = f"""Imagine you are an accountant in the United States.  Please answer the question below in this rank order format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""First Choice: <LETTER>\nSecond Choice: <LETTER>\nThird Choice: <LETTER>\nExplanation: <EXPLANATION>\n\n"""

        question_prompt += f"""Question: {question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"
        question_prompt += "####\n"
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_013(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 013"""
    question_prompt = f"""Imagine you are a tax professional in the United States.  Please answer the question below in this rank order format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""First Choice: <LETTER>\nSecond Choice: <LETTER>\nThird Choice: <LETTER>\nExplanation: <EXPLANATION>\n\n"""

        question_prompt += f"""Question: {question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"
        question_prompt += "####\n"
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_014(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 014"""
    question_prompt = f"""Imagine you are a legal professional in the United States.  Please answer the question below in this rank order format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""First Choice: <LETTER>\nSecond Choice: <LETTER>\nThird Choice: <LETTER>\nExplanation: <EXPLANATION>\n\n"""

        question_prompt += f"""Question: {question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"
        question_prompt += "####\n"
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_015(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 015"""
    question_prompt = f"""Imagine you are a Big 4 accountant in the United States.  Please answer the question below in this rank order format.\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""First Choice: <LETTER>\nSecond Choice: <LETTER>\nThird Choice: <LETTER>\nExplanation: <EXPLANATION>\n\n"""

        question_prompt += f"""----\nQuestion: {question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"
        question_prompt += "####\n"
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_016(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 011"""
    question_prompt = f"""Imagine you're designing the CPA exam.  Rank order the questions from most to least correct in this format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""---\nFirst Choice: <LETTER>\nSecond Choice: <LETTER>\nThird Choice: <LETTER>\nExplanation: <EXPLANATION>\n---\n"""

        question_prompt += f"""Question: {question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"
        question_prompt += "####\n"
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_017(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 011"""
    question_prompt = f"""Imagine you're taking the CPA exam.  Please answer the question in this format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""---\nFirst Choice: <LETTER>\nSecond Choice: <LETTER>\nThird Choice: <LETTER>\nExplanation: <EXPLANATION OF FIRST CHOICE> <REFERENCES OR CITATIONS TO AUTHORITY>\n---\n"""

        question_prompt += f"""Question: {question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"
        question_prompt += "####\n"
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_018(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 011"""
    question_prompt = f"""Imagine you're taking the CPA exam.  Please answer the question in this format:\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""---\nFirst Choice: <LETTER>\nSecond Choice: <LETTER>\nThird Choice: <LETTER>\nExplanation: <EXPLANATION>; <REFERENCES OR CITATIONS TO AUTHORITY>\n---\n"""

        question_prompt += f"""Question: {question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"
        question_prompt += "####\n"
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_019(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 011"""
    question_prompt = f"""Imagine you're taking the CPA exam.  Please answer the question using the format below.\n"""
    question_prompt += f"""Use high-quality references or citations to legal or regulatory authorities or accounting standards to choose the best answer.\n"""

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""---\nFirst Choice: <LETTER>\nSecond Choice: <LETTER>\nThird Choice: <LETTER>\nExplanation: <EXPLANATION>"""
        question_prompt += (
            f"References: <REFERENCES OR CITATIONS TO AUTHORITY>\n---\n" ""
        )

        question_prompt += f"""Question: {question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"
        question_prompt += "####\n"
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt


def generate_prompt_020(question_data: dict) -> str:
    """Generate a question prompt to send to GPT-3 API in prompt style 011"""
    question_prompt = (
        f"""Please answer the CPA exam question below using this format:\n"""
    )

    # if multiple choice, list the choices
    if question_data["question_type"] == "multiple_choice":
        question_prompt += f"""---\nFirst Choice: <LETTER>\nSecond Choice: <LETTER>\nThird Choice: <LETTER>\n"""
        question_prompt += f"""Explanation: <EXPLAIN WHY YOUR FIRST CHOICE IS MOST LIKELY AND OTHERS CHOICES ARE LESS LIKELY OR INCORRECT>\n"""
        question_prompt += f"""References: <REFERENCES OR CITATIONS TO AUTHORITY LIKE US Code, CFR, AICPA material, FASB Standards, or common law>\n---\n"""

        question_prompt += f"""Question: {question_data['question']}\n"""
        for choice in question_data["choices"]:
            question_prompt += f"{choice}. {question_data['choices'][choice]}\n"
        question_prompt += "####\n"
    else:
        raise ValueError(f"Unknown question type {question_data['question_type']}")

    return question_prompt
