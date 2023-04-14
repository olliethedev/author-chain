# Author Chain

Author Chain is a simple tool to help you research an entire article from a single keyword.

Here are the steps in the chain:

1. It uses the Google News Search API to find ~10 articles related to the keyword. 

2. Its summarizes each article

3. It writes first draft of the article using the summaries

4. It self reflects on the article to find concepts that are missing or can be expanded on.

5. It uses the Google Search API to research the missing concepts.

6. It uses the first draft in combination with the answers to write the final draft.

7. It refactors the final draft to markdown format.

8. It creates a tl;dr for the article.

8. It creates SEO title and description for the article.

## Caution!

This is an experimental tool. It is not meant to be used in production. It is meant to be used for research, education, and fun.

The entire pipeline can take a VERY long time to run (10+ minutes). You can switch to gpt-3.5-turbo for faster (and cheaper) results.

Self reflection loops are particularly time consuming.

### Diagram

Slighly out of date

![Diagram](
https://raw.githubusercontent.com/olliethedev/author-chain/main/markup_files/diagram.png)


