import json
from deep_translator import GoogleTranslator

# Load dataset
dataset=[]
with open('your_file.json', 'r', encoding='utf-8') as f:
    for line in f:
        dataset.append(json.loads(line)) 

# Initialize translator
translator = GoogleTranslator(source='auto', target='fa')

# Function to safely translate (with fallback)
def safe_translate(text):
    try:
        return translator.translate(text)
    except Exception:
        return text  # fallback to original if translation fails

# Process each example in the dataset
for item in dataset:
    inGraph = item.get("inGraph", {})

    # --- Translate g_node_names ---
    original_node_names = inGraph.get("g_node_names", {})
    translated_node_names = {}
    node_key_map = {}
    for key, val in original_node_names.items():
        translated_val = safe_translate(val)
        translated_node_names[translated_val] = translated_val
        node_key_map[key] = translated_val

    inGraph["g_node_names"] = translated_node_names

    # --- Translate g_edge_types ---
    original_edge_types = inGraph.get("g_edge_types", {})
    translated_edge_types = {}
    edge_key_map = {}
    for key, val in original_edge_types.items():
        translated_val = safe_translate(val)
        translated_edge_types[translated_val] = translated_val
        edge_key_map[key] = translated_val

    inGraph["g_edge_types"] = translated_edge_types

    # --- Translate g_adj using mapped keys ---
    original_adj = inGraph.get("g_adj", {})
    translated_adj = {}
    for subj, obj_dict in original_adj.items():
        new_subj = node_key_map.get(subj, subj)
        translated_adj[new_subj] = {}
        for obj, edges in obj_dict.items():
            new_obj = node_key_map.get(obj, obj)
            new_edges = [edge_key_map.get(edge, edge) for edge in edges]
            translated_adj[new_subj][new_obj] = new_edges

    inGraph["g_adj"] = translated_adj

# Save translated dataset
with open("translated_dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print("Translation complete. Saved to 'translated_dataset.json'")
