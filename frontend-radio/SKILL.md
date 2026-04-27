---
name: frontend-radio
description: 'Tackle Frontend System Design interview questions using the RADIO framework as a senior frontend engineer. Invoke with a product name or question. Generates a structured verbal answer for each RADIO step AND saves an Excalidraw architecture diagram to docs/Design/Frontend-system/ in the current repo.'
---

# Frontend RADIO — System Design Interview Skill

A skill for working through frontend system design interviews using the RADIO framework (Requirements, Architecture, Data Model, Interface, Optimizations), from the perspective of a senior frontend engineer.

## When to Use This Skill

- `/frontend-radio Design a news feed`
- `/frontend-radio Design YouTube's video player`
- `/frontend-radio Design a type-ahead / autocomplete`
- `/frontend-radio Design a data table component`
- `/frontend-radio Design Google Docs (collaborative editor)`
- Any request like "walk me through RADIO for X" or "how would you design X for an interview"

## What This Skill Produces

1. **Structured RADIO answer** — verbal notes for each section, written as a senior FE dev would say it
2. **Architecture Excalidraw diagram** — saved to `docs/Design/Frontend-system/<product-name>.excalidraw`

---

## Full Workflow

### STEP 0 — Parse the Question

Extract:
- **Product name** (e.g., "news feed", "autocomplete", "data table")
- **Scope hints** (if the user mentions mobile-only, real-time, etc.)
- **Output filename**: kebab-case from product name → `docs/Design/Frontend-system/<product-name>.excalidraw`

---

### STEP 1 — R: Requirements (~15% of time)

Output a requirements block. Always split into:

**Functional requirements** (the product cannot work without these):
- List 3–5 core use cases. Frame them as user stories: "User can X"
- Call out the most defining feature first (the one that makes this product unique)

**Non-functional requirements** (important but not blocking):
- Performance targets (time to first paint, interaction latency)
- Scalability (how many items before UX degrades)
- Offline support? Real-time? Accessibility?

**Core vs. nice-to-have**:
- Pick 2–3 features to focus on for the rest of the interview
- Be explicit: "For this session I'll focus on X, Y, Z and deprioritize A, B"

**Clarifying questions to ask the interviewer** (always suggest 2–3):
- "What devices/platforms should we support?"
- "Is real-time collaboration or real-time updates needed?"
- "Do we own the backend API design or is it fixed?"
- "What scale — single user, team, or millions of users?"

**Senior tip**: Don't wait to be asked. State the requirements yourself and get alignment. Shows ownership.

---

### STEP 2 — A: Architecture (~20% of time)

Output two things:
1. A **component list** with responsibilities (text)
2. An **Excalidraw architecture diagram** (file)

#### Standard Frontend Architecture Pattern

Every frontend system has these layers. Adapt, don't invent:

```
Server (black box)
   ↕ HTTP / WebSocket / GraphQL
Controller (event handler + data orchestrator)
   ↕                    ↕
Client Store        View Layer
(app-wide state)    (UI components)
```

**Components to always identify:**

| Component | Responsibility |
|---|---|
| **Server** | Black box. Just name the APIs it exposes. Don't design the backend. |
| **Controller** | Handles user interactions, calls server APIs, updates the store, transforms data for the view |
| **Client Store** | App-wide state: server data + UI state. Describe what lives here. |
| **View / UI** | Break into meaningful sub-components (e.g., FeedList, FeedPost, PostComposer) |
| **Router** | Only if the product has multiple pages/routes |

**Where computation lives** (always address this):
- Client: filtering, sorting, pagination of already-loaded data
- Server: search, heavy aggregations, auth

**Senior tip**: "I'll focus on client-side architecture. I'll treat the server as a black box and just define the API contract." This shows focus.

#### Generating the Architecture Diagram

Create a `.excalidraw` file at `docs/Design/Frontend-system/<product-name>.excalidraw`.

Use this **standard layout** (coordinates given as guide, adjust per product):

```
Canvas layout (top → bottom):
  [Server box]                     — top center, dark background
       ↓  HTTP/WS label
  [Controller box]                 — middle center  
    ↙                  ↘
[Client Store]      [View container]
                    ├── [Sub-component 1]
                    ├── [Sub-component 2]
                    └── [Sub-component 3]
```

**Color scheme (mandatory)**:
- Server: `backgroundColor: "#343a40"`, `strokeColor: "#212529"`, text white `"#f8f9fa"`
- Controller: `backgroundColor: "#a5d8ff"`, `strokeColor: "#1971c2"`
- Client Store: `backgroundColor: "#ffd8a8"`, `strokeColor: "#e67700"`
- View container: `backgroundColor: "#d3f9d8"`, `strokeColor: "#2b8a3e"`
- Sub-components (inside View): `backgroundColor: "#ebfbee"`, `strokeColor: "#40c057"`
- Arrows: match source component color

**Font**: always `fontFamily: 5` (Excalifont)

**Diagram generation rules**:
- Server box: wide, at the top. Include a subtitle showing the main API path(s).
- Controller box: wide, below server. Include 2–3 bullet responsibilities as text.
- Client Store + View: side by side below controller.
- View container: larger box. Draw sub-components inside it as nested rectangles.
- Add a data flow arrow label on each connection: "HTTP GET /feed", "dispatch(loadFeed)", etc.
- Canvas size: ~1600px wide, ~1200px tall. Center content around (800, 600).

**Example coordinates for a typical design** (scale up/down per complexity):

```
Server:       x=300, y=80,  w=700, h=90
Controller:   x=300, y=300, w=700, h=100
Client Store: x=100, y=540, w=320, h=180
View:         x=530, y=520, w=470, h=360
  Sub1:       x=550, y=570, w=200, h=55
  Sub2:       x=550, y=650, w=200, h=55
  Sub3:       x=550, y=730, w=200, h=55
```

Use the Excalidraw JSON format from the `excalidraw-diagram-generator` skill's schema reference.

---

### STEP 3 — D: Data Model (~10% of time)

Output a data model table. For each entity:

| Source | Entity | Owned by | Key Fields |
|---|---|---|---|
| Server | Post | Feed Store | id, content, author, reactions, created_at |
| Server | User | Client Store | id, name, profile_photo_url |
| Client (persisted) | DraftPost | Composer | message, attachments |
| Client (ephemeral) | FeedUIState | Feed View | isLoading, error, activeTab |

**Rules**:
- Always separate **server-originated** vs **client-only** data
- Client-only splits into **persisted** (goes to server eventually) and **ephemeral** (lost on refresh — fine)
- Don't over-design. 3–5 entities is enough for most interview questions.

**Senior tip**: When listing a field, ask yourself: "Does this need to survive a page refresh?" If no → ephemeral. If yes but stays client-side → persisted client state. If yes and shared across devices → server.

---

### STEP 4 — I: Interface / API (~15% of time)

#### Server-Client APIs

For each core API, define:

```
Method: GET
Path:   /api/feed
Params: { cursor: string, size: number }
Response: {
  items: Post[],
  pagination: { next_cursor: string, has_more: boolean }
}
```

Always use **cursor-based pagination** for feeds and lists — not offset-based.

For mutations:
```
Method: POST
Path:   /api/posts
Body:   { content: string, attachments: string[] }
Response: Post
```

#### Client-Client APIs (Component Interface)

For UI component questions, describe props:

```typescript
// FeedPost component
interface FeedPostProps {
  post: Post;
  onLike: (postId: string) => void;
  onShare: (postId: string) => void;
  isHighlighted?: boolean;
}
```

For events/store actions:
```typescript
// Store actions
loadFeed(cursor?: string): Promise<void>
createPost(draft: DraftPost): Promise<Post>
reactToPost(postId: string, reaction: ReactionType): void
```

**Senior tip**: "I define the API contract before the implementation. This lets both server and client teams work in parallel." Shows architectural thinking.

---

### STEP 5 — O: Optimizations (~40% of time)

This is where senior engineers stand out. Go deep on 2–3 areas. Always mention all areas briefly, then dive into 2.

#### Performance
- **Virtualization**: For long lists, use virtual scrolling (only render visible items). "A feed with 1000 posts will kill the DOM — windowing with react-window or intersection observer."
- **Code splitting**: Lazy load non-critical components. Route-level splits.
- **Image optimization**: Lazy load images, use srcset, WebP, content-aware lazy loading with IntersectionObserver
- **Bundle size**: Tree shaking, dynamic imports, avoid moment.js etc.
- **Memoization**: React.memo, useMemo, useCallback — but only where profiled

#### UX / Loading States
- **Skeleton screens**: Never show spinners for content that has a known shape. Use skeleton placeholders.
- **Optimistic updates**: When user likes a post, update UI immediately, revert on failure.
- **Stale-while-revalidate**: Show cached data instantly, refresh in background.
- **Error states**: Every async operation needs: loading, success, error, empty states.
- **Infinite scroll vs pagination**: Infinite scroll for social feeds, pagination for data tables (predictable position).

#### Network
- **Request deduplication**: If two components request the same resource, dedupe.
- **Debouncing/throttling**: Autocomplete → debounce 300ms. Resize handlers → throttle.
- **HTTP/2**: Multiplexed requests. No need to bundle API calls.
- **Service Worker / caching**: For offline support. Cache GET responses with stale-while-revalidate.
- **WebSocket vs polling**: Real-time notifications → WebSocket. Low-frequency updates → polling with exponential backoff.

#### Accessibility (a11y)
- Keyboard navigation: Tab order, focus management after interactions
- ARIA: `aria-label`, `aria-live` for dynamic content, `role` attributes
- Color contrast: WCAG AA minimum
- Focus traps: Modals and drawers must trap focus

#### Security
- **XSS**: Never use `innerHTML` with user content. Sanitize with DOMPurify.
- **CSRF**: Use SameSite cookies + CSRF tokens for mutations.
- **Content Security Policy**: Restrict script sources.
- **Dependency audits**: `npm audit` in CI.

#### Multilingual / i18n
- Use i18n library (i18next, FormatJS). Never hardcode strings.
- RTL layout support: Use logical CSS properties (`margin-inline-start` not `margin-left`).
- Date/number formatting: Always use `Intl.DateTimeFormat`, `Intl.NumberFormat`.

**Senior tip**: Pick the 2 areas most relevant to the product. For a feed → virtualization + optimistic updates. For a collaborative editor → conflict resolution (CRDT/OT) + real-time sync. Show depth.

---

## Output Format

When this skill runs, output in this order:

1. `## Requirements` — bullet list
2. `## Architecture` — component table + Excalidraw file generation
3. `## Data Model` — table
4. `## Interface` — API definitions
5. `## Optimizations` — structured list, go deep on 2–3 areas
6. `✅ Saved diagram to: docs/Design/Frontend-system/<name>.excalidraw`

---

## File Naming

Save diagrams to: `docs/Design/Frontend-system/<product-kebab-case>.excalidraw`

Examples:
- "Design a news feed" → `news-feed.excalidraw`
- "Design YouTube" → `youtube-video-player.excalidraw`
- "Design autocomplete" → `autocomplete.excalidraw`
- "Design a data table" → `data-table.excalidraw`
- "Design Google Docs" → `google-docs.excalidraw`

Do NOT overwrite existing files — check first. If a file exists, append `-v2` or ask the user.

---

## Senior Engineer Checklist

Before finishing, verify the answer covers:
- [ ] Explicitly stated what you're NOT designing (scope boundary)
- [ ] Architecture focuses on CLIENT-SIDE, not backend
- [ ] Data model separates server vs client, persisted vs ephemeral
- [ ] API uses cursor-based pagination for lists
- [ ] At least one deep-dive optimization relevant to the specific product
- [ ] Mentioned trade-offs (not just "I would use X" but "I chose X over Y because...")
- [ ] Diagram saved to correct path

---

## Common Product Patterns

### Social Feed (Facebook, Twitter, Instagram)
Deep dive: virtual scrolling + optimistic updates + infinite scroll
Key components: FeedList, FeedPost, PostComposer, ReactionBar

### Video Player (YouTube, Netflix)
Deep dive: adaptive bitrate streaming + buffering strategy
Key components: VideoPlayer, ProgressBar, QualitySelector, RecommendationPanel

### Autocomplete / Search
Deep dive: debouncing + request cancellation (AbortController) + cache
Key components: SearchInput, SuggestionList, SuggestionItem, HighlightMatch

### Collaborative Editor (Google Docs)
Deep dive: CRDT or OT for conflict resolution + WebSocket + offline sync
Key components: EditorCanvas, Toolbar, CollaboratorCursors, CommentPanel

### Data Table
Deep dive: virtualization for large datasets + column resize/reorder
Key components: Table, TableHeader, TableRow, VirtualScroller, ColumnResizer

### E-commerce Product Page
Deep dive: image lazy loading + above-the-fold optimization + add-to-cart optimistic update
Key components: ImageGallery, ProductInfo, ReviewList, CartButton, RecommendationCarousel

### Notification System
Deep dive: WebSocket connection management + read/unread state + badge counts
Key components: NotificationBell, NotificationList, NotificationItem, ToastSystem
