async function postJson(url, data) {
  const resp = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });
  return await resp.json();
}

function showLoading(resultElement) {
  resultElement.innerHTML = '<div class="loading"></div><span class="ms-2">Computing...</span>';
  resultElement.className = 'result-container result-placeholder';
}

function showResult(resultElement, result) {
  if (result.error) {
    resultElement.innerHTML = `<i class="fas fa-exclamation-triangle me-2"></i>Error: ${result.error}`;
    resultElement.className = 'result-container result-error';
  } else {
    resultElement.innerHTML = `<i class="fas fa-check-circle me-2"></i>Result: ${result.result}`;
    resultElement.className = 'result-container result-success';
  }
}

document.getElementById('pow-form').addEventListener('submit', async e => {
  e.preventDefault();
  const resultElement = document.getElementById('pow-result');
  showLoading(resultElement);

  const base = parseFloat(document.getElementById('base').value);
  const exponent = parseFloat(document.getElementById('exponent').value);

  try {
    const result = await postJson('/pow', { base, exponent });
    showResult(resultElement, result);
  } catch (error) {
    showResult(resultElement, { error: 'Network error' });
  }
});

document.getElementById('fib-form').addEventListener('submit', async e => {
  e.preventDefault();
  const resultElement = document.getElementById('fib-result');
  showLoading(resultElement);

  const n = parseInt(document.getElementById('fib-n').value);

  try {
    const result = await postJson('/fibonacci', { n });
    showResult(resultElement, result);
  } catch (error) {
    showResult(resultElement, { error: 'Network error' });
  }
});

document.getElementById('fact-form').addEventListener('submit', async e => {
  e.preventDefault();
  const resultElement = document.getElementById('fact-result');
  showLoading(resultElement);

  const n = parseInt(document.getElementById('fact-n').value);

  try {
    const result = await postJson('/factorial', { n });
    showResult(resultElement, result);
  } catch (error) {
    showResult(resultElement, { error: 'Network error' });
  }
});