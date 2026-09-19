import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

export const listBySession = query({
  args: { sessionId: v.string() },
  handler: async (ctx, { sessionId }) => {
    const rows = await ctx.db
      .query("threads")
      .withIndex("by_session", (q) => q.eq("sessionId", sessionId))
      .collect();
    return rows.sort((a, b) => b.updatedAt - a.updatedAt);
  },
});

export const get = query({
  args: { threadId: v.id("threads") },
  handler: async (ctx, { threadId }) => {
    return await ctx.db.get(threadId);
  },
});

export const create = mutation({
  args: {
    sessionId: v.string(),
    title: v.optional(v.string()),
  },
  handler: async (ctx, { sessionId, title }) => {
    const now = Date.now();
    return await ctx.db.insert("threads", {
      sessionId,
      title: (title || "New chat").slice(0, 120),
      updatedAt: now,
    });
  },
});

export const rename = mutation({
  args: {
    threadId: v.id("threads"),
    title: v.string(),
  },
  handler: async (ctx, { threadId, title }) => {
    await ctx.db.patch(threadId, {
      title: title.slice(0, 120),
      updatedAt: Date.now(),
    });
  },
});
