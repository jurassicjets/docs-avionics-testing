import os
import time

from ui.colors import *


CLEAR_CMD = "cls" if os.name == "nt" else "clear"


def get_status_color(status):

    if status == "RUNNING":
        return GREEN

    if status == "RECONNECTING":
        return YELLOW

    return RED


class StatusConsole:

    def __init__(self):

        self.start_time = time.time()

    def uptime(self):

        seconds = int(time.time() - self.start_time)

        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60

        return f"{h:02}:{m:02}:{s:02}"

    def draw(
            self,
            status,
            output_device,
            callback_rate,
            state,
            restart_count,
            last_error,
            warnings):
            
        os.system(CLEAR_CMD)

        color = get_status_color(status)

        print("=" * 60)
        print("JJ AUDIO BOSS")
        print("=" * 60)
        print()

        print(
            f"Status        : "
            f"{color}{status}{RESET}"
        )

        print(f"Uptime        : {self.uptime()}")
        print(f"Restart Count : {restart_count}")
        print(f"  Device      : {output_device}")
        print(f"  Callbacks/s : {callback_rate:.1f}")
        
        if last_error:
            print(f"  Last Error  : {RED}{last_error}{RESET}")
        
        print()

        if state.connected:
            print(f"{GREEN}X-PLANE CONNECTED{RESET}")
        else:
            print(f"{RED}X-PLANE CONNECTION LOST{RESET}")

        if warnings:
        
            print()
        
            for warning in warnings.values():
        
                print(
                    f"{YELLOW}"
                    f"WARNING: {warning}"
                    f"{RESET}"
                )
        
        print()

        print("RADIOS")

        print(f"  COM1        : {state.com1_freq}")
        print(f"  COM2        : {state.com2_freq}")
        print(f"  COM3        : {state.com3_freq}")

        print(f"  NAV1        : {state.nav1_freq}")
        print(f"  NAV2        : {state.nav2_freq}")

        print(f"  ADF1        : {state.adf1_freq}")
        print(f"  ADF2        : {state.adf2_freq}")

        print(f"  DME1        : {state.dme1_distance}")
        print(f"  DME2        : {state.dme2_distance}")

        print(f"  MKR         : {state.marker_state}")

        print()
        print("=" * 60)