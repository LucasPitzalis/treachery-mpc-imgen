# Treachery MPC IMGen

A lightweight tool to prepare [MTG Treachery](https://mtgtreachery.net/) cards for high-quality printing on [MakePlayingCards](https://www.makeplayingcards.com/)

---

## Quick Start

### 1. Download

Go to the **Releases** section and download the executable for your system:

* Windows → `.exe`
* Linux → binary

---

### 2. Prepare your files

Create the following structure:

```
input/
output/
```
* Get the source material (source cards images) from the [treachery website](https://mtgtreachery.net/#download). Make sure to pick the IMG (.png) versions of your desired language.
* Put your card images in the `input/` folder
* Leave `output/` empty (results will be generated there)

---

### 3. Run the tool

#### On Windows

Double-click the `.exe`
or run:

```
mtg-treachery-tool.exe
```

#### On Linux

```
chmod +x mtg-treachery-tool
./mtg-treachery-tool
```

---

## Output

Processed images will be available in the `output/` folder.

They are ready for upload to MakePlayingCards with proper bleed and alignment.

---

## What it does

* Adds print bleed (1/8 inch)
* Extends borders to avoid white edges
* Automatically matches card border color
* Fixes corner artifacts
* Processes all images in batch

## Issues

If something doesn’t look right, feel free to open an issue.
