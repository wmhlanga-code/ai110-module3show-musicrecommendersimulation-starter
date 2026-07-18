# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the AI assistant to add advanced song attributes to the dataset and update the scoring logic so the recommender could use them.

**Prompts used:**

- “Add 5+ new song attributes to the dataset such as popularity, release decade, mood tags, lyrical depth, instrumentalness, and vocal energy.”
- “Update the recommender scoring logic so these features influence the score, while keeping the existing genre, mood, energy, and acoustic behavior intact.”
- “Help me verify the changes and make sure the output still runs correctly.”

**What did the agent generate or change?**

The assistant updated the CSV data file with new columns and modified the recommender scoring code to read and use the new attributes. It also helped add a test covering the new feature logic.

**What did you verify or fix manually?**

I verified that the new attributes were loaded from the CSV and that the scorer used them in the ranking logic. I also fixed a packaging issue so the project imports the recommender module correctly during test runs.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
