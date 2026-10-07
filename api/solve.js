// Vercel function: solves a LeetCode-style problem with Gemini.
// The key lives only in the Vercel env var GEMINI_API_KEY, so the EXE needs no setup.

const MODEL = "gemini-flash-latest";
const MAX_PROBLEM_CHARS = 20000;

function buildPrompt(problemText) {
  return `
You are an expert competitive programmer solving a LeetCode-style algorithm problem.
Write clean, efficient Python 3 code that passes LeetCode constraints.
Do not include any markdown, comments, docstrings, explanation, or extra text.
Do not include input/output code, test cases, or \`if __name__ == '__main__':\`.
Return only the function or class implementation required for the problem.
Problem:
${problemText}
`;
}

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Use POST." });
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: "GEMINI_API_KEY is not set on the server." });
  }

  const problem = req.body && req.body.problem;
  if (typeof problem !== "string" || !problem.trim()) {
    return res.status(400).json({ error: "Missing problem text." });
  }
  if (problem.length > MAX_PROBLEM_CHARS) {
    return res.status(413).json({ error: "Problem text is too long." });
  }

  const geminiResponse = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-goog-api-key": apiKey },
      body: JSON.stringify({ contents: [{ parts: [{ text: buildPrompt(problem) }] }] }),
    }
  );
  const data = await geminiResponse.json().catch(() => ({}));

  if (!geminiResponse.ok) {
    const message = (data.error && data.error.message) || `Gemini returned HTTP ${geminiResponse.status}.`;
    return res.status(502).json({ error: message });
  }

  const parts = (data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts) || [];
  const solution = parts.filter((part) => !part.thought && part.text).map((part) => part.text).join("");
  if (!solution.trim()) {
    return res.status(502).json({ error: "Gemini returned no solution." });
  }

  return res.status(200).json({ solution });
};
