
def calculator():
    answer_history = []
    while True:
        expression = input('Please input a mathematical expression: ')

        try:
            result = eval(expression)
            print(result)
            answer_history.append(result)
        except ZeroDivisionError:
            print('Division by Zero!') #handles zero error
        except Exception as e:
            print(f'Error: {e}') #handles other errors

        history_question = input('Do you want to see your history of calculations?(YES/NO): ')
        if history_question.upper() == 'YES':
            print(answer_history)

        question = input('Do you want to perform another calculation?(YES/NO): ')
        if question.upper() != 'YES':
            break


calculator()



