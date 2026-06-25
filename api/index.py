import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from mangum import Mangum
from upstash_redis import Redis

# ==========================================
# 1. HERO POOL DATASET
# ==========================================
HERO_POOL = [
    {"id": 1, "nama": "Edith", "role": "Tank"},
    {"id": 2, "nama": "Gloo", "role": "Tank"},
    {"id": 3, "nama": "Barats", "role": "Tank"},
    {"id": 4, "nama": "Atlas", "role": "Tank"},
    {"id": 5, "nama": "Baxia", "role": "Tank"},
    {"id": 6, "nama": "Esmeralda", "role": "Tank"},
    {"id": 7, "nama": "Khufra", "role": "Tank"},
    {"id": 8, "nama": "Belerick", "role": "Tank"},
    {"id": 9, "nama": "Uranus", "role": "Tank"},
    {"id": 10, "nama": "Hylos", "role": "Tank"},
    {"id": 11, "nama": "Grock", "role": "Tank"},
    {"id": 12, "nama": "Gatotkaca", "role": "Tank"},
    {"id": 13, "nama": "Johnson", "role": "Tank"},
    {"id": 14, "nama": "Minotaur", "role": "Tank"},
    {"id": 15, "nama": "Franco", "role": "Tank"},
    {"id": 16, "nama": "Akai", "role": "Tank"},
    {"id": 17, "nama": "Tigreal", "role": "Tank"},
    {"id": 18, "nama": "Alice", "role": "Tank"},
    {"id": 19, "nama": "Sora", "role": "Fighter"},
    {"id": 20, "nama": "Lukas", "role": "Fighter"},
    {"id": 21, "nama": "Cici", "role": "Fighter"},
    {"id": 22, "nama": "Arlott", "role": "Fighter"},
    {"id": 23, "nama": "Fredrinn", "role": "Fighter"},
    {"id": 24, "nama": "Yin", "role": "Fighter"},
    {"id": 25, "nama": "Aulus", "role": "Fighter"},
    {"id": 26, "nama": "Phoveus", "role": "Fighter"},
    {"id": 27, "nama": "Paquito", "role": "Fighter"},
    {"id": 28, "nama": "Khaleed", "role": "Fighter"},
    {"id": 29, "nama": "Yu Zhong", "role": "Fighter"},
    {"id": 30, "nama": "Silvanna", "role": "Fighter"},
    {"id": 31, "nama": "Masha", "role": "Fighter"},
    {"id": 32, "nama": "Dyrroth", "role": "Fighter"},
    {"id": 33, "nama": "X.Borg", "role": "Fighter"},
    {"id": 34, "nama": "Terizla", "role": "Fighter"},
    {"id": 35, "nama": "Guinevere", "role": "Fighter"},
    {"id": 36, "nama": "Badang", "role": "Fighter"},
    {"id": 37, "nama": "Minsitthar", "role": "Fighter"},
    {"id": 38, "nama": "Thamuz", "role": "Fighter"},
    {"id": 39, "nama": "Leomord", "role": "Fighter"},
    {"id": 40, "nama": "Aldous", "role": "Fighter"},
    {"id": 41, "nama": "Martis", "role": "Fighter"},
    {"id": 42, "nama": "Jawhead", "role": "Fighter"},
    {"id": 43, "nama": "Argus", "role": "Fighter"},
    {"id": 44, "nama": "Roger", "role": "Fighter"},
    {"id": 45, "nama": "Lapu-Lapu", "role": "Fighter"},
    {"id": 46, "nama": "Hilda", "role": "Fighter"},
    {"id": 47, "nama": "Ruby", "role": "Fighter"},
    {"id": 48, "nama": "Alpha", "role": "Fighter"},
    {"id": 49, "nama": "Sun", "role": "Fighter"},
    {"id": 50, "nama": "Chou", "role": "Fighter"},
    {"id": 51, "nama": "Freya", "role": "Fighter"},
    {"id": 52, "nama": "Zilong", "role": "Fighter"},
    {"id": 53, "nama": "Bane", "role": "Fighter"},
    {"id": 54, "nama": "Alucard", "role": "Fighter"},
    {"id": 55, "nama": "Balmond", "role": "Fighter"},
    {"id": 56, "nama": "Suyou", "role": "Assassin"},
    {"id": 57, "nama": "Nolan", "role": "Assassin"},
    {"id": 58, "nama": "Joy", "role": "Assassin"},
    {"id": 59, "nama": "Julian", "role": "Assassin"},
    {"id": 60, "nama": "Aamon", "role": "Assassin"},
    {"id": 61, "nama": "Benedetta", "role": "Assassin"},
    {"id": 62, "nama": "Ling", "role": "Assassin"},
    {"id": 63, "nama": "Hanzo", "role": "Assassin"},
    {"id": 64, "nama": "Selena", "role": "Assassin"},
    {"id": 65, "nama": "Gusion", "role": "Assassin"},
    {"id": 66, "nama": "Helcurt", "role": "Assassin"},
    {"id": 67, "nama": "Lancelot", "role": "Assassin"},
    {"id": 68, "nama": "Harley", "role": "Assassin"},
    {"id": 69, "nama": "Yi Sun-Shin", "role": "Assassin"},
    {"id": 70, "nama": "Natalia", "role": "Assassin"},
    {"id": 71, "nama": "Hayabusa", "role": "Assassin"},
    {"id": 72, "nama": "Fanny", "role": "Assassin"},
    {"id": 73, "nama": "Karina", "role": "Assassin"},
    {"id": 74, "nama": "Saber", "role": "Assassin"},
    {"id": 75, "nama": "Zetian", "role": "Mage"},
    {"id": 76, "nama": "Zhuxin", "role": "Mage"},
    {"id": 77, "nama": "Novaria", "role": "Mage"},
    {"id": 78, "nama": "Xavier", "role": "Mage"},
    {"id": 79, "nama": "Valentina", "role": "Mage"},
    {"id": 80, "nama": "Yve", "role": "Mage"},
    {"id": 81, "nama": "Luo Yi", "role": "Mage"},
    {"id": 82, "nama": "Cecilion", "role": "Mage"},
    {"id": 83, "nama": "Lylia", "role": "Mage"},
    {"id": 84, "nama": "Kadita", "role": "Mage"},
    {"id": 85, "nama": "Harith", "role": "Mage"},
    {"id": 86, "nama": "Lunox", "role": "Mage"},
    {"id": 87, "nama": "Vale", "role": "Mage"},
    {"id": 88, "nama": "Chang'e", "role": "Mage"},
    {"id": 89, "nama": "Valir", "role": "Mage"},
    {"id": 90, "nama": "Pharsa", "role": "Mage"},
    {"id": 91, "nama": "Zhask", "role": "Mage"},
    {"id": 92, "nama": "Odette", "role": "Mage"},
    {"id": 93, "nama": "Vexana", "role": "Mage"},
    {"id": 94, "nama": "Aurora", "role": "Mage"},
    {"id": 95, "nama": "Cyclops", "role": "Mage"},
    {"id": 96, "nama": "Kagura", "role": "Mage"},
    {"id": 97, "nama": "Gord", "role": "Mage"},
    {"id": 98, "nama": "Eudora", "role": "Mage"},
    {"id": 99, "nama": "Nana", "role": "Mage"},
    {"id": 100, "nama": "Obsidia", "role": "Marksman"},
    {"id": 101, "nama": "Ixia", "role": "Marksman"},
    {"id": 102, "nama": "Melissa", "role": "Marksman"},
    {"id": 103, "nama": "Natan", "role": "Marksman"},
    {"id": 104, "nama": "Beatrix", "role": "Marksman"},
    {"id": 105, "nama": "Brody", "role": "Marksman"},
    {"id": 106, "nama": "Popol & Kupa", "role": "Marksman"},
    {"id": 107, "nama": "Wanwan", "role": "Marksman"},
    {"id": 108, "nama": "Granger", "role": "Marksman"},
    {"id": 109, "nama": "Kimmy", "role": "Marksman"},
    {"id": 110, "nama": "Claude", "role": "Marksman"},
    {"id": 111, "nama": "Hanabi", "role": "Marksman"},
    {"id": 112, "nama": "Lesley", "role": "Marksman"},
    {"id": 113, "nama": "Irithel", "role": "Marksman"},
    {"id": 114, "nama": "Karrie", "role": "Marksman"},
    {"id": 115, "nama": "Moskov", "role": "Marksman"},
    {"id": 116, "nama": "Layla", "role": "Marksman"},
    {"id": 117, "nama": "Clint", "role": "Marksman"},
    {"id": 118, "nama": "Bruno", "role": "Marksman"},
    {"id": 119, "nama": "Miya", "role": "Marksman"},
    {"id": 120, "nama": "Marcel", "role": "Support"},
    {"id": 121, "nama": "Kalea", "role": "Support"},
    {"id": 122, "nama": "Chip", "role": "Support"},
    {"id": 123, "nama": "Floryn", "role": "Support"},
    {"id": 124, "nama": "Mathilda", "role": "Support"},
    {"id": 125, "nama": "Carmilla", "role": "Support"},
    {"id": 126, "nama": "Faramis", "role": "Support"},
    {"id": 127, "nama": "Kaja", "role": "Support"},
    {"id": 128, "nama": "Angela", "role": "Support"},
    {"id": 129, "nama": "Diggie", "role": "Support"},
    {"id": 130, "nama": "Estes", "role": "Support"},
    {"id": 131, "nama": "Lolita", "role": "Support"},
    {"id": 132, "nama": "Rafaela", "role": "Support"},
]

COUNTER_MAP = {
    1: [131, 89, 116, 5, 49], 2: [126, 115, 72, 18, 38], 3: [33, 80, 55, 97, 89],
    4: [120, 129, 79, 107, 18], 5: [131, 33, 80, 53, 31], 6: [32, 5, 86, 114, 130],
    7: [33, 120, 121, 45, 125], 8: [112, 126, 80, 33, 78], 9: [114, 32, 130, 80, 128],
    10: [33, 114, 89, 76, 21], 11: [111, 18, 80, 70, 76], 12: [127, 112, 33, 9, 120],
    13: [126, 18, 2, 124, 8], 14: [81, 124, 5, 104, 80], 15: [17, 106, 13, 49, 63],
    16: [120, 6, 21, 18, 76], 17: [129, 18, 33, 89, 55], 18: [80, 128, 114, 123, 130],
    19: [102, 26, 12, 37, 41], 20: [26, 5, 114, 38, 18], 21: [49, 33, 60, 80, 130],
    22: [26, 91, 92, 20, 49], 23: [89, 114, 33, 63, 97], 24: [107, 28, 9, 46, 120],
    25: [80, 130, 123, 120, 34], 26: [33, 37, 48, 49, 97], 27: [7, 3, 26, 2, 92],
    28: [122, 26, 114, 85, 78], 29: [31, 107, 110, 86, 1], 30: [31, 3, 5, 61, 73],
    31: [49, 43, 126, 9, 3], 32: [43, 31, 38, 48, 6], 33: [70, 52, 58, 61, 80],
    34: [33, 80, 48, 97, 114], 35: [31, 129, 107, 7, 43], 36: [131, 6, 26, 73, 18],
    37: [70, 43, 5, 33, 52], 38: [21, 89, 61, 33, 114], 39: [89, 102, 114, 128, 63],
    40: [6, 95, 122, 107, 102], 41: [33, 37, 55, 120, 126], 42: [49, 6, 126, 2, 91],
    43: [6, 47, 23, 79, 9], 44: [3, 9, 122, 26, 106], 45: [6, 40, 120, 33, 85],
    46: [114, 60, 26, 109, 37], 47: [26, 33, 131, 97, 34], 48: [124, 61, 129, 33, 63],
    49: [40, 47, 54, 58, 103], 50: [6, 26, 95, 49, 103], 51: [26, 37, 3, 5, 114],
    52: [122, 98, 17, 73, 13], 53: [131, 77, 63, 97, 79], 54: [26, 3, 7, 23, 38],
    55: [80, 63, 130, 128, 33], 56: [65, 85, 30, 95, 1], 57: [74, 122, 6, 118, 46],
    58: [95, 31, 86, 115, 129], 59: [5, 35, 37, 108, 3], 60: [2, 92, 30, 74, 76],
    61: [26, 31, 100, 79, 21], 62: [126, 70, 79, 74, 95], 63: [70, 66, 49, 40, 107],
    64: [31, 122, 106, 7, 2], 65: [98, 131, 92, 3, 74], 66: [70, 73, 98, 40, 100],
    67: [31, 128, 95, 123, 118], 68: [131, 49, 106, 2, 74], 69: [131, 9, 73, 124, 60],
    70: [95, 74, 132, 54, 27], 71: [74, 122, 95, 98, 23], 72: [118, 115, 105, 79, 52],
    73: [108, 105, 129, 86, 47], 74: [3, 23, 31, 43, 119], 75: [123, 2, 130, 79, 124],
    76: [129, 1, 89, 71, 123], 77: [70, 62, 63, 115, 46], 78: [70, 128, 62, 66, 115],
    79: [26, 13, 132, 5, 91], 80: [31, 81, 50, 120, 63], 81: [131, 101, 57, 42, 120],
    82: [63, 71, 101, 24, 77], 83: [124, 107, 113, 100, 61], 84: [120, 79, 96, 31, 1],
    85: [26, 1, 37, 91, 95], 86: [3, 47, 81, 36, 117], 87: [3, 26, 2, 18, 39],
    88: [131, 110, 85, 2, 106], 89: [132, 131, 66, 70, 62], 90: [124, 122, 63, 70, 113],
    91: [5, 103, 47, 8, 124], 92: [3, 23, 99, 26, 2], 93: [18, 70, 61, 33, 125],
    94: [81, 129, 63, 70, 5], 95: [131, 130, 101, 106, 54], 96: [1, 54, 38, 95, 6],
    97: [70, 66, 31, 63, 68], 98: [3, 31, 23, 7, 39], 99: [10, 2, 80, 28, 16],
    100: [5, 119, 95, 130, 8], 101: [63, 107, 110, 84, 57], 102: [8, 5, 101, 68, 87],
    103: [131, 22, 74, 129, 105], 104: [58, 100, 115, 50, 112], 105: [49, 23, 106, 129, 3],
    106: [4, 18, 125, 111, 120], 107: [26, 95, 7, 113, 127], 108: [72, 124, 46, 100, 62],
    109: [73, 131, 80, 92, 66], 110: [112, 1, 95, 60, 114], 111: [104, 101, 131, 70, 108],
    112: [124, 49, 130, 2, 106], 113: [9, 105, 98, 23, 112], 114: [49, 43, 106, 74, 37],
    115: [95, 122, 73, 132, 42], 116: [4, 13, 9, 49, 17], 117: [124, 31, 2, 116, 91],
    118: [131, 2, 112, 14, 31], 119: [8, 12, 9, 3, 23], 120: [128, 6, 95, 130, 116],
    121: [126, 37, 53, 120, 63], 122: [80, 105, 5, 94, 53], 123: [131, 24, 101, 30, 15],
    124: [3, 1, 6, 31, 113], 125: [129, 33, 124, 72, 79], 126: [124, 123, 79, 130, 127],
    127: [47, 132, 130, 79, 92], 128: [131, 52, 24, 15, 30], 129: [130, 131, 79, 15, 123],
    130: [101, 104, 24, 4, 57], 131: [80, 6, 94, 117, 96], 132: [101, 92, 116, 87, 98],
}

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def get_hero_by_id(hero_id):
    for hero in HERO_POOL:
        if hero["id"] == hero_id:
            return hero
    return None

def get_hero_img_url(hero_name: str) -> str:
    safe_name = (hero_name
        .replace(" ", "_")
        .replace(".", "")
        .replace("'", "")
        .replace("&", "&"))
    return f"/img/{safe_name}.png"

# ==========================================
# 3. NODE & LINKED LIST STRUCTURES
# ==========================================
class HeroNode:
    def __init__(self, id: int, nama: str, role: str):
        self.id = id
        self.nama = nama
        self.role = role
        self.next = None

class HeroLinkedList:
    def __init__(self):
        self.head = None

    def append(self, node: HeroNode):
        if not self.head:
            self.head = node
            node.next = None
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = node
        node.next = None

    def find_and_remove(self, hero_id: int) -> HeroNode:
        """
        Mencari node berdasarkan hero_id di dalam list, memutuskan hubungannya
        dari list (Delete Node), menyambungkan kembali pointer list,
        lalu mengembalikan node yang dihapus.
        """
        if not self.head:
            return None
        
        if self.head.id == hero_id:
            removed = self.head
            self.head = self.head.next
            removed.next = None
            return removed
        
        curr = self.head
        while curr.next:
            if curr.next.id == hero_id:
                removed = curr.next
                curr.next = curr.next.next
                removed.next = None
                return removed
            curr = curr.next
        return None

    def to_list(self) -> list:
        nodes = []
        curr = self.head
        while curr:
            nodes.append(curr)
            curr = curr.next
        return nodes

# ==========================================
# 4. REDIS LINKED LIST PERSISTENCE & HELPERS
# ==========================================
DRAFT_KEY = "draft_list"

import json

class FileMockRedis:
    def __init__(self, filepath="local_redis.json"):
        # Put local_redis.json inside the workspace directory for clean persistence
        self.filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", filepath)

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save(self, data):
        try:
            with open(self.filepath, "w") as f:
                json.dump(data, f)
        except Exception:
            pass

    def get(self, key):
        data = self._load()
        return data.get(key, None)

    def set(self, key, value):
        data = self._load()
        data[key] = value
        self._save(data)
        return True

def get_redis():
    url = os.environ.get("UPSTASH_REDIS_REST_URL")
    token = os.environ.get("UPSTASH_REDIS_REST_TOKEN")
    if not url or not token:
        # Fallback ke file JSON lokal jika env vars Redis tidak dikonfigurasi
        global _mock_redis_instance
        if '_mock_redis_instance' not in globals():
            _mock_redis_instance = FileMockRedis()
        return _mock_redis_instance
    return Redis(url=url, token=token)

def get_draft_ids() -> list:
    redis = get_redis()
    data = redis.get(DRAFT_KEY)
    if not data:
        return []
    return json.loads(data)

def save_draft_ids(ids: list):
    redis = get_redis()
    redis.set(DRAFT_KEY, json.dumps(ids))

def reconstruct_lists():
    """
    Kondisi Awal (Inisialisasi):
    - Linked List A (Pool Hero): berisi 132 hero dari dataset.
    - Linked List B (Draft): kosong.
    
    Kemudian, untuk setiap hero yang terdaftar di database draft, lakukan operasi pemindahan node:
    - Langkah 1: Delete Node dari Pool A (memutus pointer)
    - Langkah 2: Insert Node ke Draft B (menyambung pointer)
    """
    draft_ids = get_draft_ids()
    
    list_A = HeroLinkedList()
    for hero_data in HERO_POOL:
        node = HeroNode(id=hero_data["id"], nama=hero_data["nama"], role=hero_data["role"])
        list_A.append(node)
        
    list_B = HeroLinkedList()
    
    for d_id in draft_ids:
        node = list_A.find_and_remove(d_id)
        if node:
            list_B.append(node)
            
    return list_A, list_B

def build_trace_B(list_B: HeroLinkedList) -> str:
    nodes = list_B.to_list()
    if not nodes:
        return '<span class="text-slate-600">HEAD ➔ NULL</span>'
    trace = '<span class="text-cyan-400 font-bold">HEAD</span>'
    for n in nodes:
        trace += f' <span class="text-slate-500">➔</span> <span class="bg-slate-900 border border-slate-800 px-2 py-0.5 rounded text-amber-400 font-bold">{n.nama}</span>'
    trace += ' <span class="text-slate-500">➔</span> <span class="text-slate-600 font-bold">NULL</span>'
    return trace

def build_trace_A(list_A: HeroLinkedList) -> str:
    nodes = list_A.to_list()
    if not nodes:
        return '<span class="text-slate-600">HEAD ➔ NULL</span>'
    
    # Jika <= 5 elemen, tampilkan semua
    if len(nodes) <= 5:
        trace_parts = []
        for n in nodes:
            trace_parts.append(f'<span class="bg-slate-900 border border-slate-800 px-2 py-0.5 rounded text-cyan-400 font-bold">{n.nama}</span>')
        return '<span class="text-cyan-400 font-bold">HEAD</span> ➔ ' + ' ➔ '.join(trace_parts) + ' ➔ <span class="text-slate-600 font-bold">NULL</span>'
    
    # Tampilkan 3 pertama, lalu ..., lalu terakhir
    first_nodes = nodes[:3]
    last_node = nodes[-1]
    
    trace_parts = []
    for n in first_nodes:
        trace_parts.append(f'<span class="bg-slate-900 border border-slate-800 px-2 py-0.5 rounded text-cyan-400 font-bold">{n.nama}</span>')
    
    trace = '<span class="text-cyan-400 font-bold">HEAD</span> ➔ ' + ' ➔ '.join(trace_parts)
    trace += ' ➔ <span class="text-slate-500 font-bold">...</span> ➔ '
    trace += f'<span class="bg-slate-900 border border-slate-800 px-2 py-0.5 rounded text-cyan-400 font-bold">{last_node.nama}</span> ➔ <span class="text-slate-600 font-bold">NULL</span>'
    return trace

# ==========================================
# 5. FASTAPI APP
# ==========================================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files and index.html locally
IS_LOCAL = "VERCEL" not in os.environ

if IS_LOCAL:
    index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html")
    if os.path.exists(index_path):
        @app.get("/")
        def serve_index():
            return FileResponse(index_path)

    img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img")
    if os.path.exists(img_dir):
        app.mount("/img", StaticFiles(directory=img_dir), name="img")

@app.get("/api/heroes")
def get_heroes():
    # Tetap mengembalikan data mentah pool lengkap agar UI dapat menginisialisasi
    return [dict(**h, img=get_hero_img_url(h["nama"])) for h in HERO_POOL]

@app.get("/api/draft")
def get_draft():
    list_A, list_B = reconstruct_lists()
    
    draft_heroes = []
    curr = list_B.head
    while curr:
        hero_dict = {
            "id": curr.id,
            "nama": curr.nama,
            "role": curr.role,
            "img": get_hero_img_url(curr.nama)
        }
        draft_heroes.append(hero_dict)
        curr = curr.next
        
    return {
        "size": len(draft_heroes),
        "draft": draft_heroes,
        "trace": build_trace_B(list_B),
        "pool_trace": build_trace_A(list_A)
    }

@app.get("/api/recommendations")
def get_recommendations():
    ids = get_draft_ids()
    if not ids:
        return []
    last_id = ids[-1]
    counters = COUNTER_MAP.get(last_id, [])
    result = []
    for idx, c_id in enumerate(counters):
        hero = get_hero_by_id(c_id)
        if hero:
            h = hero.copy()
            h["img"] = get_hero_img_url(h["nama"])
            result.append({
                "hero": h,
                "reason": "Counter optimal untuk laning dan teamfight.",
                "rate": 85 - (idx * 5)
            })
    return result

@app.post("/api/draft/add")
async def add_to_draft(request: Request):
    body = await request.json()
    hero_id = body.get("hero_id")
    if hero_id is None:
        return JSONResponse(status_code=400, content={"success": False, "message": "Missing hero_id"})
    
    list_A, list_B = reconstruct_lists()
    
    # Cari hero di List A dan cabut (Delete Node)
    node = list_A.find_and_remove(hero_id)
    if not node:
        # Cek apakah hero sudah ada di List B (Draft)
        curr = list_B.head
        in_draft = False
        while curr:
            if curr.id == hero_id:
                in_draft = True
                break
            curr = curr.next
        if in_draft:
            hero = get_hero_by_id(hero_id)
            return JSONResponse(status_code=400, content={"success": False, "message": f"Hero {hero['nama']} already selected"})
        else:
            return JSONResponse(status_code=404, content={"success": False, "message": "Hero not found"})
            
    # Cek apakah draft sudah penuh
    draft_nodes = list_B.to_list()
    if len(draft_nodes) >= 5:
        return JSONResponse(status_code=400, content={"success": False, "message": "Draft is full (maximum 5 heroes)"})
        
    # Sambungkan ke List B (Insert Node)
    list_B.append(node)
    
    # Simpan kembali status draft terupdate ke database
    new_draft_ids = [n.id for n in list_B.to_list()]
    save_draft_ids(new_draft_ids)
    
    return {"success": True, "message": f"Added {node.nama} to draft"}

@app.post("/api/draft/reset")
def reset_draft():
    save_draft_ids([])
    return {"success": True, "message": "Draft selection reset"}

# Vercel handler
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True, app_dir=script_dir)
