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

def random_position(width=900, height=550, margin=50):
    return {"x": random.randint(margin, width - margin), "y": random.randint(margin, height - margin)}

def generate_random_graph():
    num_nodes = random.randint(5, 15)
    nodes = []
    names =  ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack", "Kate", "Liam", "Mia", "Noah", "Olivia", "Raul", "Michel", "John", "Alex"]
    occupations = ["Engineer", "Teacher", "Doctor", "Artist", "Chef", "Lawyer", "Scientist", "Writer", "Nurse", "Programmer"]
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