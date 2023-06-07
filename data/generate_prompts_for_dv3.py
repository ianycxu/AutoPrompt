import os
import json
import random

import fire

input_data_path = os.path.join(os.path.dirname(__file__), 'bigbench-ii_split')
output_data_path = os.path.join(os.path.dirname(__file__), 'dv3prompt')

# Get a list of tasks (by looking at the names of the files in the induced directory)
# tasks = [f.split('.')[0] for f in os.listdir(input_data_path)]
tasks = ["epistemic_reasoning", "implicatures", "presuppositions_as_nli"]

def make_dv3_prompts(file_path):
    return_prompts = ""
    with open(file_path, 'r') as f:
        data = json.load(f)

    examples = data['examples']
    num_examples = len(examples)

    for i in range(num_examples):
        example = examples[i]

        if 'target_scores' in example:
            input_question, output_answer = str(example['input']), example['target_scores']
        else:
            input_question, output_answer = str(example['input']), example['target']

        # process target to be prompt friendly
        output_answer = str([k for k,v in output_answer.items() if v == 1])[2:-2]

        return_prompts += input_question + " [SEP] " + output_answer + "\n"
    
    desc = data['description']

    return return_prompts, desc


def run():
    
    for task in tasks:
        file_path = os.path.join(input_data_path, task, "train", "task.json")
        prompts, desc = make_dv3_prompts(file_path)

        if not os.path.exists(os.path.join(output_data_path, task)):
            os.makedirs(os.path.join(output_data_path, task))
        # print(prompts)
        with open(os.path.join(output_data_path, task, "task.txt"), 'w+', encoding="utf-8") as f:
            f.write(prompts)
        with open(os.path.join(output_data_path, task, "desc.txt"), 'w+', encoding="utf-8") as f:
            f.write(desc)



if __name__ == '__main__':
    fire.Fire(run)