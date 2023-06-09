import pandas as pd 
import os
import sys

def get_representative(reasoning_results, sample_number = 5, sample_method = "random_balanced"):
    """Use cluster (based on r or x,y,r) or random sample method to get a subset of reasoning results

    """
    if sample_method == "random":
        return reasoning_results.sample(n = sample_number)
    elif sample_method == "random_balanced" or sample_method == "random_balanced_separate":
        return reasoning_results.groupby('output', group_keys=False).apply(lambda x: x.sample(sample_number))
    else:
        # TODO: clustering based
        return reasoning_results


def form_prompt(template, reasoning_results, description, sample_method):
    
    template = template.replace("[DESC]", description)
    
    data = "\n"
    if sample_method == "random_balanced_separate":
        for label in reasoning_results['output'].value_counts().index:
            seg_df = reasoning_results[reasoning_results['output'] == label]
            seg_data = f"Cases for category: {label} \n"
            i = 1
            for index, row in seg_df.iterrows():
                seg_data += f"Data point {i}" + "\n"
                seg_data += "Input: "  + row["input"] + "\n"
                seg_data += "Output: "  + row["output"] + "\n"
                seg_data += "Reason: "  + row["answer"].replace(":\\n\\n","") + "\n\n"
                i += 1
            data += seg_data
    else:
        i = 1
        for index, row in reasoning_results.iterrows():
            data += f"Data point {i}" + "\n"
            data += "Input: "  + row["input"] + "\n"
            data += "Output: "  + row["output"] + "\n"
            data += "Reason: "  + row["answer"].replace(":\\n\\n","") + "\n\n"
            i += 1


    final_prompt = template.replace("[DATA]", data)
    
    return final_prompt


def main(reasoning_results, template, description, output_path, sample_number, sample_method):

    # read files
    reasoning_results = pd.read_csv(reasoning_results, sep='\t')
    with open(template) as fin:
        template = fin.readline().strip()
    with open(description) as fin:
        description = fin.readline().strip() 

    reasoning_results = get_representative(reasoning_results, sample_number, sample_method)

    final_prompt = form_prompt(template, reasoning_results, description, sample_method)

    with open(output_path, 'w') as fout:
        fout.write(final_prompt)


if __name__ == '__main__':
    if len(sys.argv) == 7:
        input1_path = sys.argv[1]
        input2_path = sys.argv[2]
        input3_path = sys.argv[3]
        output_path = sys.argv[4]
        sample_number = int(sys.argv[5])
        sample_method = sys.argv[6]
    else:
        input1_path = '../epistemic_reasoning/reasons.tsv'
        input2_path = '../prompt template.tsv'
        input3_path = '../epistemic_reasoning/description.tsv'
        output_path = '../epistemic_reasoning/final prompt.tsv'
        sample_number = 2
        sample_method = "random_balanced_separate"

    main(input1_path, input2_path, input3_path,
         output_path, sample_number, sample_method)