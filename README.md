# 🧠 Code Complexity Analyzer

A **static code analysis tool** that estimates **Time and Space Complexity** of algorithms written in **Python, C++, and Java**, with **clear reasoning** behind each result.

Built to bridge the gap between **DSA theory** and **real language-level behavior**.

---

## ✨ Features

* 🔍 **Time Complexity Analysis**

  * Loop detection (single, nested, logarithmic)
  * Recursion detection
  * Divide-and-conquer pattern recognition

* 💾 **Space Complexity Analysis**

  * Distinguishes **auxiliary space vs recursion stack**
  * Handles **language-specific memory behavior**
  * Ignores **output-only containers** (algorithmic convention)

* 🌐 **Multi-language Support**

  * Python (AST-based analysis)
  * C++ (regex + structural heuristics)
  * Java (regex + structural heuristics)

* 🧩 **Function-level Analysis (Python)**

  * Analyze only the intended algorithm
  * Prevents setup/benchmark code from polluting results

* 🖥️ **Interactive UI (Streamlit)**

  * Paste code
  * Select language
  * Get complexity + reasoning instantly

---

## 🏗️ Project Structure

```
CodeComplexityAnalyzer/
│
├── analyzer/
│   ├── parser.py          # Python AST analyzer
│   ├── cpp_parser.py      # C++ analyzer
│   ├── java_parser.py     # Java analyzer
│   ├── rules.py           # Time complexity rules
│   ├── space_rules.py     # Space complexity rules
│   └── reasoning.py       # Explanation generator
│
├── app.py                 # Streamlit UI
├── main.py                # CLI runner (optional)
├── examples/              # Sample inputs
└── README.md
```

---

## 🚀 How to Run

### 1️⃣ Install dependencies

```bash
pip install streamlit
```

### 2️⃣ Run the UI

```bash
streamlit run app.py
```

Open the browser at:

```
http://localhost:8501
```

---

## 🧪 Example Analyses

### ✅ Morris Inorder Traversal (Python / C++)

```text
Time Complexity: O(n)
Space Complexity: O(1)
```

**Why?**

* Single traversal
* No recursion
* Pointer rewiring only
* Output space ignored by convention

---

### ✅ Longest Palindromic Substring (Expand Around Center)

```text
Time Complexity: O(n²)
Space Complexity: O(1)
```

**Why?**

* Nested expansion for each index
* No auxiliary data structures

---

### ✅ Merge Sort (Python)

```text
Time Complexity: O(n log n)
Space Complexity: O(n)
```

**Why?**

* Divide-and-conquer recursion
* Python list slicing (`arr[:mid]`) allocates new lists
* Auxiliary space dominates recursion stack

> ⚠️ Note: In-place merge sort implementations may have different space complexity.

---

## 🧠 Design Decisions (Important)

### 🔹 Function-Level Analysis (Python)

Python code is analyzed **per function**, not per file.
This avoids counting:

* input construction
* benchmarking
* helper utilities

You must specify the function name in the UI.

---

### 🔹 Output Space Is Ignored

By algorithmic convention:

* Returned containers (e.g. result lists)
  **do not count as auxiliary space**

This keeps results aligned with standard DSA analysis.

---

### 🔹 Auxiliary Space Dominates Recursion Stack

If both exist:

```text
Auxiliary space O(n) > recursion stack O(log n)
```

Final space complexity = **O(n)**

---

## ⚠️ Known Limitations

This is a **static analyzer**, not a runtime profiler.

* Uses **heuristics**, not full semantic analysis
* Cannot perfectly model:

  * amortized costs in all cases
  * compiler optimizations
  * aliasing and advanced memory reuse
* Python analysis is more complex due to:

  * implicit allocations (e.g. slicing)

Despite this, the analyzer is **accurate for most interview-level algorithms**.

---

## 🎯 Why This Project Matters

Most tools:

* either show **Big-O without explanation**
* or rely on **manual annotation**

This project:

* **infers complexity**
* **explains reasoning**
* **respects language semantics**

It demonstrates:

* Algorithmic understanding
* Static analysis thinking
* Practical software design

---

## 📌 Future Improvements

* Export analysis report (PDF / JSON)
* Syntax highlighting in UI
* Detection of common STL / Java utility patterns
* Call-graph visualization

---

## 👤 Author

Built with persistence, debugging pain, and algorithmic curiosity 💪
Designed to be **honest, explainable, and interview-safe**.

---
