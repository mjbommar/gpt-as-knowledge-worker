<div style="font-size: 2em;text-align: center; padding-bottom: 8px;">
    <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4322372"><span>GPT as Knowledge Worker</span></a>
    <br />
    <span>A Zero-Shot Evaluation of (AI)CPA Capabilities</span>
</div>
<div style="font-size: 1.2em; text-align: center; padding-top: 4px; padding-bottom: 8px; border-bottom: 4px solid rgba(0.5, 0.5, 0.5, 0.25);">
    <span><a href="" target="_blank">Jillian Bommarito</a></span>, 
    <span><a href="" target="_blank">Michael Bommarito</a></span>,
    <span><a href="" target="_blank">Daniel Martin Katz</a></span>,
    <span><a href="" target="_blank">Jessica Katz</a></span><br />
    <span><a href="" target="_blank">273 Ventures, LLC</a></span>
</div>
<div style="width: 95%; font-size: 1.1em;text-align: justify; padding-left: 16px; padding-right: 4px;">
    <p>Abstract:</p>
    <p>
        The global economy is increasingly dependent on knowledge workers to meet the needs of public and private
        organizations. While there is no single definition of knowledge work, organizations and industry groups still
        attempt to measure individuals' capability to engage in it. One of the most comprehensive assessments of
        capability readiness for professional knowledge workers is the Uniform CPA Examination developed by the 
        American Institute of Certified Public Accountants (AICPA). In this paper, we experimentally evaluate OpenAI’s
        `text-davinci-003` and prior versions of GPT on both a sample Regulation (REG) exam and a battery of 
        over 200 questions based on the AICPA Blueprints for legal, financial, accounting, technology, and ethical 
        tasks.  First, we find that `text-davinci-003` achieves a correct rate of 14.4% on a real REG exam
        section, significantly underperforming test-takers on quantitative reasoning in zero-shot prompts.  Second, we 
        find that `text-davinci-003 is approaching human-level performance on the Remembering \& Understanding 
        and Application skill levels in the Exam absent calculation.  For best prompt and parameters, the model answers
        57.6% of questions correctly, significantly better than the 25% guessing rate, and its top two answers are
        correct 82.1% of the time, indicating strong non-entailment. Finally, we find that recent generations of 
        GPT-3 demonstrate material improvements on this assessment, rising from 30% for `text-davinci-001` to
        57% for `text-davinci-003`.  These findings strongly suggest that large language models have the
        potential to transform the quality and efficiency of knowledge work.
    </p>
</div>
<hr />

### Suggestions or Corrections
Do you think you've found a mistake or ambiguity in the questions?

Want to suggest additional questions for inclusion into future updates to the paper?

Please use the GitHub Issue tracker here to submit your ideas.  Thank you!


## Links
* [Questions for Assessment 2](data/questions_02.txt) 
* [Prompts](src/prompts.py)
* [Run experimental assessments](src/run_exam.py)
* [Run experimental assessments with older models](src/run_exam_old_models.py)
* [Score assessment resutls](src/score_exam.py)
* [Export sessions to HTML for review](src/export_session_html.py)

## Figures
### Performance over Time on Assessment 2
<picture>
   <img src="https://github.com/mjbommar/gpt-as-knowledge-worker/blob/main/figures/model_progression.png?raw=true" />
 </picture>

### Performance by Section in Assessment 2
<picture>
   <img src="https://github.com/mjbommar/gpt-as-knowledge-worker/blob/main/figures/best_model_performance_by_section.png?raw=true" />
 </picture>

