questions = []  # Инициализируем список items
for i in range(4):  # Предположим, что нам нужно 4 элемента
    # Создаем ответ
    
    # Если это первый элемент, создаем вопрос
    question_item = {
            "like_count": i,  # Значение like_count будет целым числом
            "title": f"What {str(i)}?",  # Заголовок будет уникальным для каждого элемента
            "desc": f"How to deal with the CORS {str(i)} ?",
            "answer_count": str(6),  # Значение answer_count будет строкой
            "tags": ['python', 'c++', 'c#', 'unity'],
            "image_url": "img/porshe.jpg",
            "answers": [],  # Добавляем первый ответ к вопросу
            "id": str(i),
        }
    
        # Если это не первый элемент, добавляем ответ к уже существующему вопросу
    for j in range(6):
        answer = {
        "like_count": j,  # Значение like_count будет целым числом, равным i
        "answer": "First of all I would like to thank you for the invitation to participate in such a … Russia is the huge territory which in many respects needs to be render habitable.",
        "isChecked": False,
        "image_url": "img/porshe.jpg",
        }
        question_item["answers"].append(answer)
    
    # Добавляем вопрос в items
    questions.append(question_item)
# Проверяем заполненную структуру
# print(questions)


# {
#     "items": [
#         {
#             "like_count": 1,
#             "title": "What 1?",
#             "desc": "me is desc",
#             "answer_count": "0",  # Это будет строка, так как изначально нет ответов
#             "tags": ["python", "c++", "c#", "unity"],
#             "image_url": "./../static/img/porshe.jpg",
#             "answers": [
#                 {
#                     "like_count": 0,
#                     "answer": "First of all I would like to thank you for the invitation to participate in such a … Russia is the huge territory which in many respects needs to be render habitable.",
#                     "isChecked": true,
#                     "image_url": "./../static/img/porshe.jpg"
#                 }
#             ]
#         },
#         {
#             "like_count": 1,
#             "title": "What 1?",
#             "desc": "me is desc",
#             "answer_count": "1",  # Здесь будет 1, так как один ответ добавлен
#             "tags": ["python", "c++", "c#", "unity"],
#             "image_url": "./../static/img/porshe.jpg",
#             "answers": [
#                 {
#                     "like_count": 0,
#                     "answer": "First of all I would like to thank you for the invitation to participate in such a … Russia is the huge territory which in many respects needs to be render habitable.",
#                     "isChecked": true,
#                     "image_url": "./../static/img/porshe.jpg"
#                 },
#                 {
#                     "like_count": 1,
#                     "answer": "First of all I would like to thank you for the invitation to participate in such a … Russia is the huge territory which in many respects needs to be render habitable.",
#                     "isChecked": true,
#                     "image_url": "./../static/img/porshe.jpg"
#                 }
#             ]
#         },
#         {
#             "like_count": 1,
#             "title": "What 1?",
#             "desc": "me is desc",
#             "answer_count": "2",  # Здесь будет 2
#             "tags": ["python", "c++", "c#", "unity"],
#             "image_url": "./../static/img/porshe.jpg",
#             "answers": [
#                 {
#                     "like_count": 0,
#                     "answer": "First of all I would like to thank you for the invitation to participate in such a … Russia is the huge territory which in many respects needs to be render habitable.",
#                     "isChecked": true,
#                     "image_url": "./../static/img/porshe.jpg"
#                 },
#                 {
#                     "like_count": 1,
#                     "answer": "First of all I would like to thank you for the invitation to participate in such a … Russia is the huge territory which in many respects needs to be render habitable.",
#                     "isChecked": true,
#                     "image_url": "./../static/img/porshe.jpg"
#                 },
#                 {
#                     "like_count": 2,
#                     "answer": "First of all I would like to thank you for the invitation to participate in such a … Russia is the huge territory which in many respects needs to be render habitable.",
#                     "isChecked": true,
#                     "image_url": "./../static/img/porshe.jpg"
#                 }
#             ]
#         },
#         {
#             "like_count": 1,
#             "title": "What 1?",
#             "desc": "me is desc",
#             "answer_count": "3",  # Здесь будет 3
#             "tags": ["python", "c++", "c#", "unity"],
#             "image_url": "./../static/img/porshe.jpg",
#             "answers": [
#                 {
#                     "like_count": 0,
#                     "answer": "First of all I would like to thank you for the invitation to participate in such a … Russia is the huge territory which in many respects needs to be render habitable.",
#                     "isChecked": true,
#                     "image_url": "./../static/img/porshe.jpg"
#                 },
#                 {
#                     "like_count": 1,
#                     "answer": "First of all I would like to thank you for the invitation to participate in such a … Russia is the huge territory which in many respects needs to be render habitable.",
#                     "isChecked": true,
#                     "image_url": "./../static/img/porshe.jpg"
#                 },
#                 {
#                     "like_count": 2,
#                     "answer": "First of all I would like to thank you for the invitation to participate in such a … Russia is the huge territory which in many respects needs to be render habitable.",
#                     "isChecked": true,
#                     "image_url": "./../static/img/porshe.jpg"
#                 },
#                 {
#                     "like_count": 3,
#                     "answer": "First of all I would like to thank you for the invitation to participate in such a … Russia is the huge territory which in many respects needs to be render habitable.",
#                     "isChecked": true,
#                     "image_url": "./../static/img/porshe.jpg"
#                 }
#             ]
#         }
#     ]
# }