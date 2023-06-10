import os
import json
import random
import copy
from collections import defaultdict

import fire

input_data_path = os.path.join(os.path.dirname(__file__), 'bigbench-ii')
output_data_path = os.path.join(os.path.dirname(__file__), 'bigbench-ii_split')

# Get a list of tasks (by looking at the names of the files in the induced directory)
tasks = [f.split('.')[0] for f in os.listdir(input_data_path)]

def split_train_test(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    def split_data(data, ratio):
        examples = data['examples']
        total_num_examples = len(examples)
        train_examples = []
        test_examples = []

        # process label (support multi-label)
        label_based_examples = defaultdict(list)
        for example in examples:
            if "target_scores" in example:
                for k, v in example["target_scores"].items():
                    if v == 1:
                        label_based_examples[k].append(example)
            else:
                for k, v in example["target"].items():
                    if v == 1:
                        label_based_examples[k].append(example)
        

        for key, value in label_based_examples.items():
            num_examples = len(value)
            indices = random.sample(range(num_examples) , int(num_examples * ratio))
            train_examples.extend([value[i] for i in range(num_examples) if i not in indices])
            test_examples.extend([value[i] for i in range(num_examples) if i in indices])


        train = copy.deepcopy(data)
        test = copy.deepcopy(data)

        train['examples'] = train_examples
        test['examples'] = test_examples

        assert total_num_examples == len(train['examples']) + len(test['examples'])
        return train, test
    
    train, test = split_data(data, 0.4)
    dev, test = split_data(test, 0.5)
    return train, dev, test


def run():
    
    for task in tasks:
        file_path = os.path.join(input_data_path, task, "task.json")

        try:
            train, dev, test = split_train_test(file_path)
        except:
            continue

        if not os.path.exists(os.path.join(output_data_path, task, "train")):
            os.makedirs(os.path.join(output_data_path, task, "train"))
        with open(os.path.join(output_data_path, task, "train","task.json"), 'w+', encoding="utf-8") as f:
            json.dump(train , f, indent=4)

        if not os.path.exists(os.path.join(output_data_path, task, "test")):
            os.makedirs(os.path.join(output_data_path, task, "test"))
        with open(os.path.join(output_data_path, task, "test","task.json"), 'w+', encoding="utf-8") as f:
            json.dump(test , f, indent=4)

        if not os.path.exists(os.path.join(output_data_path, task, "dev")):
            os.makedirs(os.path.join(output_data_path, task, "dev"))
        with open(os.path.join(output_data_path, task, "dev","task.json"), 'w+', encoding="utf-8") as f:
            json.dump(dev , f, indent=4)


if __name__ == '__main__':
    fire.Fire(run)