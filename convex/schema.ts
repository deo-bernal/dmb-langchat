import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  threads: defineTable({
    sessionId: v.string(),
    title: v.string(),
    updatedAt: v.number(),
  }).index("by_session", ["sessionId"]),

  messages: defineTable({
    threadId: v.id("threads"),
    role: v.union(v.literal("system"), v.literal("human"), v.literal("ai")),
    content: v.string(),
    createdAt: v.number(),
  }).index("by_thread", ["threadId"]),
});
