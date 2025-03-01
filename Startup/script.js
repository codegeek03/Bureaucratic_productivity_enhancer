$(document).ready(function() {
    const currentUser = 'bibhabasuiitkgp';
    const currentUTCDate = '2025-03-01 08:31:19';

    // Initialize Evo Calendar with current date
    $('#calendar').evoCalendar({
        theme: 'Royal Navy',
        todayHighlight: true,
        calendarEvents: [
            {
                id: '1',
                name: 'New Year',
                date: '2025-01-01',
                type: 'holiday',
                everyYear: true
            }
        ]
    });

    // Update current time
    function updateTime() {
        // Parse the UTC date string
        const now = new Date(currentUTCDate);
        const options = {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        };
        const timeString = now.toLocaleString('en-US', options).replace(',', '');
        $('#current-time').text(timeString + ' UTC');
    }

    // Update time initially
    updateTime();

    // Modal Elements
    const modal = document.getElementById('eventModal');
    const closeModal = document.querySelector('.close-modal');
    const eventForm = document.getElementById('eventForm');
    const btnCancel = document.querySelector('.btn-cancel');

    // Show Modal Function
    function showModal() {
        modal.classList.add('show');
        // Set default date to current UTC date
        const defaultDate = currentUTCDate.split(' ')[0]; // Extract YYYY-MM-DD
        document.getElementById('eventDate').value = defaultDate;
        
        // Set minimum date for both date inputs to current date
        document.getElementById('eventDate').min = defaultDate;
        document.getElementById('eventEndDate').min = defaultDate;
    }

    // Hide Modal Function
    function hideModal() {
        modal.classList.remove('show');
        eventForm.reset();
    }

    // Generate Random ID
    function generateEventId() {
        return `evt_${currentUser}_${Date.now()}`;
    }

    // Event Color Map
    const eventTypeColors = {
        event: '#3498db',
        holiday: '#e74c3c',
        birthday: '#2ecc71',
        meeting: '#9b59b6'
    };

    // Add Event Button Click Handler
    $('#addEventBtn').on('click', function() {
        showModal();
    });

    // Close Modal Handlers
    closeModal.addEventListener('click', hideModal);
    btnCancel.addEventListener('click', hideModal);
    window.addEventListener('click', (e) => {
        if (e.target === modal) hideModal();
    });

    // Event Type Change Handler
    document.getElementById('eventType').addEventListener('change', function(e) {
        const color = eventTypeColors[e.target.value];
        if (color) {
            document.getElementById('eventColor').value = color;
        }
    });

    // Handle start date change
    document.getElementById('eventDate').addEventListener('change', function(e) {
        const startDate = e.target.value;
        document.getElementById('eventEndDate').min = startDate;
        
        // If end date is before start date, update it
        const endDate = document.getElementById('eventEndDate').value;
        if (endDate && endDate < startDate) {
            document.getElementById('eventEndDate').value = startDate;
        }
    });

    // Form Submit Handler
    eventForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // Get form values
        const eventName = document.getElementById('eventName').value;
        const startDate = document.getElementById('eventDate').value;
        const endDate = document.getElementById('eventEndDate').value;
        const description = document.getElementById('eventDescription').value;
        const eventType = document.getElementById('eventType').value;
        const color = document.getElementById('eventColor').value;

        // Validate dates
        const currentDate = currentUTCDate.split(' ')[0];
        if (startDate < currentDate) {
            alert('Cannot create events in the past!');
            return;
        }

        // Create event data object
        const eventData = {
            id: generateEventId(),
            name: eventName,
            date: startDate,
            type: eventType,
            description: description,
            color: color,
            createdBy: currentUser,
            createdAt: currentUTCDate
        };

        // Handle end date if provided
        if (endDate && endDate > startDate) {
            eventData.date = [startDate, endDate];
        }

        // Add event to calendar
        try {
            $('#calendar').evoCalendar('addCalendarEvent', eventData);
            
            // Save to localStorage with user information
            const savedEvents = JSON.parse(localStorage.getItem(`calendarEvents_${currentUser}`) || '[]');
            savedEvents.push(eventData);
            localStorage.setItem(`calendarEvents_${currentUser}`, JSON.stringify(savedEvents));
            
            // Show success message
            alert(`Event "${eventName}" added successfully!`);
            
            // Hide modal and reset form
            hideModal();
        } catch (error) {
            console.error('Error adding event:', error);
            alert('Error adding event. Please try again.');
        }
    });

    // Load saved events from localStorage
    try {
        const savedEvents = JSON.parse(localStorage.getItem(`calendarEvents_${currentUser}`) || '[]');
        savedEvents.forEach(event => {
            $('#calendar').evoCalendar('addCalendarEvent', event);
        });
    } catch (error) {
        console.error('Error loading saved events:', error);
    }

    // Event click handler
    $('#calendar').on('selectEvent', function(event, activeEvent) {
        const dateInfo = Array.isArray(activeEvent.date) 
            ? `From: ${activeEvent.date[0]}\nTo: ${activeEvent.date[1]}` 
            : `Date: ${activeEvent.date}`;
            
        let eventInfo = `Event Details:\n\nName: ${activeEvent.name}\n${dateInfo}`;
        
        if (activeEvent.description) {
            eventInfo += `\nDescription: ${activeEvent.description}`;
        }
        if (activeEvent.createdBy) {
            eventInfo += `\n\nCreated by: ${activeEvent.createdBy}\nCreated at: ${activeEvent.createdAt}`;
        }
        
        alert(eventInfo);
    });
});