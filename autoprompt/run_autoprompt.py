""" Run this script to 
    1. use our proposed method to generate prompt
    2. evaluate prompt 
"""
import fire

from prompt import SUMMERY_PROMPT, EVL_PROMPT



def get_reasoning_results(task):
    """
    Read reasoning results files from dv3 results folder

    Return:
        reasoning_results: List of str
    """
    pass

def get_representative(reasoning_results, task):
    """
    Use cluster (based on r or x,y,r) or random sample method to get a subset of reasoning results

    Return:
        reasoning_results: List of str
    """
    pass


def get_final_reasoning(reasoning_results):
    """
    Call GPT-4 to get reasoning summary

    Return:
        final_reasoning: str
    """

    # form summerize prompt
    final_prompt = SUMMERY_PROMPT
    return final_prompt
    

def evaluate(final_reasoning, task):
    """
    Evaliuate final prompt
    """

    # form eval prompt
    eval_prompt = EVL_PROMPT




def run(task):
    
    """Steps (not iterative):
    1. Split data into train and test                 data\split_train_test.py
    3. Aether to get r_i of every (xi, yi) in train   data\generate_prompts_for_dv3.py
    4. Read all r_i of each task
    5. Summarize r_i into r 
    6. Evaluate prompt in test
    """

    # load GPT-4 generated Reasoning
    reasoning_results = get_reasoning_results(task)

    # get reasoning representative
    reasoning_results = get_representative(reasoning_results, task)

    # summerize returned reasoning results throught gpt
    final_reasoning = get_final_reasoning(reasoning_results)
    

    # Evaluate on test data
    print('Evaluating on test data...')

    test_res = evaluate(final_reasoning, task) 

    test_score = test_res.sorted()[1][0]
    print(f'Test score: {test_score}')

    with open(f'autoprompt/results/{task}.txt', 'w') as f:
        f.write(f'Test score: {test_score}\n')
        f.write(f'Prompt: {prompts[0]}\n')


if __name__ == '__main__':
    fire.Fire(run)
