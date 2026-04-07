Efficient Inverted Index Search Engine (In-Memory)
📌 Project OverviewThis project implements a high-performance In-Memory Search Engine using the Inverted Index data structure.
It is designed to process large text datasets and provide instantaneous multi-keyword search results by pre-indexing words and their corresponding record locations.
This implementation focuses on algorithmic efficiency, specifically during the intersection of multiple posting lists, which is the heart of modern information retrieval systems.
🚀 Key FeaturesInverted Indexing: Builds a map of words -> [record_ids] to transform a slow O(N) linear search into a high-speed O(1) hash-map lookup.
Optimized Intersection Algorithm: Implements a linear-time Two-Pointer Intersection algorithm with O(L1 + L2)complexity, avoiding the overhead of built-in set operations.
Memory Efficient: Stores raw data in a list of tuples and utilizes Python's dictionary for fast word-to-ID mapping.
Robust Text Processing: Handles large-scale text files with a custom UTF-8 decoding strategy and regex-based tokenization to handle noisy data.
CLI Interface: Features a real-time interactive query loop with snippet previews for quick data inspection.
🧠 Algorithmic Deep DiveThe core of this project is the intersect() method. 
Unlike naive approaches that might use O(N^2) comparisons or memory-intensive set conversions, this system uses:Sorted Posting Lists: Record IDs are appended in ascending order during index construction.
Two-Pointer Merge: Simultaneously traverses two sorted lists, skipping irrelevant IDs and only recording commonalities in a single pass.
💻 Tech StackLanguage: Python 3.xStandard Libraries: re (Regular Expressions), sys (Command-line arguments), typing (Static type hinting for code clarity).
