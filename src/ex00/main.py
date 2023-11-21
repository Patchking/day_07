import argparse, random, json

def is_a_lie(resp, heart, blush, pop):
    score = 0
    if not 12 <= resp <= 16:
        score += 1
    if not 60 <= heart <= 100:
        score += 1
    if not blush >= 5:
        score += 1
    if not 2 <= pop <= 8:
        score += 1
    if score >= 2:
        return True
    return False

def get_int(minlim, maxlim):
    while True:
        wrong_input_ans = "Wrong input. Try again"
        got_in = input()
        if not got_in.isdigit():
            print(wrong_input_ans)
            continue
        got_in = int(got_in)
        if not minlim <= got_in <= maxlim:
            print(wrong_input_ans)
            continue
        break
    return got_in

def print_survay(filename, ask_for_state):

    try:
        with open(filename) as f:
            questions_list = json.load(f)
    except FileNotFoundError as e:
        print("File not found")
        return None

    questions_list = random.sample(questions_list, 10)
    answer_list = []
    for que in questions_list:
        print(que["text"])
        i = 1
        for ans in que["options"]:
            print(f"{i}. {ans}", end=" ")
            i += 1
        print()
        curans = get_int(1, len(que["options"])) - 1
        if ask_for_state:
            print("\nEnter resperation, heart rate, blushing level and pupillary dilation")
            curansstate = [get_int(0, 9999) for _ in range(4)]
            if not is_a_lie(*curansstate):
                answer_list.append(que["coefficients"][curans])
        else:
            answer_list.append(que["coefficients"][curans])
        
    mid = sum(answer_list) / len(answer_list)
    return True if mid <= 0.5 else False



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--question-file")
    parser.add_argument("-a", "--ask-for-state", action="store_false")
    args = parser.parse_args()

    question_file = "questions.json"
    ask_for_state = True
    if args.question_file:
        question_file = args.question_file
    ask_for_state = args.ask_for_state

    print(print_survay(question_file, ask_for_state))

    