questions = {"answers": [], "question": {}}
for i in range(4):  # Предположим, что нам нужно 4 элемента
    item = {
        "like_count": i,  # Значение like_count будет целым числом, равным i
        "answer": "First of all I would like to thank you for the invitation to participate in such a … Russia is the huge territory which in many respects needs to be render habitable.",
        "isChecked": True,
        "image_url":"./../static/img/porshe.jpg",
    }
    questions["answers"].append(item)
# Создаем вопрос
questions["question"] = {
    "like_count": 1,  # Значение like_count будет целым числом
    "title": "What 1?",  # Заголовок будет уникальным для каждого элемента
    "desc": "me is desc",
    "answer_count": str(len(questions['answers'])),  # Значение answer_count будет строкой
    "tags": ['python', 'c++', 'c#', 'unity'],
    "image_url":"./../static/img/porshe.jpg",
}