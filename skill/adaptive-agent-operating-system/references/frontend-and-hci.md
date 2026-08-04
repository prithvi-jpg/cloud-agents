# Frontend engineering and human-centered interaction

## Contents

1. Product and interaction framing
2. Seven-stage completion contract
3. Real-browser verification
4. Visual craft and reference use
5. Journey and progressive disclosure
6. State, feedback, and repair
7. Accessibility and responsive behavior

## 1. Product and interaction framing

Before implementation identify:

- primary user and job;
- information hierarchy;
- conceptual model;
- critical journey;
- states and transitions;
- decisions and actions;
- evidence and trust needs;
- error, empty, loading, permission, and recovery states;
- taste/reference bar;
- what should be previewed for human steering.

Create an interaction flow or editable preview when the interaction model—not code—is the main uncertainty.

Do not default to a dashboard, card grid, green AI aesthetic, or component-library look. The visual system must follow the project brief and references.

## 2. Seven-stage completion contract

Evaluate in order.

### Gate 0 — Real artifact

Require:

- expected source files;
- genuine implementation;
- no screenshot, placeholder, or fake interaction;
- no hidden external dependency that violates scope.

Failure blocks completion.

### Gate 1 — Build and runtime

Require:

- install/build in one declared runtime;
- successful page load;
- no unhandled runtime or console errors;
- working routes and assets.

Failure blocks completion.

### Gate 2 — Functional behavior

Require:

- critical flows through real input and state;
- persistence where promised;
- relevant loading, empty, error, permission, and recovery states;
- meaningful action feedback;
- working keyboard and pointer interactions.

Failure of the primary job blocks completion.

### Gate 3 — Structure and accessibility

Check:

- semantic hierarchy;
- focus order and visible focus;
- labels and names;
- keyboard operation;
- contrast;
- target sizes;
- responsive structure;
- reduced-motion behavior where relevant.

### Gate 4 — Visual craft

Inspect rendered output for:

- typography and hierarchy;
- spacing rhythm and density;
- alignment and grid;
- color/material language;
- component specificity;
- iconography and imagery;
- motion timing and restraint;
- fidelity to an approved reference or direction.

Reject structurally valid but generic output when the brief calls for authored craft.

### Gate 5 — Interaction experience

A fresh user should understand:

- where they are;
- what state the system is in;
- what matters now;
- why a recommendation or action exists;
- what happens after action;
- how to correct, undo, defer, or recover;
- where to go next.

Motion should clarify continuity, causality, hierarchy, or feedback.

### Gate 6 — Independent receipt

Combine deterministic checks with fresh visual and product review. Give the evaluator the artifact and criteria, not the builder's persuasive explanation. Link completion claims to evidence.

## 3. Real-browser verification

For meaningful interactive work:

1. build and serve the actual artifact;
2. navigate with a real browser;
3. exercise critical controls;
4. inspect state changes and persistence;
5. capture console/runtime errors;
6. test desktop and mobile;
7. inspect screenshots;
8. rerun affected checks after repair.

Structural HTML or unit tests alone do not prove rendered quality or interaction.

Record:

- browser/version;
- viewport sizes;
- tested routes and flows;
- assertion counts;
- console/runtime result;
- screenshots reviewed;
- known untested behavior.

## 4. Visual craft and reference use

When taste matters:

- research or inspect actual references before styling;
- extract principles rather than copying superficial motifs;
- produce a directional preview early enough for steering;
- compare rendered output rather than source code;
- keep the solution coherent across every page.

The optional Foundry/Studio visual direction, when no project-specific direction supersedes it:

- warm paper or material surface;
- black/ink structure;
- yellow and orange signals;
- oversized editorial typography;
- tactile or industrial controls;
- visible borders and construction;
- restrained purposeful motion;
- no generic green SaaS/AI shell.

This is a default reference, not a universal brand requirement.

## 5. Journey and progressive disclosure

Every long HTML/site surface should provide:

- persistent small journey/navigation;
- current-page or current-section highlight;
- logical sequence without pretending every route is strictly linear;
- one clear next meaningful page/action;
- route back to the system home;
- supporting readers behind secondary navigation.

Use progressive disclosure:

- start with orientation and current decision;
- expose evidence and detail on demand;
- keep sources traceable;
- avoid overwhelming the user with implementation telemetry.

## 6. State, feedback, and repair

Design all relevant states:

- initial;
- loading;
- success;
- partial;
- empty;
- stale;
- offline;
- error;
- permission needed;
- declined/cancelled;
- recovery;
- complete.

Give feedback close to the action. Preserve user inputs where safe. Explain what happened and what the user can do next. For AI recommendations, show source, confidence/uncertainty, and correction/defer controls.

## 7. Accessibility and responsive behavior

At minimum:

- semantic landmarks and headings;
- labels for controls;
- visible focus;
- keyboard access;
- adequate hit targets;
- readable line length and type scale;
- no unintended horizontal overflow;
- responsive hierarchy, not merely stacked desktop cards;
- motion alternatives when animation is substantial;
- understandable errors and status announcements.

Scale checks to the product and risk. Do not claim full conformance from a small mechanical scan.
