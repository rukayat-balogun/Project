# bmi_predictor/recommendations.py

recommendations = {
    'Underweight': {
        'diet': [
            'Increase your calorie intake with nutrient-dense foods.',
            'Eat more frequently and include snacks.',
            'Incorporate healthy fats like avocados and nuts.',
        ],
        'exercise': [
            'Focus on strength training to build muscle mass.',
            'Avoid excessive cardio exercises.',
            'Consider yoga or Pilates for flexibility and muscle tone.',
        ]
    },
    'Normal weight': {
        'diet': [
            'Maintain a balanced diet with a variety of nutrients.',
            'Include plenty of fruits and vegetables.',
            'Stay hydrated and avoid sugary drinks.',
        ],
        'exercise': [
            'Engage in regular aerobic exercises like walking, running, or swimming.',
            'Include strength training exercises twice a week.',
            'Incorporate flexibility and balance exercises like yoga.',
        ]
    },
    'Overweight': {
        'diet': [
            'Reduce intake of high-calorie, low-nutrient foods.',
            'Increase consumption of fruits, vegetables, and lean proteins.',
            'Drink plenty of water and avoid sugary drinks.',
        ],
        'exercise': [
            'Engage in moderate-intensity aerobic activities like brisk walking.',
            'Include strength training exercises to build muscle.',
            'Increase daily activity by taking the stairs and walking more.',
        ]
    },
    'Obese': {
        'diet': [
            'Follow a calorie-restricted, balanced diet.',
            'Consult a nutritionist for a personalized meal plan.',
            'Avoid processed foods and sugary beverages.',
        ],
        'exercise': [
            'Start with low-impact aerobic activities like swimming or cycling.',
            'Gradually increase the duration and intensity of workouts.',
            'Include strength training exercises to build muscle.',
        ]
    },
    'Morbid Obesity': {
        'diet': [
            'Seek professional medical advice for a supervised diet plan.',
            'Focus on nutrient-dense, low-calorie foods.',
            'Monitor portion sizes and avoid high-calorie snacks.',
        ],
        'exercise': [
            'Begin with very low-impact exercises such as water aerobics or seated exercises.',
            'Gradually increase physical activity under medical supervision.',
            'Consider physical therapy to increase mobility safely.',
        ]
    }
}
