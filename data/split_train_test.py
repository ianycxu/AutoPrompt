import os
import json
import random
import copy

import fire

input_data_path = os.path.join(os.path.dirname(__file__), 'bigbench-ii')
output_data_path = os.path.join(os.path.dirname(__file__), 'bigbench-ii_split')

# Get a list of tasks (by looking at the names of the files in the induced directory)
tasks = [f.split('.')[0] for f in os.listdir(input_data_path)]

def split_train_test(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    examples = data['examples']
    num_examples = len(examples)

    indices = random.sample(range(num_examples) , int(num_examples * 0.2))
    train_examples = [examples[i] for i in range(num_examples) if i not in indices]
    test_examples = [examples[i] for i in range(num_examples) if i in indices]

    train = copy.deepcopy(data)
    test = copy.deepcopy(data)

    train['examples'] = train_examples
    test['examples'] = test_examples

    assert num_examples == len(train['examples']) + len(test['examples'])
    return train, test


def run():
    
    for task in tasks:
        file_path = os.path.join(input_data_path, task, "task.json")
        train, test = split_train_test(file_path)

        if not os.path.exists(os.path.join(output_data_path, task, "train")):
            os.makedirs(os.path.join(output_data_path, task, "train"))
        with open(os.path.join(output_data_path, task, "train","task.json"), 'w+', encoding="utf-8") as f:
            json.dump(train , f)

        if not os.path.exists(os.path.join(output_data_path, task, "test")):
            os.makedirs(os.path.join(output_data_path, task, "test"))
        with open(os.path.join(output_data_path, task, "test","task.json"), 'w+', encoding="utf-8") as f:
            json.dump(test , f)


if __name__ == '__main__':
    fire.Fire(run)