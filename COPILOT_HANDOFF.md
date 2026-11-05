# Handoff prompt: port the Agent provisioning prototype into the app

Paste everything below the line into GitHub Copilot (Agent mode) in the app repo.
Copy the prototype folder next to the repo first so Copilot can read
`Prototype.dc.html` as the visual reference. Fill in the two `<...>` placeholders.

---

You are replacing the UI of the existing Agent Create / Edit flow with a new
experience. The reference is `<path-to>/Prototype.dc.html` (a design-tool export:
React runtime + inline styles). **Do not copy its markup, runtime, or inline
styles.** Use it as the spec for layout, spacing, states, copy and behavior, and
implement it with this repo's own component library, styling system and
conventions. Stack: `<framework / styling system>`.

## Ground rules

1. Keep the existing data layer: same field names, same validation, same API calls,
   same state store. Only the view layer changes. Do not rename fields to match the
   prototype.
2. Read the current Create and Edit screens first and list every field, validation
   rule and API call they use before writing new UI. The prototype has the same
   fields; map each one.
3. Work in slices, each its own PR behind a feature flag `agentFlowV2` so the old UI
   stays reachable until the flag flips:
   - Slice 1: design tokens + modal shell + Create wizard (4 steps).
   - Slice 2: Edit shell (section nav, single scrolling form, scroll-spy) + deployment strip.
   - Slice 3: Publishing view wired to the real deployment status endpoint.
   - Slice 4: Playground and Consume tabs.
4. Max ~300 lines per file. Split before adding.
5. Write tests after each slice renders, in the same session. Minimum: wizard step
   gating, Enter-to-send, modal responsive behavior.
6. No secrets, tokens or sample credentials anywhere in code. The Consume tab shows
   `Bearer $TOKEN` as a literal placeholder.

## Design tokens (define once in the app's token system)

| Token | Value |
|---|---|
| font | Inter, system-ui fallback; base 14px / line-height 1.4; antialiased |
| text | #1F2937 · heading #111827 · muted #5B6472 · placeholder #8A94A3 |
| primary | #2F6BD8 · hover #2559BD · disabled #9DB8F0 |
| navy (header, selected step) | #1C3A6B · link #2B5BB5 |
| success | #1E7B3A · success bg #F2F8F3 · success border #D9E6DC |
| border | #CBD2DC · divider #E5E8EE · outline button border #B9C4D4 |
| surfaces | page #F3F5F8 · panel #F7F8FA · chip #EEF1F5 · selected #F3F7FE · nav-active #E3ECFA |
| warning chip | bg #FFF1DB · text #8A4B00 |
| code block | bg #0F1C33 · text #E6EDF7 · mono 12.5px / 1.55 |
| radius | inputs, buttons, cards 8px · modal, page cards 12px · chips 14px (pill) |
| control height | inputs/selects/buttons 40px · tertiary button 32px · tabs 46px |
| focus ring | 2px solid #2F6BD8, offset -1px |
| label | 12.5px / 500 / #374151, 6px below gap · help text 12px #5B6472 |
| section heading | 16px / 600 / #111827 · subtitle 13px #5B6472 |
| eyebrow | 11.5px / 600 / uppercase / letter-spacing .05em / #5B6472 |

Buttons: primary (filled), outline (white, navy text), tertiary (text, 32px, hover
#E3ECFA), icon (32px square). Font weight 600, padding 0 18px.

## Screens

### 1. Agents list page
- Top bar 56px navy: `[Platform] / Agents`.
- Page padding 36px 48px; H1 24px/600 "Agents" with primary "+ Create Agent" on the right.
- Empty state: dashed card, "No agents in DEV yet" / "Create one to provision it on Foundry."
- With agents: white card, grid columns `2fr 1.2fr 1.6fr 1fr`, eyebrow header row on
  panel bg. Row: name (600) + description (12.5px muted) · `Type · Env` ·
  deployment status (spinner "Publishing vN · m:ss" while active, green check
  "vN published · 1m 10s" when idle) · right-aligned tertiary "Playground" and
  outline "Edit" (36px).

### 2. Modal shell (shared by Create, Edit, Publishing)
- Overlay fixed to viewport, rgba(20,30,48,.58), padding 24px 16px, scrolls if needed.
- Dialog: width `min(1200px, 100%)`, **height = content**, `min-height: min(700px, 100%)`,
  `max-height: 100%`, radius 12px, shadow `0 24px 64px rgba(10,20,40,.45)`.
  Column flex: header (60px navy) · body (`flex:1; min-height:0; overflow:auto`) ·
  footer (68px, top divider).
- Header: title 17px/600 white. Create mode: right side "Step N of 4". Edit mode:
  1px divider, agent name, right pill `Type · Env` (rgba white .14 bg). Close icon
  button far right.
- Modal must never leave dead space below the content, and must never clip its footer.

### 3. Create wizard (4 steps)
- Stepper strip 64px, panel bg, padding 0 48px: 4 steps with 26px numbered circles
  joined by 1.5px lines. States: pending (grey ring), current (navy fill, label
  navy 600), done (green fill with check, line turns green). Done steps are clickable.
- Body: centered column max-width 760px, padding 36px 24px, 36px gap between sections.
- Footer: left hint text ("Nothing is deployed until step 4." / on step 4 "Creating
  publishes version 1 and provisions the agent on Foundry."), "Back" outline from
  step 2, right-aligned primary "Next: <next step name> ›" or "Create Agent" on step 4.
- Next is disabled until the current step is valid; Create Agent disabled until all
  steps are valid.
- Steps and fields (2-column grid, gap 16px 20px):
  1. **Basics**: Env (select), Project (select), Agent Name, Agent Type (select,
     Hosted), Agent Description (textarea 72px, full width).
  2. **Source & runtime**: subtitle "Source-code hosted agents are deployed from a
     GitHub repository." Deployment Method as two 48px radio cards: "Container
     Image" | "Source Code (GitHub repository)". GitHub Repository (help: "The GitHub
     App must have access to the repository."), Branch (optional, help "Defaults to
     main."), Runtime (select), Dependency Resolution (select), Entry Point (help
     shows the derived command, e.g. `Command: ["python","main.py"]`).
  3. **Resources & protocols**: CPU Allocation, Memory Allocation (selects with info
     icon). Hosted Protocols as 40px checkbox chips: Responses, Invocations,
     Invocations_WS, help "Select at least one." Environment variables (optional):
     key/value rows with a delete icon button, "+ Add Variable" tertiary on the right.
  4. **Registry & review**: Solution Registry select, help "EAI, DPC and Project are
     inherited from the selected solution." Inherited values shown as chips. Then
     **Review**: rows with grid `180px 1fr auto` (label 13px/600, value 13.5px,
     sub 12.5px muted, tertiary "Edit" that jumps to the step).

### 4. Edit shell
- Header in Edit mode. Below it the **deployment strip** (success bg, 52px row):
  check icon, eyebrow "LAST DEPLOYMENT", green 600 "Version N published in 1m 10s",
  `repo · branch @ sha` muted, right tertiary "View stages / Hide stages" with
  chevron. Expanded: stacked 14px phase bar (fetch #9DB8F0 / build #2F6BD8 /
  finalize #1E7B3A, widths by duration), legend row, then a 3-column grid of phase
  cards each listing its stages with durations.
- Tabs row (46px): Configure · Playground · Consume, active = navy text + 2px primary underline.
- Configure: left nav 232px panel bg (Basics, Source & runtime, Resources,
  Protocols, Environment variables "Optional", Solution registry; 40px items,
  active bg #E3ECFA). Right: one scrolling form with all sections, padding
  28px 44px 28px 36px, 36px gaps. Scroll-spy highlights the nav item for the
  section nearest the top.
- Footer: hint "No changes since version N." or "Updating publishes version N+1 and
  redeploys the agent." · outline "Close" · primary "Update Agent" (disabled until dirty).

### 5. Publishing view (replaces modal body while a deployment runs)
- Centered column max-width 800px. Header row: 30px spinner (or green check when
  done), title 20px/600 "Publishing version N" (done: "Version N published in 1m
  10s"), subtitle "Elapsed m:ss · last deployment took …" (done: "Ready · first
  response in 17.4 s"). Right: chips `repo · branch @ sha` and any environment chip,
  grouped so they wrap together under the title on narrow widths.
- Stacked phase progress bar + legend ("Fetch source · 3.3 s", "Build & provision ·
  12.8 s so far", "Finalize · pending").
- Three phase groups (eyebrow + total on the right), each with 36px stage rows:
  done = check + duration, running = highlighted bg #EEF4FD, 600, navy, live
  elapsed "8.3 s…", waiting = greyed with "—". Stages:
  - Fetch source: Validate request · Authenticate with GitHub · Resolve branch
    commit (meta `branch @ sha`) · Download source (meta `3 files · 744 B`) · Package source.
  - Build & provision: Upload to Foundry · Foundry provisioning (meta "Foundry
    version N"; while running "usually the longest stage (44.3 s last time)").
  - Finalize: Save configuration · Readiness check (cold start) (meta "First response in 17.4 s").
- Footer while running: hint "You can close this dialog — publishing continues, and
  the result lands in the deployment strip." · outline "Close" · primary
  "Publishing…" disabled. When done: hint "The agent is live. Try it in the
  playground, or open it to review the configuration." · "Close" · outline "Open in
  Edit" · primary "Try in Playground".
- Drive this from the real deployment status API (poll or stream). The prototype
  fakes it with a timer; do not port the timer. Closing the dialog must not cancel
  the deployment; the list row and deployment strip reflect status.

### 6. Playground tab
- Two panes: transcript column (flex 1, min-height 480px) and right aside 320px panel bg.
- Status bar 44px: green dot, "Agent is running · vN · <protocol> · first response in
  17.4 s", right tertiary "Clear".
- Transcript: 24px 28px padding, 14px gaps, bubbles max-width 72%, radius 12px
  with a 4px corner on the sender side; user = navy bg white text, agent = #F3F5F8.
  Meta line 11.5px muted under each bubble. Optional raw JSON block under agent
  replies when "Show raw response" is on. Thinking state = spinner bubble.
  Empty state centered: "Send a message to verify the agent responds" / "Replies
  come from the published version over the selected protocol."
- Composer: label "Message", 56px textarea, primary "Send" (disabled when empty or
  while waiting). **Enter sends, Shift+Enter inserts a newline.** Auto-scroll to
  the newest message.
- Aside: Protocol select (only protocols enabled in Configure, help text says so),
  "Show raw response" checkbox chip, "Last response" latency (22px) + note, and
  "Checks" list (Version N published · Readiness check passed · CPU · Memory).
- Footer hint: "Messages here go to the published agent; nothing is saved to the configuration."

### 7. Consume tab
- Key/value rows (grid `150px 1fr auto`, 10px padding, dividers): Agent ID, Endpoint
  (`https://<gateway-host>/agents/<agent-id>`), Authentication ("Bearer token from
  [identity provider] · scope [agent-invoke]"), Enabled protocols (chips). Copy
  tertiary button on ID and Endpoint.
- Segmented control for protocol (Responses / Invocations / Invocations_WS; disabled
  ones greyed, help "Greyed-out protocols are not enabled for this agent.") and a
  second segmented control cURL / Python / TypeScript on the right.
- Code block with "Copy" and a note: "Samples are generated from this agent's
  configuration (version N, <protocol>). Host, token and scope are placeholders
  until the gateway supplies the real values."
- Footer hint: "Re-publishing does not change the endpoint, only the version behind it."

## Responsive rules (verified in the prototype at 1440, 1280, 1024, 768, 375)

- `≤1100px`: page padding 24px; stepper and edit form padding 24px.
- `≤900px`: hide the Edit section nav (keep scroll-spy harmless); playground stacks
  (transcript on top, aside full width, max 40% height); phase cards grid → 1 column;
  agents table → stacked card per row, header row hidden; review rows and key/value
  rows → 1 column; chat bubbles max-width 90%; stepper shows numbers only
  (labels hidden); expanded stage list capped at 40vh and scrolls internally.
- `≤640px`: dialog is full-screen (no radius, height 100%), body scrolls, footer
  stays pinned; 2-column grids → 1 column; page and form padding 16–20px; modal
  header drops the agent name and shrinks padding; footers wrap, hint text hidden,
  buttons right-aligned; deployment strip wraps and hides the `repo · branch @ sha`
  text; legends wrap with nowrap items.
- Must include `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- Never horizontal page scroll at any width. Never clip a footer button.

## Acceptance checklist (run before each PR)

- [ ] Wizard: Next disabled until the step is valid; stepper done-steps clickable; modal
      height stable across steps 1–3, grows only on step 4; no empty space under the form.
- [ ] Edit: scroll-spy tracks sections; Update disabled until dirty; deployment strip
      expands/collapses without the form losing scroll position.
- [ ] Publishing: live stage states from the API; closing the dialog keeps the
      deployment running; list row shows publishing/idle state.
- [ ] Playground: Enter sends, Shift+Enter newline, Send disabled while waiting,
      auto-scroll, protocol list limited to enabled protocols.
- [ ] Consume: segmented controls disable un-enabled protocols; copy buttons work.
- [ ] Viewports 1440, 1280, 1024, 768, 375: no clipping, no horizontal scroll, footer visible.
- [ ] No long tasks > 50 ms during the publishing view; typing has no visible lag.
- [ ] Old UI still reachable with `agentFlowV2` off.
