# Data Structure Visualizer

A desktop application for visualizing data structures and algorithms, built as an academic project for ROSP (Research Oriented Software Project).

## Project Objective

The goal of this project is to create an interactive educational tool that helps students visually understand data structures and algorithms through animations and interactive operations. The application will eventually support:

- **Data Structures**: Array, Stack, Queue, Linked List, Binary Search Tree, Heap, Graph
- **Algorithms**: Sorting (Bubble, Selection, Insertion, Merge, Quick), Searching (Linear, Binary), Graph Algorithms (BFS, DFS, Dijkstra, etc.)

## Technology Stack

- **Language**: Python 3
- **GUI Framework**: PyQt6
- **Architecture**: Object-oriented, clean modular design
- **Platform**: Desktop (Windows, macOS, Linux)

## Current Implementation Status

**Phase 1 - Foundation (COMPLETED):**
- [x] Project structure and modular architecture
- [x] Main application window with responsive layout
- [x] Left sidebar with placeholder buttons for all planned data structures
- [x] Central visualization panel with placeholder content
- [x] Bottom control panel with operation selector, value input, Execute/Reset buttons
- [x] Status bar for operation information
- [x] Clean, modern UI with consistent styling

**Phase 2 - Array Visualization (COMPLETED):**
- [x] Array data structure implementation (`data_structures/array.py`)
- [x] Array visualization with indexed cells (`visualization/array_visualizer.py`)
- [x] Array operations: Append, Insert, Delete, Search, Update, Get, Traverse, Clear
- [x] Input handling with index,value format support
- [x] Visual highlighting for operations
- [x] Operation feedback with time/space complexity
- [x] Error handling for invalid inputs
- [x] Unit tests (`tests/test_array.py`)

**Phase 3 - Stack Visualization (COMPLETED):**
- [x] Stack data structure implementation (`data_structures/stack.py`)
- [x] Stack visualization with vertical layout (`visualization/stack_visualizer.py`)
- [x] Stack operations: Push, Pop, Peek, Is Empty, Size, Traverse, Clear
- [x] TOP/BOTTOM indicators with arrow
- [x] Visual highlighting for operations
- [x] Operation feedback with time/space complexity
- [x] Error handling for invalid inputs
- [x] Unit tests (`tests/test_stack.py`)

**Upcoming Phases:**
- [ ] Phase 4: Queue visualization
- [ ] Phase 5: Linked List visualization
- [ ] Phase 6: Binary Search Tree visualization
- [ ] Phase 7: Heap visualization
- [ ] Phase 8: Graph visualization
- [ ] Phase 9: Sorting algorithms
- [ ] Phase 10: Searching algorithms
- [ ] Phase 11: Graph algorithms

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

From the project root directory:

```bash
python main.py
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run Array tests specifically
python -m pytest tests/test_array.py -v

# Run Stack tests specifically
python -m pytest tests/test_stack.py -v

# Run with unittest
python -m unittest tests.test_array tests.test_stack -v
```

## Array Visualization

The Array module is the first fully functional data structure in the application.

### Supported Operations

| Operation | Description | Input Format |
|-----------|-------------|--------------|
| **Append** | Add element to end | `50` (value only) |
| **Insert** | Insert at specific index | `2,50` (index,value) |
| **Delete** | Remove element at index | `2` (index only) |
| **Search** | Find value in array | `50` (value only) |
| **Update** | Change value at index | `2,50` (index,value) |
| **Get** | Retrieve value at index | `2` (index only) |
| **Traverse** | Display all elements | (no input required) |
| **Clear** | Remove all elements | (no input required) |

### Input Format Examples

- **Value only** (Append, Search): `50`, `100`, `-5`
- **Index only** (Delete, Get): `0`, `2`, `5`
- **Index,value** (Insert, Update): `2,50`, `0,100`, `5,-10`

The Value input field shows contextual placeholder text for each operation.

### Visual Features

- Array displayed as indexed cells with clear index labels
- Highlighted elements for Search and Get operations
- Green highlight for newly inserted elements
- Red highlight for deleted elements (shows deleted value)
- Blue highlight for searched/found elements
- Operation feedback displayed below visualization
- Status bar shows current operation with time/space complexity

### Time & Space Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Append | O(1) amortized | O(1) auxiliary |
| Insert | O(n) | O(1) auxiliary |
| Delete | O(n) | O(1) auxiliary |
| Search | O(n) | O(1) auxiliary |
| Update | O(1) | O(1) |
| Get | O(1) | O(1) |
| Traverse | O(n) | O(1) auxiliary |
| Clear | O(n) | O(1) auxiliary |

## Stack Visualization

The Stack module is the second fully functional data structure in the application.

### Supported Operations

| Operation | Description | Input Format |
|-----------|-------------|--------------|
| **Push** | Add element to top | `42` (value only) |
| **Pop** | Remove and return top | (no input required) |
| **Peek** | View top without removing | (no input required) |
| **Is Empty** | Check if stack is empty | (no input required) |
| **Size** | Return element count | (no input required) |
| **Traverse** | Display all elements | (no input required) |
| **Clear** | Remove all elements | (no input required) |

### Visual Features

- Stack displayed vertically with TOP indicator and arrow
- Elements shown as horizontal cells
- TOP → BOTTOM traversal order
- Blue highlight for Peek (top element)
- Green highlight for newly pushed elements
- Operation feedback displayed below visualization

### Time & Space Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Push | O(1) amortized | O(1) auxiliary |
| Pop | O(1) | O(1) |
| Peek | O(1) | O(1) |
| Is Empty | O(1) | O(1) |
| Size | O(1) | O(1) |
| Traverse | O(n) | O(1) auxiliary |
| Clear | O(n) | O(1) auxiliary |

## Project Structure

```
DataStructureVisualizer/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── app/                   # Main application package
│   ├── __init__.py
│   ├── main_window.py     # Main window implementation
│   ├── ui/                # UI components
│   │   ├── __init__.py
│   │   ├── sidebar.py     # Left sidebar with data structure selection
│   │   └── visualization_panel.py  # Central visualization area
│   └── core/              # Core utilities
│       ├── __init__.py
│       └── constants.py   # Application constants and styles
├── data_structures/       # Data structure implementations
│   ├── __init__.py
│   ├── array.py           # Array implementation
│   └── stack.py           # Stack implementation
├── algorithms/            # Algorithm implementations (future)
│   └── __init__.py
├── visualization/         # Visualization utilities
│   ├── __init__.py
│   ├── array_visualizer.py  # Array visualization widget
│   └── stack_visualizer.py  # Stack visualization widget
└── tests/                 # Unit tests
    ├── __init__.py
    ├── test_array.py      # Array unit tests
    └── test_stack.py      # Stack unit tests
```

## Architecture Overview

- **main.py**: Only responsible for starting the application
- **app/main_window.py**: Main window composition, connects all components
- **app/ui/sidebar.py**: Sidebar UI with data structure selection buttons
- **app/ui/visualization_panel.py**: Central area for visualizations (placeholder)
- **app/core/constants.py**: All reusable constants, styles, and configuration
- **data_structures/array.py**: Pure Python Array implementation (no GUI dependencies)
- **data_structures/stack.py**: Pure Python Stack implementation (no GUI dependencies)
- **visualization/array_visualizer.py**: PyQt6 widget for Array visualization
- **visualization/stack_visualizer.py**: PyQt6 widget for Stack visualization
- **tests/test_array.py**: Unit tests for Array data structure
- **tests/test_stack.py**: Unit tests for Stack data structure

The codebase follows separation of concerns - UI code is separate from data structure logic, making it easy to extend.

## License

Academic project - ROSP