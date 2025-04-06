// Example: Fetch workout suggestions and display
async function fetchWorkoutSuggestions(workoutPlanId) {
    try {
        const response = await fetch(`/api/workoutplans/${workoutPlanId}/ai_suggestion/`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching workout suggestions:', error);
    }
}

async function displayWorkoutSuggestions(workoutPlanId) {
    const data = await fetchWorkoutSuggestions(workoutPlanId);
    const workoutList = document.getElementById('workout-list');
    workoutList.innerHTML = ''; // Clear previous suggestions

    data.suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = `${suggestion.name} - ${suggestion.reps} reps, ${suggestion.duration} mins`;
        workoutList.appendChild(li);
    });
}

// Example: Fetch nutrition suggestions and display
async function fetchNutritionSuggestions(nutritionPlanId) {
    try {
        const response = await fetch(`/api/nutritionplans/${nutritionPlanId}/ai_suggestion/`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching nutrition suggestions:', error);
    }
}

async function displayNutritionSuggestions(nutritionPlanId) {
    const data = await fetchNutritionSuggestions(nutritionPlanId);
    const nutritionList = document.getElementById('nutrition-list');
    nutritionList.innerHTML = ''; // Clear previous suggestions

    data.suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = `${suggestion.meal} - Calories: ${suggestion.calories}, Protein: ${suggestion.protein}g`;
        nutritionList.appendChild(li);
    });
}

// Example: Fetch progress and display
async function fetchProgressTracker(userId) {
    try {
        const response = await fetch(`/api/progresstracker/${userId}/progress/`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching progress data:', error);
    }
}

async function displayProgress(userId) {
    const progress = await fetchProgressTracker(userId);
    document.getElementById('weight-progress').textContent = `${progress.weight} kg`;
    document.getElementById('body-fat-progress').textContent = `${progress.body_fat_percentage}%`;
    document.getElementById('muscle-mass-progress').textContent = `${progress.muscle_mass} kg`;
}

// Example: Chatbot function
document.getElementById('send-message').addEventListener('click', async () => {
    const userMessage = document.getElementById('user-message').value;

    const reply = await sendChatMessage(userMessage);

    const chatbox = document.getElementById('chatbox');
    const botMessage = document.createElement('p');
    botMessage.textContent = `AI: ${reply}`;
    chatbox.appendChild(botMessage);

    // Clear the input field
    document.getElementById('user-message').value = '';
});

// Send message to AI Chatbot API
async function sendChatMessage(userMessage) {
    try {
        const response = await fetch('/api/ai_chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        });
        const data = await response.json();
        return data.reply; // AI response from the chatbot
    } catch (error) {
        console.error('Error with chatbot:', error);
    }
}

// Example calls with actual IDs (replace with actual IDs)
displayWorkoutSuggestions(1); // Replace '1' with the actual workout plan ID
displayNutritionSuggestions(1); // Replace '1' with the actual nutrition plan ID
displayProgress(1); // Replace '1' with the actual user ID
