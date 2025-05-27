function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

const csrftoken = getCookie('csrftoken')
const likeButtons = document.querySelectorAll('button[data-image-id]')
console.log(likeButtons)
for (const item of likeButtons) {
  // console.log(item)
  item.addEventListener('click', (e) => {
    const request = new Request(`/question/${item.dataset.imageId}/like/`, {
      method: 'POST',
      body: new URLSearchParams({
        key1: 'value1',
        key2: 2,
      }),
      headers: { 'X-CSRFToken': csrftoken },
      mode: 'same-origin',
    })

    fetch(request).then((response) => {
      response.json().then((data) => {
        const path = document.querySelector(`path[data-path-id="${item.dataset.imageId}"]`)
        if (!data.isLiked) {
          path.style.fill = '#0F0F0F'
        } else {
          path.style.fill = '#00FF00'
        }
        const counter = document.querySelector(`p[data-like-counter="${item.dataset.imageId}"]`)
        counter.innerHTML = data.likes_count
      })
    })
  })
}

const likeAnswerButtons = document.querySelectorAll('button[data-answer-image-id]')
console.log(likeAnswerButtons)

for (const item of likeAnswerButtons) {
  item.addEventListener('click', (e) => {
    // console.log(item.dataset)
    const request = new Request(`/answer/${item.dataset.answerImageId}/like/`, {
      method: 'POST',
      body: new URLSearchParams({
        key1: 'value1',
        key2: 2,
      }),
      headers: { 'X-CSRFToken': csrftoken },
      mode: 'same-origin',
    })

    fetch(request).then((response) => {
      response.json().then((data) => {
        const path = document.querySelector(`path[data-answer-path-id="${item.dataset.answerImageId}"]`)
        if (!data.isLiked) {
          path.style.fill = '#0F0F0F'
        } else {
          path.style.fill = '#00FF00'
        }
        const counter = document.querySelector(`p[data-answer-like-counter="${item.dataset.answerImageId}"]`)
        console.log(counter)
        counter.innerHTML = data.likes_count
      })
    })
  })
}
