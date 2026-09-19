import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

export const listByThread = query({
  args: { threadId: v.id("threads") },
  handler: async (ctx, { threadId }) => {
    return await ctx.db
      .query("messages")
      .withIndex("by_thread", (q) => q.eq("threadId", threadId))
      .collect();
  },
});

export const append = mutation({
  args: {
    threadId: v.id("threads"),
    role: v.union(v.literal("system"), v.literal("human"), v.literal("ai")),
    content: v.string(),
  },
  handler: async (ctx, { threadId, role, content }) => {
    const thread = await ctx.db.get(threadId);
    if (!thread) {
      throw new Error("Thread not found");
    }
    const now = Date.now();
    const messageId = await ctx.db.insert("messages", {
      threadId,
      role,
      content: content.slice(0, 8000),
      createdAt: now,
    });
    const patch: { updatedAt: number; title?: string } = { updatedAt: now };
    if (role === "human" && thread.title === "New chat") {
      patch.title = content.trim().slice(0, 60) || "New chat";
    }
    await ctx.db.patch(threadId, patch);
    return messageId;
  },
});
