import random

def initial_position(num, width=900, height=550, margin=50):
    nodes = []
    if num == 0:
        return nodes
    row1_count = num // 2
    row2_count = num - row1_count
    y1 = height // 4
    y2 = 3 * height // 4
    for i in range(1, num + 1):
        if i <= row1_count:
            x = (i - 1) * (width - 2 * margin) // (row1_count - 1) + margin if row1_count > 1 else width // 2
            y = y1
        else:
            idx = i - row1_count
            x = (idx - 1) * (width - 2 * margin) // (row2_count - 1) + margin if row2_count > 1 else width // 2
            y = y2
        nodes.append({
            "data": {"id": str(i), "label": f"Person {i}"},
            "position": {"x": x, "y": y}
        })
    return nodes

def random_position(width=5000, height=1500, margin=50):
    return {"x": random.randint(margin, width - margin), "y": random.randint(margin, height - margin)}

def generate_random_graph():
    num_nodes = random.randint(100, 1000)
    nodes = []
    names = [
        "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack",
        "Kate", "Liam", "Mia", "Noah", "Olivia", "Raul", "Michel", "John", "Alex",
        "Aaron", "Abigail", "Adrian", "Agnes", "Alan", "Albert", "Amanda", "Amelia", "Andreas", "Angela",
        "Anita", "Anthony", "Antonio", "April", "Aria", "Ariana", "Ashley", "Astrid", "Barbara", "Beatrice",
        "Benjamin", "Bianca", "Brandon", "Brenda", "Brian", "Brittany", "Bryan", "Carlos", "Caroline", "Carla",
        "Casey", "Cecilia", "Christian", "Christina", "Clara", "Claudia", "Cole", "Colin", "Connor", "Daniel",
        "Danielle", "David", "Deborah", "Denise", "Derek", "Dominic", "Eleanor", "Elena", "Elijah", "Elisa",
        "Elizabeth", "Emily", "Emma", "Eric", "Esther", "Ethan", "Eva", "Felix", "Felicia", "Fernanda",
        "Fernando", "Fiona", "Florence", "Francesca", "Frederick", "Gabriel", "Gabriella", "Geoffrey", "Georgia", "Gerald",
        "Gianna", "Gloria", "Grant", "Gustavo", "Hannah", "Harold", "Heather", "Helen", "Hugo", "Igor",
        "Isabella", "Isla", "Jacob", "James", "Janet", "Jason", "Jasper", "Jeremy", "Jessica", "Joan",
        "Joe", "Joseph", "Joshua", "Julia", "Julian", "Justin", "Karen", "Karl", "Katherine", "Kayla",
        "Keith", "Kelly", "Kevin", "Kyle", "Laura", "Lawrence", "Leon", "Linda", "Luis", "Lydia",
        "Madeline", "Maria", "Mariana", "Mark", "Martha", "Martin", "Martina", "Matthew", "Max", "Melanie",
        "Melissa", "Michael", "Mikhail", "Morgan", "Natalie", "Nathan", "Neil", "Nico", "Nicole", "Nina",
        "Oliver", "Oscar", "Pamela", "Patricia", "Patrick", "Paula", "Peter", "Philippa", "Phillip", "Quentin",
        "Rachel", "Ralph", "Rebecca", "Regina", "Renata", "Richard", "Roberto", "Robert", "Rosa", "Ross",
        "Ruby", "Ryan", "Sabrina", "Samantha", "Samuel", "Scott", "Sean", "Sebastian", "Shawn", "Sophia",
        "Stephanie", "Steve", "Steven", "Stella", "Susan", "Teresa", "Thomas", "Tiffany", "Timothy", "Travis",
        "Tristan", "Valentina", "Valerie", "Vanessa", "Victor", "Victoria", "Vincent", "Walter", "Wayne", "Xavier",
        "Yasmine", "Yolanda", "Zachary", "Zoe"
    ]    
    occupations = [
        "Engineer", "Teacher", "Doctor", "Artist", "Chef", "Lawyer", "Scientist", "Writer", "Nurse", "Programmer",
        "Architect", "Accountant", "Designer", "Photographer", "Pharmacist", "Electrician", "Plumber", "Mechanic", "Farmer", "Pilot",
        "Flight Attendant", "Police Officer", "Firefighter", "Paramedic", "Social Worker", "Psychologist", "Researcher", "Data Scientist", "Machine Learning Engineer", "Web Developer",
        "Mobile Developer", "Database Administrator", "System Administrator", "Network Engineer", "DevOps Engineer", "Product Manager", "Project Manager", "Business Analyst", "Marketing Manager", "Sales Representative",
        "HR Specialist", "Recruiter", "Consultant", "Financial Analyst", "Investment Banker", "Real Estate Agent", "Interior Designer", "UX Designer", "UI Designer", "Graphic Designer",
        "Animator", "Video Editor", "Sound Engineer", "Actor", "Director", "Producer", "Translator", "Interpreter", "Journalist", "Editor",
        "Biologist", "Chemist", "Physicist", "Geologist", "Mathematician", "Statistician", "Economist", "Zoologist", "Logistician", "Supply Chain Manager",
        "Quality Assurance Tester", "Cybersecurity Analyst", "IT Support Specialist", "Petroleum Engineer", "Civil Engineer", "Mechanical Engineer", "Chemical Engineer", "Biomedical Engineer", "Environmental Scientist", "Urban Planner",
        "Principal", "Librarian", "Coach", "Personal Trainer", "Dentist", "Orthodontist", "Optometrist", "Veterinarian", "Investment Advisor", "Event Planner",
        "Bartender", "Barista", "Receptionist", "Customer Support Representative", "Legal Assistant", "Paralegal", "Judge", "Clergy", "Historian", "Archivist"
    ]
    for i in range(1, num_nodes + 1):
        name = random.choice(names)
        age = random.randint(18, 65)
        occupation = random.choice(occupations)
        nodes.append({
            "data": {"id": str(i), "label": name, "name": name, "age": age, "occupation": occupation},
            "position": random_position()
        })
    edges = []
    edge_types = ["friend", "close_friend", "work_colleagues", "family", "acquaintance"]
    possible_edges = [(str(a), str(b)) for a in range(1, num_nodes + 1) for b in range(a + 1, num_nodes + 1)]
    num_edges = random.randint(0, min(len(possible_edges), num_nodes * 2))
    selected_edges = random.sample(possible_edges, num_edges)
    for source, target in selected_edges:
        edge_type = random.choice(edge_types)
        edges.append({"data": {"source": source, "target": target, "type": edge_type}})
    return nodes + edges