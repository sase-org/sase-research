---
name: research/prompt
description: Research prior art and alternative solutions for a prompt, then write it up with #research.
input:
  - name: prompt
    type: text
    description: The prompt or topic to research.
---

Can you help me do some research on the below prompt? Investigate prior art, propose a few alternative solutions,
and end your analysis with a recommended solution. #research

## THE PROMPT
{{ prompt }}
