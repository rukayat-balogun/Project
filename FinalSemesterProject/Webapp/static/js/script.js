document.getElementById('bmiForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form submission to the server

    const height = parseFloat(document.getElementById('id_height').value);  // Assuming form fields are id_height and id_weight
    const weight = parseFloat(document.getElementById('id_weight').value);

    if (isNaN(height) || isNaN(weight)) {
        alert('Please enter valid numbers for height and weight.');
        return;
    }

    // Convert height to meters (assuming 1 foot = 0.3048 meters)
    const heightInMeters = height * 0.3048;
    const bmi = weight / (heightInMeters * heightInMeters);

    // Redirect to the BMI result page or update UI
    alert(`Your BMI is ${bmi.toFixed(1)}`);
    window.location.href = `/bmi_result?bmi=${bmi.toFixed(1)}`;
});


document.addEventListener("DOMContentLoaded", function() {
    const category = "{{ category }}";
    const quoteElement = document.getElementById('quote');
    let quote;

    switch(category) {
        case 'Underweight':
            quote = "You are stronger than you think!";
            break;
        case 'Normal weight':
            quote = "Keep up the great work!";
            break;
        case 'Overweight':
            quote = "Consistency is key to success.";
            break;
        case 'Obese':
            quote = "Every journey begins with a single step.";
            break;
        default:
            quote = "Stay healthy, stay happy!";
    }

    quoteElement.textContent = quote;
});


