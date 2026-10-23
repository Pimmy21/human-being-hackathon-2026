# Antenna Design Comparison

Working title · Proposal from Josh · Suggested Track 1: Solving Fragmented Intelligence

## What we want to do

We want to help RF engineers and students compare antenna designs from research papers before choosing one to build.

Today, someone may read ten PDFs, copy the dimensions by hand and struggle to compare designs that use different names, units or materials. Important missing details or manufacturing problems may only become obvious later.

Our agent would bring these scattered details into one place, with links back to the papers.

## How it works

The user chooses one type of antenna and a small set of papers. The agent:

- Finds the design dimensions, materials and other key details in each paper.
- Converts units and matches different names for the same part, while keeping the original values and sources.
- Checks for missing details, contradictions and a small set of design rules chosen with an RF expert.
- Checks the design against selected manufacturing limits, such as a PCB maker's published minimum hole or track size, where those limits apply.
- Shows the designs side by side in an interactive 3D view, with evidence and warnings attached.

Missing dimensions stay marked as missing. The agent should ask for clarification rather than silently invent a buildable design.

## Our first demo

Start with **one antenna type and two or three papers**. Show how the agent turns their different descriptions into a consistent comparison and a simple 3D view.

For each design, users can open the source for a dimension and see what is missing or needs checking. Any estimated geometry must be labelled. We should first confirm that the chosen papers contain enough information to make a useful model.

The first version checks selected rules; it does not prove that an antenna will work or replace electromagnetic simulation. Connections between conductors depend on the antenna type, so there is no universal rule that inner and outer conductors must always connect.

## Where the tools fit

- **Zetaris:** make structured design details from different papers available for comparison and querying. It does not automatically find or read every paper.
- **Meterless H-MEM:** remember sourced design details, unresolved questions and user corrections.
- **NVIDIA models:** help read papers and suggest structured values or explanations, with sources for human checking.
- **Nightshift:** a planned AI provider connection to complete and test.
- **Cursor, ChatGPT and Codex:** help build and test the extraction, comparison and interface.
- **3D and design tools:** display parameter-based geometry and make the comparison easy to use. Geometry comes from sourced parameters, not an image generator.

## What we want your feedback on

Which antenna type should we start with? Can we find two or three papers with enough design details? Which simple checks would be useful and safe to demonstrate during the hackathon?
