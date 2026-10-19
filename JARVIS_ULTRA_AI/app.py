import os
import threading
import webbrowser
from datetime import datetime

import requests
from dotenv import load_dotenv
import customtkinter as ctk

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat").strip() or "deepseek-chat"
API_URL = "https://api.deepseek.com/chat/completions"

SYSTEM_PROMPT = (
    "You are JARVIS, a helpful AI desktop assistant. Be clear and honest. "
    "Help with coding, research, and trading education. Never promise profits. "
    "This app does not place trades. Never ask for passwords or private API keys."
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class JarvisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JARVIS ULTRA AI")
        self.geometry("1000x720")
        self.minsize(760, 560)
        self.configure(fg_color="#07111f")
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.busy = False
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="#0d1d30", corner_radius=18)
        header.grid(row=0, column=0, padx=18, pady=(18, 10), sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="J.A.R.V.I.S. / ULTRA AI",
                     font=ctk.CTkFont(size=26, weight="bold"),
                     text_color="#66d9ff").grid(row=0, column=0, padx=20, pady=(15, 2), sticky="w")
        ctk.CTkLabel(header, text="DESKTOP AI • DEEPSEEK API • SAFE SHORTCUTS",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#9bb8d1").grid(row=1, column=0, padx=22, pady=(0, 14), sticky="w")
        links = ctk.CTkFrame(header, fg_color="transparent")
        links.grid(row=0, column=1, rowspan=2, padx=12, pady=12, sticky="e")
        ctk.CTkButton(links, text="YouTube", width=95,
                      command=lambda: webbrowser.open("https://www.youtube.com")).grid(row=0, column=0, padx=3)
        ctk.CTkButton(links, text="TradingView", width=105,
                      command=lambda: webbrowser.open("https://www.tradingview.com")).grid(row=0, column=1, padx=3)

        self.chat = ctk.CTkTextbox(self, corner_radius=16, wrap="word",
                                   fg_color="#0a1727", text_color="#e5f2ff",
                                   font=ctk.CTkFont(size=14))
        self.chat.grid(row=1, column=0, padx=18, pady=8, sticky="nsew")
        self.chat.configure(state="disabled")
        self.add_message("JARVIS", "Systems online. Ask a question below.\n\n"
                         "I can help with questions, coding, research, and trading education. "
                         "This starter does not place trades or control arbitrary computer functions.")

        bottom = ctk.CTkFrame(self, fg_color="#0d1d30", corner_radius=16)
        bottom.grid(row=2, column=0, padx=18, pady=(8, 10), sticky="ew")
        bottom.grid_columnconfigure(0, weight=1)
        self.entry = ctk.CTkTextbox(bottom, height=76, corner_radius=12,
                                    fg_color="#101f32", text_color="#ffffff",
                                    font=ctk.CTkFont(size=14))
        self.entry.grid(row=0, column=0, padx=(12, 8), pady=12, sticky="ew")
        self.entry.bind("<Control-Return>", self.send_shortcut)
        actions = ctk.CTkFrame(bottom, fg_color="transparent")
        actions.grid(row=0, column=1, padx=(0, 12), pady=12)
        self.send_button = ctk.CTkButton(actions, text="SEND  ➤", width=120,
                                         command=self.send_message)
        self.send_button.grid(row=0, column=0, pady=(0, 6))
        ctk.CTkButton(actions, text="Clear chat", width=120, fg_color="#263b52",
                      command=self.clear_chat).grid(row=1, column=0)
        self.status = ctk.CTkLabel(self, text="Ready • Ctrl+Enter to send",
                                   text_color="#7f9db8", anchor="w")
        self.status.grid(row=3, column=0, padx=24, pady=(0, 10), sticky="ew")

    def add_message(self, speaker, text):
        self.chat.configure(state="normal")
        stamp = datetime.now().strftime("%H:%M")
        self.chat.insert("end", f"[{stamp}] {speaker}\n{text.strip()}\n\n")
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def send_shortcut(self, _event):
        self.send_message()
        return "break"

    def send_message(self):
        if self.busy:
            return
        prompt = self.entry.get("1.0", "end").strip()
        if not prompt:
            return
        self.entry.delete("1.0", "end")
        self.add_message("YOU", prompt)
        shortcuts = {
            "open youtube": "https://www.youtube.com",
            "open tradingview": "https://www.tradingview.com",
            "open google": "https://www.google.com",
        }
        if prompt.lower().strip() in shortcuts:
            webbrowser.open(shortcuts[prompt.lower().strip()])
            self.add_message("JARVIS", "Opened that website in your browser.")
            return
        if not API_KEY or API_KEY == "paste_your_key_here":
            self.add_message("JARVIS", "DeepSeek API key is not configured. Edit the local .env file "
                             "and set DEEPSEEK_API_KEY=your_key, then restart. Never share the key.")
            return
        self.history.append({"role": "user", "content": prompt})
        self.busy = True
        self.send_button.configure(state="disabled", text="THINKING…")
        self.status.configure(text="Connecting to DeepSeek…")
        threading.Thread(target=self.call_api, daemon=True).start()

    def call_api(self):
        try:
            response = requests.post(
                API_URL,
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                json={"model": MODEL, "messages": self.history, "stream": False},
                timeout=60,
            )
            if response.status_code >= 400:
                try:
                    detail = response.json().get("error", {}).get("message", response.text)
                except ValueError:
                    detail = response.text
                answer = f"DeepSeek API error ({response.status_code}): {detail}"
            else:
                answer = response.json()["choices"][0]["message"]["content"].strip()
                self.history.append({"role": "assistant", "content": answer})
        except requests.RequestException as exc:
            answer = f"Network request failed: {exc}"
        except (KeyError, TypeError, ValueError) as exc:
            answer = f"Could not read the API response: {exc}"
        self.after(0, self.finish_response, answer)

    def finish_response(self, answer):
        self.add_message("JARVIS", answer)
        self.busy = False
        self.send_button.configure(state="normal", text="SEND  ➤")
        self.status.configure(text="Ready • Ctrl+Enter to send")

    def clear_chat(self):
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.chat.configure(state="normal")
        self.chat.delete("1.0", "end")
        self.chat.configure(state="disabled")
        self.add_message("JARVIS", "Chat cleared. Ready for your next question.")


if __name__ == "__main__":
    JarvisApp().mainloop()
