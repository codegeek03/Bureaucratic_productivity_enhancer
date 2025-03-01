// Chat functionality
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendMessage = document.getElementById('sendMessage');

// Todo functionality
const todoInput = document.getElementById('todoInput');
const addTodo = document.getElementById('addTodo');
const todoList = document.getElementById('todoList');

// Load todos from localStorage
let todos = JSON.parse(localStorage.getItem('todos')) || [];

// Chat Functions
function addMessage(message, isUser = true) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function handleChatSubmit() {
    const message = chatInput.value.trim();
    if (message) {
        addMessage(message, true);
        // Simulate bot response
        setTimeout(() => {
            addMessage('This is a demo response from the chatbot!', false);
        }, 1000);
        chatInput.value = '';
    }
}

// Todo Functions
function saveTodos() {
    localStorage.setItem('todos', JSON.stringify(todos));
}

function createTodoElement(todo) {
    const li = document.createElement('li');
    li.classList.add('todo-item');
    if (todo.completed) {
        li.classList.add('completed');
    }

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.classList.add('checkbox');
    checkbox.checked = todo.completed;
    checkbox.addEventListener('change', () => toggleTodo(todo.id));

    const todoText = document.createElement('span');
    todoText.classList.add('todo-text');
    todoText.textContent = todo.text;

    const deleteButton = document.createElement('button');
    deleteButton.classList.add('delete-todo');
    deleteButton.innerHTML = '<i class="fas fa-trash"></i>';
    deleteButton.addEventListener('click', () => deleteTodo(todo.id));

    li.appendChild(checkbox);
    li.appendChild(todoText);
    li.appendChild(deleteButton);

    return li;
}

function renderTodos() {
    todoList.innerHTML = '';
    todos.forEach(todo => {
        todoList.appendChild(createTodoElement(todo));
    });
}

function addTodoItem() {
    const text = todoInput.value.trim();
    if (text) {
        const todo = {
            id: Date.now(),
            text,
            completed: false
        };
        todos.push(todo);
        saveTodos();
        renderTodos();
        todoInput.value = '';
    }
}

function deleteTodo(id) {
    todos = todos.filter(todo => todo.id !== id);
    saveTodos();
    renderTodos();
}

function toggleTodo(id) {
    todos = todos.map(todo =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
    );
    saveTodos();
    renderTodos();
}

// Event Listeners
sendMessage.addEventListener('click', handleChatSubmit);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleChatSubmit();
    }
});

addTodo.addEventListener('click', addTodoItem);
todoInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addTodoItem();
    }
});

// Initial render
renderTodos();

// Add some sample messages to the chat
setTimeout(() => {
    addMessage('Welcome to the chat! 👋', false);
    addMessage('How can I help you today?', false);
}, 500);