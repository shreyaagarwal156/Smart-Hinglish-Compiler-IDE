# 🚀 Smart Hinglish Compiler IDE

![Status](https://img.shields.io/badge/Status-Completed-success)
![Version](https://img.shields.io/badge/Version-1.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)
![Flask](https://img.shields.io/badge/Backend-Flask-lightgrey)

**Smart Hinglish Compiler IDE** is a web-based educational programming environment designed to lower the barrier to entry for coding. It allows users to write logic in "Hinglish" (a blend of Hindi and English), bridging the gap between basic pseudocode and production-level syntax. 

Developed as a major project at **Graphic Era University**, this IDE doesn't just parse custom syntax—it optimizes the logic and translates it into four major industry languages simultaneously while executing it natively in the browser.

---

## ✨ Key Features

* **🧠 Custom Compiler Engine:** Built from scratch using Lexical Analysis and Parsing (via Context-Free Grammar) to construct an Abstract Syntax Tree (AST).
* **⚡ AST Optimization Pass:** Features mathematical Constant Folding (e.g., evaluating `10 * 5 * 2` at compile-time) and Dead Code Elimination for faster execution.
* **🌍 Multi-Target Code Generation:** Simultaneously translates Hinglish AST into **Python, C++, Java, and C**.
* **💻 Real-Time Execution Engine:** Runs the generated Python code securely in the background with standard input (`stdin`) support via the `poocho()` keyword. Includes a 5-second timeout safeguard to prevent infinite loops.
* **🎨 Pro-Level UI/UX:** Features a dark-themed dashboard built with TailwindCSS, integrating the Microsoft Monaco Editor API for syntax highlighting, and a dynamic Blob API for downloading generated code files.
* **📚 Interactive Hinglish Library:** A built-in modal dictionary mapping Hinglish keywords to standard programming logic.

---

## 🛠️ Tech Stack

* **Compiler Core:** Python, `sly` (Lex/Yacc framework for tokenization and parsing)
* **Backend Engine:** Flask (Python), `subprocess` (for secure execution)
* **Frontend UI:** HTML5, TailwindCSS, Vanilla JavaScript
* **Code Editor:** Microsoft Monaco Editor API

---

## 📖 The Hinglish Syntax Guide

Here is a quick look at the custom syntax supported by the compiler:

| Hinglish Keyword | Standard Meaning | Example Usage |
| :--- | :--- | :--- |
| `maan_lo` | Variable Declaration (`var`/`let`) | `maan_lo x = 10;` |
| `dikhao` | Print to Console | `dikhao("Hello World");` |
| `poocho` | Take User Input (`stdin`) | `maan_lo age = poocho();` |
| `agar` / `warna` | If / Else Condition | `agar (x > 5) { ... } warna { ... }` |
| `jab_tak` | While Loop | `jab_tak (i < 10) { ... }` |
| `kaam` | Function Definition | `kaam add() { ... }` |
| `bhej_do` | Return Statement | `bhej_do result;` |

*(Note: The compiler also fully supports Array creation, updating, and indexing using standard `[]` brackets.)*

---

## 🚀 Local Installation & Setup

Want to run this God-Level IDE on your local machine? Follow these steps:

### Prerequisites
* Python 3.8 or higher installed on your system.
* Git installed.

### Steps
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/shreyaagarwal156/Smart-Hinglish-Compiler-IDE.git](https://github.com/shreyaagarwal156/Smart-Hinglish-Compiler-IDE.git)
   cd Smart-Hinglish-Compiler-IDE-Phase
Create a Virtual Environment (Optional but recommended):

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install the dependencies:

Bash
pip install Flask sly
Run the Flask Backend:

Bash
python app.py
Open the IDE:
Open your browser and navigate to http://localhost:5000 or http://127.0.0.1:5000.
