document.querySelector('button').addEventListener('click', () => {
  // call your backend API here
  showResults(data)
})
const response = await fetch('/analyze', {
  method: 'POST',
  body: formData
})
const result = await response.json()