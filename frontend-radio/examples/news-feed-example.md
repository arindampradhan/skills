# Example: Design a News Feed (Facebook/Twitter style)

This is a complete worked RADIO answer for reference.

---

## Requirements

**Functional:**
- User can see a paginated feed of posts from people they follow
- User can create a new text/image post
- User can react (like/love/haha) to a post
- User can comment on a post (out of scope for this session)
- Feed updates with new posts when user scrolls to top

**Non-functional:**
- Feed loads in <2s on 4G
- Smooth infinite scroll (no jank at 60fps)
- Optimistic updates on reactions (no latency on like button)
- Accessible: keyboard navigable, screen reader compatible

**Core focus**: Feed display + infinite scroll + post composer + reactions
**Deprioritized**: Comments, Stories, Groups, Ads

**Clarifying questions asked:**
- "Real-time updates via WebSocket or polling?" → polling with pull-to-refresh
- "Mobile-first or desktop?" → both, responsive
- "Do we own the API design?" → yes

---

## Architecture

**Components:**

| Component | Responsibility |
|---|---|
| Server | Exposes `GET /api/feed`, `POST /api/posts`, `POST /api/reactions` |
| Controller | Fetches feed on mount, handles scroll events, handles post/reaction actions |
| Feed Store | Holds posts[], currentUser, pagination cursor |
| Feed UI | Root view, renders FeedList + PostComposer |
| FeedList | Virtualised list of FeedPost items + infinite scroll trigger |
| FeedPost | Renders a single post: content, author, reactions bar |
| PostComposer | Controlled form for creating new posts, handles draft state |

**Where computation lives:**
- Client: rendering, sorting by created_at (already sorted by server), optimistic reaction counts
- Server: feed ranking/algorithm, auth, pagination

**Diagram saved to**: `docs/Design/Frontend-system/news-feed.excalidraw`

---

## Data Model

| Source | Entity | Owned by | Fields |
|---|---|---|---|
| Server | Post | Feed Store | id, content, author(User), reactions{like,love,haha}, image_url, created_at |
| Server | User | Feed Store | id, name, profile_photo_url |
| Server | Feed | Feed Store | posts: Post[], pagination: {next_cursor, has_more} |
| Client (persisted) | DraftPost | PostComposer | message: string, attachments: File[] |
| Client (ephemeral) | FeedUIState | Feed UI | isLoading, error, isComposerOpen |
| Client (ephemeral) | ReactionState | FeedPost | optimistic counts per postId |

---

## Interface

**Server-Client APIs:**

```
GET /api/feed
Params: { cursor?: string, size: 20 }
Response: {
  items: Post[],
  pagination: { next_cursor: string, has_more: boolean }
}

POST /api/posts
Body: { content: string, image_url?: string }
Response: Post

POST /api/reactions
Body: { post_id: string, reaction: "like" | "love" | "haha" }
Response: { post_id: string, reactions: ReactionCounts }
```

**Client-Client (component API):**

```typescript
// FeedPost props
interface FeedPostProps {
  post: Post;
  onReact: (postId: string, reaction: ReactionType) => void;
}

// Store actions
feedStore.loadNextPage(): Promise<void>
feedStore.prependPost(post: Post): void
feedStore.applyOptimisticReaction(postId: string, reaction: ReactionType): void
feedStore.revertReaction(postId: string, previous: ReactionCounts): void
```

---

## Optimizations

### Deep dive 1: Virtual Scrolling
The DOM cannot hold 500 FeedPost nodes without killing performance. Use windowing:
- Only render ~20 visible items + a buffer of 5 above/below
- Use `IntersectionObserver` on the last visible item to trigger `loadNextPage()`
- Use `react-window` or a custom hook with absolute positioning
- **Trade-off**: VirtualList loses native browser find-in-page — acceptable for feeds

### Deep dive 2: Optimistic Updates for Reactions
Reaction latency feels bad. Fix with optimistic UI:
1. User clicks Like → immediately increment count in store
2. Fire `POST /api/reactions` in background
3. On success: do nothing (server confirmed)
4. On failure: revert to previous count, show toast "Failed to react"
- **Trade-off**: Temporary visual inconsistency if the request fails, but rare and recoverable

### Other optimizations (brief mention):
- **Images**: Lazy load with `loading="lazy"`, use WebP with `<picture>` fallback
- **Skeleton screens**: Show placeholder cards on initial load, not a spinner
- **Stale-while-revalidate**: Show cached feed immediately, fetch fresh data in background
- **Security**: Sanitize post content with DOMPurify before `innerHTML` (or use textContent)
- **a11y**: `role="feed"` on FeedList, `aria-label` on reaction buttons, keyboard shortcuts for compose
