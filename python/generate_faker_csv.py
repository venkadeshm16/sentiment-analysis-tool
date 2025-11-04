from faker import Faker
import random

fake = Faker()

# Generate 1000 random messages using Faker
data = []

# Positive sentiment templates
positive_templates = [
    "I love {product}! {reason}",
    "{product} is amazing! {reason}",
    "Best {product} ever! {reason}",
    "Highly recommend {product}. {reason}",
    "Outstanding {product}! {reason}",
    "Perfect {product} for {use_case}. {reason}",
    "Excellent {product}! {reason}",
    "Great {product}! {reason}",
    "Fantastic {product}! {reason}",
    "Wonderful {product}! {reason}"
]

negative_templates = [
    "Terrible {product}. {reason}",
    "Worst {product} ever! {reason}",
    "Hate this {product}. {reason}",
    "Completely disappointed with {product}. {reason}",
    "Awful {product}! {reason}",
    "Horrible {product}. {reason}",
    "Regret buying {product}. {reason}",
    "Useless {product}! {reason}",
    "Broken {product}. {reason}",
    "Failed {product}! {reason}"
]

neutral_templates = [
    "{product} is okay. {reason}",
    "Average {product}. {reason}",
    "{product} works fine. {reason}",
    "Standard {product}. {reason}",
    "Normal {product}. {reason}",
    "{product} meets expectations. {reason}",
    "Decent {product}. {reason}",
    "Fair {product}. {reason}",
    "Acceptable {product}. {reason}",
    "Regular {product}. {reason}"
]

products = ["service", "product", "app", "software", "tool", "platform", "system", "solution", "device", "website"]
use_cases = ["business", "personal use", "work", "home", "office", "daily tasks", "projects", "team collaboration"]

positive_reasons = [
    "Great quality and fast delivery",
    "Excellent customer support",
    "Easy to use interface",
    "Perfect for my needs",
    "Outstanding performance",
    "Amazing features",
    "Great value for money",
    "Highly reliable",
    "Fantastic user experience",
    "Exceeded expectations"
]

negative_reasons = [
    "Poor quality and slow delivery",
    "Terrible customer support",
    "Confusing interface",
    "Doesn't meet my needs",
    "Poor performance",
    "Missing features",
    "Overpriced",
    "Unreliable",
    "Bad user experience",
    "Below expectations"
]

neutral_reasons = [
    "Does what it's supposed to do",
    "Standard features available",
    "Average performance",
    "Fair pricing",
    "Basic functionality works",
    "Meets basic requirements",
    "Nothing special",
    "Typical for this category",
    "Standard quality",
    "Works as expected"
]

# Generate 334 positive messages
for _ in range(334):
    template = random.choice(positive_templates)
    product = random.choice(products)
    reason = random.choice(positive_reasons)
    use_case = random.choice(use_cases)
    
    message = template.format(product=product, reason=reason, use_case=use_case)
    data.append([message, 'Positive'])

# Generate 333 negative messages
for _ in range(333):
    template = random.choice(negative_templates)
    product = random.choice(products)
    reason = random.choice(negative_reasons)
    use_case = random.choice(use_cases)
    
    message = template.format(product=product, reason=reason, use_case=use_case)
    data.append([message, 'Negative'])

# Generate 333 neutral messages
for _ in range(333):
    template = random.choice(neutral_templates)
    product = random.choice(products)
    reason = random.choice(neutral_reasons)
    use_case = random.choice(use_cases)
    
    message = template.format(product=product, reason=reason, use_case=use_case)
    data.append([message, 'Neutral'])

# Add some completely random sentences using Faker
for _ in range(50):
    sentiment = random.choice(['Positive', 'Negative', 'Neutral'])
    if sentiment == 'Positive':
        message = f"{fake.sentence()} {random.choice(['Great!', 'Excellent!', 'Amazing!', 'Perfect!', 'Love it!'])}"
    elif sentiment == 'Negative':
        message = f"{fake.sentence()} {random.choice(['Terrible!', 'Awful!', 'Hate it!', 'Worst ever!', 'Disappointed!'])}"
    else:
        message = f"{fake.sentence()} {random.choice(['Its okay.', 'Average.', 'Nothing special.', 'Fair enough.', 'Standard.'])}"
    
    data.append([message, sentiment])

# Shuffle the data
random.shuffle(data)

# Take only first 1000 entries
data = data[:1000]

# Write CSV
with open('testdata.csv', 'w') as f:
    f.write('A,B\n')
    for row in data:
        f.write(f'"{row[0]}",{row[1]}\n')

print('CSV with 1000 random Faker-generated messages created successfully')