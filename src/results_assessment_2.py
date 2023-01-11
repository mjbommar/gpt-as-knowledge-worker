"""
Provide results in csv/latex and various figures for Assessment 1, including:
  * headline accuracy and spread over guessing rate (25%)
  * performance by section of exam
  * performance by prompt method
  * performance by temperature
  * performance by `best of`
"""

# imports
import io
import json
import os
import textwrap
from pathlib import Path

# packages
import matplotlib.pyplot
import numpy
import pandas

# project imports
from question_data import parse_question_source

DATA_PATH = Path(os.getcwd()).parent / "data"
RESULTS_PATH = Path(os.getcwd()).parent / "results"

# add this path to the matplotlib font manager
# add all fonts under ~/.local/share/fonts/ to the matplotlib font manager
for font_file in Path("~/.local/share/fonts/").rglob("*.ttf"):
    matplotlib.font_manager.fontManager.addfont(font_file)

# set /usr/share/fonts/truetype/noto/NotoSerif-SemiCondensedThin.ttf as default font
matplotlib.font_manager.fontManager.addfont(
    Path("/usr/share/fonts/truetype/noto/NotoSerif-SemiCondensed.ttf")
)
matplotlib.rcParams["font.family"] = "Noto Serif"
matplotlib.rcParams.update({"font.size": 14})


def plot_accuracy_bar_chart(session_df: pandas.DataFrame) -> matplotlib.pyplot.Figure:
    """Plot the accuracy bar chart comparing the best model against the baseline
    guess rate."""

    # set the font size to 14
    matplotlib.pyplot.rcParams["font.size"] = 12

    # font color to 34343 80%
    matplotlib.pyplot.rcParams["text.color"] = "#343434"

    # set the background color to white
    matplotlib.pyplot.rcParams["figure.facecolor"] = "white"

    # set the axes background color to white
    matplotlib.pyplot.rcParams["axes.facecolor"] = "white"

    # set the axes grid color to white
    matplotlib.pyplot.rcParams["axes.grid"] = False

    # set grid lines to 343434
    matplotlib.pyplot.rcParams["grid.color"] = "#343434"

    # get the accuracy by section and SEM
    correct_by_section_mean = session_df.groupby("question_section")[
        "is_correct"
    ].mean()
    correct_by_section_sem = session_df.groupby("question_section")["is_correct"].sem()

    categories = list(correct_by_section_mean.index)

    # get top two correct rate and SEM
    t2_correct_by_section_mean = session_df.groupby("question_section")[
        "is_top_two_correct"
    ].mean()
    t2_correct_by_section_sem = session_df.groupby("question_section")[
        "is_top_two_correct"
    ].sem()

    # get the baseline guess rate
    baseline_guess_rate = 0.25

    # plot the 25% random chance guessing line
    matplotlib.pyplot.axhline(0.25, color="#343434", alpha=0.25, linestyle="--")

    # set ylim from 0 to 1
    matplotlib.pyplot.ylim(0, 1)

    # set the y ticks in percentages by 10% and add grid lines
    matplotlib.pyplot.yticks(
        numpy.arange(0, 1.1, 0.1),
        ["0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"],
    )
    matplotlib.pyplot.grid(axis="y", color="#787878", linewidth=1, alpha=0.25)

    # add text to annotate the 25% random chance guessing line
    matplotlib.pyplot.text(
        0.075,
        0.265,
        "Random Chance",
        ha="right",
        va="center",
        color="#343434",
        fontsize=8,
        alpha=0.75,
    )

    # add similar annotation for the GPT-3 correct average
    matplotlib.pyplot.axhline(
        numpy.mean(correct_by_section_mean), color="#343434", alpha=0.25, linestyle="--"
    )

    matplotlib.pyplot.text(
        0.075,
        # mean of GPT correct rates
        numpy.mean(correct_by_section_mean) + 0.02,
        "GPT-3.5 Average",
        ha="right",
        va="center",
        color="#343434",
        fontsize=8,
        alpha=0.75,
    )

    # plot the AICPA-reported pass rates
    aicpa_pass_rates = {
        "AUD": 0.481,
        "BEC": 0.597,
        "FAR": 0.450,
        "REG": 0.611,
    }

    # add the GPT-3 top two correct rate as very faint bars
    matplotlib.pyplot.bar(
        numpy.arange(len(categories)),
        numpy.array(t2_correct_by_section_mean),
        alpha=0.25,
        label="GPT Top Two Choices",
        capsize=10,
        hatch="////",
        color="#ffffff",
        edgecolor="#787878",
        linewidth=0.5,
        error_kw={
            "elinewidth": 2,
            "capthick": 2,
            "capsize": 16,
            # make teh error bars black
            "ecolor": "#898989",
            "alpha": 0.5,
        },
    )

    # plot the GPT-3 correct rates with prettier error bars
    matplotlib.pyplot.bar(
        numpy.arange(len(categories)),
        numpy.array(correct_by_section_mean),
        color="#F6A6A6",
        label="GPT First Choice",
        yerr=numpy.array(correct_by_section_sem),
        capsize=10,
        error_kw={
            "elinewidth": 1,
            "capthick": 1,
            "capsize": 16,
            # make teh error bars black
            "ecolor": "#787878",
            "alpha": 0.5,
        },
    )

    # plot a filled circle symbol where each section's pass rate is
    """
    matplotlib.pyplot.scatter(
        numpy.arange(len(categories)),
        [aicpa_pass_rates[category] for category in categories],
        marker=".",
        s=96,
        color="#787878",
        alpha=0.5,
        label="AICPA-Reported Pass Rates",
    )
    """

    # set the xticks with padding between the categories
    x_category_labels = numpy.array(categories)
    x_category_labels = [textwrap.fill(label, width=16) for label in x_category_labels]

    matplotlib.pyplot.xticks(
        numpy.arange(len(categories)),
        x_category_labels,
    )

    # add the legend in the order of GPT First Choice, GPT Top Two Choices, AICPA Pass Rates
    matplotlib.pyplot.legend(
        ncol=3,
        borderaxespad=0,
        frameon=False,
        fontsize=8.75,
    )

    # add the title
    matplotlib.pyplot.title(
        "GPT-3.5 Performance on Assessment 2 by Section",
        fontsize=14,
        pad=20,
    )

    # xlabel
    matplotlib.pyplot.xlabel(
        "Section",
        labelpad=1,
        fontsize=14,
    )

    # ylabel
    matplotlib.pyplot.ylabel(
        "Correct Rate",
        labelpad=2,
        fontsize=14,
    )

    # set the tight layout
    matplotlib.pyplot.tight_layout()

    # return the figure
    return matplotlib.pyplot.gcf()


def plot_accuracy_bar_chart_progression(
    all_exam_df: pandas.DataFrame,
) -> matplotlib.pyplot.Figure:
    """PLot the progression of model performance across model_name values
    in ascending performance order."""

    # create a new figure
    matplotlib.pyplot.figure(figsize=(8, 6))

    # set the font size to 14
    matplotlib.pyplot.rcParams["font.size"] = 12

    # font color to 34343 80%
    matplotlib.pyplot.rcParams["text.color"] = "#343434"

    # set the background color to white
    matplotlib.pyplot.rcParams["figure.facecolor"] = "white"

    # set the axes background color to white
    matplotlib.pyplot.rcParams["axes.facecolor"] = "white"

    # set the axes grid color to white
    matplotlib.pyplot.rcParams["axes.grid"] = False

    # set grid lines to 343434
    matplotlib.pyplot.rcParams["grid.color"] = "#343434"

    # plot horizontal line
    matplotlib.pyplot.axhline(0.25, color="#343434", alpha=0.25, linestyle="--")

    # add the title
    matplotlib.pyplot.title(
        "Progression of GPT Models on Assessment 2 (CPA Exam)",
        fontsize=14,
        pad=20,
    )

    # get values
    model_performance = all_exam_df.groupby("model_name")["is_correct"].mean()

    # add gpt-2 as 0
    model_performance["GPT-2"] = 0.0

    # cleanup titles
    model_performance.index = [
        "ada-001",
        "babbage-001",
        "curie-001",
        "davinci-001",
        "davinci-003",
        "GPT-2",
    ]

    # sort the model performance by value
    model_performance = model_performance.sort_values()

    # set the y ticks in percentages by 10% and add grid lines
    matplotlib.pyplot.yticks(
        numpy.arange(0, 1.1, 0.1),
        ["0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"],
    )
    matplotlib.pyplot.grid(axis="y", color="#787878", linewidth=1, alpha=0.25)

    # add text to annotate the 25% random chance guessing line
    matplotlib.pyplot.text(
        0.075,
        0.26,
        "Random Chance",
        ha="right",
        va="center",
        color="#343434",
        fontsize=8,
        alpha=0.75,
    )

    # plot the bar chart
    matplotlib.pyplot.bar(
        numpy.arange(len(model_performance)),
        model_performance,
        color="#F6A6A6",
        label="Model Performance",
        capsize=10,
    )

    # do the same thing between x=0 and x=1 for Q1 2019
    matplotlib.pyplot.axvline(x=0.5, color="#343434", linestyle="--", linewidth=0.5)
    matplotlib.pyplot.text(
        x=0.57,
        y=0.575,
        s="Q1 2019",
        ha="center",
        va="center",
        color="#343434",
        fontweight="bold",
        fontsize=12,
    )

    # draw a line between x=5 and x=6 to label Q4 2022
    matplotlib.pyplot.axvline(x=4.5, color="#343434", linestyle="--", linewidth=0.5)
    matplotlib.pyplot.text(
        x=4.57,
        y=0.575,
        s="Q4 2022",
        ha="center",
        va="center",
        color="#343434",
        fontweight="bold",
        fontsize=12,
    )

    # add xticks for model names
    matplotlib.pyplot.xticks(
        numpy.arange(len(model_performance)),
        model_performance.index,
    )

    # set ylim to 0.6
    matplotlib.pyplot.ylim((0, 0.6))

    # xlabel
    matplotlib.pyplot.xlabel(
        "Model",
        labelpad=4,
        fontsize=14,
    )

    # ylabel
    matplotlib.pyplot.ylabel(
        "Correct Rate",
        labelpad=2,
        fontsize=14,
    )

    # set the tight layout
    matplotlib.pyplot.tight_layout()

    # return the figure
    return matplotlib.pyplot.gcf()


if __name__ == "__main__":
    # load the questions
    question_list = parse_question_source(DATA_PATH / "questions_02.txt")

    # load the exam result data
    exam_df = pandas.read_csv(
        RESULTS_PATH / "questions-02" / "sessions-001" / "exam_results.csv",
        low_memory=False,
    )
    old_exam_df = pandas.read_csv(
        RESULTS_PATH / "questions-02" / "sessions-002" / "exam_results.csv",
        low_memory=False,
    )

    # calculate the baseline multiple choice rate by averaging 1/N, N=len(choices)
    multiple_choice_counts = []
    for question in question_list:
        if question["question_type"] == "multiple_choice":
            multiple_choice_counts.append(len(question["choices"]))

    # print key stats on counts
    print(f"Questions: {len(question_list)}")
    print(f"Exam Data: {exam_df.shape}")
    print(f"Old Model Exam Data: {old_exam_df.shape}")

    # get the number of unique sessions for both new and old
    session_count = exam_df["session_name"].unique()
    old_session_count = old_exam_df["session_name"].unique()
    print(f"Sessions: {len(session_count)}")
    print(f"Old Model Sessions: {len(old_session_count)}")

    # get performance by prompt
    prompt_performance = exam_df.groupby("prompt_method")["is_correct"].mean()

    # performance by prompts print
    print("\nPrompt Performance:")
    print(prompt_performance.sort_values(ascending=False))
    print()

    # print mean performance by prompt
    print("\nMean prompt:")
    print(prompt_performance.mean())
    print()

    # get the performance by prompt and temperature
    performance_prompt_temp_df = (
        exam_df.groupby(["prompt_method", "temperature"])["is_correct"]
        .mean()
        .reset_index()
        .sort_values("is_correct", ascending=False)
    )

    # best prompt and parameter are in the first row
    best_prompt = performance_prompt_temp_df.iloc[0]["prompt_method"]
    best_temp = performance_prompt_temp_df.iloc[0]["temperature"]
    print(f"Best Prompt: {best_prompt}")
    print(f"Best Temperature: {best_temp}")
    print(f"Worst Prompt: {performance_prompt_temp_df.iloc[-1]['prompt_method']}")
    print(f"Worst Temperature: {performance_prompt_temp_df.iloc[-1]['temperature']}")

    # get the subset of exam_df for best prompt and temp
    best_exam_df = exam_df[
        (exam_df["prompt_method"] == best_prompt)
        & (exam_df["temperature"] == best_temp)
    ]

    print(f"Best Correct / Top Two Correct:")
    print(best_exam_df["is_correct"].mean())
    print(best_exam_df["is_top_two_correct"].mean())

    # get the accuracy by section for this data
    best_performance_section_df = best_exam_df.groupby(["question_section"])[
        "is_correct"
    ].mean()
    print("\nBest Model by Section:")
    print(
        pandas.DataFrame(
            (100.0 * best_performance_section_df).sort_values(ascending=False)
        ).style.to_latex()
    )
    print()

    # now print with both is_correct and is_top_two_correct combined
    best_performance_section_df = best_exam_df.groupby(["question_section"])[
        "is_correct", "is_top_two_correct"
    ].mean()
    print("\nBest Model by Section (with top two):")
    print(
        pandas.DataFrame(
            (100.0 * best_performance_section_df).sort_values(
                "is_correct", ascending=False
            )
        ).style.to_latex()
    )

    # get the headline accuracy rate for old and new data by model name
    all_exam_df = pandas.concat([exam_df, old_exam_df])
    performance_by_model = all_exam_df.groupby("model_name")["is_correct"].mean()
    print("\nPerformance by Model:")
    print(
        pandas.DataFrame(
            (100.0 * performance_by_model).sort_values(ascending=False)
        ).style.to_latex()
    )
    print()

    # generate a bar chart of the best model performance by section
    f = plot_accuracy_bar_chart(exam_df)

    # save the pdf and png
    f.savefig("best_model_performance_by_section.pdf", dpi=300)
    f.savefig("best_model_performance_by_section.png", dpi=300)

    # get the progression bar chart
    f = plot_accuracy_bar_chart_progression(all_exam_df)
    f.savefig("model_progression.pdf", dpi=300)
    f.savefig("model_progression.png", dpi=300)
    f.show()
