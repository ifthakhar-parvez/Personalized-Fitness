// java scrip for loading view recipe
   
        function toggleRecipe(recipeId) {
            var recipe = document.getElementById(recipeId);
            if (recipe.style.display === "none" || recipe.style.display === "") {
                recipe.style.display = "block";
            } else {
                recipe.style.display = "none";
            }
        }
        // For Meal log section

            document.getElementById("add-entry").addEventListener("click", function () {
                const mealEntries = document.getElementById("meal-entries");
                const newEntry = document.createElement("div");
                newEntry.classList.add("meal-entry");
                newEntry.innerHTML = `
                    <input type="text" name="food_name[]" placeholder="Food Name" required>
                    <input type="number" name="quantity[]" placeholder="Quantity" required>
                    <input type="time" name="time[]" required>
                    <button type="button" class="remove-entry" onclick="removeEntry(this)">X</button>
                `;
                mealEntries.appendChild(newEntry);
            });
            
            function removeEntry(button) {
                button.parentElement.remove();
            }
           // for chart
                document.addEventListener('DOMContentLoaded', function() {
                    // Mock Data for Weight Progress
                    const weightGoal = 70; // Target weight
                    const currentWeight = 65; // Current weight
                    const weightProgressBar = document.querySelector('.progress-bar-weight span');
                    
                    // Calculate absolute difference and percentage from the target weight
                    const weightDifference = Math.abs(currentWeight - weightGoal);
                    const weightPercentage = (weightDifference / weightGoal) * 100; // Calculate percentage
                    
                    // Set the progress bar width based on the percentage
                    weightProgressBar.style.width = `${weightPercentage}%`;
                    
                    // Mock Data for Daily Calorie Intake Progress
                    const dailyGoal = 2500; // Daily Calorie Goal
                    const currentCalories = 1800; // Calories consumed so far today
                    const calorieProgressBar = document.querySelector('.progress-bar-calories span');
                    const caloriePercentage = (currentCalories / dailyGoal) * 100; // Calculate the percentage
                    calorieProgressBar.style.width = `${caloriePercentage}%`; // Set the width of the calorie progress bar
            
                    // Mock Data for Weekly Budget Progress
                    const weeklyBudget = 500; // Weekly Budget
                    const spentBudget = 350; // Budget spent so far
                    const budgetProgressBar = document.querySelector('.progress-bar-budget span');
                    const budgetPercentage = (spentBudget / weeklyBudget) * 100; // Calculate the percentage
                    budgetProgressBar.style.width = `${budgetPercentage}%`; // Set the width of the budget progress bar
            
                    const ctx = document.getElementById('caloriesChart').getContext('2d');
                    const caloriesChart = new Chart(ctx, {
                        type: 'line', // Line chart for daily calorie intake
                        data: {
                        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], // Days of the week
                        datasets: [{
                        label: 'Daily Calorie Intake',
                        data: [2500, 2200, 1800, 2400, 2100, 2300, 2500], // Example data for each day
                        borderColor: '#3498db',
                         backgroundColor: 'rgba(52, 152, 219, 0.2)',
                        fill: true,
                        lineTension: 0.4,
                        borderWidth: 2
                            }]
                        },
                options: {
                    responsive: true,
                         scales: {
                         x: {
                         beginAtZero: true,
                            },
                                y: {
                             beginAtZero: true,
                             max: 3000 // Set a max value based on daily goal
                         }
                             }
                         }
                        });
                });