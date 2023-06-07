""" Run this script to 
    1. use our proposed method to generate prompt
    2. evaluate prompt 
"""

import random

import fire

from automatic_prompt_engineer import ape, data
from experiments.data.instruction_induction.load_data import load_data, tasks
from experiments.evaluation.instruction_induction.exec_accuracy import exec_accuracy_evaluator


def run(task):
    
    """Steps (not iterative):
    1. Split data into train and test                 data\split_train_test.py
    3. Aether to get r_i of every (xi, yi) in train   data\generate_prompts_for_dv3.py
    4. Read all r_i of each task
    5. Summarize r_i into r 
    6. Evaluate prompt in test
    """

    # induce_data, test_data = load_data('induce', task), load_data('eval', task)  # Need to change this load_data to load GPT-4 generated Reasoning

    # Get size of the induce data
    induce_data_size = len(induce_data[0])
    prompt_gen_size = min(int(induce_data_size * 0.5), 100)
    # Induce data is split into prompt_gen_data and eval_data
    prompt_gen_data, eval_data = data.create_split(
        induce_data, prompt_gen_size)


    eval_template = "Instruction: [PROMPT]\n\nInput: [INPUT]\nOutput: [OUTPUT]"
    prompt_gen_template = "I gave a friend a instruction. Based on the instruction they produced " \
                          "the following input-output pairs:\n\n[full_DEMO]\n\nThe instruction was to [APE]"
    demos_template = "Input: [INPUT]\nOutput: [OUTPUT]"

    base_config = '../experiments/configs/instruction_induction.yaml'
    conf = {
        'generation': {
            'num_subsamples': 3,
            'num_demos': 5,
            'num_prompts_per_subsample': 30,
            'model': {
                'gpt_config': {
                    # 'model': 'text-ada-001'
                }
            }
        },
        'evaluation': {
            'method': exec_accuracy_evaluator,
            'task': task,
            'num_samples': min(20, len(eval_data[0])),
            'model': {
                'gpt_config': {
                    # 'model': 'text-ada-001'
                }
            }
        }
    }

    res, demo_fn = ape.find_prompts(eval_template=eval_template,
                                    prompt_gen_data=prompt_gen_data,
                                    eval_data=eval_data,
                                    conf=conf,
                                    base_conf=base_config,
                                    few_shot_data=prompt_gen_data,
                                    demos_template=demos_template,
                                    prompt_gen_template=prompt_gen_template)

    print('Finished finding prompts.')
    prompts, scores = res.sorted()
    print('Prompts:')
    for prompt, score in list(zip(prompts, scores))[:10]:
        print(f'  {score}: {prompt}')

    # Evaluate on test data
    print('Evaluating on test data...')

    test_conf = {
        'generation': {
            'num_subsamples': 3,
            'num_demos': 5,
            'num_prompts_per_subsample': 30,
            'model': {
                'gpt_config': {
                    # 'model': 'text-ada-001'
                }
            }
        },
        'evaluation': {
            'method': exec_accuracy_evaluator,
            'task': task,
            'num_samples': min(100, len(test_data[0])),
            'model': {
                'gpt_config': {
                    # 'model': 'text-ada-001'
                }
            }
        }
    }

    test_res = ape.evaluate_prompts(prompts=[prompts[0]],
                                    eval_template=eval_template,
                                    eval_data=test_data,
                                    few_shot_data=prompt_gen_data,
                                    demos_template=demos_template,
                                    conf=test_conf,
                                    base_conf=base_config)

    test_score = test_res.sorted()[1][0]
    print(f'Test score: {test_score}')

    # Save a text file to experiments/results/instruction_induction/task.txt with the best prompt and test score
    with open(f'experiments/results/instruction_induction/{task}.txt', 'w') as f:
        f.write(f'Test score: {test_score}\n')
        f.write(f'Prompt: {prompts[0]}\n')


if __name__ == '__main__':
    fire.Fire(run)
