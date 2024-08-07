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
