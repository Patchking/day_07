import argparse, random, json, logging

def is_it_truth(resp: int, heart: int, blush: int, pop: int) -> bool:
    """
    Check weather interviewee lie or not

    Attributes
    -----------
    resp
        Respiration (measured in BPM, normally around 12-16 breaths per minute)
    heart
        Respiration (measured in BPM, normally around 12-16 breaths per minute)
    blush
        Blushing level (categorical, 6 possible levels)
    pop
        Pupillary dilation (current pupil size, 2 to 8 mm)

    return value
    -----------
    Answer on question
    """
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

def get_int(minlim: int, maxlim: int) -> int:
    """
    Trying to get the value between minlim and maxlim in loop.
    Nums can be negative. 
    If minlim more then maxlim raise ValueError
    """
    if minlim >= maxlim:
        raise ValueError("minlim should be less then maxlim")
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
    "Get list from file. File must be json."
    with open(filename) as f:
        questions_list = json.load(f)
    return questions_list

def print_survay(filename: str, ask_for_state: bool) -> str:
    """
    Main part of program. 

    Attributes
    ---------
    filename
        The name of file with questions
    ask_for_state
        Weather or not programm will check health parameters to determinate do interviewee lie

    Return
    ---------
    Answer on question
    """
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


    