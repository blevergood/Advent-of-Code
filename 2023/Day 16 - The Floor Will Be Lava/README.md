# Day 16: The Floor Will Be Lava

### Summary

_You have a grid (represented by a list of strings) made up of empty spaces (`.`), mirrors (`/`, `\`), and splitters (`|`, `-`)_

_You have a "beam of light" that traverses the grid based on how it reaches each tile. Determine how many unique tiles are traversed given the following rules:_

- _(`.`): Keep traversing in the same direction_
- _(`/`, `\`): rotate direction 90° based on symbol and approaching direction:_
  - _`/`_
    - _`right` <-> `up`_
    - _`left` <-> `down_`
  - _`\`_
    - _`right` <-> `down`_
    - _`left` <-> `up`_
- _(`|`, `-`)_
  - _If approaching from the "flat" side, split into two beams moving in he direction perpendicular to the flat side._
    - _If you hit a `|` from the left or right, create two beams moving up and down respectively_
    - _if you hit a `-` from the top or bottom, create two beams moving left and right respectively_
  - _If approaching for the other side, treat it like an empty space (`.`)_

_Return the number of tiles hit by all beams of light._

### Problem Statement

With the beam of light completely focused **somewhere**, the reindeer leads you deeper still into the Lava Production Facility. At some point, you realize that the steel facility walls have been replaced with cave, and the doorways are just cave, and the floor is cave, and you're pretty sure this is actually just a giant cave.

Finally, as you approach what must be the heart of the mountain, you see a bright light in a cavern up ahead. There, you discover that the beam of light you so carefully focused is emerging from the cavern wall closest to the facility and pouring all of its energy into a contraption on the opposite side.

## Part One

Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing **empty space** (`.`), **mirrors** (`/` and `\`), and **splitters** (`|` and `-`).

The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of the beam's light into **heat** to melt the rock in the cavern.

You note the layout of the contraption (your puzzle input). For example:

```
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
```

The beam enters in the top-left corner from the left and heading to the **right**. Then, its behavior depends on what it encounters as it moves:

- If the beam encounters **empty space** (`.`), it continues in the same direction.
- If the beam encounters a **mirror** (`/` or `\`), the beam is **reflected** 90 degrees depending on the angle of the mirror. For instance, a rightward-moving beam that encounters a `/` mirror would continue **upward** in the mirror's column, while a rightward-moving beam that encounters a `\` mirror would continue **downward** from the mirror's column.
- If the beam encounters the **pointy end of a splitter** (`|` or `-`), the beam passes through the splitter as if the splitter were **empty space**. For instance, a rightward-moving beam that encounters a `-` splitter would continue in the same direction.
- If the beam encounters the **flat side of a splitter** (`|` or `-`), the beam is **split into two beams** going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a `|` splitter would split into two beams: one that continues **upward** from the splitter's column and one that continues **downward** from the splitter's column.

Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is **energized** if that tile has at least one beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the contraption:

```
> |<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..
```

Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only showing whether a tile is **energized** (**`#`**) or not (`.`):

```
######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..
```

Ultimately, in this example, **`46`** tiles become **energized**.

The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation. With the beam starting in the top-left heading right, **how many tiles end up being energized?**

### Solution

Your puzzle answer was **`7860`**.

## Part Two

### Summary

_Same as part 1, but figure out the largest number of tiles energized by starting a beam from each of the edge tiles._

_Beams move away from the edge that they enter from._

- _Top tiles move down, bottom tiles move up_
- _Left tiles move right, right tiles move left_
- _Corner tiles generate two beams each moving in one of the appropriate directions_

### Problem Statement

As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you to a nearby control panel. There, a collection of buttons lets you align the contraption so that the beam enters from any edge tile and heading away from that edge. (You can choose either of two directions for the beam if it starts on a corner; for instance, if the beam starts in the bottom-right corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading upward), any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left). To produce lava, you need to find the configuration that energizes as many tiles as possible.

In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:

```
.|<2<\....
|v-v\^....
.v.v.|->>>
.v.v.v^.|.
.v.v.v^...
.v.v.v^..\
.v.v/2\\..
<-2-/vv|..
.|<<<2-|.\
.v//.|.v..
```

Using this configuration, 51 tiles are energized:

```
.#####....
.#.#.#....
.#.#.#####
.#.#.##...
.#.#.##...
.#.#.##...
.#.#####..
########..
.#######..
.#...#.#..
```

Find the initial beam configuration that energizes the largest number of tiles; **how many tiles are energized in that configuration?**

### Solution

Your puzzle answer was **`8331`**.
