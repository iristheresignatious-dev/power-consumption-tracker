// ===== GET ALL ELEMENTS FROM HTML =====
const resumeFile = document.getElementById('resumeFile');
const fileName = document.getElementById('fileName');
const jobDesc = document.getElementById('jobDesc');
const analyzeBtn = document.getElementById('analyzeBtn');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const scoreValue = document.getElementById('scoreValue');
const strengthsList = document.getElementById('strengthsList');
const weaknessesList = document.getElementById('weaknessesList');
const keywordsList = document.getElementById('keywordsList');


// ===== SHOW FILE NAME WHEN USER PICKS A FILE =====
resumeFile.addEventListener('change', function() {
  if (resumeFile.files.length > 0) {
    fileName.textContent = resumeFile.files[0].name;
  } else {
    fileName.textContent = 'No file chosen';
  }
});


// ===== WHEN ANALYZE BUTTON IS CLICKED =====
analyzeBtn.addEventListener('click', async function() {

  // check if user uploaded a file
  if (!resumeFile.files[0]) {
    alert('Please upload a resume first!');
    return;
  }

  // show loading, hide results, disable button
  showLoading();

  try {

    // build the form data to send to backend
    const formData = new FormData();
    formData.append('resume', resumeFile.files[0]);
    formData.append('jobDescription', jobDesc.value);

    // send to backend
    const response = await fetch('http://127.0.0.1:8000/analyze', {
      method: 'POST',
      body: formData
    });

    // check if backend returned an error
    if (!response.ok) {
      throw new Error('Server error. Please try again.');
    }

    // convert response to javascript object
    const result = await response.json();

    // print result in console so you can see what backend returns
    console.log('Backend returned:', result);

    // display the results on screen
    displayResults(result);

  } catch (error) {
    // something went wrong
    hideLoading();
    alert('Error: ' + error.message);
  }

});


// ===== SHOW LOADING STATE =====
function showLoading() {
  loading.classList.remove('hidden');   // show loading
  results.classList.add('hidden');      // hide old results
  analyzeBtn.disabled = true;           // disable button
  analyzeBtn.textContent = 'Analyzing...';
}


// ===== HIDE LOADING STATE =====
function hideLoading() {
  loading.classList.add('hidden');      // hide loading
  analyzeBtn.disabled = false;          // enable button
  analyzeBtn.textContent = 'Analyze Resume';
}


// ===== DISPLAY RESULTS ON SCREEN =====
function displayResults(data) {

  hideLoading();

  // ===== FIX: if data is wrapped in an extra layer, unwrap it =====
  if (data.result) data = data.result;

  // ===== FIX: use safe fallbacks so forEach never crashes =====
  const score     = data.score      || 0;
  const strengths = data.strengths  || [];
  const weaknesses= data.weaknesses || [];
  const keywords  = data.keywords   || [];

  // show the score
  scoreValue.textContent = score + '/100';

  // color the score based on value
  scoreValue.className = 'score';
  if (score >= 75) {
    scoreValue.classList.add('high');    // green
  } else if (score >= 50) {
    scoreValue.classList.add('mid');     // yellow
  } else {
    scoreValue.classList.add('low');     // orange
  }

  // fill strengths list
  strengthsList.innerHTML = '';
  strengths.forEach(function(item) {
    const li = document.createElement('li');
    li.textContent = item;
    strengthsList.appendChild(li);
  });

  // fill weaknesses list
  weaknessesList.innerHTML = '';
  weaknesses.forEach(function(item) {
    const li = document.createElement('li');
    li.textContent = item;
    weaknessesList.appendChild(li);
  });

  // fill missing keywords list
  keywordsList.innerHTML = '';
  keywords.forEach(function(item) {
    const li = document.createElement('li');
    li.textContent = item;
    keywordsList.appendChild(li);
  });

  // show results section
  results.classList.remove('hidden');

  // smoothly scroll down to results
  results.scrollIntoView({ behavior: 'smooth' });

}


// ===== MOCK DATA FOR TESTING (use this before backend is ready) =====
function getMockResult() {
  return {
    score: 78,
    strengths: [
      'Strong work experience section',
      'Good use of action verbs',
      'Clear contact information'
    ],
    weaknesses: [
      'Missing skills section',
      'No measurable achievements',
      'Summary section too vague'
    ],
    keywords: [
      'Python',
      'Machine Learning',
      'REST API',
      'Agile'
    ]
  };
}

