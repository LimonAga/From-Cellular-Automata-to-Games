# Wolfram’s Cellular Automata

**Wolfram’s Cellular Automata** (also known as **Elementary Cellular Automata**) is a 1-dimensional cellular automaton.  
Each cell can be in one of two possible states: **0** or **1**.

The system starts with a single line of cells, typically with only one cell in the middle set to **1**, and all others set to **0**.  
Future states of cells depend on their **neighbors** — the cells to their immediate left and right.

---

## How It Works

Each cell’s next state is determined by a **rule** that maps every possible 3-cell neighborhood (left, center, right) to an output state.  
There are **8 possible neighborhood patterns**, ranging from `111` to `000`.

Each pattern’s outcome is defined by a **rule number**, between **0 and 255**.  
This rule number is converted into binary form, and each bit of that binary sequence represents the output for one neighborhood pattern.

For example, **Rule 98** works like this:

```
98 in binary → 01100010
```

| Neighborhood | Next State |
|---------------|------------|
| 111 | 0 |
| 110 | 1 |
| 101 | 1 |
| 100 | 0 |
| 011 | 0 |
| 010 | 0 |
| 001 | 1 |
| 000 | 0 |

To learn more about binary representation, see:  
[Binary Number - Wikipedia](https://en.wikipedia.org/wiki/Binary_number)

---

## Visualizing the Automaton

By applying the rule repeatedly, we can generate new generations of cells.  
Each new generation is drawn **below** the previous one, forming a visual pattern over time.

Some rules produce highly structured patterns (like the **Sierpiński triangle**), while others appear chaotic or random.

*Example output images:*  
_(Rule 30, Rule 90, or Rule 110.)_

---

## Implementation

This repository includes **two implementations**:

1. **Console Version**  
   Runs entirely in the terminal.  
   No external modules required.

2. **Pygame Version**  
   Uses `pygame` for better visuals.  
   To install pygame:

   ```bash
   pip3 install pygame-ce
   ```

---

## References

- [Stephen Wolfram – Elementary Cellular Automata](https://en.wikipedia.org/wiki/Elementary_cellular_automaton)
- [Binary Numbers – Wikipedia](https://en.wikipedia.org/wiki/Binary_number)
