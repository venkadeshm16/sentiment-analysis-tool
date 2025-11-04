import random

# Generate 1000 rows of sample data
positive_comments = [
    'I love this product so much!', 'Amazing quality and fast delivery', 'Outstanding service quality',
    'Exceeded my expectations', 'Brilliant solution to my problem', 'Incredible value for money',
    'Superb customer service', 'Perfect for my needs', 'Highly recommend this',
    'Excellent build quality', 'Love the design and features', 'Best purchase this year',
    'Wonderful experience overall', 'Impressive functionality', 'Fantastic customer support',
    'Absolutely love it', 'Exceptional quality control', 'Great value proposition',
    'Outstanding performance', 'Brilliant engineering', 'Perfect solution',
    'Amazing attention to detail', 'Highly satisfied customer', 'Superb product quality',
    'Love the innovative features', 'Exceptional user experience', 'Best in class performance',
    'Wonderful product design', 'Impressive build quality', 'Fantastic return policy',
    'Outstanding technical support', 'Great customer experience', 'Excellent problem resolution'
]

negative_comments = [
    'This is the worst experience ever', 'Terrible customer support', 'Complete waste of money',
    'Very disappointed with this', 'Poor quality materials', 'Horrible user interface',
    'Worst purchase I have made', 'Completely broken on arrival', 'Frustrating to use',
    'Regret buying this', 'Defective product received', 'Completely useless',
    'Disappointing results', 'Broke after one week', 'Overpriced for what you get',
    'Not worth the money', 'Faulty from day one', 'Terrible build quality',
    'Completely dissatisfied', 'Worst customer service', 'Major design flaws',
    'Unreliable product', 'Poor value for money', 'Regrettable purchase',
    'Completely malfunctioned', 'Frustratingly slow performance', 'Defective unit received',
    'Horrible packaging quality', 'Disappointing durability', 'Broke within warranty period',
    'Overpriced compared to competitors', 'Completely unreliable', 'Terrible product quality',
    'Major compatibility issues'
]

neutral_comments = [
    'The service was okay', 'It is fine I guess', 'Nothing special about it',
    'It works as expected', 'Standard features available', 'Meets basic requirements',
    'Acceptable quality', 'Works fine', 'Ordinary performance', 'Does what it is supposed to',
    'Fair enough for the cost', 'Typical product in this range', 'Reasonable quality',
    'Adequate for basic use', 'Standard industry quality', 'Meets expectations',
    'Normal functionality', 'Basic functionality works', 'Standard features included',
    'Acceptable build quality', 'Ordinary user interface', 'Decent customer support',
    'Standard warranty coverage', 'Fair pricing structure', 'Reasonable delivery time',
    'Typical market offering', 'Adequate documentation provided', 'Standard installation process',
    'Meets industry standards', 'Average performance', 'Standard quality product',
    'Satisfactory performance', 'Average user experience'
]

# Create balanced dataset
data = []
for i in range(334):
    data.append([random.choice(positive_comments), 'Positive'])
for i in range(333):
    data.append([random.choice(negative_comments), 'Negative'])
for i in range(333):
    data.append([random.choice(neutral_comments), 'Neutral'])

# Shuffle the data
random.shuffle(data)

# Write CSV
with open('testdata.csv', 'w') as f:
    f.write('A,B\n')
    for row in data:
        f.write(f'"{row[0]}",{row[1]}\n')

print('CSV with 1000 rows created successfully')