# DevNotebook Design Guidelines

## Design Approach: Productivity-First System Design

**Selected Framework**: Material Design principles with Bootstrap 5 implementation
**Rationale**: DevNotebook is a productivity tool where clarity, efficiency, and information density matter most. Drawing from Linear's clean interfaces and Notion's content organization, with Bootstrap 5 for responsive foundation.

## Core Design Principles

1. **Information Hierarchy**: Clear visual priority for active projects and tasks
2. **Scannable Content**: Quick identification of status, priority, and progress
3. **Action-Oriented**: Primary actions immediately accessible
4. **Contextual Focus**: Minimize distractions, maximize workspace

---

## Typography System

**Font Stack**: System fonts via Bootstrap (fast, native feel)
```
Primary: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto
Monospace: "SFMono-Regular", Consolas, "Courier New" (for code/tech stack displays)
```

**Hierarchy**:
- Page Headers: 2rem (32px), font-weight 700
- Section Titles: 1.5rem (24px), font-weight 600
- Card Headers: 1.125rem (18px), font-weight 600
- Body Text: 1rem (16px), font-weight 400
- Captions/Meta: 0.875rem (14px), font-weight 400
- Labels: 0.75rem (12px), font-weight 600, uppercase with letter-spacing

---

## Layout System

**Spacing Primitives**: Bootstrap spacing scale (0.25rem increments)
- Core units: 2, 3, 4, 5 (0.5rem, 0.75rem, 1rem, 1.25rem)
- Component padding: p-3 to p-4
- Section spacing: my-4 to my-5
- Card gaps: gap-3

**Grid Structure**:
- Main Container: `container-fluid` with `max-width: 1400px`
- Dashboard Layout: Sidebar (250px fixed) + Main Content (fluid)
- Responsive Breakpoints: Mobile-first, stack to columns at md (768px)

**Page Layouts**:

1. **Dashboard**: 
   - Sidebar navigation (fixed left, 250px)
   - Top bar with user menu + quick actions (h-16)
   - Main content area with padding p-4

2. **List Views** (Ideas, Plans, Todos):
   - Search/filter bar at top (sticky)
   - Grid of cards: 1 column mobile, 2 columns tablet, 3 columns desktop
   - Card spacing: gap-4

3. **Detail/Form Pages**:
   - Single column, max-width 800px, centered
   - Form sections with clear grouping (border or background cards)

---

## Component Library

### Navigation
**Sidebar**:
- Fixed position, full height
- Logo/app name at top (h-16)
- Navigation items with icons (Heroicons via CDN)
- Active state: subtle background with border-left accent
- User profile at bottom

**Top Bar**:
- Search input (w-64 on desktop, hidden on mobile)
- Notification icon
- User avatar dropdown
- Mobile: hamburger menu for sidebar toggle

### Cards & Containers
**Project/Idea Cards**:
- Border radius: 0.5rem
- Shadow: subtle elevation (shadow-sm)
- Padding: p-4
- Header: title + status badge
- Body: 2-3 line description with ellipsis
- Footer: metadata (date, author) + action buttons

**Status Badges**:
- Pill shape (rounded-full)
- Small size: px-2.5, py-0.5
- Font: 0.75rem, font-weight 600

### Forms
**Input Fields**:
- Height: h-10 (2.5rem)
- Padding: px-3
- Border: 1px solid
- Border radius: 0.375rem
- Focus: 2px ring offset

**Buttons**:
- Primary: h-10, px-4, font-weight 600, rounded-md
- Secondary: outline variant
- Icon buttons: square (w-10 h-10), centered icon
- Button groups: join with border-radius on ends only

**Select/Dropdowns**:
- Same height as inputs (h-10)
- Chevron icon right-aligned
- Dropdown menu: shadow-lg, max-height with scroll

### Data Display
**Todo List Items**:
- Checkbox left-aligned
- Content with strikethrough when completed
- Priority indicator (dot or border-left accent)
- Category tag (small badge)
- Actions on hover/mobile always visible

**Tables** (Admin panel):
- Striped rows for readability
- Fixed header on scroll
- Action column right-aligned
- Responsive: stack to cards on mobile

**Progress Indicators**:
- Feasibility scores: horizontal bar chart (h-2, rounded-full)
- Completion status: circular progress or percentage badge

### Modals & Overlays
- Modal max-width: 600px
- Backdrop: semi-transparent overlay
- Header with title + close button (X icon)
- Content padding: p-6
- Footer with action buttons (right-aligned)

---

## Responsive Behavior

**Mobile (< 768px)**:
- Sidebar becomes slide-over drawer
- Top bar: logo + hamburger only
- Cards: single column, full width
- Tables: transform to stacked cards
- Form fields: full width

**Tablet (768px - 1024px)**:
- Collapsible sidebar (icon only mode)
- 2-column card grids
- Optimized spacing (p-3 instead of p-4)

**Desktop (> 1024px)**:
- Full sidebar visible
- 3-column card grids where applicable
- Hover states for interactive elements
- Expanded table views

---

## Icons

**Library**: Heroicons via CDN (outline style primary, solid for active states)

**Key Icons**:
- Lightbulb: Ideas
- Document: Plans
- CheckSquare: Todos
- User: Profile
- Cog: Settings
- Plus: Add new
- Pencil: Edit
- Trash: Delete
- ChevronDown: Dropdowns
- Search: Search functionality

---

## Animation (Minimal Use)

- Transitions: 150ms ease-in-out for hover states
- Sidebar: 200ms slide animation
- Modal: 150ms fade-in
- No scroll-triggered animations
- Focus: no animation, instant feedback

---

## Images

**Dashboard Hero/Welcome Section**:
- Optional banner image (illustration of developer workspace/dashboard concept)
- Height: 200px on desktop, 150px mobile
- Position: top of main content area, below top bar
- Content: welcome message overlaid with semi-transparent background

**Empty States**:
- Placeholder illustrations when no data exists (Ideas, Plans, Todos lists)
- Centered, max-width 300px
- Simple line-art style illustrations

**No large hero sections needed** - this is a dashboard application focused on productivity, not marketing.

---

## Accessibility

- All form inputs have visible labels
- Sufficient contrast ratios (4.5:1 minimum)
- Keyboard navigation for all interactive elements
- Focus indicators on all focusable elements
- Screen reader text for icon-only buttons
- ARIA labels for complex components (tabs, modals)