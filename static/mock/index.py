data = {"data": []}
for i in range(4):  # Предположим, что нам нужно 4 элемента
    item = {
        "like_count": str(i),  # Значение like_count будет строкой, равной i
        "title": "How to deal with the CORS",  # Заголовок будет уникальным для каждого элемента
        "desc": f"What {i}?",
        "answer_count": str(i * 5),  # Значение answer_count будет равным i * 5
        "tags": ['python', 'c++', 'c#', 'unity'],
    }
    data["data"].append(item)