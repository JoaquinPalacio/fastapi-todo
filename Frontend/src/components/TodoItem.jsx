// src/components/TodoItem.js
import React, { useState } from 'react';

const TodoItem = ({ todo, onToggleTodo, onDeleteTodo, onEditTodo, editingTodo, onSaveTodo }) => {
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description);

  const handleSave = () => {
    onSaveTodo(todo._id, editTitle, editDescription);
  };

  return (
    <li className={todo.completed ? "completed" : ""}>
      {editingTodo && editingTodo.id === todo._id ? (
        <div>
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
          ></textarea>
          <button onClick={handleSave}>Guardar</button>
        </div>
      ) : (
        <div>
          <h3 className={todo.completed ? 'completed' : ''}>{todo.title}</h3>
          <p>{todo.description}</p>
          <button onClick={() => onToggleTodo(todo._id, !todo.completed)}>
            {todo.completed ? 'Desmarcar' : 'Completar'}
          </button>
          <button onClick={() => onEditTodo(todo._id, todo.title, todo.description)}>Editar</button>
          <button onClick={() => onDeleteTodo(todo._id)}>Eliminar</button>
        </div>
      )}
    </li>
  );
};

export default TodoItem;
