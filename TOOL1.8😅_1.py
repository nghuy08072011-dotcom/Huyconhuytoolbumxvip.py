from __future__ import annotations
import json
import sys
import time
from time import sleep  # Thêm dòng này
import threading
import random
import logging
import math
import re
import base64
import os
from collections import defaultdict, deque
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from typing import Any, Dict, Tuple, Optional, List
import concurrent.futures

import pytz
import requests
import websocket
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.align import Align
from rich.rule import Rule
from rich.text import Text
from rich import box
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.style import Style
from rich.bar import Bar
from rich.color import Color
from rich.emoji import Emoji
from bs4 import BeautifulSoup
from faker import Faker
from colorama import Fore, Style, init as colorama_init
import pystyle
from pyfiglet import Figlet

# Khởi tạo colorama
colorama_init(autoreset=True)

# ============================================
# HỆ THỐNG MÀU SẮC MỚI - HIỆN ĐẠI
# ============================================
class Colors:
    AQUA = "\033[1;36m"
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[1;34m"
    PURPLE = "\033[1;35m"
    WHITE = "\033[1;97m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    END = '\033[0m'
    
    # Gradient colors for modern look
    GRADIENT = [RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, MAGENTA]

class Styles:
    BORDER_DOUBLE = "═" * 60
    BORDER_SINGLE = "─" * 60
    BORDER_STAR = "✦" * 60
    ARROW = "➤"
    CHECK = "✅"
    CROSS = "❌"
    INFO = "ℹ"
    KEY = "🔑"
    LINK = "🔗"
    USER = "👤"
    TIME = "⏰"
    LOCK = "🔒"
    UNLOCK = "🔓"
    WARNING = "⚠"
    LOADING = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]

# ============================================
# GIAO DIỆN HIỆN ĐẠI - KEY ACTIVATION
# ============================================
def print_gradient(text, speed=0.000001):
    """Hiệu ứng chữ gradient hiện đại"""
    gradient = Colors.GRADIENT
    for i, char in enumerate(text):
        color = gradient[i % len(gradient)]
        sys.stdout.write(f"{color}{char}")
        sys.stdout.flush()
        sleep(speed)
    print(Colors.END)

def print_centered(text, color=Colors.WHITE):
    """In chữ căn giữa"""
    width = 60
    padding = (width - len(text)) // 2
    print(f"{' ' * padding}{color}{text}{Colors.END}")

def print_section(title, color=Colors.CYAN):
    """In section với border đẹp"""
    print(f"\n{Colors.PURPLE}{Styles.BORDER_SINGLE}")
    print_centered(f" {Styles.ARROW} {title} {Styles.ARROW} ", color)
    print(f"{Colors.PURPLE}{Styles.BORDER_SINGLE}{Colors.END}")

def print_menu_item(number, text, icon="•"):
    """In item menu đẹp"""
    print(f"  {Colors.WHITE}[{Colors.GREEN}{number}{Colors.WHITE}] {Colors.YELLOW}{icon} {Colors.CYAN}{text}")

def print_status(message, status_type="info"):
    """In thông báo trạng thái"""
    icons = {
        "success": f"{Colors.GREEN}{Styles.CHECK}",
        "error": f"{Colors.RED}{Styles.CROSS}",
        "warning": f"{Colors.YELLOW}{Styles.WARNING}",
        "info": f"{Colors.BLUE}{Styles.INFO}",
        "key": f"{Colors.YELLOW}{Styles.KEY}"
    }
    icon = icons.get(status_type, icons["info"])
    print(f"\n  {icon} {Colors.WHITE}{message}{Colors.END}")

def loading_animation(text="Đang xử lý", duration=1):
    """Hiệu ứng loading đẹp"""
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r  {Colors.YELLOW}{Styles.LOADING[i % len(Styles.LOADING)]} {text}{' ' * 10}")
        sys.stdout.flush()
        i += 1
        sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")

# ============================================
# BANNER MỚI - SIÊU ĐẸP
# ============================================
def banner():
    os.system("cls" if os.name == "nt" else "clear")
    
    # Tạo banner với gradient effect
    banner_text = f"""
{Colors.BLUE}{Styles.BORDER_DOUBLE}
{Colors.PURPLE}      ██████╗ ██╗   ██╗████████╗ ██████╗  ██████╗ ██╗     
{Colors.BLUE}      ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     
{Colors.CYAN}      ██████╔╝██║   ██║   ██║   ██║   ██║██║   ██║██║     
{Colors.GREEN}      ██╔═══╝ ██║   ██║   ██║   ██║   ██║██║   ██║██║     
{Colors.YELLOW}      ██║     ╚██████╔╝   ██║   ╚██████╔╝╚██████╔╝███████╗
{Colors.RED}      ╚═╝      ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
{Colors.MAGENTA}               ✦ P R E M I U M  T O O L  V 4 ✦
{Colors.BLUE}{Styles.BORDER_DOUBLE}{Colors.END}
"""
    
    for line in banner_text.split('\n'):
        if any(char in line for char in ['█', '╗', '║', '╝', '╔', '═', '╚']):
            print_gradient(line, 0.00001)
        else:
            print(line)
    
    # Thông tin tool với icon
    info_lines = [
        f"{Colors.WHITE}{Styles.USER}  Tác Giả: {Colors.GREEN}DUY PHÚC",
        f"{Colors.WHITE}{Styles.LOCK}  Phiên Bản: {Colors.YELLOW}VIP PREMIUM",
        f"{Colors.WHITE}{Styles.TIME}  Ngày: {Colors.CYAN}{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        f"{Colors.WHITE}{Styles.LINK}  Zalo: {Colors.AQUA}https://zalo.me/g/nguadz335",
        f"{Colors.WHITE}{Styles.LINK}  YouTube: {Colors.RED}REVIEWTOOL247NK"
    ]
    
    for line in info_lines:
        print_centered(line)
    
    print(f"\n{Colors.PURPLE}{Styles.BORDER_STAR}{Colors.END}")

# ============================================
# CÁC HÀM CHỨC NĂNG KEY ACTIVATION
# ============================================
# Tạo hoặc đọc khóa mã hóa bằng base64
secret_key = base64.urlsafe_b64encode(os.urandom(32))

# Mã hóa và giải mã dữ liệu bằng base64
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    return base64.b64decode(encrypted_data.encode()).decode()

def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        ip_address = ip_data['ip']
        return ip_address
    except Exception as e:
        print_status(f"Lỗi khi lấy địa chỉ IP: {e}", "error")
        return None

def display_ip_address(ip_address):
    if ip_address:
        banner()
        print_section("THÔNG TIN HỆ THỐNG", Colors.GREEN)
        print_centered(f"{Styles.INFO} Địa Chỉ IP: {Colors.CYAN}{ip_address}", Colors.WHITE)
        print_centered(f"{Styles.TIME} Thời Gian: {Colors.YELLOW}{datetime.now().strftime('%H:%M:%S')}", Colors.WHITE)
    else:
        print_status("Không thể lấy địa chỉ IP của thiết bị", "error")

def luu_thong_tin_ip(ip, key, expiration_date):
    data = {ip: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    encrypted_data = encrypt_data(json.dumps(data))

    with open('ip_key.json', 'w') as file:
        file.write(encrypted_data)

def tai_thong_tin_ip():
    try:
        with open('ip_key.json', 'r') as file:
            encrypted_data = file.read()
        data = json.loads(decrypt_data(encrypted_data))
        return data
    except FileNotFoundError:
        return None

def kiem_tra_ip(ip):
    data = tai_thong_tin_ip()
    if data and ip in data:
        expiration_date = datetime.fromisoformat(data[ip]['expiration_date'])
        if expiration_date > datetime.now():
            return data[ip]['key']
    return None

def generate_key_and_url(ip_address):
    ngay = int(datetime.now().day)
    key1 = str(ngay * 27 + 27)
    ip_numbers = ''.join(filter(str.isdigit, ip_address))
    key = f'DUYTOOL143613treytdio91so{key1}{ip_numbers}'
    expiration_date = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    url = f'https://www.webkey.x10.mx/?ma={key}'
    return url, key, expiration_date

def da_qua_gio_moi():
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return now >= midnight

def get_shortened_link_phu(url):
    """
    Hàm để rút gọn URL bằng một dịch vụ API.
    """
    try:
        token = "66bc3245dfd246144040ac98"  # Thay bằng API Token Của Bạn
        api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={url}"

        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"status": "error", "message": "Không thể kết nối đến dịch vụ rút gọn URL."}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi khi rút gọn URL: {e}"}

# ============================================
# HÀM KEY ACTIVATION MAIN
# ============================================
def key_activation_main():
    ip_address = get_ip_address()
    display_ip_address(ip_address)

    if ip_address:
        existing_key = kiem_tra_ip(ip_address)
        if existing_key:
            print_status(f"{Styles.UNLOCK} Tool còn hạn sử dụng, mời bạn tiếp tục...", "success")
            loading_animation("Đang mở công cụ", 2)
            return True
        else:
            if da_qua_gio_moi():
                print_status("Đã quá giờ sử dụng tool! Vui lòng thử lại vào ngày mai.", "warning")
                return False

            url, key, expiration_date = generate_key_and_url(ip_address)

            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                print_section("LỰA CHỌN KÍCH HOẠT", Colors.YELLOW)
                print_menu_item("1", "LẤY KEY KÍCH HOẠT MIỄN PHÍ", Styles.KEY)
                print_menu_item("0", "THOÁT CHƯƠNG TRÌNH", Styles.CROSS)
                print(f"\n{Colors.PURPLE}{Styles.BORDER_SINGLE}{Colors.END}")

                while True:
                    try:
                        choice = input(f"\n  {Colors.WHITE}[{Colors.GREEN}?{Colors.WHITE}] {Colors.CYAN}Nhập lựa chọn của bạn: {Colors.YELLOW}")
                        
                        if choice == "1":
                            print_status("Đang tạo liên kết kích hoạt...", "info")
                            loading_animation("Đang xử lý API", 1)
                            
                            yeumoney_future = executor.submit(get_shortened_link_phu, url)
                            yeumoney_data = yeumoney_future.result()
                            
                            if yeumoney_data and yeumoney_data.get('status') == "error":
                                print_status(yeumoney_data.get('message'), "error")
                                return False
                            else:
                                link_key_yeumoney = yeumoney_data.get('shortenedUrl')
                                print_section("LIÊN KẾT KÍCH HOẠT", Colors.GREEN)
                                print_centered(f"{Styles.LINK} {Colors.CYAN}{link_key_yeumoney}", Colors.WHITE)
                                print(f"\n{Colors.PURPLE}{Styles.BORDER_SINGLE}{Colors.END}")
                            
                            # Vòng lặp nhập key
                            attempts = 3
                            while attempts > 0:
                                print_status(f"Số lần thử còn lại: {attempts}", "info")
                                keynhap = input(f"\n  {Colors.WHITE}[{Colors.YELLOW}🔑{Colors.WHITE}] {Colors.CYAN}Nhập key đã lấy được: {Colors.GREEN}")
                                
                                if keynhap == key:
                                    print_status(f"{Styles.CHECK} Xác thực thành công! Key chính xác.", "success")
                                    loading_animation("Đang kích hoạt bản quyền", 2)
                                    luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                                    
                                    # Hiển thị thông tin kích hoạt thành công
                                    print_section("KÍCH HOẠT THÀNH CÔNG", Colors.GREEN)
                                    print_centered(f"{Styles.CHECK} Bản quyền đã được kích hoạt!", Colors.GREEN)
                                    print_centered(f"{Styles.TIME} Hạn sử dụng đến: {Colors.YELLOW}{expiration_date.strftime('%H:%M %d/%m/%Y')}", Colors.WHITE)
                                    loading_animation("Chuyển hướng đến công cụ chính", 2)
                                    return True
                                else:
                                    attempts -= 1
                                    if attempts > 0:
                                        print_status(f"{Styles.CROSS} Key không chính xác! Vui lòng thử lại.", "error")
                                        print_centered(f"{Styles.LINK} Truy cập lại: {Colors.CYAN}{link_key_yeumoney}", Colors.WHITE)
                                    else:
                                        print_status("Đã hết số lần thử! Vui lòng khởi động lại tool.", "error")
                                        return False
                            
                        elif choice == "0":
                            print_status("Cảm ơn bạn đã sử dụng tool! Hẹn gặp lại.", "info")
                            sys.exit()
                        else:
                            print_status("Lựa chọn không hợp lệ! Vui lòng nhập 1 hoặc 0.", "warning")
                            
                    except ValueError:
                        print_status("Vui lòng nhập số hợp lệ.", "warning")
                    except KeyboardInterrupt:
                        print_status("Cảm ơn bạn đã sử dụng Tool! Chương trình sẽ đóng.", "info")
                        sys.exit()
    return False

# ============================================
# ESCAPE MASTER VIP PRO - PHẦN CHÍNH
# ============================================
console = Console()
tz = pytz.timezone("Asia/Ho_Chi_Minh")

logger = logging.getLogger("escape_master_pro")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("escape_master_pro.log", encoding="utf-8")
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Endpoints
BET_API_URL = "https://api.escapemaster.net/escape_game/bet"
WS_URL = "wss://api.escapemaster.net/escape_master/ws"
WALLET_API_URL = "https://wallet.3games.io/api/wallet/user_asset"

HTTP = requests.Session()
try:
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    adapter = HTTPAdapter(
        pool_connections=20, pool_maxsize=50,
        max_retries=Retry(total=3, backoff_factor=0.2,
                          status_forcelist=(500, 502, 503, 504))
    )
    HTTP.mount("https://", adapter)
    HTTP.mount("http://", adapter)
except Exception:
    pass

# TÊN PHÒNG
ROOM_NAMES = {
    1: "📦 Nhà kho", 
    2: "🪑 Phòng họp", 
    3: "👔 Phòng giám đốc",
    4: "💬 Phòng trò chuyện", 
    5: "🎥 Phòng giám sát", 
    6: "🏢 Văn phòng",
    7: "💰 Phòng tài vụ", 
    8: "👥 Phòng nhân sự"
}
ROOM_ORDER = [1, 2, 3, 4, 5, 6, 7, 8]

# runtime state
USER_ID: Optional[int] = None
SECRET_KEY: Optional[str] = None
issue_id: Optional[int] = None
issue_start_ts: Optional[float] = None
count_down: Optional[int] = None
killed_room: Optional[int] = None
round_index: int = 0
_skip_active_issue: Optional[int] = None

room_state: Dict[int, Dict[str, Any]] = {r: {"players": 0, "bet": 0} for r in ROOM_ORDER}
room_stats: Dict[int, Dict[str, Any]] = {r: {"kills": 0, "survives": 0, "last_kill_round": None, "last_players": 0, "last_bet": 0} for r in ROOM_ORDER}

predicted_room: Optional[int] = None
last_killed_room: Optional[int] = None
prediction_locked: bool = False

# balances & pnl
current_build: Optional[float] = None
current_usdt: Optional[float] = None
current_world: Optional[float] = None
last_balance_ts: Optional[float] = None
last_balance_val: Optional[float] = None
starting_balance: Optional[float] = None
cumulative_profit: float = 0.0

# streaks
win_streak: int = 0
lose_streak: int = 0
max_win_streak: int = 0
max_lose_streak: int = 0

# betting
base_bet: float = 1.0
multiplier: float = 2.0
current_bet: Optional[float] = None
run_mode: str = "AUTO"

# AUTO or STAT
bet_rounds_before_skip: int = 0
_rounds_placed_since_skip: int = 0
skip_next_round_flag: bool = False

bet_history: deque = deque(maxlen=500)
bet_sent_for_issue: set = set()

# new controls
pause_after_losses: int = 0
_skip_rounds_remaining: int = 0
profit_target: Optional[float] = None
stop_when_profit_reached: bool = False
stop_loss_target: Optional[float] = None
stop_when_loss_reached: bool = False
stop_flag: bool = False

# UI / timing
ui_state: str = "IDLE"
analysis_start_ts: Optional[float] = None
analysis_blur: bool = False
last_msg_ts: float = time.time()
last_balance_fetch_ts: float = 0.0
BALANCE_POLL_INTERVAL: float = 4.0
_ws: Dict[str, Any] = {"ws": None}

# selection config
SELECTION_CONFIG = {
    "max_bet_allowed": float("inf"),
    "max_players_allowed": 9999,
    "avoid_last_kill": True,
}

# Thuật toán mới với tên VIP
SELECTION_MODES = {
    "VIP_NEURAL": "VIP Neural AI",
    "VIP_QUANTUM": "VIP Quantum AI", 
    "VIP_DEEP": "VIP Deep AI",
    "VIP_FUSION": "VIP Fusion AI"
}
settings = {"algo": "VIP_NEURAL"}

# Màu sắc chuyên nghiệp cho VIP
VIP_COLORS = {
    "gold": "#FFD700",
    "silver": "#C0C0C0", 
    "bronze": "#CD7F32",
    "purple": "#9B59B6",
    "blue": "#3498DB",
    "green": "#2ECC71",
    "red": "#E74C3C",
    "orange": "#E67E22"
}

GRADIENT_COLORS = ["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe", "#00f2fe"]

# Banner ASCII Art
BANNERS = [
    """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ███████╗███████╗ ██████╗ █████╗ ██████╗ ███████╗    ███╗   ███╗ █████╗     ║
║  ██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝    ████╗ ████║██╔══██╗    ║
║  █████╗  ███████╗██║     ███████║██████╔╝█████╗      ██╔████╔██║███████║    ║
║  ██╔══╝  ╚════██║██║     ██╔══██║██╔═══╝ ██╔══╝      ██║╚██╔╝██║██╔══██║    ║
║  ███████╗███████║╚██████╗██║  ██║██║     ███████╗    ██║ ╚═╝ ██║██║  ██║    ║
║  ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝    ║
║                                                                              ║
║                      ██╗   ██╗██╗██████╗     ██████╗ ██████╗                 ║
║                      ██║   ██║██║██╔══██╗    ██╔══██╗██╔══██╗                ║
║                      ██║   ██║██║██████╔╝    ██████╔╝██████╔╝                ║
║                      ╚██╗ ██╔╝██║██╔═══╝     ██╔═══╝ ██╔══██╗                ║
║                       ╚████╔╝ ██║██║         ██║     ██║  ██║                ║
║                        ╚═══╝  ╚═╝╚═╝         ╚═╝     ╚═╝  ╚═╝                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """,
    """
███████╗███████╗ ██████╗ █████╗ ██████╗ ███████╗    ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ 
██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝    ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
████╗  ███████╗██║     ███████║██████╔╝█████╗      ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝
██╔══╝  ╚════██║██║     ██╔══██║██╔═══╝ ██╔══╝      ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
███████╗███████║╚██████╗██║  ██║██║     ███████╗    ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║
╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                                                                        
                        ██╗   ██╗██╗██████╗     ██████╗ ██████╗ 
                        ██║   ██║██║██╔══██╗    ██╔══██╗██╔══██╗
                        ██║   ██║██║██████╔╝    ██████╔╝██████╔╝
                        ╚██╗ ██╔╝██║██╔═══╝     ██╔═══╝ ██╔══██╗
                         ╚████╔╝ ██║██║         ██║     ██║  ██║
                          ╚═══╝  ╚═╝╚═╝         ╚═╝     ╚═╝  ╚═╝
    """
]

# Biểu tượng VIP
VIP_SYMBOLS = {
    "crown": "👑",
    "diamond": "💎",
    "trophy": "🏆",
    "fire": "🔥",
    "star": "⭐",
    "shield": "🛡️",
    "rocket": "🚀",
    "brain": "🧠",
    "money": "💰",
    "chart": "📈",
    "clock": "⏱️",
    "warning": "⚠️",
    "success": "✅",
    "error": "❌"
}

_num_re = re.compile(r"-?\d+[\d,]*\.?\d*")

# -------------------- UTILITIES --------------------

def log_debug(msg: str):
    try:
        logger.debug(msg)
    except Exception:
        pass

def _parse_number(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x)
    m = _num_re.search(s)
    if not m:
        return None
    token = m.group(0).replace(",", "")
    try:
        return float(token)
    except Exception:
        return None

def human_ts() -> str:
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

def safe_input(prompt: str, default=None, cast=None):
    try:
        s = input(prompt).strip()
    except EOFError:
        return default
    if s == "":
        return default
    if cast:
        try:
            return cast(s)
        except Exception:
            return default
    return s

def get_vip_color(color_name: str = "gold") -> str:
    """Lấy màu VIP"""
    return VIP_COLORS.get(color_name, VIP_COLORS["gold"])

def get_gradient_color(progress: float) -> str:
    """Lấy màu gradient theo tiến trình"""
    idx = min(int(progress * (len(GRADIENT_COLORS) - 1)), len(GRADIENT_COLORS) - 1)
    return GRADIENT_COLORS[idx]

def get_spinner() -> str:
    """Lấy spinner animation"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    return frames[int(time.time() * 10) % len(frames)]

def print_vip_banner():
    """In banner VIP đẹp"""
    banner = random.choice(BANNERS)
    lines = banner.split('\n')
    for line in lines:
        if '█' in line or '║' in line or '╔' in line or '╚' in line:
            console.print(f"[{get_vip_color('gold')}]{line}[/]")
        else:
            console.print(f"[{get_vip_color('purple')}]{line}[/]")

# -------------------- BALANCE PARSING & FETCH --------------------

def _parse_balance_from_json(j: Dict[str, Any]) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    if not isinstance(j, dict):
        return None, None, None
    build = None
    world = None
    usdt = None

    data = j.get("data") if isinstance(j.get("data"), dict) else j
    if isinstance(data, dict):
        cwallet = data.get("cwallet") if isinstance(data.get("cwallet"), dict) else None
        if cwallet:
            for key in ("ctoken_contribute", "ctoken", "build", "balance", "amount"):
                if key in cwallet and build is None:
                    build = _parse_number(cwallet.get(key))
        for k in ("build", "ctoken", "ctoken_contribute"):
            if build is None and k in data:
                build = _parse_number(data.get(k))
        for k in ("usdt", "kusdt", "usdt_balance"):
            if usdt is None and k in data:
                usdt = _parse_number(data.get(k))
        for k in ("world", "xworld"):
            if world is None and k in data:
                world = _parse_number(data.get(k))

    found = []

    def walk(o: Any, path=""):
        if isinstance(o, dict):
            for kk, vv in o.items():
                nk = (path + "." + str(kk)).strip(".")
                if isinstance(vv, (dict, list)):
                    walk(vv, nk)
                else:
                    n = _parse_number(vv)
                    if n is not None:
                        found.append((nk.lower(), n))
        elif isinstance(o, list):
            for idx, it in enumerate(o):
                walk(it, f"{path}[{idx}]")

    walk(j)

    for k, n in found:
        if build is None and any(x in k for x in ("ctoken", "build", "contribute", "balance")):
            build = n
        if usdt is None and "usdt" in k:
            usdt = n
        if world is None and any(x in k for x in ("world", "xworld")):
            world = n

    return build, world, usdt

def balance_headers_for(uid: Optional[int] = None, secret: Optional[str] = None) -> Dict[str, str]:
    h = {
        "accept": "*/*",
        "accept-language": "vi,en;q=0.9",
        "cache-control": "no-cache",
        "country-code": "vn",
        "origin": "https://xworld.info",
        "pragma": "no-cache",
        "referer": "https://xworld.info/",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
        "user-login": "login_v2",
        "xb-language": "vi-VN",
    }
    if uid is not None:
        h["user-id"] = str(uid)
    if secret:
        h["user-secret-key"] = str(secret)
    return h

def fetch_balances_3games(retries=2, timeout=6, params=None, uid=None, secret=None):
    """
    Non-blocking friendly: call from background threads if you don't want UI block.
    """
    global current_build, current_usdt, current_world, last_balance_ts
    global starting_balance, last_balance_val, cumulative_profit

    uid = uid or USER_ID
    secret = secret or SECRET_KEY
    payload = {"user_id": int(uid) if uid is not None else None, "source": "home"}

    attempt = 0
    while attempt <= retries:
        attempt += 1
        try:
            r = HTTP.post(
                WALLET_API_URL,
                json=payload,
                headers=balance_headers_for(uid, secret),
                timeout=timeout,
            )
            r.raise_for_status()
            j = r.json()

            build, world, usdt = _parse_balance_from_json(j)

            if build is not None:
                if last_balance_val is None:
                    starting_balance = build
                    last_balance_val = build
                else:
                    delta = float(build) - float(last_balance_val)
                    if abs(delta) > 0:
                        cumulative_profit += delta
                        last_balance_val = build
                current_build = build
            if usdt is not None:
                current_usdt = usdt
            if world is not None:
                current_world = world

            last_balance_ts = time.time()
            return current_build, current_world, current_usdt

        except Exception as e:
            log_debug(f"wallet fetch attempt {attempt} error: {e}")
            time.sleep(min(0.6 * attempt, 2))

    return current_build, current_world, current_usdt

# -------------------- VIP ALGORITHM SELECTION --------------------

def _room_features(rid: int):
    """Tính toán đặc trưng phòng"""
    st = room_state.get(rid, {})
    stats = room_stats.get(rid, {})
    players = float(st.get("players", 0))
    bet = float(st.get("bet", 0))
    bet_per_player = (bet / players) if players > 0 else bet
    kill_count = float(stats.get("kills", 0))
    survive_count = float(stats.get("survives", 0))
    kill_rate = (kill_count + 0.5) / (kill_count + survive_count + 1.0)
    survive_score = 1.0 - kill_rate
    
    recent_history = list(bet_history)[-8:]
    recent_pen = 0.0
    for i, rec in enumerate(reversed(recent_history)):
        if rec.get("room") == rid:
            recent_pen += 0.12 * (1.0 / (i + 1))
    
    last_pen = 0.0
    if last_killed_room == rid:
        last_pen = 0.35 if SELECTION_CONFIG.get("avoid_last_kill", True) else 0.0
    
    players_norm = min(1.0, players / 50.0)
    bet_norm = 1.0 / (1.0 + bet / 2000.0)
    bpp_norm = 1.0 / (1.0 + bet_per_player / 1200.0)
    
    return {
        "players": players,
        "players_norm": players_norm,
        "bet": bet,
        "bet_norm": bet_norm,
        "bet_per_player": bet_per_player,
        "bpp_norm": bpp_norm,
        "kill_rate": kill_rate,
        "survive_score": survive_score,
        "recent_pen": recent_pen,
        "last_pen": last_pen
    }

def choose_room_vip_neural() -> Tuple[int, str]:
    """VIP Neural AI Algorithm"""
    cand = [r for r in ROOM_ORDER]
    
    # Tạo neural network VIP
    rng = random.Random(999888777)
    layer1_neurons = []
    for _ in range(12):  # 12 neuron layer 1
        weights = [rng.uniform(-0.8, 0.8) for _ in range(6)]
        bias = rng.uniform(-0.3, 0.3)
        layer1_neurons.append((weights, bias))
    
    layer2_neurons = []
    for _ in range(6):  # 6 neuron layer 2
        weights = [rng.uniform(-0.8, 0.8) for _ in range(12)]
        bias = rng.uniform(-0.3, 0.3)
        layer2_neurons.append((weights, bias))
    
    output_weights = [rng.uniform(-0.8, 0.8) for _ in range(6)]
    output_bias = rng.uniform(-0.3, 0.3)
    
    scores = {}
    for room in cand:
        features = _room_features(room)
        
        inputs = [
            features["players_norm"],
            features["bet_norm"],
            features["bpp_norm"],
            features["survive_score"],
            1.0 - features["recent_pen"],
            1.0 - features["last_pen"]
        ]
        
        # Layer 1 với activation ReLU
        layer1_output = []
        for weights, bias in layer1_neurons:
            z = sum(w * i for w, i in zip(weights, inputs)) + bias
            a = max(0, z)  # ReLU
            layer1_output.append(a)
        
        # Layer 2 với activation tanh
        layer2_output = []
        for weights, bias in layer2_neurons:
            z = sum(w * i for w, i in zip(weights, layer1_output)) + bias
            a = math.tanh(z)
            layer2_output.append(a)
        
        # Output layer
        final_score = sum(w * i for w, i in zip(output_weights, layer2_output)) + output_bias
        scores[room] = final_score
    
    best_room = max(scores.items(), key=lambda x: x[1])[0]
    return best_room, "VIP_NEURAL"

def choose_room_vip_quantum() -> Tuple[int, str]:
    """VIP Quantum AI Algorithm"""
    cand = [r for r in ROOM_ORDER]
    
    # Quantum probability distribution
    quantum_probs = {}
    for room in cand:
        features = _room_features(room)
        
        # Quantum state superposition
        state_amplitude = 0.0
        state_amplitude += 0.25 * features["survive_score"]  # Survival probability
        state_amplitude += 0.20 * (1.0 - features["last_pen"])  # Avoid last kill
        state_amplitude += 0.15 * features["players_norm"]  # Player distribution
        state_amplitude += 0.15 * (1.0 - features["recent_pen"])  # Recent history
        state_amplitude += 0.10 * features["bet_norm"]  # Bet amount
        state_amplitude += 0.10 * features["bpp_norm"]  # Bet per player
        
        # Quantum interference
        interference = math.sin(room * 1.618 + time.time() * 0.05) * 0.08
        state_amplitude += interference
        
        # Quantum tunneling effect for underdog rooms
        if features["players"] < 8:
            state_amplitude += 0.12
        
        # Probability = |amplitude|^2
        probability = abs(state_amplitude) ** 2
        quantum_probs[room] = probability
    
    best_room = max(quantum_probs.items(), key=lambda x: x[1])[0]
    return best_room, "VIP_QUANTUM"

def choose_room_vip_deep() -> Tuple[int, str]:
    """VIP Deep Learning Algorithm"""
    cand = [r for r in ROOM_ORDER]
    
    # Deep learning model với multiple factors
    deep_scores = {}
    
    # Lấy lịch sử 20 ván gần nhất
    history_depth = min(20, len(bet_history))
    recent_bets = list(bet_history)[-history_depth:] if bet_history else []
    
    for room in cand:
        features = _room_features(room)
        
        # Base score từ đặc trưng
        score = 0.0
        
        # Factor 1: Survival rate (35%)
        score += 0.35 * features["survive_score"]
        
        # Factor 2: Avoid recent patterns (25%)
        score += 0.25 * (1.0 - features["recent_pen"])
        
        # Factor 3: Player distribution (20%)
        player_score = 1.0 - abs(features["players_norm"] - 0.3)  # Ưu tiên ~30% capacity
        score += 0.20 * player_score
        
        # Factor 4: Bet patterns (15%)
        bet_score = features["bet_norm"] * 0.7 + features["bpp_norm"] * 0.3
        score += 0.15 * bet_score
        
        # Factor 5: Avoid last kill (5%)
        score += 0.05 * (1.0 - features["last_pen"])
        
        # Historical win rate adjustment
        room_wins = sum(1 for bet in recent_bets if bet.get("room") == room and bet.get("result") in ["Thắng", "Win"])
        room_total = sum(1 for bet in recent_bets if bet.get("room") == room)
        if room_total > 2:
            win_rate = room_wins / room_total
            score += 0.10 * win_rate
        
        # Random noise for exploration
        exploration = (math.sin(room * 3.14159) * 0.03)
        score += exploration
        
        deep_scores[room] = score
    
    best_room = max(deep_scores.items(), key=lambda x: x[1])[0]
    return best_room, "VIP_DEEP"

def choose_room_vip_fusion() -> Tuple[int, str]:
    """VIP Fusion AI - Kết hợp tất cả thuật toán"""
    # Lấy kết quả từ 3 thuật toán VIP
    results = []
    
    # Neural
    neural_room, _ = choose_room_vip_neural()
    results.append(neural_room)
    
    # Quantum
    quantum_room, _ = choose_room_vip_quantum()
    results.append(quantum_room)
    
    # Deep
    deep_room, _ = choose_room_vip_deep()
    results.append(deep_room)
    
    # Bỏ phiếu có trọng số
    from collections import Counter
    vote_counts = Counter(results)
    
    # Nếu có hòa, ưu tiên theo độ tin cậy
    if len(set(results)) == 3:  # Cả 3 khác nhau
        # Tính confidence score cho mỗi phòng
        conf_scores = {}
        for room in set(results):
            features = _room_features(room)
            # Phòng có survival score cao và ít người được ưu tiên
            confidence = features["survive_score"] * 0.6 + (1.0 - features["players_norm"]) * 0.4
            conf_scores[room] = confidence
        
        best_room = max(conf_scores.items(), key=lambda x: x[1])[0]
    else:
        best_room = vote_counts.most_common(1)[0][0]
    
    return best_room, "VIP_FUSION"

# -------------------- BETTING HELPERS --------------------

def api_headers() -> Dict[str, str]:
    return {
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0",
        "user-id": str(USER_ID) if USER_ID else "",
        "user-secret-key": SECRET_KEY if SECRET_KEY else ""
    }

def place_bet_http(issue: int, room_id: int, amount: float) -> dict:
    payload = {"asset_type": "BUILD", "user_id": USER_ID, "room_id": int(room_id), "bet_amount": float(amount)}
    try:
        r = HTTP.post(BET_API_URL, headers=api_headers(), json=payload, timeout=6)
        try:
            return r.json()
        except Exception:
            return {"raw": r.text, "http_status": r.status_code}
    except Exception as e:
        return {"error": str(e)}

def record_bet(issue: int, room_id: int, amount: float, resp: dict, algo_used: Optional[str] = None) -> dict:
    now = datetime.now(tz).strftime("%H:%M:%S")
    rec = {
        "issue": issue, 
        "room": room_id, 
        "amount": float(amount), 
        "time": now, 
        "resp": resp, 
        "result": "Đang chờ", 
        "algo": algo_used, 
        "delta": 0.0, 
        "win_streak": win_streak, 
        "lose_streak": lose_streak
    }
    bet_history.append(rec)
    return rec

def place_bet_async(issue: int, room_id: int, amount: float, algo_used: Optional[str] = None):
    def worker():
        console.print(f"[{get_vip_color('blue')}]{VIP_SYMBOLS['rocket']} VIP Đang đặt {amount} BUILD → {ROOM_NAMES.get(room_id)} (v{issue})[/]")
        time.sleep(random.uniform(0.02, 0.25))
        res = place_bet_http(issue, room_id, amount)
        rec = record_bet(issue, room_id, amount, res, algo_used=algo_used)
        if isinstance(res, dict) and (res.get("msg") == "ok" or res.get("code") == 0 or res.get("status") in ("ok", 1)):
            bet_sent_for_issue.add(issue)
            console.print(f"[{get_vip_color('green')}]{VIP_SYMBOLS['success']} VIP Đặt thành công {amount} BUILD vào {ROOM_NAMES.get(room_id)}[/]")
        else:
            console.print(f"[{get_vip_color('red')}]{VIP_SYMBOLS['error']} VIP Đặt lỗi v{issue}[/]")
    threading.Thread(target=worker, daemon=True).start()

# -------------------- LOCK & AUTO-BET --------------------

def lock_prediction_if_needed(force: bool = False):
    global prediction_locked, predicted_room, ui_state, current_bet, _rounds_placed_since_skip, skip_next_round_flag, _skip_rounds_remaining, _skip_active_issue
    
    if stop_flag:
        return
    if prediction_locked and not force:
        return
    if issue_id is None:
        return
    
    # Nghỉ sau khi thua
    if _skip_rounds_remaining > 0:
        if _skip_active_issue != issue_id:
            console.print(f"[{get_vip_color('orange')}]{VIP_SYMBOLS['clock']} VIP Đang nghỉ {_skip_rounds_remaining} ván sau khi thua[/]")
            _skip_rounds_remaining -= 1
            _skip_active_issue = issue_id
        
        prediction_locked = True
        ui_state = "ANALYZING"
        return
    
    # Chọn thuật toán VIP
    algo_funcs = {
        "VIP_NEURAL": choose_room_vip_neural,
        "VIP_QUANTUM": choose_room_vip_quantum,
        "VIP_DEEP": choose_room_vip_deep,
        "VIP_FUSION": choose_room_vip_fusion
    }
    
    chosen, algo_used = algo_funcs.get(settings.get('algo', 'VIP_NEURAL'), choose_room_vip_neural)()
    predicted_room = chosen
    prediction_locked = True
    ui_state = "PREDICTED"
    
    # Đặt cược nếu ở chế độ AUTO
    if run_mode == "AUTO" and not skip_next_round_flag:
        bld, _, _ = fetch_balances_3games(params={"userId": str(USER_ID)} if USER_ID else None)
        if bld is None:
            console.print(f"[{get_vip_color('orange')}]{VIP_SYMBOLS['warning']} VIP Không lấy được số dư[/]")
            prediction_locked = False
            return
        
        if current_bet is None:
            current_bet = base_bet
        
        amt = float(current_bet)
        if amt <= 0:
            console.print(f"[{get_vip_color('red')}]{VIP_SYMBOLS['error']} VIP Số tiền không hợp lệ[/]")
            prediction_locked = False
            return
        
        place_bet_async(issue_id, predicted_room, amt, algo_used=algo_used)
        _rounds_placed_since_skip += 1
        
        if bet_rounds_before_skip > 0 and _rounds_placed_since_skip >= bet_rounds_before_skip:
            skip_next_round_flag = True
            _rounds_placed_since_skip = 0
    elif skip_next_round_flag:
        console.print(f"[{get_vip_color('orange')}]{VIP_SYMBOLS['clock']} VIP Tạm dừng theo cấu hình[/]")
        skip_next_round_flag = False

# -------------------- WEBSOCKET HANDLERS --------------------

def safe_send_enter_game(ws):
    if not ws:
        return
    try:
        payload = {"msg_type": "handle_enter_game", "asset_type": "BUILD", "user_id": USER_ID, "user_secret_key": SECRET_KEY}
        ws.send(json.dumps(payload))
    except Exception:
        pass

def _extract_issue_id(d: Dict[str, Any]) -> Optional[int]:
    if not isinstance(d, dict):
        return None
    possible = []
    for key in ("issue_id", "issueId", "issue", "id"):
        v = d.get(key)
        if v is not None:
            possible.append(v)
    if isinstance(d.get("data"), dict):
        for key in ("issue_id", "issueId", "issue", "id"):
            v = d["data"].get(key)
            if v is not None:
                possible.append(v)
    for p in possible:
        try:
            return int(p)
        except Exception:
            try:
                return int(str(p))
            except Exception:
                continue
    return None

def on_open(ws):
    _ws["ws"] = ws
    console.print(f"[{get_vip_color('gold')}]{VIP_SYMBOLS['rocket']} VIP Đang kết nối đến game server...[/]")
    safe_send_enter_game(ws)

def _background_fetch_balance_after_result():
    try:
        fetch_balances_3games()
    except Exception:
        pass

def _mark_bet_result_from_issue(res_issue: Optional[int], krid: int):
    global current_bet, win_streak, lose_streak, max_win_streak, max_lose_streak
    global _skip_rounds_remaining, stop_flag, _skip_active_issue
    
    if res_issue is None:
        return
    
    if res_issue not in bet_sent_for_issue:
        return
    
    rec = next((b for b in reversed(bet_history) if b.get("issue") == res_issue), None)
    if rec is None:
        return
    
    if rec.get("settled"):
        return
    
    try:
        placed_room = int(rec.get("room"))
        
        if placed_room != int(krid):
            rec["result"] = "Thắng"
            rec["settled"] = True
            current_bet = base_bet
            win_streak += 1
            lose_streak = 0
            if win_streak > max_win_streak:
                max_win_streak = win_streak
            console.print(f"[{get_vip_color('green')}]{VIP_SYMBOLS['trophy']} 🎉 VIP THẮNG LỚN! Chuỗi thắng: {win_streak}[/]")
        else:
            rec["result"] = "Thua"
            rec["settled"] = True
            try:
                old_bet = current_bet
                current_bet = float(rec.get("amount")) * float(multiplier)
                console.print(f"[{get_vip_color('red')}]{VIP_SYMBOLS['fire']} 🔴 VIP THUA! Tăng cược: {current_bet} BUILD[/]")
            except Exception as e:
                current_bet = base_bet
            
            lose_streak += 1
            win_streak = 0
            if lose_streak > max_lose_streak:
                max_lose_streak = lose_streak
            
            if pause_after_losses > 0:
                _skip_rounds_remaining = pause_after_losses
                _skip_active_issue = None
                console.print(f"[{get_vip_color('orange')}]{VIP_SYMBOLS['clock']} VIP Sẽ nghỉ {pause_after_losses} ván sau khi thua[/]")
    except Exception as e:
        log_debug(f"_mark_bet_result_from_issue err: {e}")
    finally:
        try:
            bet_sent_for_issue.discard(res_issue)
        except Exception:
            pass

def on_message(ws, message):
    global issue_id, count_down, killed_room, round_index, ui_state, analysis_start_ts, issue_start_ts
    global prediction_locked, predicted_room, last_killed_room, last_msg_ts, current_bet
    global win_streak, lose_streak, max_win_streak, max_lose_streak, cumulative_profit, _skip_rounds_remaining, stop_flag, analysis_blur
    
    last_msg_ts = time.time()
    try:
        if isinstance(message, bytes):
            try:
                message = message.decode("utf-8", errors="replace")
            except Exception:
                message = str(message)
        
        data = None
        try:
            data = json.loads(message)
        except Exception:
            try:
                data = json.loads(message.replace("'", '"'))
            except Exception:
                return

        if isinstance(data, dict) and isinstance(data.get("data"), str):
            try:
                inner = json.loads(data.get("data"))
                merged = dict(data)
                merged.update(inner)
                data = merged
            except Exception:
                pass

        msg_type = data.get("msg_type") or data.get("type") or ""
        msg_type = str(msg_type)
        new_issue = _extract_issue_id(data)

        # Cập nhật thông tin phòng
        if msg_type == "notify_issue_stat" or "issue_stat" in msg_type:
            rooms = data.get("rooms") or []
            if not rooms and isinstance(data.get("data"), dict):
                rooms = data["data"].get("rooms", [])
            for rm in (rooms or []):
                try:
                    rid = int(rm.get("room_id") or rm.get("roomId") or rm.get("id"))
                except Exception:
                    continue
                players = int(rm.get("user_cnt") or rm.get("userCount") or rm.get("user_cnt") or 0) or 0
                bet = int(rm.get("total_bet_amount") or rm.get("totalBet") or rm.get("bet") or 0) or 0
                room_state[rid] = {"players": players, "bet": bet}
                room_stats[rid]["last_players"] = players
                room_stats[rid]["last_bet"] = bet
            
            if new_issue is not None and new_issue != issue_id:
                issue_id = new_issue
                issue_start_ts = time.time()
                round_index += 1
                killed_room = None
                prediction_locked = False
                predicted_room = None
                ui_state = "ANALYZING"
                analysis_start_ts = time.time()

        # Countdown
        elif msg_type == "notify_count_down" or "count_down" in msg_type:
            count_down = data.get("count_down") or data.get("countDown") or data.get("count") or count_down
            try:
                count_val = int(count_down)
            except Exception:
                count_val = None
            
            if count_val is not None:
                try:
                    if count_val <= 10 and not prediction_locked:
                        analysis_blur = False
                        lock_prediction_if_needed()
                    elif count_val <= 45:
                        ui_state = "ANALYZING"
                        analysis_start_ts = time.time()
                        analysis_blur = True
                except Exception:
                    pass

        # Kết quả
        elif msg_type == "notify_result" or "result" in msg_type:
            kr = data.get("killed_room") if data.get("killed_room") is not None else data.get("killed_room_id")
            if kr is None and isinstance(data.get("data"), dict):
                kr = data["data"].get("killed_room") or data["data"].get("killed_room_id")
            
            if kr is not None:
                try:
                    krid = int(kr)
                except Exception:
                    krid = kr
                
                killed_room = krid
                last_killed_room = krid
                
                for rid in ROOM_ORDER:
                    if rid == krid:
                        room_stats[rid]["kills"] += 1
                        room_stats[rid]["last_kill_round"] = round_index
                    else:
                        room_stats[rid]["survives"] += 1

                res_issue = new_issue if new_issue is not None else issue_id
                _mark_bet_result_from_issue(res_issue, krid)
                threading.Thread(target=_background_fetch_balance_after_result, daemon=True).start()

            ui_state = "RESULT"

            def _check_stop_conditions():
                global stop_flag
                try:
                    if stop_when_profit_reached and profit_target is not None and isinstance(current_build, (int, float)) and current_build >= profit_target:
                        console.print(f"[{get_vip_color('green')}]{VIP_SYMBOLS['trophy']} 🎉 VIP ĐẠT MỤC TIÊU LÃI: {current_build} BUILD[/]")
                        stop_flag = True
                        try:
                            wsobj = _ws.get("ws")
                            if wsobj:
                                wsobj.close()
                        except Exception:
                            pass
                    if stop_when_loss_reached and stop_loss_target is not None and isinstance(current_build, (int, float)) and current_build <= stop_loss_target:
                        console.print(f"[{get_vip_color('red')}]{VIP_SYMBOLS['warning']} ⚠️ VIP STOP-LOSS: {current_build} BUILD[/]")
                        stop_flag = True
                        try:
                            wsobj = _ws.get("ws")
                            if wsobj:
                                wsobj.close()
                        except Exception:
                            pass
                except Exception:
                    pass
            
            threading.Timer(1.2, _check_stop_conditions).start()

    except Exception as e:
        log_debug(f"on_message err: {e}")

def on_close(ws, code, reason):
    log_debug(f"WS closed: {code} {reason}")

def on_error(ws, err):
    log_debug(f"WS error: {err}")

def start_ws():
    backoff = 0.6
    while not stop_flag:
        try:
            ws_app = websocket.WebSocketApp(WS_URL, on_open=on_open, on_message=on_message, on_close=on_close, on_error=on_error)
            _ws["ws"] = ws_app
            ws_app.run_forever(ping_interval=12, ping_timeout=6)
        except Exception as e:
            log_debug(f"start_ws exception: {e}")
        t = min(backoff + random.random() * 0.5, 30)
        time.sleep(t)
        backoff = min(backoff * 1.5, 30)

# -------------------- BALANCE POLLER --------------------

class BalancePoller(threading.Thread):
    def __init__(self, uid: Optional[int], secret: Optional[str], poll_seconds: int = 2):
        super().__init__(daemon=True)
        self.uid = uid
        self.secret = secret
        self.poll_seconds = max(1, int(poll_seconds))
        self._running = True

    def stop(self):
        self._running = False

    def run(self):
        while self._running and not stop_flag:
            try:
                fetch_balances_3games(params={"userId": str(self.uid)} if self.uid else None, uid=self.uid, secret=self.secret)
            except Exception:
                pass
            
            for _ in range(max(1, int(self.poll_seconds * 5))):
                if not self._running or stop_flag:
                    break
                time.sleep(0.2)

# -------------------- MONITOR --------------------

def monitor_loop():
    global last_balance_fetch_ts, last_msg_ts, stop_flag
    while not stop_flag:
        now = time.time()
        if now - last_balance_fetch_ts >= BALANCE_POLL_INTERVAL:
            last_balance_fetch_ts = now
            try:
                fetch_balances_3games(params={"userId": str(USER_ID)} if USER_ID else None)
            except Exception as e:
                log_debug(f"monitor fetch err: {e}")
        
        if now - last_msg_ts > 8:
            try:
                safe_send_enter_game(_ws.get("ws"))
            except Exception:
                pass
        
        if now - last_msg_ts > 30:
            try:
                wsobj = _ws.get("ws")
                if wsobj:
                    try:
                        wsobj.close()
                    except Exception:
                        pass
            except Exception:
                pass
        
        time.sleep(0.6)

# -------------------- VIP UI COMPONENTS --------------------

def create_vip_header() -> Panel:
    """Tạo header VIP với thông tin số dư"""
    current_time = datetime.now(tz).strftime("%H:%M:%S")
    
    # Format số dư
    b = f"{current_build:,.4f}" if isinstance(current_build, (int, float)) else "-"
    u = f"{current_usdt:,.4f}" if isinstance(current_usdt, (int, float)) else "-"
    x = f"{current_world:,.4f}" if isinstance(current_world, (int, float)) else "-"
    
    # PNL
    pnl_val = cumulative_profit if cumulative_profit is not None else 0.0
    pnl_str = f"{pnl_val:+,.4f}"
    pnl_color = get_vip_color("green") if pnl_val > 0 else (get_vip_color("red") if pnl_val < 0 else get_vip_color("silver"))
    
    # Tạo grid layout
    header_grid = Table.grid(expand=True)
    header_grid.add_column(ratio=3)
    header_grid.add_column(ratio=2)
    
    # Bên trái: Thông tin chính
    left_content = Table.grid(padding=(0, 1))
    left_content.add_row(
        Text(f"{VIP_SYMBOLS['crown']} ESCAPE MASTER VIP PRO", style=f"bold {get_vip_color('gold')}"),
        Text(f"{VIP_SYMBOLS['clock']} {current_time}  {get_spinner()}", style=f"dim {get_vip_color('silver')}")
    )
    left_content.add_row(
        Text(f"{VIP_SYMBOLS['money']} BUILD: {b}  |  USDT: {u}  |  XWORLD: {x}", style=f"bold {get_vip_color('blue')}")
    )
    
    # Bên phải: Thông tin chi tiết
    right_content = Table.grid(padding=(0, 1))
    right_content.add_row(
        Text(f"Thuật toán: {SELECTION_MODES.get(settings.get('algo', 'VIP_NEURAL'))}", style=f"bold {get_vip_color('purple')}")
    )
    right_content.add_row(
        Text(f"Lãi/Lỗ: [{pnl_color}]{pnl_str} BUILD[/{pnl_color}]", style="bold")
    )
    right_content.add_row(
        Text(f"Ván: {issue_id or '-'}  |  Tổng: {round_index}", style=f"dim {get_vip_color('silver')}")
    )
    
    # Progress bar cho mục tiêu lãi
    if profit_target and current_build:
        progress = min(1.0, float(current_build) / float(profit_target))
        bar_len = 20
        filled = int(bar_len * progress)
        bar = f"[{get_vip_color('green')}]{"█" * filled}[/{get_vip_color('green')}][{get_vip_color('silver')}]{"░" * (bar_len - filled)}[/{get_vip_color('silver')}]"
        right_content.add_row(
            Text(f"Mục tiêu: {bar} {progress*100:.1f}%", style=f"dim {get_vip_color('blue')}")
        )
    
    header_grid.add_row(left_content, right_content)
    
    return Panel(
        header_grid,
        title=f"[bold {get_vip_color('gold')}]HỆ THỐNG VIP PRO - QUẢN LÝ RỦI RO THÔNG MINH[/]",
        border_style=get_vip_color("gold"),
        padding=(1, 2),
        box=box.ROUNDED
    )

def create_streak_display() -> Panel:
    """Hiển thị chuỗi thắng/thua VIP"""
    streak_table = Table.grid(padding=(0, 1))
    
    # Chuỗi hiện tại với hiệu ứng
    streak_icon = VIP_SYMBOLS['fire'] if win_streak >= 3 else (VIP_SYMBOLS['star'] if win_streak > 0 else VIP_SYMBOLS['shield'])
    
    current_streak = Text.assemble(
        (f"{streak_icon} Chuỗi hiện tại: ", f"bold {get_vip_color('gold')}"),
        (f"Thắng: {win_streak}", f"bold {get_vip_color('green')}"),
        (" | ", f"dim {get_vip_color('silver')}"),
        (f"Thua: {lose_streak}", f"bold {get_vip_color('red')}")
    )
    
    # Kỷ lục
    max_streak = Text.assemble(
        (f"{VIP_SYMBOLS['trophy']} Kỷ lục: ", f"bold {get_vip_color('gold')}"),
        (f"Thắng: {max_win_streak}", f"bold {get_vip_color('green')}"),
        (" | ", f"dim {get_vip_color('silver')}"),
        (f"Thua: {max_lose_streak}", f"bold {get_vip_color('red')}")
    )
    
    # Hiệu ứng đặc biệt
    streak_effect = ""
    if win_streak >= 5:
        streak_effect = f"{VIP_SYMBOLS['fire']} [bold {get_vip_color('orange')}]SIÊU NÓNG![/]"
    elif win_streak >= 3:
        streak_effect = f"{VIP_SYMBOLS['fire']} [bold {get_vip_color('green')}]ĐANG NÓNG![/]"
    elif lose_streak >= 3:
        streak_effect = f"{VIP_SYMBOLS['shield']} [bold {get_vip_color('orange')}]CẦN BẢO VỆ[/]"
    
    streak_table.add_row(current_streak)
    streak_table.add_row(max_streak)
    if streak_effect:
        streak_table.add_row(Text.from_markup(streak_effect))
    
    return Panel(
        streak_table,
        title=f"[bold {get_vip_color('purple')}]THỐNG KÊ CHUỖI VIP[/]",
        border_style=get_vip_color("purple"),
        padding=(1, 1),
        box=box.SQUARE
    )

def create_rooms_display() -> Panel:
    """Hiển thị thông tin các phòng với tên gốc"""
    rooms_table = Table(
        show_header=True,
        header_style=f"bold {get_vip_color('blue')}",
        box=box.SIMPLE,
        expand=True
    )
    
    rooms_table.add_column("PHÒNG", width=4, justify="center")
    rooms_table.add_column("TÊN PHÒNG", width=18)
    rooms_table.add_column("SỐ NGƯỜI", width=8, justify="right")
    rooms_table.add_column("TỔNG CƯỢC", width=12, justify="right")
    rooms_table.add_column("TRẠNG THÁI", width=14)
    
    for room_id in ROOM_ORDER:
        st = room_state.get(room_id, {})
        players = st.get("players", 0)
        bet = st.get("bet", 0)
        room_name = ROOM_NAMES.get(room_id, f"Phòng {room_id}")
        
        # Xác định trạng thái
        status_text = ""
        status_style = ""
        
        if killed_room is not None and room_id == killed_room:
            status_text = f"{VIP_SYMBOLS['error']} SÁT THỦ"
            status_style = f"bold {get_vip_color('red')}"
        elif predicted_room is not None and room_id == predicted_room:
            status_text = f"{VIP_SYMBOLS['brain']} DỰ ĐOÁN"
            status_style = f"bold {get_vip_color('green')}"
        elif players == 0:
            status_text = f"{VIP_SYMBOLS['shield']} TRỐNG"
            status_style = f"dim {get_vip_color('silver')}"
        elif players < 10:
            status_text = f"{VIP_SYMBOLS['star']} AN TOÀN"
            status_style = f"bold {get_vip_color('green')}"
        elif players > 25:
            status_text = f"{VIP_SYMBOLS['warning']} ĐÔNG"
            status_style = f"bold {get_vip_color('orange')}"
        else:
            status_text = f"{VIP_SYMBOLS['chart']} BÌNH THƯỜNG"
            status_style = f"bold {get_vip_color('blue')}"
        
        # Format số
        bet_fmt = f"{int(bet):,}" if bet else "0"
        
        rooms_table.add_row(
            Text(str(room_id), style=f"bold {get_vip_color('gold')}"),
            Text(room_name),
            Text(str(players), style="bold" if players > 0 else "dim"),
            Text(bet_fmt),
            Text(status_text, style=status_style)
        )
    
    return Panel(
        rooms_table,
        title=f"[bold {get_vip_color('blue')}]THÔNG TIN CÁC PHÒNG[/]",
        border_style=get_vip_color("blue"),
        padding=(0, 1)
    )

def create_main_display() -> Panel:
    """Hiển thị trạng thái chính VIP"""
    if ui_state == "ANALYZING":
        # Hiệu ứng phân tích VIP
        lines = []
        lines.append(f"{VIP_SYMBOLS['brain']} [bold {get_vip_color('purple')}]VIP AI ĐANG PHÂN TÍCH[/]")
        lines.append("")
        
        if analysis_blur:
            # Hiệu ứng phân tích nâng cao
            bar_len = 40
            t = int(time.time() * 8)
            analysis_bars = []
            for i in range(bar_len):
                wave = math.sin(t * 0.1 + i * 0.3) * 0.5 + 0.5
                if wave > 0.7:
                    char = "█"
                    color = get_vip_color("green")
                elif wave > 0.4:
                    char = "▓"
                    color = get_vip_color("blue")
                elif wave > 0.2:
                    char = "▒"
                    color = get_vip_color("purple")
                else:
                    char = "░"
                    color = get_vip_color("silver")
                analysis_bars.append(f"[{color}]{char}[/{color}]")
            
            lines.append("".join(analysis_bars))
            lines.append("")
            lines.append(f"[{get_vip_color('silver')}]AI VIP đang tính toán xác suất tối ưu... {get_spinner()}[/]")
        
        if count_down is not None:
            try:
                cd = int(count_down)
                if cd > 30:
                    lines.append(f"{VIP_SYMBOLS['clock']} Thời gian còn: [bold {get_vip_color('blue')}]{cd}s[/]")
                elif cd > 10:
                    lines.append(f"{VIP_SYMBOLS['clock']} Thời gian còn: [bold {get_vip_color('orange')}]{cd}s[/]")
                else:
                    lines.append(f"{VIP_SYMBOLS['clock']} [bold {get_vip_color('red')}]CÒN {cd}s - CHUẨN BỊ ĐẶT CƯỢC![/]")
            except Exception:
                pass
        
        if last_killed_room:
            lines.append("")
            lines.append(f"{VIP_SYMBOLS['warning']} Sát thủ ván trước: [{get_vip_color('red')}]{ROOM_NAMES.get(last_killed_room)}[/]")
        
        content = "\n".join(lines)
        border_color = get_vip_color("purple")
        
        return Panel(
            Align.center(Text.from_markup(content), vertical="middle"),
            title=f"[bold {get_vip_color('purple')}]PHÂN TÍCH THỜI GIAN THỰC VIP[/]",
            border_style=border_color,
            padding=(2, 3),
            box=box.DOUBLE
        )
    
    elif ui_state == "PREDICTED":
        # Hiển thị dự đoán VIP
        predicted_name = ROOM_NAMES.get(predicted_room, f"Phòng {predicted_room}") if predicted_room else "Đang tính..."
        bet_amount = f"{current_bet:,.4f}" if current_bet else "-"
        algo_name = SELECTION_MODES.get(settings.get('algo', 'VIP_NEURAL'))
        
        lines = []
        lines.append(f"{VIP_SYMBOLS['brain']} [bold {get_vip_color('gold')}]KẾT QUẢ PHÂN TÍCH VIP[/]")
        lines.append("")
        lines.append(f"[bold {get_vip_color('green')}]🎯 PHÒNG AN TOÀN NHẤT: {predicted_name}[/]")
        lines.append("")
        lines.append(f"{VIP_SYMBOLS['money']} Số cược: [bold {get_vip_color('gold')}]{bet_amount} BUILD[/]")
        lines.append(f"{VIP_SYMBOLS['chart']} Thuật toán: [bold {get_vip_color('purple')}]{algo_name}[/]")
        lines.append("")
        
        if count_down is not None:
            try:
                cd = int(count_down)
                lines.append(f"{VIP_SYMBOLS['clock']} Còn lại: [bold {get_vip_color('blue')}]{cd}s[/]")
            except Exception:
                pass
        
        content = "\n".join(lines)
        
        return Panel(
            Align.center(Text.from_markup(content), vertical="middle"),
            title=f"[bold {get_vip_color('green')}]DỰ ĐOÁN CHÍNH XÁC VIP[/]",
            border_style=get_vip_color("green"),
            padding=(2, 3),
            box=box.ROUNDED
        )
    
    elif ui_state == "RESULT":
        # Hiển thị kết quả VIP
        killed_name = ROOM_NAMES.get(killed_room, "-") if killed_room else "-"
        predicted_name = ROOM_NAMES.get(predicted_room, "-") if predicted_room else "-"
        
        # Kiểm tra kết quả
        result_text = ""
        result_style = ""
        result_icon = ""
        
        if killed_room is not None and predicted_room is not None:
            if killed_room != predicted_room:
                result_text = f"{VIP_SYMBOLS['trophy']} [bold {get_vip_color('green')}]VIP THẮNG LỚN![/]"
                result_style = "green"
                result_icon = VIP_SYMBOLS['trophy']
            else:
                result_text = f"{VIP_SYMBOLS['fire']} [bold {get_vip_color('red')}]VIP THUA[/]"
                result_style = "red"
                result_icon = VIP_SYMBOLS['fire']
        
        lines = []
        lines.append(f"{VIP_SYMBOLS['chart']} [bold {get_vip_color('gold')}]KẾT QUẢ VÁN ĐẤU VIP[/]")
        lines.append("")
        lines.append(result_text)
        lines.append("")
        lines.append(f"{VIP_SYMBOLS['error']} Sát thủ vào: [bold]{killed_name}[/]")
        lines.append(f"{VIP_SYMBOLS['brain']} Dự đoán VIP: [bold]{predicted_name}[/]")
        lines.append("")
        lines.append(f"{VIP_SYMBOLS['money']} Lãi/Lỗ tích lũy: [bold {get_vip_color('gold')}]{cumulative_profit:+,.4f} BUILD[/]")
        lines.append(f"{VIP_SYMBOLS['chart']} Tổng số ván: [bold]{round_index}[/]")
        
        content = "\n".join(lines)
        
        return Panel(
            Align.center(Text.from_markup(content), vertical="middle"),
            title=f"[bold {get_vip_color('blue')}]BÁO CÁO KẾT QUẢ VIP[/]",
            border_style=result_style if result_style else get_vip_color("blue"),
            padding=(2, 3),
            box=box.HEAVY
        )
    
    else:
        # Trạng thái chờ VIP
        lines = []
        lines.append(f"{VIP_SYMBOLS['crown']} [bold {get_vip_color('gold')}]ĐANG CHỜ VÁN MỚI VIP[/]")
        lines.append("")
        lines.append(f"[{get_vip_color('silver')}]Kết nối đến game server...[/]")
        lines.append("")
        lines.append(f"{get_spinner()} [{get_vip_color('silver')}]Khởi tạo hệ thống AI VIP...[/]")
        
        content = "\n".join(lines)
        
        return Panel(
            Align.center(Text.from_markup(content), vertical="middle"),
            title=f"[bold {get_vip_color('silver')}]TRẠNG THÁI HỆ THỐNG VIP[/]",
            border_style=get_vip_color("silver"),
            padding=(2, 3),
            box=box.ROUNDED
        )

def create_bet_history() -> Panel:
    """Hiển thị lịch sử cược VIP"""
    history_table = Table(
        show_header=True,
        header_style=f"bold {get_vip_color('orange')}",
        box=box.SIMPLE,
        expand=True
    )
    
    history_table.add_column("THỜI GIAN", width=8)
    history_table.add_column("PHÒNG", width=6, justify="center")
    history_table.add_column("CƯỢC", width=12, justify="right")
    history_table.add_column("KẾT QUẢ", width=10)
    history_table.add_column("THUẬT TOÁN", width=14)
    
    # Lấy 5 ván gần nhất
    last_bets = list(bet_history)[-5:]
    for bet in reversed(last_bets):
        time_str = bet.get('time', '-')
        room = str(bet.get('room', '-'))
        amount = f"{float(bet.get('amount', 0)):,.4f}"
        result = str(bet.get('result', 'Đang chờ'))
        algo = str(bet.get('algo', '-'))
        
        # Màu sắc kết quả
        result_style = ""
        result_icon = ""
        if 'Thắng' in result or 'Win' in result:
            result_style = f"bold {get_vip_color('green')}"
            result_icon = VIP_SYMBOLS['trophy']
        elif 'Thua' in result or 'Lose' in result:
            result_style = f"bold {get_vip_color('red')}"
            result_icon = VIP_SYMBOLS['fire']
        else:
            result_style = f"dim {get_vip_color('yellow')}"
            result_icon = VIP_SYMBOLS['clock']
        
        history_table.add_row(
            Text(time_str, style=f"dim {get_vip_color('silver')}"),
            Text(room, style=f"bold {get_vip_color('blue')}"),
            Text(amount),
            Text(f"{result_icon} {result}", style=result_style),
            Text(algo, style=f"bold {get_vip_color('purple')}")
        )
    
    return Panel(
        history_table,
        title=f"[bold {get_vip_color('orange')}]LỊCH SỬ CƯỢC VIP[/]",
        border_style=get_vip_color("orange"),
        padding=(0, 1)
    )

# -------------------- VIP SETTINGS & CONFIG --------------------

def show_vip_welcome():
    """Hiển thị màn hình chào VIP"""
    os.system("cls" if os.name == "nt" else "clear")
    
    # Hiển thị banner VIP
    print_vip_banner()
    
    # Hiệu ứng loading VIP
    with console.status(f"[bold {get_vip_color('gold')}]Đang khởi động hệ thống VIP...[/]", spinner="dots") as status:
        time.sleep(1)
        status.update(f"[bold {get_vip_color('purple')}]Đang tải module AI VIP...[/]")
        time.sleep(1)
        status.update(f"[bold {get_vip_color('blue')}]Đang kết nối neural network VIP...[/]")
        time.sleep(1)
        status.update(f"[bold {get_vip_color('green')}]Khởi tạo thuật toán lượng tử VIP...[/]")
        time.sleep(1)

def prompt_vip_settings():
    """Cấu hình hệ thống VIP"""
    global base_bet, multiplier, run_mode, bet_rounds_before_skip
    global current_bet, pause_after_losses, profit_target, stop_when_profit_reached
    global stop_loss_target, stop_when_loss_reached, settings
    
    console.print(f"\n[{get_vip_color('gold')}]══════════════════════════════════════════════════════════════[/]")
    console.print(f"[bold {get_vip_color('gold')}]                  CẤU HÌNH HỆ THỐNG VIP                    [/]")
    console.print(f"[{get_vip_color('gold')}]══════════════════════════════════════════════════════════════[/]\n")
    
    # Số BUILD đặt mỗi ván
    base = safe_input(f"[{get_vip_color('blue')}]💰 Số BUILD đặt mỗi ván (mặc định: 1): [/]", default="1")
    try:
        base_bet = float(base)
    except Exception:
        base_bet = 1.0
    
    # Số nhân sau khi thua
    m = safe_input(f"[{get_vip_color('blue')}]📈 Nhân cược sau khi thua (mặc định: 2): [/]", default="2")
    try:
        multiplier = float(m)
    except Exception:
        multiplier = 2.0
    
    current_bet = base_bet
    
    # Chọn thuật toán VIP
    console.print(f"\n[{get_vip_color('purple')}]🤖 CHỌN THUẬT TOÁN VIP:[/]")
    console.print(f"[{get_vip_color('gold')}]1) VIP_NEURAL - Neural AI (Độ chính xác cao nhất)[/]")
    console.print(f"[{get_vip_color('gold')}]2) VIP_QUANTUM - Quantum AI (Tối ưu rủi ro)[/]")
    console.print(f"[{get_vip_color('gold')}]3) VIP_DEEP - Deep Learning AI (Thích nghi nhanh)[/]")
    console.print(f"[{get_vip_color('gold')}]4) VIP_FUSION - Fusion AI (Tổng hợp đa thuật toán)[/]")
    
    alg = safe_input(f"[{get_vip_color('blue')}]Chọn thuật toán VIP (1-4, mặc định: 1): [/]", default="1")
    algo_map = {"1": "VIP_NEURAL", "2": "VIP_QUANTUM", "3": "VIP_DEEP", "4": "VIP_FUSION"}
    settings["algo"] = algo_map.get(alg.strip(), "VIP_NEURAL")
    
    # Chống soi VIP
    s = safe_input(f"[{get_vip_color('blue')}]🛡️ Chống soi: sau bao nhiêu ván thì nghỉ 1 ván (0 = tắt): [/]", default="0")
    try:
        bet_rounds_before_skip = int(s)
    except Exception:
        bet_rounds_before_skip = 0
    
    # Nghỉ sau khi thua
    pl = safe_input(f"[{get_vip_color('blue')}]⏸️ Nếu thua, nghỉ bao nhiêu tay trước khi cược lại (0 = tắt): [/]", default="0")
    try:
        pause_after_losses = int(pl)
    except Exception:
        pause_after_losses = 0
    
    # Take profit VIP
    pt = safe_input(f"[{get_vip_color('blue')}]🎯 Lãi bao nhiêu BUILD thì chốt (Enter để bỏ qua): [/]", default="")
    if pt and pt.strip():
        try:
            profit_target = float(pt)
            stop_when_profit_reached = True
        except Exception:
            profit_target = None
            stop_when_profit_reached = False
    
    # Stop loss VIP
    sl = safe_input(f"[{get_vip_color('blue')}]⚠️ Lỗ bao nhiêu BUILD thì dừng (Enter để bỏ qua): [/]", default="")
    if sl and sl.strip():
        try:
            stop_loss_target = float(sl)
            stop_when_loss_reached = True
        except Exception:
            stop_loss_target = None
            stop_when_loss_reached = False
    
    # Xác nhận VIP
    console.print(f"\n[{get_vip_color('green')}]══════════════════════════════════════════════════════════════[/]")
    console.print(f"[bold {get_vip_color('green')}]✅ CẤU HÌNH VIP HOÀN TẤT[/]")
    console.print(f"[{get_vip_color('green')}]══════════════════════════════════════════════════════════════[/]\n")
    
    run_mode = "AUTO"  # Mặc định chạy tự động

def parse_vip_login():
    """Đăng nhập hệ thống VIP"""
    global USER_ID, SECRET_KEY
    
    console.print(f"[{get_vip_color('gold')}]══════════════════════════════════════════════════════════════[/]")
    console.print(f"[bold {get_vip_color('gold')}]                  ĐĂNG NHẬP HỆ THỐNG VIP                    [/]")
    console.print(f"[{get_vip_color('gold')}]══════════════════════════════════════════════════════════════[/]\n")
    
    link = safe_input(f"[{get_vip_color('blue')}]🔗 Dán link trò chơi từ xworld.info: [/]", default=None)
    
    if not link:
        console.print(f"[{get_vip_color('red')}]❌ Không có link đăng nhập. Thoát chương trình.[/]")
        sys.exit(1)
    
    try:
        parsed = urlparse(link)
        params = parse_qs(parsed.query)
        
        if 'userId' in params:
            USER_ID = int(params.get('userId')[0])
        
        SECRET_KEY = params.get('secretKey', [None])[0]
        
        console.print(f"[{get_vip_color('green')}]✅ Đã đọc thông tin VIP: UserID = {USER_ID}[/]")
        
    except Exception as e:
        console.print(f"[{get_vip_color('red')}]❌ Link không hợp lệ: {e}[/]")
        console.print(f"[{get_vip_color('red')}]Thoát chương trình.[/]")
        sys.exit(1)

# -------------------- MAIN FUNCTION --------------------

def start_vip_threads():
    """Khởi chạy các thread phụ VIP"""
    threading.Thread(target=start_ws, daemon=True).start()
    threading.Thread(target=monitor_loop, daemon=True).start()

def escape_master_vip_pro_main():
    """Hàm chính Escape Master VIP Pro"""
    # Hiển thị màn hình chào VIP
    show_vip_welcome()
    
    # Đăng nhập VIP
    parse_vip_login()
    
    # Cấu hình VIP
    prompt_vip_settings()
    
    console.print(f"\n[{get_vip_color('gold')}]{VIP_SYMBOLS['rocket']} 🚀 Khởi động hệ thống VIP AI...[/]")
    
    # Khởi động balance poller
    poller = BalancePoller(USER_ID, SECRET_KEY, poll_seconds=max(1, int(BALANCE_POLL_INTERVAL)))
    poller.start()
    
    # Khởi động các thread khác
    start_vip_threads()
    
    # Main UI loop VIP
    try:
        with Live(refresh_per_second=10, console=console, screen=False) as live:
            while not stop_flag:
                # Tạo layout VIP
                layout_content = Group(
                    create_vip_header(),
                    Columns([create_streak_display(), create_bet_history()], equal=True),
                    create_main_display(),
                    create_rooms_display()
                )
                
                live.update(layout_content)
                time.sleep(0.1)
                
    except KeyboardInterrupt:
        console.print(f"\n[{get_vip_color('orange')}]{VIP_SYMBOLS['shield']} ⏹️ Dừng chương trình VIP theo yêu cầu...[/]")
        poller.stop()
    except Exception as e:
        console.print(f"[{get_vip_color('red')}]{VIP_SYMBOLS['error']} ❌ Lỗi VIP: {e}[/]")
        poller.stop()
    
    # Kết thúc VIP
    console.print(f"\n[{get_vip_color('gold')}]══════════════════════════════════════════════════════════════[/]")
    console.print(f"[bold {get_vip_color('gold')}]         CẢM ƠN ĐÃ SỬ DỤNG ESCAPE MASTER VIP PRO         [/]")
    console.print(f"[{get_vip_color('gold')}]══════════════════════════════════════════════════════════════[/]\n")

# ============================================
# HÀM MAIN TỔNG HỢP
# ============================================
def main():
    try:
        # Hiển thị banner
        banner()
        
        # Kiểm tra key activation
        print_section("KIỂM TRA BẢN QUYỀN", Colors.YELLOW)
        loading_animation("Đang kiểm tra bản quyền...", 2)
        
        if key_activation_main():
            print_status("Bản quyền hợp lệ! Đang chuyển đến Escape Master VIP Pro...", "success")
            time.sleep(2)
            
            # Chuyển sang Escape Master VIP Pro
            escape_master_vip_pro_main()
        else:
            print_status("Không thể kích hoạt tool. Vui lòng thử lại!", "error")
            input(f"\n  {Colors.WHITE}[{Colors.RED}!{Colors.WHITE}] {Colors.YELLOW}Nhấn Enter để thoát...")
            sys.exit()
            
    except KeyboardInterrupt:
        print_status("Cảm ơn bạn đã sử dụng Tool! Hẹn gặp lại.", "info")
        sys.exit()
    except Exception as e:
        print_status(f"Lỗi không mong muốn: {str(e)}", "error")
        input(f"\n  {Colors.WHITE}[{Colors.RED}!{Colors.WHITE}] {Colors.YELLOW}Nhấn Enter để thoát...")
        sys.exit()

if __name__ == '__main__':
    main()