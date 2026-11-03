# Day Blocks — Quality review

**Stable baseline: v1.0.0.** The user confirmed that the latest beta behavior works in the installed Super Productivity application. This checklist records our ongoing quality standards for future changes; it is not a list of unfinished release blockers.

Screenshots and the full user guide are available in the [README](../README.md).

## Planning a day

- [ ] The four blocks stay left-to-right: Morning → Afternoon → Evening → Night, including on small phones.
- [ ] Tasks and habits scheduled today appear in Unassigned until placed.
- [ ] Drag an item into a block. Verify it disappears from Unassigned and can be moved back.
- [ ] Use Plan instead of dragging, especially on a phone.
- [ ] Reorder several tasks and habits together in one block with drag or the visible up/down arrow icons.
- [ ] Each planned session is visually distinct, with enough contrast in light and dark modes.
- [ ] The README shows the latest desktop timeline, session action controls, centered color popup, and mobile popup screenshots.
- [ ] Each card shows exactly five icon-only actions in one horizontal row: Done (or relevant habit action), Up, Down, Time / Move, More.
- [ ] Each icon has an accessible label and a tooltip; the **More** icon opens a centered popup without expanding or shifting other cards.
- [ ] The two session buttons, **Add session** and **Remove**, sit side by side below the five icons in each card.
- [ ] The popup focuses on colors (no duplicate Add/Remove controls).
- [ ] Close the popup via Escape, close control, or outside click. On mobile, the centered popup stays inside the viewport.
- [ ] Keep the popup open while native tasks, habits or synced plugin data refresh automatically. Close it only when the user dismisses it, changes days or the original session disappears.
- [ ] The Night block uses a muted slate/gray header with readable text in both themes.
- [ ] Dragging, saving, logging time, and moving sessions do not leave persistent success notices at the bottom. Failures still show useful feedback.
- [ ] Select a preset background, then a custom hex color or use Hue/Saturation/Lightness sliders. **Apply color** must save the color and close the popup immediately.
- [ ] Reopen More after applying a color; verify the saved hex value, and confirm focus returns to the original More control.
- [ ] Enter an invalid hex: Apply color should be disabled while the popup remains open. Valid colors should update only the selected session.
- [ ] The custom controls stay inside the popup (no extra native/system color window). After applying a color, Close, Escape, and outside click should all dismiss the popup.
- [ ] Reopen the popup and verify the chosen color remains selected, including on a narrow mobile screen.
- [ ] Move a colored session between blocks, reorder it, and reopen the app. The chosen color stays with that session.
- [ ] Reset a session to automatic color. Changing the color of one linked session must not recolor its other appearances.
- [ ] Verify the Unassigned list remains next to the timeline on desktop, so drag-and-drop stays convenient.
- [ ] Add a second session for one task. Its linked cards should appear in both blocks, but it should count as one item.
- [ ] Move just one linked session to another block without moving the other sessions.
- [ ] Set exact times within a block; try an invalid time and check the explanation.
- [ ] Plan a session ending at midnight in Night.
- [ ] Use a flexible session without an exact start or end.

## Habits

- [ ] Add a habit to the timeline, even when its daily goal has already been reached.
- [ ] Log extra actual time on a stopwatch habit and verify the original habit's progress updates.
- [ ] Keep scheduled time separate from actual time.
- [ ] Choose Repeat for a habit session and check it appears on the following scheduled day.
- [ ] Remove a repeated habit session just for today without affecting future scheduled days.
- [ ] Restart the app and check that today's plan is restored.

## Completion and safety

- [ ] Clicking a task title in Unassigned opens its original details in Super Productivity.
- [ ] Clicking a task title in a planned Morning or Afternoon session opens the same original task; the plan and completion remain unchanged.
- [ ] Clicking a subtask title opens that subtask's details, whereas its checkbox still toggles completion.
- [ ] Task titles are keyboard accessible and no navigation is triggered by dragging/reordering, marking Done, or pressing other card buttons.
- [ ] Habit titles remain unchanged (they are not tasks).
- [ ] Completing a task in one block updates its other sessions.
- [ ] A repeated habit counts as completed once, even when planned several times.
- [ ] Expand a task with subtasks and complete one. Its status updates in every linked session.
- [ ] When planning tomorrow, task and habit completion controls are disabled; only the plan can be changed.
- [ ] No duplicate native task or habit is created.
- [ ] Both Today+ and Day Blocks can be installed together without changing each other's settings.

## Appearance and navigation

- [ ] On a wide desktop, open any task detail. The timeline still has four separate blocks in one horizontal row.
- [ ] Keep task details open while narrowing the plugin view to about 1100, 900, 720 and 560 pixels: Unassigned stays to the left, the day blocks never stack or become squeezed, and the timeline scrolls sideways.
- [ ] Close task details and widen the view again: the full four-column timeline is restored without losing its planned sessions.
- [ ] Check the screenshot documenting the narrower task-details layout.

- [ ] Check desktop, tablet, and 320px / 390px mobile widths.
- [ ] Check touch, mouse, keyboard, and long Vietnamese titles.
- [ ] Check light/dark theme, the application's font, and wallpaper transparency.
- [ ] Make sure the main page has no horizontal overflow on mobile; only the timeline scrolls sideways.

## Known constraints

- Time blocks begin at 5 AM and end at midnight in this first preview.
- Planned sessions aren't native calendar appointments or notifications.
- Day Blocks does not start an independent task or habit timer.
- Cross-device preference sync depends on the Super Productivity sync provider and configuration.
- Native habit counter changes are only valid for the actual current day; other days are planning views.
