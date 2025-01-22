import { useState, useEffect } from 'react';
import TodoForm from './components/TodoForm';
import TodoList from './components/TodoList';
import { fetchTodos, createTodo, updateTodo, deleteTodoRequest } from './api';
import './App.css';

const App = () => {
  const [todos, setTodos] = useState([]);
  const [editingTodo, setEditingTodo] = useState(null);

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    try {
      const data = await fetchTodos();
      setTodos(data);
    } catch (error) {
      console.error('Error fetching todos:', error);
    }
  };

  const handleAddTodo = async (title, description) => {
    try {
      await createTodo({ title, description, completed: false });
      loadTodos();
    } catch (error) {
      console.error('Error adding todo:', error);
    }
  };

  const handleToggleTodo = async (id, completed) => {
    const todo = todos.find(t => t._id === id);
    try {
      await updateTodo(id, { ...todo, completed });
      loadTodos();
    } catch (error) {
      console.error('Error toggling todo:', error);
    }
  };

  const handleDeleteTodo = async (id) => {
    try {
      await deleteTodoRequest(id);
      loadTodos();
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  const handleEditTodo = (id, title, description) => {
    setEditingTodo({ id, title, description });
  };

  const handleSaveTodo = async (id, title, description) => {
    try {
      await updateTodo(id, { title, description, completed: false });
      setEditingTodo(null);
      loadTodos();
    } catch (error) {
      console.error('Error saving todo:', error);
    }
  };

  return (
    <div className="App">
      <h1>Mi Lista de Tareas</h1>
      <TodoForm onAddTodo={handleAddTodo} />
      <TodoList
        todos={todos}
        onToggleTodo={handleToggleTodo}
        onDeleteTodo={handleDeleteTodo}
        onEditTodo={handleEditTodo}
        editingTodo={editingTodo}
        onSaveTodo={handleSaveTodo}
      />
    </div>
  );
};

export default App;
