import argparse, random, json, logging

def is_it_truth(resp, heart, blush, pop):
    score = 0
    if not 12 <= resp <= 16:
        score += 1
    if not 60 <= heart <= 100:
        score += 1
    if not blush >= 5:
        score += 1
    if not 2 <= pop <= 8:
        score += 1

    return False if score >= 2 else True

def get_int(minlim, maxlim):
    while True:
        wrong_input_ans = "Wrong input. Try again"
        got_in = input()
        if not got_in.replace("-", "").isdecimal():
            print(wrong_input_ans)
            continue
        got_in = int(got_in)
        if not minlim <= got_in <= maxlim:
            print(wrong_input_ans)
            continue
        break
    return got_in

def get_question_list(filename):
    with open(filename) as f:
        questions_list = json.load(f)
    return questions_list

def print_survay(filename, ask_for_state):
    questions_list = get_question_list(filename)
    questions_list = random.sample(questions_list, 10)
    answer_list = [0.5]
    for que in questions_list:
        print(que["text"])
        i = 1
        for ans in que["options"]:
            print(f"{i}. {ans}", end=" ")
            i += 1
        print()
        curans = get_int(1, len(que["options"])) - 1
        print(f"Just got ans {curans + 1}")
        if ask_for_state:
            print("\nEnter resperation, heart rate, blushing level and pupillary dilation")
            curansstate = [get_int(0, 500) for _ in range(4)]
            if is_it_truth(*curansstate):
                answer_list.append(que["coefficients"][curans])
        else:
            answer_list.append(que["coefficients"][curans])
        
    mid = sum(answer_list) / len(answer_list)
    return "He is a robot" if mid <= 0.5 else "He is not a robot"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--question-file")
    parser.add_argument("-a", "--ask-for-state", action="store_false")
    args = parser.parse_args()

    question_file = "questions.json"
    ask_for_state = True
    if args.question_file:
        question_file = args.question_file
    ask_for_state = args.ask_for_state
    try:
        print(print_survay(question_file, ask_for_state))
    except FileNotFoundError:
        print("File not found")
    except json.decoder.JSONDecodeError:
        print("Json file are corrupted. Are you sure that's json?")
    except KeyboardInterrupt:
        print("bye!!")

if __name__ == "__main__":
    main()


    