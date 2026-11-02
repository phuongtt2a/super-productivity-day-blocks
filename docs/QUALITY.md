# Day Blocks — Preview review

This page is for testing the Day Blocks preview. The plugin is not yet a stable release.

## Planning a day

- [ ] The four blocks stay left-to-right: Morning → Afternoon → Evening → Night, including on small phones.
- [ ] Tasks and habits scheduled today appear in Unassigned until placed.
- [ ] Drag an item into a block. Verify it disappears from Unassigned and can be moved back.
- [ ] Use Plan instead of dragging, especially on a phone.
- [ ] Reorder several tasks and habits together in one block with drag or **More → Move up / Move down**.
- [ ] Each planned session is visually distinct, with enough contrast in light and dark modes.
- [ ] Each card has a tidy primary area and **More** for additional commands, without clipped controls or visual overflow.
- [ ] Select a preset background, then a custom hex color; both should apply to just that session.
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

- [ ] Completing a task in one block updates its other sessions.
- [ ] A repeated habit counts as completed once, even when planned several times.
- [ ] Expand a task with subtasks and complete one. Its status updates in every linked session.
- [ ] When planning tomorrow, task and habit completion controls are disabled; only the plan can be changed.
- [ ] No duplicate native task or habit is created.
- [ ] Both Today+ and Day Blocks can be installed together without changing each other's settings.

## Appearance and navigation

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
