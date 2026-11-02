# Day Blocks

**Plan your day, one block at a time.**

Day Blocks is a Super Productivity companion that helps you decide **when** to work on today's tasks and habits. Keep your day simple: drag an item into Morning, Afternoon, Evening, or Night, then arrange the order that feels right to you.

> Day Blocks is a separate plugin from [Today+](https://github.com/phuongtt2a/super-productivity-today-plus). They work independently, and you can keep using either or both.

## Your day at a glance

![Day Blocks dashboard with four time blocks in a single horizontal timeline](docs/screenshots/day-blocks-desktop.webp)

**Simple controls, distinct sessions**

![Session actions and personalized background-color choices](docs/screenshots/session-color-options.webp)

<details>
<summary>See the phone layout and a task continuing into another block</summary>

![Swipe horizontally between day blocks on your phone](docs/screenshots/day-blocks-phone.webp)

![Continue the same task in another time block](docs/screenshots/continuing-session.webp)

![Phone view after swiping along the daily timeline](docs/screenshots/day-blocks-phone-scroll.webp)

</details>

## Make space for what matters

- **Four blocks, one day.** Follow Morning (5 AM–noon), Afternoon (noon–6 PM), Evening (6–10 PM), and the slate-gray Night (10 PM–midnight) from left to right.
- **Tasks and habits together.** Find today's items in **Unassigned**. Move them into a block with a drag or the **Plan** button. Expand a planned task to see and complete its subtasks.
- **Clean, one-line controls.** Five compact icons for Done (or habit progress), Move up, Move down, Time / Move, and More. Hover or focus to see what each icon does. **More** opens a separate popup for another session, removing a session, and choosing colors.
- **Make colors yours.** Each session has a soft background by default. Pick a preset or set any custom color; the choice is saved for that individual session.
- **Choose your order.** Drag planned sessions to another position, or use the visible up/down arrows on each card.
- **Plan the time you need.** Leave a session flexible, give it a planned duration, or choose an exact start and end time within its block.
- **Continue in another block.** Use **+ Session** when one task or habit needs more than one part of the day. The linked cards still represent the same original item.
- **Keep a daily habit routine.** Choose **Repeat this habit session on future scheduled days** when planning a habit you want to do regularly.
- **Stay in charge of progress.** Mark tasks done, update habit counters, or add time you've already spent on stopwatch habits. Scheduling never marks an item completed.
- **Keep tomorrow flexible.** Go to the previous or next day to plan ahead, while repeating habits follow their existing scheduled days.

An item disappears from **Unassigned** after you plan its first session. You can add further sessions without creating duplicate tasks or habits. Removing all of today's sessions returns it to Unassigned.

## On your phone

The four time blocks **remain in one horizontal row**, just like a timeline. Swipe sideways to move through the day. **Plan**, the clock icon, and up/down arrows work without dragging.

![Compact Day Blocks layout on a small phone](docs/screenshots/day-blocks-small-phone.webp)

## Install the preview

**Status: v0.1.1-beta.2 preview — not a stable release yet.**

1. Open the [Day Blocks repository](https://github.com/phuongtt2a/super-productivity-day-blocks) and find the latest successful **Check Day Blocks plugin** run for the preview pull request.
2. Download the `day-blocks-preview` artifact and extract it.
3. Inside, locate `dist/day-blocks-super-productivity.zip`.
4. In Super Productivity, open **Settings → Plugins → Choose Plugin File** and install that ZIP **without unpacking the plugin ZIP itself**.
5. Open **Day Blocks** from the plugins menu.

When we've finished testing together, the stable version will be available from [GitHub Releases](https://github.com/phuongtt2a/super-productivity-day-blocks/releases) in one step.

## A few things to know

Day Blocks plans your time; it is **not a second timer or calendar**. Planning 45 minutes does not log 45 minutes of completed work. A habit's daily goal and actual progress still belong to Super Productivity. Actual progress controls are enabled when viewing Today; planning past or future days doesn't secretly change today's habit values.

A task appearing in Morning and Afternoon is **one task with two planned sessions**. Finishing it updates both cards. Tasks and habits you've deleted in Super Productivity can be removed from the plan.

Routine planning actions quietly update the board. If something fails, Day Blocks briefly shows an explanation rather than leaving a permanent notification at the bottom.

You can keep using Today+ v2.0.0 exactly as before. Day Blocks doesn't modify its layout, preferences, or plugin release.

---

**Simple planning, a calmer day.**

[Release history](CHANGELOG.md) · [Testing notes](docs/QUALITY.md)
