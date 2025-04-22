// URL al servidor
const API_URL = import.meta.env.VITE_API_URL;

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
