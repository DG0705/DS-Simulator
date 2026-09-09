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
- [x] Pop animation with QTimer transition
- [x] Operation feedback with time/space complexity
- [x] Error handling for invalid inputs
- [x] Unit tests (`tests/test_stack.py`)

**Phase 4 - Queue Visualization (COMPLETED):**
- [x] Queue data structure implementation (`data_structures/queue.py`)
- [x] Queue visualization with horizontal layout (`visualization/queue_visualizer.py`)
- [x] Queue operations: Enqueue, Dequeue, Front, Rear, Is Empty, Size, Traverse, Clear
- [x] FRONT/REAR indicators with direction arrows
- [x] FIFO direction visualization
- [x] Visual highlighting for operations
- [x] Dequeue animation with QTimer transition
- [x] Operation feedback with time/space complexity
- [x] Error handling for invalid inputs
- [x] Unit tests (`tests/test_queue.py`)

**Phase 5 - Linked List Visualization (COMPLETED):**
- [x] Singly Linked List implementation (`data_structures/linked_list.py`)
- [x] Node class with data and next pointer
- [x] Linked List visualization with horizontal nodes (`visualization/linked_list_visualizer.py`)
- [x] Linked List operations: Insert at Head/Tail/Index, Delete Head/Tail/Index, Search, Update, Get, Traverse, Size, Is Empty, Clear
- [x] HEAD/TAIL/NULL indicators with arrows
- [x] Node visual design: [DATA | NEXT →]
- [x] Visual highlighting for operations
- [x] Operation feedback with time/space complexity
- [x] Error handling for invalid inputs
- [x] Horizontal scrolling for long lists
- [x] Unit tests (`tests/test_linked_list.py`)

**Upcoming Phases:**
- [ ] Phase 9: Sorting algorithms
- [ ] Phase 10: Searching algorithms
- [ ] Phase 11: Graph algorithms (BFS, DFS, Dijkstra, etc.)

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

# Run Queue tests specifically
python -m pytest tests/test_queue.py -v

# Run Linked List tests specifically
python -m pytest tests/test_linked_list.py -v

# Run BST tests specifically
python -m pytest tests/test_bst.py -v

# Run with unittest
python -m unittest tests.test_array tests.test_stack tests.test_queue tests.test_linked_list tests.test_bst -v
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

## Queue Visualization

The Queue module is the third fully functional data structure in the application.

### Supported Operations

| Operation | Description | Input Format |
|-----------|-------------|--------------|
| **Enqueue** | Add element to rear | `50` (value only) |
| **Dequeue** | Remove and return front | (no input required) |
| **Front** | View front without removing | (no input required) |
| **Rear** | View rear without removing | (no input required) |
| **Is Empty** | Check if queue is empty | (no input required) |
| **Size** | Return element count | (no input required) |
| **Traverse** | Display all elements | (no input required) |
| **Clear** | Remove all elements | (no input required) |

### Visual Features

- Queue displayed horizontally with FRONT (left) and REAR (right) indicators
- FIFO direction arrows: DEQUEUE ← (left) and ENQUEUE → (right)
- BLUE highlight for Front element
- GREEN highlight for Rear element
- YELLOW highlight for newly enqueued elements
- RED highlight for dequeued element (animation)
- Top and bottom FRONT/REAR labels
- Operation feedback displayed below visualization

### Time & Space Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Enqueue | O(1) | O(1) auxiliary |
| Dequeue | O(1) | O(1) |
| Front | O(1) | O(1) |
| Rear | O(1) | O(1) |
| Is Empty | O(1) | O(1) |
| Size | O(1) | O(1) |
| Traverse | O(n) | O(1) auxiliary |
| Clear | O(n) | O(1) auxiliary |

## Linked List Visualization

The Linked List module is the fourth fully functional data structure in the application.

### Node Structure

Each node contains:
- **data**: The stored value
- **next**: Pointer to the next node (None for the last node)

### HEAD / TAIL / NULL

- **HEAD**: Points to the first node
- **TAIL**: Points to the last node
- **NULL**: The last node's next pointer

### Supported Operations

| Operation | Description | Input Format |
|-----------|-------------|--------------|
| **Insert at Head** | Add node at the beginning | `50` (value only) |
| **Insert at Tail** | Add node at the end | `50` (value only) |
| **Insert at Index** | Add node at specific index | `2,50` (index,value) |
| **Delete Head** | Remove the first node | (no input required) |
| **Delete Tail** | Remove the last node | (no input required) |
| **Delete at Index** | Remove node at index | `2` (index only) |
| **Search** | Find value in list | `50` (value only) |
| **Update** | Change value at index | `2,50` (index,value) |
| **Get** | Retrieve value at index | `2` (index only) |
| **Traverse** | Display all nodes | (no input required) |
| **Size** | Return node count | (no input required) |
| **Is Empty** | Check if list is empty | (no input required) |
| **Clear** | Remove all nodes | (no input required) |

### Visual Features

- Nodes displayed horizontally with [DATA | NEXT →] design
- Arrows between nodes represent next pointers
- HEAD indicator pointing to first node
- TAIL indicator pointing to last node
- NULL label at the end of the list
- Blue highlight for Search/Get operations
- Green highlight for newly inserted nodes
- Horizontal scrolling for long lists
- Operation feedback displayed below visualization

### Time & Space Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Insert at Head | O(1) | O(1) |
| Insert at Tail | O(1) | O(1) |
| Insert at Index | O(n) | O(1) |
| Delete Head | O(1) | O(1) |
| Delete Tail | O(n) | O(1) |
| Delete at Index | O(n) | O(1) |
| Search | O(n) | O(1) |
| Update | O(n) | O(1) |
| Get | O(n) | O(1) |
| Traverse | O(n) | O(1) auxiliary |
| Size | O(1) | O(1) |
| Is Empty | O(1) | O(1) |
| Clear | O(n) | O(1) auxiliary |

## Binary Search Tree Visualization

The Binary Search Tree module is the fifth fully functional data structure in the application.

### Properties

- **No duplicates**: Inserting a duplicate value raises BSTValueError
- **Height convention**: Empty tree = 0, single node = 1
- **Delete handles 3 cases**: Leaf, one child, two children (inorder successor)

### Supported Operations

| Operation | Description | Input Format |
|-----------|-------------|--------------|
| **Insert** | Add value to BST | `50` (value only) |
| **Delete** | Remove value from BST | `50` (value only) |
| **Search** | Find value in BST | `50` (value only) |
| **Inorder Traversal** | Visit nodes sorted (L→Root→R) | (no input required) |
| **Preorder Traversal** | Visit nodes root-first (Root→L→R) | (no input required) |
| **Postorder Traversal** | Visit nodes children-first (L→R→Root) | (no input required) |
| **Level Order Traversal** | Visit nodes level by level (BFS) | (no input required) |
| **Find Minimum** | Find minimum value | (no input required) |
| **Find Maximum** | Find maximum value | (no input required) |
| **Height** | Return tree height | (no input required) |
| **Size** | Return node count | (no input required) |
| **Is Empty** | Check if BST is empty | (no input required) |
| **Clear** | Remove all nodes | (no input required) |

### Visual Features

- Hierarchical tree layout with nodes drawn as circles
- Edges connecting parent to child nodes
- ROOT label above the root node
- Blue highlight for nodes in search path
- Green highlight for newly inserted nodes
- Traversal results displayed in feedback panel
- Horizontal and vertical scrolling for large trees
- Operation feedback displayed below visualization

### Time & Space Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Insert | O(log n) avg, O(n) worst | O(log n) stack |
| Delete | O(log n) avg, O(n) worst | O(log n) stack |
| Search | O(log n) avg, O(n) worst | O(log n) stack |
| Inorder | O(n) | O(h) stack |
| Preorder | O(n) | O(h) stack |
| Postorder | O(n) | O(h) stack |
| Level Order | O(n) | O(w) queue |
| Find Minimum | O(log n) avg, O(n) worst | O(1) |
| Find Maximum | O(log n) avg, O(n) worst | O(1) |
| Height | O(n) | O(h) stack |
| Size | O(1) | O(1) |
| Is Empty | O(1) | O(1) |
| Clear | O(1) | O(1) |

## Max Heap Visualization

The Heap module is the sixth fully functional data structure in the application.

### Properties

- **Max Heap**: Every parent node is greater than or equal to its children
- **Array representation**: Heap stored as a complete binary tree in an array
- **Zero-based indexing**: parent(i) = (i-1)//2, left(i) = 2*i+1, right(i) = 2*i+2

### Supported Operations

| Operation | Description | Input Format |
|-----------|-------------|--------------|
| **Insert** | Add value to heap | `50` (value only) |
| **Extract Max** | Remove and return maximum | (no input required) |
| **Peek** | View maximum without removing | (no input required) |
| **Build Heap** | Build heap from value list | `50,30,70,20` (comma-separated) |
| **Traverse** | Display heap array | (no input required) |
| **Size** | Return element count | (no input required) |
| **Is Empty** | Check if heap is empty | (no input required) |
| **Clear** | Remove all elements | (no input required) |

### Visual Features

- Hierarchical tree layout with nodes drawn as circles
- Edges connecting parent to child nodes
- ROOT label above the root node
- Heap array representation displayed below tree
- Heap property indicator message
- Green highlight for newly inserted nodes
- Blue highlight for peek operation
- Horizontal and vertical scrolling for large heaps
- Operation feedback displayed below visualization

### Build Heap

Uses bottom-up heap construction for O(n) complexity:
- Start from last non-leaf node
- Apply heapify_down to each node
- More efficient than inserting elements one by one

### Time & Space Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Insert | O(log n) | O(1) auxiliary |
| Extract Max | O(log n) | O(1) auxiliary |
| Peek | O(1) | O(1) |
| Build Heap | O(n) | O(n) |
| Traverse | O(n) | O(1) auxiliary |
| Size | O(1) | O(1) |
| Is Empty | O(1) | O(1) |
| Clear | O(1) | O(1) |

## Undirected Graph Visualization

The Graph module is the seventh functional data structure in the application.

### Properties

- **Undirected**: Edges have no direction; A—B is the same as B—A
- **Adjacency list**: Dictionary mapping vertices to sets of neighbors
- **No self-loops**: Vertices cannot connect to themselves
- **No duplicate edges**: Adding an existing edge is handled gracefully

### Supported Operations

| Operation | Description | Input Format |
|-----------|-------------|--------------|
| **Add Vertex** | Add a vertex to the graph | `A` (vertex value) |
| **Add Edge** | Add undirected edge | `A,B` (two vertices) |
| **Remove Vertex** | Remove vertex and its edges | `A` (vertex value) |
| **Remove Edge** | Remove undirected edge | `A,B` (two vertices) |
| **Neighbors** | Return adjacent vertices | `A` (vertex value) |
| **Vertices** | Return all vertices | (no input required) |
| **Edges** | Return all unique edges | (no input required) |
| **Size** | Return vertex count | (no input required) |
| **Is Empty** | Check if graph is empty | (no input required) |
| **Has Vertex** | Check if vertex exists | `A` (vertex value) |
| **Has Edge** | Check if edge exists | `A,B` (two vertices) |
| **Clear** | Remove all vertices/edges | (no input required) |

### Visual Features

- Circular layout for vertex placement
- Vertices drawn as circles with labels
- Edges drawn as lines between vertices (no arrows)
- Green highlight for newly added vertices
- Blue highlight for edge operations
- Empty state message when graph is empty
- Scrolling for large graphs

### Vertex Values

Supports both string and numeric vertices:
- Strings: `A`, `B`, `C`
- Numbers: `1`, `2`, `3`

For edge operations (Add Edge, Remove Edge, Has Edge), input format is `A,B` with comma separation.

### Time & Space Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Add Vertex | O(1) | O(1) |
| Add Edge | O(1) | O(1) |
| Remove Vertex | O(degree) | O(1) |
| Remove Edge | O(1) | O(1) |
| Neighbors | O(1) | O(degree) |
| Vertices | O(V log V) | O(V) |
| Edges | O(V + E) | O(E) |
| Size | O(1) | O(1) |
| Is Empty | O(1) | O(1) |
| Has Vertex | O(1) | O(1) |
| Has Edge | O(1) | O(1) |
| Clear | O(1) | O(1) |

**Note:** BFS and DFS will be added in a future phase.

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
│   ├── stack.py           # Stack implementation
│   ├── queue.py           # Queue implementation (collections.deque)
│   ├── linked_list.py     # Singly Linked List implementation
│   ├── bst.py             # Binary Search Tree implementation
│   ├── heap.py            # Max Heap implementation
│   └── graph.py           # Undirected Graph implementation
├── algorithms/            # Algorithm implementations (future)
│   └── __init__.py
├── visualization/         # Visualization utilities
│   ├── __init__.py
│   ├── array_visualizer.py     # Array visualization widget
│   ├── stack_visualizer.py     # Stack visualization widget
│   ├── queue_visualizer.py     # Queue visualization widget
│   ├── linked_list_visualizer.py  # Linked List visualization widget
│   ├── bst_visualizer.py       # BST visualization widget
│   ├── heap_visualizer.py      # Heap visualization widget
│   └── graph_visualizer.py     # Graph visualization widget
└── tests/                 # Unit tests
    ├── __init__.py
    ├── test_array.py      # Array unit tests
    ├── test_stack.py      # Stack unit tests
    ├── test_queue.py      # Queue unit tests
    ├── test_linked_list.py  # Linked List unit tests
    ├── test_bst.py        # BST unit tests
    ├── test_heap.py       # Heap unit tests
    └── test_graph.py      # Graph unit tests
```

## Architecture Overview

- **main.py**: Only responsible for starting the application
- **app/main_window.py**: Main window composition, connects all components
- **app/ui/sidebar.py**: Sidebar UI with data structure selection buttons
- **app/ui/visualization_panel.py**: Central area for visualizations (placeholder)
- **app/core/constants.py**: All reusable constants, styles, and configuration
- **data_structures/array.py**: Pure Python Array implementation (no GUI dependencies)
- **data_structures/stack.py**: Pure Python Stack implementation (no GUI dependencies)
- **data_structures/queue.py**: Pure Python Queue implementation using collections.deque (no GUI dependencies)
- **data_structures/linked_list.py**: Pure Python Singly Linked List implementation (no GUI dependencies)
- **data_structures/bst.py**: Pure Python Binary Search Tree implementation (no GUI dependencies)
- **data_structures/heap.py**: Pure Python Max Heap implementation (no GUI dependencies)
- **data_structures/graph.py**: Pure Python Undirected Graph implementation (no GUI dependencies)
- **visualization/array_visualizer.py**: PyQt6 widget for Array visualization
- **visualization/stack_visualizer.py**: PyQt6 widget for Stack visualization
- **visualization/queue_visualizer.py**: PyQt6 widget for Queue visualization
- **visualization/linked_list_visualizer.py**: PyQt6 widget for Linked List visualization
- **visualization/bst_visualizer.py**: PyQt6 widget for BST visualization
- **visualization/heap_visualizer.py**: PyQt6 widget for Heap visualization
- **visualization/graph_visualizer.py**: PyQt6 widget for Graph visualization
- **tests/test_array.py**: Unit tests for Array data structure
- **tests/test_stack.py**: Unit tests for Stack data structure
- **tests/test_queue.py**: Unit tests for Queue data structure
- **tests/test_linked_list.py**: Unit tests for Linked List data structure
- **tests/test_bst.py**: Unit tests for BST data structure
- **tests/test_heap.py**: Unit tests for Heap data structure
- **tests/test_graph.py**: Unit tests for Graph data structure

The codebase follows separation of concerns - UI code is separate from data structure logic, making it easy to extend.

## License

Academic project - ROSP