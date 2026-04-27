---
name: 0-dollar-stack-project
description: Scaffold and wire up a production-ready SaaS using only free-tier tools (Next.js + Tailwind + Motion + Shadcn/UI + Aceternity UI + Supabase + Drizzle + Better Auth + Resend + Polar/Dodo + Vercel). Inspired by Manu Arora's zero-dollar SaaS playbook. Invoke with a product idea or app name.
---

# Zero-Dollar SaaS Stack — Scaffold Skill

Bootstrap a full-stack SaaS application that costs **$0 to launch** using only free tiers. Every tool chosen is production-grade and can grow with you — upgrade only after you have paying users.

## When to Use This Skill

- `/0-dollar-stack-project Build a link-shortener SaaS`
- `/0-dollar-stack-project Scaffold a AI writing tool`
- `/0-dollar-stack-project Start a project management SaaS`
- Any time the user says "build a SaaS", "start a new project", or "zero cost stack"

---

## The Stack at a Glance

| Layer | Tool | Free Tier Limit |
|---|---|---|
| Framework | Next.js (App Router) | Open source |
| Styling | Tailwind CSS v4 | Open source |
| Animations | Motion (Framer Motion) | Open source |
| Base UI | Shadcn/UI + Radix UI | Open source |
| Landing UI | Aceternity UI | Free components |
| Database | Supabase (Postgres) | 500 MB · 50k MAU |
| ORM | Drizzle ORM | Open source |
| Auth | Better Auth | Open source (BYOI) |
| Email | Resend | 3,000/mo · 100/day |
| Payments | Polar or Dodo Payments | % per transaction only |
| Hosting | Vercel | Hobby tier — unlimited |

**BYOI** = Bring Your Own Infrastructure (auth stays in your DB, portable forever).

---

## Full Scaffold Workflow

### STEP 0 — Parse the Product Idea

Extract from the user's message:
- **App name** (use as project folder name, kebab-case)
- **Core value proposition** (1 sentence)
- **Primary user action** (what does the user DO in the app?)
- **Monetization model** (one-time, subscription, usage-based — default to subscription)

If unclear, ask one focused question: *"What does a paying user do in 30 seconds that a free user cannot?"*

---

### STEP 1 — Initialize Next.js Project

```bash
npx create-next-app@latest <app-name> \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"
cd <app-name>
```

**Project structure to create** (always use `src/` layout):

```
src/
  app/
    (marketing)/          # landing page, pricing, blog
      page.tsx
      layout.tsx
    (dashboard)/          # authenticated app shell
      dashboard/
        page.tsx
      layout.tsx
    api/
      auth/[...all]/
        route.ts          # Better Auth catch-all
  components/
    ui/                   # Shadcn generated components
    aceternity/           # Aceternity UI components
    marketing/            # Landing page sections
    dashboard/            # App-specific components
  lib/
    db/
      schema.ts           # Drizzle schema
      index.ts            # DB client
    auth.ts               # Better Auth config
    email/
      index.ts            # Resend client
    payments/
      index.ts            # Polar or Dodo client
  server/
    actions/              # Next.js Server Actions
  types/
    index.ts
```

---

### STEP 2 — Tailwind CSS + Motion

Tailwind is already wired by `create-next-app`. Add Motion:

```bash
npm install motion
```

**Motion usage pattern** — always import from `motion/react`:

```tsx
import { motion } from "motion/react"

// Fade-in page wrapper (use this on every major section)
<motion.div
  initial={{ opacity: 0, y: 16 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.4, ease: "easeOut" }}
>
  {children}
</motion.div>
```

Add a shared `AnimatedSection` wrapper component at `src/components/ui/animated-section.tsx` that every landing page section uses.

---

### STEP 3 — Install Shadcn/UI

```bash
npx shadcn@latest init
```

Select: Default style, Slate base color, CSS variables: yes.

Install the core components needed for every SaaS:

```bash
npx shadcn@latest add button card input label badge
npx shadcn@latest add dialog sheet dropdown-menu
npx shadcn@latest add form toast avatar separator
npx shadcn@latest add table tabs skeleton
```

**Convention**: All Shadcn components live in `src/components/ui/`. Never edit them directly — extend them by wrapping.

---

### STEP 4 — Aceternity UI (Landing Page Layer)

Aceternity UI is Manu Arora's component library. Use it for the **marketing/landing** pages only — it provides the premium animated feel that makes a SaaS look polished on day one.

Install dependencies:

```bash
npm install clsx tailwind-merge framer-motion @tabler/icons-react
```

Add the utility merger (required by Aceternity components):

```typescript
// src/lib/utils.ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

**Key Aceternity components to grab** for a SaaS landing page (copy from aceternity.com/components):

| Component | Use case |
|---|---|
| `HeroHighlight` | Main hero with animated gradient |
| `BackgroundBeams` | Hero section background |
| `TextGenerateEffect` | Animated headline |
| `BentoGrid` | Feature showcase section |
| `InfiniteMovingCards` | Testimonials / logo strip |
| `StickyScroll` | Feature walkthrough |
| `Spotlight` | Pricing card highlight |
| `FloatingNav` | Navbar that appears on scroll |

Copy each component's source into `src/components/aceternity/<component-name>.tsx`.

**Landing page structure** (`src/app/(marketing)/page.tsx`):

```tsx
export default function LandingPage() {
  return (
    <main>
      <FloatingNav />
      <HeroSection />        {/* BackgroundBeams + TextGenerateEffect + CTA */}
      <LogoStrip />          {/* InfiniteMovingCards */}
      <FeaturesSection />    {/* BentoGrid */}
      <HowItWorksSection />  {/* StickyScroll */}
      <PricingSection />     {/* Spotlight cards */}
      <TestimonialsSection />
      <CTASection />
      <Footer />
    </main>
  )
}
```

---

### STEP 5 — Supabase (Database)

**Create project** at supabase.com (free, no card required).

Install client + server helpers:

```bash
npm install @supabase/supabase-js @supabase/ssr
```

**Environment variables** (add to `.env.local`):

```env
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon-key>
DATABASE_URL=postgresql://postgres:<password>@db.<project>.supabase.co:5432/postgres
```

**Free tier limits to know**:
- 500 MB database storage
- 50,000 monthly active users
- 2 GB bandwidth/month
- Pause after 1 week of inactivity (upgrade when earning)

**Do NOT use Supabase Auth** — use Better Auth instead (Step 7) so your users are portable.

---

### STEP 6 — Drizzle ORM

```bash
npm install drizzle-orm pg
npm install -D drizzle-kit @types/pg
```

**`src/lib/db/index.ts`**:

```typescript
import { drizzle } from "drizzle-orm/node-postgres"
import { Pool } from "pg"
import * as schema from "./schema"

const pool = new Pool({ connectionString: process.env.DATABASE_URL })
export const db = drizzle(pool, { schema })
```

**`src/lib/db/schema.ts`** — starter schema for any SaaS:

```typescript
import { pgTable, text, timestamp, boolean, integer } from "drizzle-orm/pg-core"

export const users = pgTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  name: text("name"),
  image: text("image"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
})

export const sessions = pgTable("sessions", {
  id: text("id").primaryKey(),
  userId: text("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  token: text("token").notNull().unique(),
  expiresAt: timestamp("expires_at").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
})

// Add your app-specific tables below
```

**`drizzle.config.ts`** (project root):

```typescript
import type { Config } from "drizzle-kit"

export default {
  schema: "./src/lib/db/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: { url: process.env.DATABASE_URL! },
} satisfies Config
```

**`package.json` scripts**:

```json
{
  "scripts": {
    "db:generate": "drizzle-kit generate",
    "db:migrate": "drizzle-kit migrate",
    "db:studio": "drizzle-kit studio"
  }
}
```

---

### STEP 7 — Better Auth

Better Auth is open source, self-hosted, and **your user table is your user table** — no lock-in.

```bash
npm install better-auth
```

**`src/lib/auth.ts`**:

```typescript
import { betterAuth } from "better-auth"
import { drizzleAdapter } from "better-auth/adapters/drizzle"
import { db } from "@/lib/db"
import * as schema from "@/lib/db/schema"

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg",
    schema: { users: schema.users, sessions: schema.sessions },
  }),
  emailAndPassword: { enabled: true },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
  },
})

export type Session = typeof auth.$Infer.Session
```

**`src/app/api/auth/[...all]/route.ts`**:

```typescript
import { auth } from "@/lib/auth"
import { toNextJsHandler } from "better-auth/next-js"

export const { POST, GET } = toNextJsHandler(auth)
```

**Auth client** (`src/lib/auth-client.ts`):

```typescript
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL,
})

export const { signIn, signOut, signUp, useSession } = authClient
```

**Environment variables** to add:

```env
NEXT_PUBLIC_APP_URL=http://localhost:3000
BETTER_AUTH_SECRET=<generate: openssl rand -base64 32>
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
```

---

### STEP 8 — Resend (Email)

Free tier: 3,000 emails/month, 100/day. No credit card.

```bash
npm install resend react-email @react-email/components
```

**`src/lib/email/index.ts`**:

```typescript
import { Resend } from "resend"

export const resend = new Resend(process.env.RESEND_API_KEY)

export async function sendWelcomeEmail(to: string, name: string) {
  await resend.emails.send({
    from: "Your App <hello@yourdomain.com>",
    to,
    subject: "Welcome to <App Name>",
    react: WelcomeEmail({ name }),  // React Email template
  })
}
```

Create email templates in `src/emails/` using React Email components.

**Environment variable**:

```env
RESEND_API_KEY=re_...
```

**When to send emails** (implement these from day one):
1. Welcome email on sign-up
2. Magic link / OTP (handled by Better Auth)
3. Payment confirmation
4. Weekly digest / engagement nudge

---

### STEP 9 — Payments (Polar or Dodo)

Both are **Merchant of Record** — they handle VAT/GST/sales tax for every country automatically. You just receive payouts.

**Choose based on location**:
- India: use **Dodo Payments** (Stripe is unavailable for new accounts)
- Elsewhere: **Polar** is the default pick

#### Polar Setup

```bash
npm install @polar-sh/nextjs @polar-sh/sdk
```

**`src/lib/payments/index.ts`**:

```typescript
import { Polar } from "@polar-sh/sdk"

export const polar = new Polar({ accessToken: process.env.POLAR_ACCESS_TOKEN! })
```

**Checkout route** (`src/app/api/checkout/route.ts`):

```typescript
import { Checkout } from "@polar-sh/nextjs"

export const GET = Checkout({
  accessToken: process.env.POLAR_ACCESS_TOKEN!,
  successUrl: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard?success=true`,
  server: "sandbox",  // change to "production" when live
})
```

**Webhook handler** (`src/app/api/webhooks/polar/route.ts`):

```typescript
import { Webhooks } from "@polar-sh/nextjs"

export const POST = Webhooks({
  webhookSecret: process.env.POLAR_WEBHOOK_SECRET!,
  onOrderCreated: async (payload) => {
    // Provision access for the user
  },
  onSubscriptionActive: async (payload) => {
    // Upgrade user to paid tier
  },
  onSubscriptionCanceled: async (payload) => {
    // Downgrade user
  },
})
```

#### Dodo Payments Setup (India)

```bash
npm install dodopayments
```

```typescript
import DodoPayments from "dodopayments"

export const dodo = new DodoPayments({
  bearerToken: process.env.DODO_API_KEY!,
})
```

**Environment variables**:

```env
# Polar
POLAR_ACCESS_TOKEN=
POLAR_WEBHOOK_SECRET=

# OR Dodo Payments
DODO_API_KEY=
DODO_WEBHOOK_SECRET=
```

---

### STEP 10 — Deploy to Vercel

Free hobby tier: unlimited projects, CI/CD on every push, edge network, DDoS mitigation built in.

```bash
npm install -g vercel
vercel
```

Or connect the GitHub repo at vercel.com — every push to `main` auto-deploys.

**`vercel.json`** (project root):

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["iad1"]
}
```

**Environment variables**: Copy all `.env.local` keys into Vercel's dashboard → Project → Settings → Environment Variables.

**Free tier gives you**:
- Unlimited bandwidth for hobby
- Automatic HTTPS
- Preview deployments on every PR
- Built-in image optimization
- Edge middleware

---

## Deliverables Checklist

After running this skill, the following should exist and work:

- [ ] `npm run dev` starts the app on `localhost:3000`
- [ ] Landing page renders with at least Hero + Features + Pricing sections
- [ ] Sign up / Sign in works (email + password, plus at least one OAuth)
- [ ] Dashboard is protected (redirects unauthenticated users to `/login`)
- [ ] Database migrations run via `npm run db:migrate`
- [ ] Welcome email sends on new user sign-up
- [ ] Checkout link redirects to Polar/Dodo payment page
- [ ] Webhook updates user's plan in the database
- [ ] `vercel --prod` deploys without errors
- [ ] All env vars documented in `.env.example` (never commit `.env.local`)

---

## Key Architectural Rules

1. **Route groups**: Use `(marketing)` and `(dashboard)` to separate public and authenticated layouts cleanly.
2. **Server Actions over API routes**: For mutations inside the dashboard, prefer `use server` Server Actions over creating API routes — less boilerplate, type-safe end-to-end.
3. **Auth guard in layout**: Protect the dashboard at the layout level, not page by page.
4. **Drizzle over raw SQL**: Never write raw SQL queries. Drizzle is type-safe and AI-friendly.
5. **React Email for all emails**: Plain HTML emails break across clients. React Email + Resend ensures deliverability.
6. **Webhook idempotency**: Always check if a webhook event was already processed before applying it.

---

## Free Tier Upgrade Triggers

Know when to upgrade before you hit the wall:

| Tool | Upgrade when... |
|---|---|
| Supabase | DB approaching 400 MB or 40k MAU |
| Resend | Sending close to 90 emails/day consistently |
| Vercel | Needing team features, SSO, or >100 GB bandwidth/month |
| Supabase → PlanetScale | Need read replicas, global distribution |

**Rule**: If you're hitting these limits, your app has traction — you should already have revenue to pay for upgrades.

---

## Marketing Layer (Non-Code)

After shipping, the acquisition loop is:

1. **Build in public on X (Twitter)**: Show the product being used, not just built. Post demo clips, milestone numbers, user stories.
2. **Provide value first**: Share something genuinely useful (tutorial, open-source tool, data insight) and let your product solve the natural next-step problem.
3. **Peerlist + LinkedIn**: Cross-post launches. Peerlist is high signal for developer tools.
4. **Don't optimize creator revenue** — optimize for leads and sign-ups.

Study how Jack (PostBridge founder) markets: he ships genuinely useful things that happen to also need his product. That is the model.

---

## Output Format

When this skill runs, produce in order:

1. **Project overview** — app name, value prop, monetization model (1 paragraph)
2. **Scaffold all files** — run through Steps 1–10, creating actual files
3. **`.env.example`** — every required key with placeholder values
4. **`README.md`** — quick-start instructions (clone → install → env → migrate → dev)
5. **Summary checklist** — what's wired, what needs manual config (OAuth credentials, domain for email, Polar/Dodo account)

State clearly at the end: *"This costs $0 to run. Upgrade Supabase and Vercel when you have paying users."*
