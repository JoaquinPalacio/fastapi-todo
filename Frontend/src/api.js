// URL al servidor local
const API_URL = 'http://localhost:8000/todos/';
// URL al servidor
// const API_URL = 'https://todo-backend-g8fyw7qcl-joaquinpalacios-projects-95416ffb.vercel.app/todos/';

export async function fetchTodos() {
  const response = await fetch(API_URL);
  if (!response.ok) throw new Error('Error fetching todos');
  return await response.json();
}

export async function createTodo(todo) {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(todo),
  });
  if (!response.ok) throw new Error('Error creating todo');
  return await response.json();
}

export async function updateTodo(id, todo) {
  const response = await fetch(`${API_URL}${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(todo),
  });
  if (!response.ok) throw new Error('Error updating todo');
  return await response.json();
}

export async function deleteTodoRequest(id) {
  const response = await fetch(`${API_URL}${id}`, { method: 'DELETE' });
  if (!response.ok) throw new Error('Error deleting todo');
  return;
}
