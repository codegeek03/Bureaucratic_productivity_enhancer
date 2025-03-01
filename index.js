// Constants
const USER = 'bibhabasuiitkgp';
const STORAGE_KEYS = {
    EVENTS: `events_${USER}`,
    TODOS: `todos_${USER}`
};

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    initializeCalendar();
    initializeTodoList();
});

// Calendar Implementation
function initializeCalendar() {
    const calendarEl = document.getElementById('calendar');
    if (!calendarEl) return;

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth'
        },
        height: 'auto',
        eventColor: '#FFD700',
        eventTextColor: '#000000',
        dateClick: function (info) {
            openEventModal(info.dateStr);
        },
        events: getStoredEvents(),
        eventDidMount: function (info) {
            // Add tooltip
            info.el.title = info.event.extendedProps.description || info.event.title;
        }
    });

    calendar.render();

    // Handle Event Modal
    const modal = document.getElementById('eventModal');
    const closeBtn = modal.querySelector('.close');
    const eventForm = document.getElementById('eventForm');

    closeBtn.onclick = () => modal.style.display = 'none';
    window.onclick = (e) => {
        if (e.target === modal) modal.style.display = 'none';
    };

    eventForm.onsubmit = function (e) {
        e.preventDefault();
        const title = document.getElementById('eventTitle').value;
        const description = document.getElementById('eventDescription').value;
        const dateTime = document.getElementById('eventDateTime').value;

        addEvent({
            title,
            description,
            start: dateTime,
            allDay: !dateTime.includes('T')
        });

        calendar.refetchEvents();
        updateUpcomingEvents();
        modal.style.display = 'none';
        this.reset();
    };

    // Initial update of upcoming events
    updateUpcomingEvents();
}

// Event Functions
function getStoredEvents() {
    return JSON.parse(localStorage.getItem(STORAGE_KEYS.EVENTS)) || [];
}

function addEvent(event) {
    const events = getStoredEvents();
    events.push({
        ...event,
        id: Date.now().toString()
    });
    localStorage.setItem(STORAGE_KEYS.EVENTS, JSON.stringify(events));
}

function updateUpcomingEvents() {
    const upcomingEventsDiv = document.getElementById('upcomingEvents');
    if (!upcomingEventsDiv) return;

    const events = getStoredEvents()
        .filter(event => new Date(event.start) >= new Date())
        .sort((a, b) => new Date(a.start) - new Date(b.start))
        .slice(0, 5);

    upcomingEventsDiv.innerHTML = events.length ? '' : '<p>No upcoming events</p>';

    events.forEach(event => {
        const date = new Date(event.start);
        const eventElement = document.createElement('div');
        eventElement.className = 'upcoming-event';
        eventElement.innerHTML = `
            <h4>${event.title}</h4>
            <p>${date.toLocaleDateString()} ${date.toLocaleTimeString()}</p>
            ${event.description ? `<p>${event.description}</p>` : ''}
        `;
        upcomingEventsDiv.appendChild(eventElement);
    });
}

function openEventModal(dateStr) {
    const modal = document.getElementById('eventModal');
    const dateTimeInput = document.getElementById('eventDateTime');
    dateTimeInput.value = dateStr + 'T00:00';
    modal.style.display = 'block';
}

// Todo List Implementation
function initializeTodoList() {
    const todoForm = document.getElementById('todoForm');
    const todoInput = document.getElementById('todoInput');

    if (!todoForm || !todoInput) return;

    loadTodos();

    todoForm.onsubmit = function (e) {
        e.preventDefault();
        const text = todoInput.value.trim();
        if (text) {
            addTodo(text);
            todoInput.value = '';
        }
    };
}

function getStoredTodos() {
    return JSON.parse(localStorage.getItem(STORAGE_KEYS.TODOS)) || [];
}

function addTodo(text) {
    const todos = getStoredTodos();
    todos.push({
        id: Date.now(),
        text,
        completed: false,
        createdAt: new Date().toISOString()
    });
    localStorage.setItem(STORAGE_KEYS.TODOS, JSON.stringify(todos));
    loadTodos();
}

function loadTodos() {
    const todoList = document.getElementById('todoList');
    if (!todoList) return;

    const todos = getStoredTodos();
    todoList.innerHTML = '';

    todos.forEach(todo => {
        const li = document.createElement('li');
        li.className = 'todo-item';
        li.innerHTML = `
            <div class="todo-content">
                <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''}>
                <span class="todo-text ${todo.completed ? 'completed' : ''}">${todo.text}</span>
            </div>
            <button class="delete-todo" title="Delete task">×</button>
        `;

        // Add event listeners
        const checkbox = li.querySelector('.todo-checkbox');
        checkbox.onchange = () => toggleTodo(todo.id);

        const deleteBtn = li.querySelector('.delete-todo');
        deleteBtn.onclick = () => deleteTodo(todo.id);

        todoList.appendChild(li);
    });
}

function toggleTodo(id) {
    const todos = getStoredTodos();
    const todo = todos.find(t => t.id === id);
    if (todo) {
        todo.completed = !todo.completed;
        localStorage.setItem(STORAGE_KEYS.TODOS, JSON.stringify(todos));
        loadTodos();
    }
}

function deleteTodo(id) {
    const todos = getStoredTodos().filter(t => t.id !== id);
    localStorage.setItem(STORAGE_KEYS.TODOS, JSON.stringify(todos));
    loadTodos();
}

function initializeCalendar() {
    const calendarEl = document.getElementById('calendar');
    if (!calendarEl) return;

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next',
            center: 'title',
            right: 'today'
        },
        height: '100%', // Set to 100% to fit container
        contentHeight: 'auto',
        aspectRatio: 1.2, // Make calendar more compact
        handleWindowResize: true,
        dayMaxEventRows: 2, // Limit number of events shown per day
        moreLinkClick: 'popover',
        eventDisplay: 'block',
        eventColor: '#FFD700',
        eventTextColor: '#000000',
        dateClick: function (info) {
            openEventModal(info.dateStr);
        },
        events: getStoredEvents(),
        eventDidMount: function (info) {
            info.el.title = info.event.extendedProps.description || info.event.title;
        },
        // Set current date
        initialDate: '2025-02-28', // Using the provided current date
        views: {
            dayGridMonth: {
                titleFormat: { year: 'numeric', month: 'short' }
            }
        }
    });

    calendar.render();

    // Adjust calendar size when window resizes
    window.addEventListener('resize', () => {
        calendar.updateSize();
    });

    // Rest of the calendar initialization code...
}

// Add this function to handle calendar size updates
function updateCalendarSize() {
    const calendar = document.querySelector('.fc');
    if (calendar) {
        const container = calendar.closest('.calendar-container');
        const containerHeight = container.offsetHeight;
        calendar.style.height = `${containerHeight}px`;
    }
}

// Call this function after calendar initialization and on window resize
window.addEventListener('load', updateCalendarSize);
window.addEventListener('resize', updateCalendarSize);

// Add some CSS styles programmatically for the calendar
document.head.insertAdjacentHTML('beforeend', `
    <style>
        .fc { background-color: var(--primary-black); color: var(--text-light); }
        .fc-button { background-color: var(--primary-yellow) !important; color: var(--primary-black) !important; }
        .fc-day { background-color: var(--secondary-black) !important; }
        .fc-day-today { background-color: var(--primary-black) !important; }
        .fc-daygrid-day-number { color: var(--text-light) !important; }
        .fc-toolbar-title { color: var(--primary-yellow) !important; }
    </style>
`);